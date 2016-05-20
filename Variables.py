import numpy as np
import datetime as ft

from BD import VariableBD


class Variable(object):
    def __init__(símismo, receta=None, fuente=None):
        """

        :param receta:
        :param fuente:
        :type fuente: VariableBD
        """

        símismo.receta = receta
        símismo.fuente = fuente
        símismo.datos = None
        símismo.fecha_inic = None
        símismo.nombre = None

        if receta is not None:
            símismo.recalcular(receta, fuente)

    def recalcular(símismo, receta, fuente):
        """

        :param receta:
        :param fuente:

        """

        assert type(fuente) is VariableBD

        # Poner los atributos del Variable a fecha
        símismo.receta = receta
        símismo.fecha_inic = fuente.fecha_inic_datos
        símismo.nombre = receta['Nombre']

        # El método de cálculo del variable
        mét_calc = receta['MétodoCalc']

        # El tipo de filtro para valores del variable fuente
        tipo_filtro_val = receta['FiltroVal']

        # Variables para contener los límites del filtro de valores
        filtro_val_exact = filtro_val_inf = filtro_val_sup = None

        if tipo_filtro_val == 'ninguno':

            # Si no hay filtro, no hacer nada.
            pass

        elif tipo_filtro_val == 'igual':

            # Si el filtro es de valores igual a un valor particular, guardar este valor
            filtro_val_exact = receta['FiltroValÚn']

        elif tipo_filtro_val == 'sup':

            # Si el filtro es de valores superiores a un valor particular, guardar este valor
            filtro_val_inf = receta['FiltroValÚn']

        elif tipo_filtro_val == 'inf':

            # Si el filtro es de valores inferiores a un valor particular, guardar este valor
            filtro_val_sup = receta['FiltroValÚn']

        elif tipo_filtro_val == 'entre':

            # Si el filtro es de valores entre dos valores particulares, guardar los dos valores
            filtro_val_inf = receta['FitroValEntre1']
            filtro_val_sup = receta['FitroValEntre2']

        else:

            # Si tipo_filtro_val no era una de las
            raise KeyError(tipo_filtro_val)

        # El tiempo inicial para calcular el variable
        filtro_tmp_inic = receta['FiltroTmpInic']

        # La referencia para el tiempo inicial (abs = día del año, rel = relativo a hoy)
        ref_tmp_inic = receta['RefTmpInic']

        # El tiempo final para el variable
        filtro_tmp_fin = receta['FiltroTmpFin']

        # La referencia para el tiempo final
        ref_tmp_fin = receta['RefTmpFin']

        # para simplificar el código
        datos_fuente = fuente.datos

        # La lista en cual pondremos los datos calculados
        datos = []

        for n_año, año in enumerate(datos_fuente):
            datos_año = []
            for n_día, día in enumerate(año):

                # Filtrar por la fecha

                if ref_tmp_inic == 'abs':
                    lím_infer = filtro_tmp_inic
                elif ref_tmp_inic == 'rel':
                    lím_infer = n_día + filtro_tmp_inic
                else:
                    raise KeyError

                if ref_tmp_fin == 'abs':
                    lím_super = filtro_tmp_fin + 1
                elif ref_tmp_fin == 'rel':
                    lím_super = n_día + filtro_tmp_fin + 1
                else:
                    raise KeyError

                cabeza = []
                cola = []
                if lím_infer < 0:
                    if (n_año - 1) >= 0:
                        cabeza = datos_fuente[n_año - 1][lím_infer:]
                    else:
                        cabeza = [float('NaN')] * (-lím_infer)
                    lím_infer = 0

                if lím_super > (len(año) + 1):
                    if (n_año + 1) < len(datos_fuente):
                        cola = datos_fuente[n_año + 1][:lím_super - len(año)]
                    else:
                        cola = [float('NaN')] * (lím_super-len(año))
                    lím_super = len(año) + 1

                plazo = np.array(np.concatenate((cabeza, año[lím_infer:lím_super+1], cola)), dtype=float)

                # Filtrar por el valor

                if filtro_val_exact is not None:
                    np.place(plazo, plazo != filtro_val_exact, [float('NaN')])
                if filtro_val_inf is not None:
                    np.place(plazo, plazo <= filtro_val_inf, [float('NaN')])
                if filtro_val_sup is not None:
                    np.place(plazo, plazo >= filtro_val_sup, [float('NaN')])

                # Calcular el variable
                if mét_calc == 'val_tot':
                    valor = np.nansum(plazo)
                elif mét_calc == 'val_prom':
                    valor = np.nanmean(plazo)
                elif mét_calc == 'núm_días':
                    valor = np.count_nonzero(~np.isnan(plazo))
                elif mét_calc == 'núm_días_consec':
                    valor = [np.count_nonzero(~np.isnan(x)) for x in np.split(plazo, np.where(np.isnan(plazo))[0])]
                else:
                    raise KeyError('Método de cálculo {0} para no reconocido.'.format(mét_calc))

                datos_año.append(valor)

            datos.append(np.array(datos_año))

        símismo.datos = datos
