import numpy as np
import scipy as sp


class Control(object):
    def __init_(símismo, base_central):
        símismo.base_central = base_central
        símismo.base_derivados = None


class Modelo(object):
    def __init__(símismo, varsx, vary):
        símismo.varsX = varsx
        símismo.varY = vary
        símismo.datos = []

    def añadir_varx(símismo, varx):
        símismo.varsX.append(varx)
        for año, datos_año in enumerate(varx.datos):
            símismo.datos = np.vstack((símismo.datos[año], datos_año))

    def calibrar(símismo):
        pesos =
        pesos_calibrados = sp.minimize(símismo.predecir, pesos)

    @staticmethod
    def predecir(datos_x_actuales, datos_x, datos_y, pesos_vars):

        def calc_dist(datos1, datos2, pesos=pesos_vars):
            peso_año = 0
            for n_var, dato in enumerate(datos1):
                simil = sp.wilcoxon(dato, datos2[n_var])
                peso_año += simil ** pesos[n_var]
            return peso_año

        pesos_años = np.empty(shape=len(datos_x))
        for n, año in enumerate(datos_x):
            pesos_años[n] = (calc_dist(datos_x_actuales[año], datos_x))

        predicciones = [datos_y, pesos_años]
        return predicciones




        predicciones = datos_y[len(datos_x_act - 1)]
        pesos_predicciones = pesos_años

        distrib_predic = [predicciones, pesos_predicciones]

        return distrib_predic



    @staticmethod
    def validar(predicciones, obs):
        porcentil_datos = np.inverse_percentile(obs, predicciones[0], weights=predicciones[1])
        x = unique(porcentil_datos)
        y = []
        for porcentil in x:
            y.append(np.sum(porcentil_datos <= porcentil))

        rmse = rmse_1(x,y)

        return rmse, [x, y]


def rmse_1(x, y):

