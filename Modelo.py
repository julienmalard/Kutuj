import os.path
import numpy as np
import scipy.stats as estad
import scipy.optimize as optimizar
import math as mat

from BD import BaseCentral


class Modelo(object):
    def __init__(símismo, archivo_base_central):
        tipo_arciho = os.path.splitext(os.path.split(archivo_base_central)[1])[1][1:]
        símismo.base_central = BaseCentral(archivo_base_central, tipo_arciho)
        símismo.base_derivados = None

        símismo.config = ConfigModelo()


class ConfigModelo(object):
    def __init__(símismo, varsx=None, vary=None):
        símismo.varsX = varsx
        símismo.varY = vary

        if símismo.varsX is None:
            símismo.varsX = {}

        símismo.datosX = []
        símismo.datosY = []
        símismo.pesos_vars = None

    def actualizar_datos(símismo):
        símismo.datosX = []
        for ll, varx in sorted(símismo.varsX.items()):
            for año, datos in enumerate(varx.datos):
                if año >= len(símismo.datosX):
                    símismo.datosX.append([])
                símismo.datosX[año].append([datos])
        símismo.datosY = símismo.varY.datos

    def calibrar(símismo, datos_x, datos_y):
        def calc_error_intervalos(pesos_var):
            distribs = []
            pesos = []
            y_preds = []
            for n_año, año in enumerate(datos_x):
                x_conocido = datos_x.copy
                y_conocido = datos_y.copy
                x_pred = x_conocido.pop(n_año)
                y_pred = y_conocido.pop(n_año)

                distrib, pesos_años = símismo.predecir(x_pred, x_conocido, y_conocido, pesos_var)

                y_preds.append(y_pred)
                distribs.append(np.array(distrib))
                pesos.append(pesos_años)

            predicciones = (np.array(distribs), np.array(pesos))
            error = símismo.validar(predicciones, np.array(y_preds))[0]

            return error

        pesos_var_inic = np.repeat([1], datos_x[0].shape[0])
        pesos_calibrados = optimizar.minimize(calc_error_intervalos, pesos_var_inic).x

        return pesos_calibrados

    def calibrar_todos_días(símismo, datos_x, datos_y):
        pesos_vars_diarios = np.zeros((365, datos_x[0].shape[0]))
        for i in range(365):
            pesos_vars_diarios[i] = símismo.calibrar(datos_x[:i+1], datos_y[:i+1])

        símismo.pesos_vars = pesos_vars_diarios

    @staticmethod
    def predecir(datos_x_actuales, datos_x, datos_y, pesos_vars):

        def calc_dist(datos1, datos2, pesos=pesos_vars):
            peso_año = 0
            for n_var, dato in enumerate(datos1):
                simil = (1-estad.wilcoxon(dato, datos2[n_var]).pvalue)
                peso_año += simil ** pesos[n_var]
            return peso_año

        pesos_años = np.empty(shape=len(datos_x))
        for n, año in enumerate(datos_x):
            pesos_años[n] = (calc_dist(datos_x_actuales[año], datos_x))

        predicciones = [datos_y, pesos_años]
        return predicciones

    @staticmethod
    def validar(predicciones, obs):
        distribuciones = predicciones[0]
        pesos_años = predicciones[1]
        assert len(distribuciones) == len(pesos_años) == len(obs)
        p = np.sum(np.greater(distribuciones, 0) * pesos_años, axis=1) * 2 / np.sum(pesos_años, axis=1)

        p_único = np.unique(p)
        p_obs = np.zeros(np.size(p_único))
        for n, q in enumerate(p_único):
            p_obs[n] = np.sum(p <= q) / len(p)

        recm = calc_recm(p_obs, p)

        return recm, (p, p_obs)


def calc_recm(y, y_pred):
    recm = mat.sqrt(np.sum(np.square(y-y_pred))/y.size)

    return recm
