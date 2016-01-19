import numpy as np
import datetime as ft


class BaseCentral(object):
    def __init__(símismo, archivo, sistema='csv'):
        símismo.sistema = sistema.lower()
        símismo.archivo = archivo
        símismo.temporal_a_diario = {}

        símismo.nombres_cols = leer_columnas(sistema, archivo)

        símismo.id_cols = {'fecha': '', 'tiempo': '', 'vars': {}}
        símismo.fecha_inic = None
        símismo.fechas = []
        símismo.fechas_únicas = []
        símismo.tiempos = []
        símismo.datos = {}
        símismo.info_datos = {'mét_combin_tiempo': {}, 'mét_interpol': {}}

    def estab_col_fecha(símismo, col=None):
        if col is None:
            col = símismo.id_cols['fecha']
        lista_fechas = cargar_columna(col, símismo.sistema, símismo.archivo)
        símismo.fecha_inic, símismo.fechas = leer_fechas(lista_fechas)
        símismo.fechas_únicas = list(set(símismo.fechas))
        símismo.fechas_únicas.sort()
        símismo.id_cols['fecha'] = col

    def estab_col_hora(símismo, col=None):
        if col is None:
            col = símismo.id_cols['tiempo']
        lista_horas = cargar_columna(col, símismo.sistema, símismo.archivo)
        símismo.tiempos = leer_tiempo(lista_horas)
        símismo.id_cols['tiempo'] = col

    def cargar_var(símismo, nombre, col_datos=None, mét_combin_tiempo=None, mét_interpol=None):
        if símismo.fechas_únicas is None or símismo.tiempos is None:
            return 'Hay que especificar los datos de fechas y horas primero.'

        if mét_combin_tiempo is None:
            try:
                mét_combin_tiempo = símismo.info_datos['mét_combin_tiempo'][nombre]
            except KeyError:
                pass
        if mét_interpol is None:
            try:
                mét_interpol = símismo.info_datos['mét_interpol'][nombre]
            except KeyError:
                pass

        if col_datos is None:
            col_datos = símismo.id_cols['vars'][nombre]

        símismo.datos[nombre] = VariableBD(símismo, nombre, columna=col_datos,
                                           transformación=mét_combin_tiempo, interpol=mét_interpol)
        símismo.info_datos['mét_combin_tiempo'][nombre] = mét_combin_tiempo
        símismo.info_datos['mét_interpol'][nombre] = mét_interpol

    def olvidar_var(símismo, nombre):
        símismo.datos.pop(nombre)
        símismo.info_datos['mét_combin_tiempo'].pop(nombre)
        símismo.info_datos['mét_interpol'].pop(nombre)


class VariableBD(object):
    def __init__(símismo, base_de_datos, nombre, columna, interpol, transformación):
        símismo.nombre = nombre
        símismo.base_de_datos = base_de_datos
        símismo.fecha_inic = símismo.base_de_datos.fecha_inic

        datos_crudos_tx = cargar_columna(columna, base_de_datos.sistema, base_de_datos.archivo)
        datos_crudos = [float(x) for x in datos_crudos_tx]
        símismo.lista_fechas = base_de_datos.fechas
        lista_tiempos = base_de_datos.tiempos

        if transformación is None:
            transformación = 'prom'
        if interpol is None:
            interpol = 'trap'
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

        for n, f in enumerate(símismo.lista_fechas[:fin]):
            if interpol == 'trap':
                vals_var_día.append((datos_crudos[n] + datos_crudos[n+1])/2)
                ajust_día = símismo.lista_fechas[n + 1] - f
                pesos.append((lista_tiempos[n+1]-lista_tiempos[n] + ajust_día*24*60*60)/(60*60))

                if n+1 == len(símismo.lista_fechas) or f != símismo.lista_fechas[n + 1]:
                    terminado = True
            elif interpol == 'ninguno':
                vals_var_día.append(datos_crudos[n])
                if n == len(símismo.lista_fechas) or f != símismo.lista_fechas[n + 1]:
                    terminado = True
            else:
                raise ValueError('Metodo de interpolación {0} no reconocido.'.format(interpol))

            if terminado:
                vals_var_día = np.array(vals_var_día)

                if interpol == 'ninguno':
                    pesos = [1]*len(vals_var_día)
                elif interpol == 'ninguno':
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

                datos += [var] + [float('NaN')] * (símismo.lista_fechas[n+1] - f - 1)
                vals_var_día = []
                pesos = []

                terminado = False

        símismo.datos = np.array(datos)


def leer_columnas(sistema, archivo):
    columnas = None
    if sistema == 'csv':
        try:
            with open(archivo, 'r') as d:
                for lín in d:
                    if len(lín) > 0:
                        columnas = lín.replace('\n', '').split(',')
                        break
        except FileNotFoundError:
            print('¡Error!')
            raise FileNotFoundError

        return columnas
    else:
        raise NotImplementedError('Falta código para comunicar con el formato de datos: '
                                  '{0}'.format(sistema))


def cargar_columna(columna, sistema, archivo):
    if sistema == 'csv':
        try:
            with open(archivo, 'r') as d:
                doc = d.readlines()
        except FileNotFoundError:
            print('¡Error!')
            raise FileNotFoundError

        n_col = doc[0].split(',').index(columna)
        datos = [l.split(',')[n_col] for l in doc[1:]]

    else:
        raise NotImplementedError('Falta código para comunicar con el formato de datos'
                                  '{0}'.format(sistema))
    return datos


def leer_fechas(fechas_crudas):
    lista_pos = [0, 1, 2]
    pos_año = pos_mes = pos_día = None
    lista_fechas = []

    for div in ['/', '-', '.']:
        if len(fechas_crudas[0].split(div)) == 3:
            lista_fechas = [x.split(div) for x in fechas_crudas if x != '\n' and x != '']
            for n in lista_fechas:
                for i in lista_pos:
                    if int(n[i]) > 31:
                        pos_año = i
                        lista_pos.pop(i)
                        continue
                    if 12 < int(n[i]) <= 31 and pos_año is not None:
                        pos_día = i
                        lista_pos.pop(i)
                        continue
                if len(lista_pos) == 1:
                    pos_mes = lista_pos[0]
                    break
        else:
            continue

    if pos_año is None or pos_mes is None or pos_día is None:
        raise ValueError('No se pudieron leer las fechas de la base de datos.')

    fecha_inic = ft.date(year=int(lista_fechas[0][pos_año]),
                         month=int(lista_fechas[0][pos_mes]),
                         day=int(lista_fechas[0][pos_día]))

    fechas = [(ft.date(year=int(x[pos_año]), month=int(x[pos_mes]), day=int(x[pos_día]))-fecha_inic).days
              for x in lista_fechas]

    return fecha_inic, np.array(fechas)


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
