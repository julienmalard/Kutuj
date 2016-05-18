import os.path
import warnings as aviso
import numpy as np
import scipy.stats as estad
import scipy.optimize as optimizar
import math as mat

from BD import BaseCentral
from Variables import Variable


class ControladorModelo(object):
    def __init__(símismo, archivo_base_central):
        tipo_archivo = os.path.splitext(os.path.split(archivo_base_central)[1])[1][1:]
        símismo.base_central = BaseCentral(archivo_base_central, tipo_archivo)
        símismo.base_derivados = None

        símismo.config = Modelo()


class Modelo(object):
    def __init__(símismo, varsx=None, vary=None):
        """
        Un modelo de predicción de datos climáticos.

        :param varsx: Variables con cuales vamos a predecir lo que queremos predecir.
        :type varsx: dict

        :param vary: El variable que queremos predecir.
        :type vary: Variable
        """

        # Guardar los variables predictores y para predecir
        símismo.varsX = varsx
        símismo.varY = vary

        # Si varsX no se especificó, crear un diccionario vacío
        if símismo.varsX is None:
            símismo.varsX = {}

        # Dos listas para guardar referencias a los datos de los variables.
        # datosY es simplemente una lista de matrices numpy con datos del variable.
        # datosX es una lista de matrices numpy, cada una con eje 0 = variable X y eje 1 = día del año.
        símismo.datosX = []
        símismo.datosY = []

        # El peso de cada variable X en las predicciones, en general
        símismo.pesos_vars = np.array([])

        # El peso de cada año en la predicción de un año en particular
        símismo.pesos_años = np.array([])

    def actualizar_datos(símismo, recalc=False):
        """
        Esta función actualiza las
        :param recalc: Determina si vamos a recalcular los pesos de los años basado en los nuevos datos o no.
        :type recalc: bool

        """

        datosx = []

        # Para cada variable X, en orden...
        for nombre, varx in sorted(símismo.varsX.items()):

            # Para cada año en los datos del variable...
            for año, datos in enumerate(varx.datos):

                # Si el año no existe ya en datosx, añadirlo
                if año >= len(datosx):
                    datosx.append([])

                # Guardar los datos de este variable
                datosx[año].append(datos)

        # Guardar los datos de los variables en el Modelo
        símismo.datosY = símismo.varY.datos
        símismo.datosX = [np.array(x) for x in datosx]

        # Si existen datos X e Y y queremos recalcular los pesos de los años, hacerlo ahora.
        if recalc:
            if len(símismo.datosX) and len(símismo.datosY):
                símismo.recalcular_pesos_años()
            else:
                aviso.warn('No se pudo recalcular los pesos anuales por falta de variable dependiente o independiente.')

    def recalcular_pesos_años(símismo):
        """
        Esta función recalcula los pesos de los años en comparación al año actual.
        """

        #
        x_conoc = símismo.datosX[:-1]
        x_actual = símismo.datosX[-1]
        pesos = símismo.pesos_vars

        for n, año in enumerate(x_conoc):
            x_conoc[n] = año[:, :x_actual.shape[1]]

        símismo.pesos_años = np.array([símismo.calc_peso_año(x_año, x_actual, pesos_vars=pesos) for x_año in x_conoc])

    def predecir(símismo, n_día):
        if not len(símismo.pesos_años):
            símismo.recalcular_pesos_años()
        assert type(símismo.pesos_años) is np.ndarray

        y_conoc = símismo.datosY[:-1]
        pesos_pred = símismo.pesos_años[:, n_día-1]

        return pesos_pred, y_conoc

    def calibrar(símismo):
        n_vars = símismo.datosX[0].shape[0]
        print('datosX: ', símismo.datosX)
        print(símismo.datosX[0].shape)
        símismo.pesos_vars = np.zeros((n_vars, 365), dtype=float)
        print('símismo.pesos_vars', símismo.pesos_vars)

        for i in range(1, 366):
            print('i: ', i)
            paráms = (símismo.datosX, símismo.datosY, i)
            print('símismo.datosY: ', símismo.datosY)
            inic = np.zeros(n_vars)
            print('inic.shape: ', inic.shape)
            calibrados = optimizar.minimize(símismo.calc_ajust_modelo, inic, args=paráms).x

            símismo.pesos_vars[:, i] = calibrados

    def calc_ajust_modelo(símismo, pesos, datos_x, datos_y, n_día):
        print('n_día', n_día)

        def calc_densidad(simil_años, y_años, y_observ):
            print('calculando densidad...')
            print('simil_años: ', simil_años)
            print('y_años: ', y_años)
            print('y_observ: ', y_observ)
            peso_años_norm = simil_años / np.sum(simil_años)
            dist_y = (y_años - y_observ) / (y_años.max() - y_años.min())
            densidad = np.sum(peso_años_norm * (1 - dist_y))

            return densidad

        densidades = np.empty(len(datos_x))
        print('dim densidades: ', len(datos_x))
        for n in range(len(datos_x)):
            print('n: ', n)
            x_ant = datos_x.copy()
            x_pred = x_ant.pop(n)
            y_ant = datos_y.copy()
            y_obs = y_ant.pop(n)

            x_ant = np.array(x_ant)
            print('x_ant 2: ', x_ant)
            print(x_ant.shape)
            x_pred = np.array(x_pred)
            y_ant = np.array(y_ant)
            y_obs = np.array(y_obs)

            if n_día is not None:
                x_ant = x_ant[:, :, :n_día]
                x_pred = x_pred[:, :n_día]
                y_ant = y_ant[:, :n_día]
                y_obs = y_obs[:n_día]

            print('x_ant 3: ', x_ant)

            print('x_pred', x_pred)
            print('y_ant', y_ant)
            print('y_obs', y_obs)

            print('x_ant', x_ant.shape)
            print('x_pred', x_pred.shape)
            print('y_ant', y_ant.shape)
            print('y_obs', y_obs.shape)

            matr_simil = np.empty(len(x_ant))

            for x in x_ant:
                print('x.shape', x.shape)
                matr_simil = símismo.calc_peso_año(x_pred, x, pesos_vars=pesos, día_único=True)

            densidades[n] = calc_densidad(matr_simil, y_ant, y_obs)
            print('densidades: ', densidades)

        return np.sum(densidades)

    @staticmethod
    def calc_peso_año(x1, x2, pesos_vars, día_único=False):
        print(x1.shape, x2.shape)
        assert x1.shape == x2.shape

        def wilcoxon(x_1, x_2):
            if np.array_equal(x_1, x_2):
                p = 1
            else:
                p = estad.wilcoxon(x_1, x_2).pvalue
            return p

        if día_único:
            simil = np.empty((x1.shape[0],1), dtype=float)
            for n, var in enumerate(x1):
                simil[n] = wilcoxon(x1[n], x2[n])

        else:
            simil = np.empty(x1.shape, dtype=float)
            for n, var in enumerate(x1):
                simil[n] = [wilcoxon(x1[n, :día], x2[n, :día]).pvalue for día in range(x1.shape[1])]

        print('simil', simil)
        print(simil.shape)
        print('pesos_vars', pesos_vars)
        print(pesos_vars.shape)
        peso_año = simil * pesos_vars.reshape((len(pesos_vars), 1))

        return peso_año

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
