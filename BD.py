import csv
import numpy as np
import datetime as ft


class BaseCentral(object):
    def __init__(símismo, archivo, sistema='csv'):
        símismo.sistema = sistema.lower()
        símismo.archivo = archivo

        símismo.nombres_cols = leer_columnas(sistema, archivo)

        símismo.receta = {'sistema': 'csv',
                          'id_cols': {'fecha': '', 'tiempo': '', 'vars': {}},
                          'mét_combin_tiempo': {},
                          'mét_interpol': {}
                          }

        símismo.fecha_inic_datos = None
        símismo.día_inic_año = 1
        símismo.fechas = []
        símismo.tiempos = []
        símismo.datos = {}

        símismo.vars = {}

    def estab_col_fecha(símismo, col=None):
        """
        Esta funcion establece la columna de la base de datos con los datos de fechas de observaciones.

        :param col: El nombre de la columna
        :type col: str

        """

        if col is None:
            col = símismo.receta['id_cols']['fecha']

        try:
            lista_fechas = cargar_columna(columna=col, sistema=símismo.sistema, archivo=símismo.archivo)
        except ValueError:
            raise ValueError('Columna de datos de fechas errada o no especificada.')

        # Guardar la fecha inicial del base de datos, tanto como un vector de la posición de cada dís en comparación
        # a esta.
        símismo.fecha_inic_datos, símismo.fechas = leer_fechas(lista_fechas)

        # Acordarse de cuál era la columna de fechas
        símismo.receta['id_cols']['fecha'] = col

    def estab_col_hora(símismo, col=None):

        # Si no se especificó la columna de horas, usar la guardada
        if col is None:
            col = símismo.receta['id_cols']['tiempo']

        try:
            lista_horas = cargar_columna(col, símismo.sistema, símismo.archivo)
        except ValueError:
            raise ValueError('Columna de datos de fechas errada o no especificada.')

        # Guardar un vector del tiempo del día, en segundos, para cada observación en el base de datos
        símismo.tiempos = leer_tiempo(lista_horas)

        # Acordarse de cuál era la columna de horas
        símismo.receta['id_cols']['tiempo'] = col

    def cargar_var(símismo, nombre, col_datos=None, mét_combin_tiempo=None, mét_interpol=None):

        # Si no especificamos ya la columna de datos o de horas, quejarse.
        if símismo.fecha_inic_datos is None or símismo.tiempos is None:
            raise ValueError('Hay que especificar los datos de fechas y horas primero.')

        if mét_combin_tiempo is not None:
            símismo.receta['mét_combin_tiempo'][nombre] = mét_combin_tiempo
        else:
            try:
                mét_combin_tiempo = símismo.receta['mét_combin_tiempo'][nombre]
            except KeyError:
                raise ValueError('Hay que especificar el método para combinar datos horarios en datos diarios.')

        if mét_interpol is not None:
            símismo.receta['mét_interpol'][nombre] = mét_interpol
        else:
            try:
                mét_interpol = símismo.receta['mét_interpol'][nombre]
            except KeyError:
                raise ValueError('Hay que especificar el método para interpolar datos horarios.')

        if col_datos is not None:
            símismo.receta['id_cols']['vars'][nombre] = col_datos
        else:
            try:
                col_datos = símismo.receta['id_cols']['vars'][nombre]
            except KeyError:
                col_datos = nombre

        símismo.datos[nombre] = VariableBD(nombre=nombre, base=símismo, columna=col_datos,
                                           transformación=mét_combin_tiempo, interpol=mét_interpol
                                           )

    def olvidar_var(símismo, nombre):
        símismo.datos.pop(nombre)
        símismo.receta['mét_combin_tiempo'].pop(nombre)
        símismo.receta['mét_interpol'].pop(nombre)
        símismo.receta['id_cols']['vars'].pop(nombre)

    def guardar(símismo, archivo):
        pass

    def cargar(símismo, archivo=None):
        pass


