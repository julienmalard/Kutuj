import numpy as np
import datetime as ft


class BaseCentral(object):
    def __init__(símismo, archivo, sistema='csv'):
        símismo.sistema = sistema.lower()
        símismo.archivo = archivo
        símismo.temporal_a_diario = {}
        símismo.id_cols = {'fecha': '', 'tiempo': '', 'vars': {}}
        símismo.fecha_inic = None
        símismo.datos = {}
        símismo.info_datos = {'mét_combin_tiempo': {}, 'mét_interpol': {}}

    def cargar_var(símismo, nombre, col_datos=None, mét_combin_tiempo=None, mét_interpol=None):
        if mét_combin_tiempo is None:
            mét_combin_tiempo = símismo.info_datos['mét_combin_tiempo'][nombre]
        if mét_interpol is None:
            mét_interpol = símismo.info_datos['mét_interpol'][nombre]

        if col_datos is None:
            col_datos = símismo.id_cols['vars'][nombre]

        datos_crudos = cargar_columna(col_datos, símismo.sistema, símismo.archivo)
        lista_fechas = cargar_columna(símismo.id_cols['fecha'], símismo.sistema, símismo.archivo)
        lista_tiempos = cargar_columna(símismo.id_cols['tiempo'], símismo.sistema, símismo.archivo)
        símismo.datos[nombre] = gen_datos_diarios(datos_crudos=datos_crudos, lista_fechas=lista_fechas,
                                                  lista_tiempos=lista_tiempos,
                                                  mét_tiempo_a_día=mét_combin_tiempo, mét_interpol=mét_interpol)
        símismo.info_datos['mét_combin_tiempo'][nombre] = mét_combin_tiempo
        símismo.info_datos['mét_interpol'][nombre] = mét_interpol


def gen_datos_diarios(datos_crudos, lista_fechas, lista_tiempos=None,
                      mét_tiempo_a_día='prom', mét_interpol='trap'):
        lista_var = []
        vals_var_día = []

        for n, f in enumerate(lista_fechas[1:]):
            if mét_interpol == 'trap':
                vals_var_día += [(datos_crudos[n] + datos_crudos[n-1])/2 *
                                 (lista_tiempos[n]-lista_tiempos[n-1])]
            elif mét_interpol == 'ninguno':
                vals_var_día += datos_crudos[n]
            else:
                raise ValueError('Metodo de interpolación {0} no reconocido.'.format(mét_interpol))

            if lista_fechas[n] != lista_fechas[n + 1] or n == len(lista_fechas):

                vals_var_día = np.array(vals_var_día)
                if mét_interpol == 'trap':
                    vals_var_día /= np.sum(lista_fechas[-1] - lista_fechas[0])

                if mét_tiempo_a_día == 'sumar':
                    var = vals_var_día.sum()
                elif mét_tiempo_a_día == 'máx':
                    var = vals_var_día.max()
                elif mét_tiempo_a_día == 'mín':
                    var = vals_var_día.min()
                elif mét_tiempo_a_día == 'prom':
                    var = vals_var_día.mean()
                else:
                    raise ValueError('Metodo de generación de datos diarios "{0}" '
                                     'no reconocido.'.format(mét_tiempo_a_día))

                lista_var += [var]
                vals_var_día = []

        datos = [lista_var[0]]

        for n, f in enumerate(lista_fechas[1:]):
            datos += [float('NaN')] * (f - lista_fechas[n] - 1) + lista_var[n+1]
            
        return datos


def cargar_columna(columna, sistema, archivo):
    if sistema == 'csv':
        try:
            with open(archivo, 'r') as d:
                doc = d.readlines()
        except FileNotFoundError:
            print('¡Error!')
            raise FileNotFoundError

        datos = [l[columna] for l in doc]
    else:
        raise NotImplementedError('Falta código para comunicar con el formato de datos'
                                  '{0}'.format(sistema))
    return datos


def leer_fechas(lista_fechas):
    lista_pos = [0, 1, 2]
    pos_año = pos_mes = pos_día = None
    for div in ['/', '-', '.']:
        if len(lista_fechas[0].split(div)) == 3:
            lista_fechas = [x.split(div) for x in lista_fechas]
            for n in lista_fechas:
                for i in lista_pos:
                    if n[i] > 31:
                        pos_año = i
                        lista_pos.pop(i)
                        continue
                    if 12 < n[i] <= 31 and pos_año is not None:
                        pos_día = i
                        lista_pos.pop(i)
                        continue
                if len(lista_pos) == 1:
                    pos_mes = lista_pos[0]
                    break
        else:
            continue
    if pos_año is None or pos_mes is None or pos_día is None:
        print('No se pudieron leer las fechas de la base de datos.')
        return ValueError('No se pudieron leer las fechas de la base de datos.')

    fecha_inic = ft.date(year=lista_fechas[0][pos_año],
                         month=lista_fechas[0][pos_mes],
                         day=lista_fechas[0][pos_día])

    fechas = [(ft.date(year=x[pos_año], month=x[pos_mes], day=x[pos_día])-fecha_inic).days
              for x in lista_fechas]

    return fecha_inic, fechas


def leer_tiempo(lista_tiempos):
    lista_tiempos = [x.split(':') for x in lista_tiempos]
    if len(lista_tiempos[0]) == 3:
        lista_tiempos = [((x[0] * 60) + x[1]) * 60 + x[2] for x in lista_tiempos]
    elif len(lista_tiempos[0]) == 2:
        lista_tiempos = [((x[0] * 60) + x[1]) * 60 for x in lista_tiempos]
    else:
        print('No se pudieron leer los datos de hora de la base de datos.')
        return ValueError('No se pudieron leer los datos de hora de la base de datos.')

    return lista_tiempos
