import numpy as np
import datetime as ft


class Variable(object):
    def __init__(símismo, subyacente, fecha_inic):
        símismo.subyacente = subyacente
        símismo.fecha_inic = fecha_inic

        símismo.mét_derivación = ''
        símismo.filtros_deriv = []
        símismo.lím_infer = ()
        símismo.lím_super = ()
        símismo.día_inic_año = 0
        símismo.datos = None

    def recalcular(símismo):
        datos = []
        vals_año_act = []

        for n, i in enumerate(símismo.subyacente):
            fecha_act = (símismo.fecha_inic + ft.timedelta(days=n))
            año_act = fecha_act.year

            if símismo.lím_infer[1] == 'abs':
                lím_infer = símismo.lím_infer[0]
            elif símismo.lím_infer[1] == 'rel':
                lím_infer = n + símismo.lím_infer[0]

            if símismo.lím_super[1] == 'abs':
                lím_super = símismo.lím_super[0]
            elif símismo.lím_super[1] == 'rel':
                lím_super = n + símismo.lím_super[0]

            if lím_infer >= 0 and (lím_super + 1) < len(símismo.subyacente):
                rango_activo = símismo.subyacente[lím_infer:lím_super+1]

                for f in símismo.filtros_deriv:
                    if f[0] == '<':
                        rango_filtrado = [x for x in rango_activo if x < f[1]]
                    if f[0] == '>':
                        rango_filtrado = [x for x in rango_activo if x > f[1]]
                    if f[0] == '<=':
                        rango_filtrado = [x for x in rango_activo if x <= f[1]]
                    if f[0] == '>=':
                        rango_filtrado = [x for x in rango_activo if x >= f[1]]

                if símismo.mét_derivación == 'máximo':
                    val = np.max(rango_filtrado)
                elif símismo.mét_derivación == 'mínimo':
                    val = np.min(rango_filtrado)
                elif símismo.mét_derivación == 'cumulativo':
                    val = np.sum(rango_filtrado)
                elif símismo.mét_derivación == 'número':
                    val = len(rango_filtrado)
                else:
                    raise ValueError('Método de derivación {0} para no reconocido.'.format(símismo.mét_derivación))
            else:
                val = float('NaN')

            if len(datos) == 0:
                vals_año_act += [float('NaN')] * (fecha_act-símismo.fecha_inic).days

            vals_año_act += val

            if (ft.date(year=año_act, month=1, day=1) - fecha_act).days == símismo.día_inic_año:
                datos.append(vals_año_act)
                vals_año_act = []

        símismo.datos = datos