class VariableBD(object):
    def __init__(símismo, nombre, base, columna, interpol, transformación):

        assert type(base) is BaseCentral

        # El nombre del variable
        símismo.nombre = nombre

        # La base de datos central
        símismo.base = base

        # Leer datos y convertir a números
        datos_crudos = cargar_columna(columna=columna, sistema=base.sistema,
                                      archivo=base.archivo)
        datos_crudos[datos_crudos == ''] = 'NaN'
        datos_crudos = np.array(datos_crudos, dtype=float)

        # La fecha inicial de los datos crudos, y el día del inicio del año del modelo
        símismo.fecha_inic = fecha_inic = base.fecha_inic_datos
        día_inic_año = base.día_inic_año

        # El vector de las fechas, relativas a la fecha inicial de los datos
        lista_fechas = base.fechas

        # El vector de los tiempos de cada observación
        lista_tiempos = base.tiempos

        datos = []
        vals_var_día = []
        pesos = []
        terminado = False

        if interpol == 'trap':
            fin = -2
        elif interpol == 'ninguno':
            fin = -1
        else:
            raise ValueError

        for n, f in enumerate(lista_fechas[:fin]):
            if interpol == 'trap':
                vals_var_día.append((datos_crudos[n] + datos_crudos[n+1])/2)
                ajust_día = lista_fechas[n + 1] - f
                pesos.append((lista_tiempos[n+1]-lista_tiempos[n] + ajust_día*24*60*60)/(60*60))

                if n+1 == len(lista_fechas) or f != lista_fechas[n + 1]:
                    terminado = True
            elif interpol == 'ninguno':
                vals_var_día.append(datos_crudos[n])
                if n == len(lista_fechas) or f != lista_fechas[n + 1]:
                    terminado = True
            else:
                raise ValueError('Metodo de interpolación {0} no reconocido.'.format(interpol))

            if terminado:
                vals_var_día = np.array(vals_var_día)

                if interpol == 'ninguno':
                    pesos = [1]*len(vals_var_día)
                elif interpol == 'trap':
                    pesos = np.divide(pesos, np.sum(pesos))

                if transformación == 'sumar':
                    var = np.sum(vals_var_día*pesos)
                elif transformación == 'máx':
                    var = vals_var_día.max()
                elif transformación == 'mín':
                    var = vals_var_día.min()
                elif transformación == 'prom':
                    var = np.average(vals_var_día, weights=pesos)
                else:
                    raise ValueError('Metodo de generación de datos diarios "{0}" '
                                     'no reconocido.'.format(transformación))

                datos += [var] + [float('NaN')] * (lista_fechas[n+1] - f - 1)
                vals_var_día = []
                pesos = []

                terminado = False

        símismo.datos = np.array(datos)

        fecha_inic = fecha_inic

        datos = símismo.datos

        datos_por_año = []
        if día_inic_año > (fecha_inic - ft.date(fecha_inic.year, 1, 1)).days:
            fecha_ref = ft.date(fecha_inic.year-1, 1, 1) + ft.timedelta(days=día_inic_año-1)
        else:
            fecha_ref = ft.date(fecha_inic.year, 1, 1) + ft.timedelta(days=día_inic_año-1)

        fecha_inic_año_act = fecha_ref
        while True:
            datos_año_actual = []
            fecha_inic_año_próx = ft.date(fecha_inic_año_act.year + 1, 1, 1) + ft.timedelta(days=día_inic_año-1)

            inic = (fecha_inic_año_act - fecha_inic).days
            if inic < 0:
                datos_año_actual = [float('NaN')] * (fecha_inic-fecha_ref).days
                inic = 0
            fin = (fecha_inic_año_próx - fecha_inic).days

            if fin > len(datos):
                datos_año_actual = np.concatenate((datos_año_actual, datos[inic:]))
                datos_por_año.append(datos_año_actual)
                break

            datos_año_actual = np.concatenate((datos_año_actual, datos[inic:fin]))
            datos_por_año.append(datos_año_actual)
            fecha_inic_año_act = fecha_inic_año_próx

        # Una lista de matrices numpy de los datos de cada año
        símismo.datos = datos_por_año


def leer_columnas(sistema, archivo):
    """
    Esta función lee los nombres de las columnas de una base de datos.

    :param sistema:
    :param archivo:

    :return: La lista de los nombres de las columnas
    :rtype: list
    """

    if sistema == 'csv':

        try:
            with open(archivo, 'r') as d:
                l = csv.reader(d)

                # Tomar la primera fila, guardarla como nombres de columnas
                columnas = next(l)

        except FileNotFoundError:
            print('¡Error abriendo el archivo de datos!')
            raise FileNotFoundError

    else:
        raise NotImplementedError('Falta código para comunicar con el formato de datos: '
                                  '{0}'.format(sistema))

    return columnas


def cargar_columna(columna, sistema, archivo):

    if sistema == 'csv':  # Para documentos de tipo .csv

        try:
            with open(archivo, 'r') as d:
                l = csv.reader(d)  # Leer el csv

                # Buscar el nombre de la columna en la base de datos
                n_col = next(l).index(columna)

                # Sacar el valor de esta columna en cada fila
                datos = [f[n_col] for f in l]

                # Convertir los datos a formato de matriz numpy numérica, con np.nan para datos que faltan
                # datos = np.array(datos)
                # datos[datos == ''] = np.nan
                # datos = datos.astype(np.float)

        except ValueError:
            raise ValueError('El nombre de columna no existe en la base de datos.')

        except FileNotFoundError:
            print('¡Error!')
            raise FileNotFoundError

    else:
        raise NotImplementedError('Falta código para comunicar con el formato de datos'
                                  '{0}'.format(sistema))
    return datos


def leer_fechas(lista_cruda):
    """
    Esta función toma una lista de datos de fecha en formato de texto y detecta 1) la primera fecha de la lista,
      y 2) la posición relativa de cada fecha a esta.

    :param lista_cruda: Una lista con las fechas en formato de texto
    :type lista_cruda: list

    :return: Un tuple de la primera fecha y del vector numpy de la posición de cada fecha relativa a la primera.
    :rtype: (ft.date, np.ndarray())

    """

    # Una lista de lso formatos de fecha posibles. Esta función intentará de leer los datos de fechas con cada
    # formato en esta lista y, si encuentra un que funciona, parará allí.
    separadores = ['-', '/', ' ', '.']

    f = ['%d{0}%m{0}%y', '%m{0}%d{0}%y', '%d{0}%m{0}%Y', '%m{0}%d{0}%Y',
         '%d{0}%b{0}%y', '%m{0}%b{0}%y', '%d{0}%b{0}%Y', '%b{0}%d{0}%Y',
         '%d{0}%B{0}%y', '%m{0}%B{0}%y', '%d{0}%B{0}%Y', '%m{0}%B{0}%Y',
         '%y{0}%m{0}%d', '%y{0}%d{0}%m', '%Y{0}%m{0}%d', '%Y{0}%d{0}%m',
         '%y{0}%b{0}%d', '%y{0}%d{0}%b', '%Y{0}%b{0}%d', '%Y{0}%d{0}%b',
         '%y{0}%B{0}%d', '%y{0}%d{0}%B', '%Y{0}%B{0}%d', '%Y{0}%d{0}%B']

    formatos_posibles = [x.format(s) for s in separadores for x in f]

    # Primero, si los datos de fechas están en formato simplemente numérico...
    if all([x.isdigit() for x in lista_cruda]):

        # Entonces, no conocemos la fecha inicial
        fecha_inic_datos = None

        # Pero podemos regresar un vector numpy con los números de cada fecha
        vector_núm_fechas = np.array(lista_cruda, dtype=float)

    else:

        # Sino, intentar de leer el formato de fecha
        fechas = None

        # Intentar con cada formato en la lista de formatos posibles
        for formato in formatos_posibles:

            try:
                # Intentar de convertir todas las fechas a objetos ft.datetime
                fechas = [ft.datetime.strptime(x, formato).date() for x in lista_cruda]

                # Si funcionó, parar aquí
                break

            except ValueError:
                # Si no funcionó, intentar el próximo formato
                continue

        # Si todavía no lo hemos logrado, tenemos un problema.
        if fechas is None:
            raise ValueError('No puedo leer los datos de fechas. ¿Mejor le eches un vistazo a tu base de datos?')

        else:
            # Pero si está bien, ya tenemos que encontrar la primera fecha y calcular la posición relativa de las
            # otras con referencia en esta.

            # La primera fecha de la base de datos. Este paso se queda un poco lento, así que para largas bases de
            # datos podría ser útil suponer que la primera fila también contiene la primera fecha.
            fecha_inic_datos = min(fechas)

            # fecha_inic_datos = fechas[0]  # Ejemplo de código menos seguro pero mucho más rápido

            # La posición relativa de todas las fechas a esta
            vector_núm_fechas = np.array([(x - fecha_inic_datos).days for x in fechas])

    return fecha_inic_datos, vector_núm_fechas


def leer_tiempo(tiempos_crudos):

    lista_tiempos = [x.split(':') for x in tiempos_crudos if x != '\n' and x != '']
    if len(lista_tiempos[0]) == 3:
        tiempos_finales = [((int(x[0]) * 60) + int(x[1])) * 60 + int(x[2]) for x in lista_tiempos]
    elif len(lista_tiempos[0]) == 2:
        tiempos_finales = [((int(x[0]) * 60) + int(x[1])) * 60 for x in lista_tiempos]
    else:
        print('No se pudieron leer los datos de hora de la base de datos.')
        raise ValueError('No se pudieron leer los datos de hora de la base de datos.')

    return np.array(tiempos_finales)
