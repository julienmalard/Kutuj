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

        # El peso de cada año en la predicción de un año en particular.
        # Eje 0 = año, eje 1 = día del año
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

        # Los años conocidos son todos menos el año más recién
        x_anterior = símismo.datosX[:-1]

        # El año actual es el más recién
        x_actual = símismo.datosX[-1]

        # Para cada año de datos anteriores (conocidos), guardamos únicamente los datos hasta el último día para cuál
        # hay datos en el año actual.
        for n, año in enumerate(x_anterior):
            # Guardamos todo el eje 0 (variable), pero únicamente los valores del eje 1 correspondiendo a los datos
            # disponibles para el año actual.
            x_anterior[n] = año[:, :x_actual.shape[1]]

        # Calculamos los pesos de los años anteriores (conocidos) por su semejanza al año actual
        símismo.pesos_años = np.array([símismo.calc_peso_año(x_año, x_actual, pesos_vars=símismo.pesos_vars)
                                       for x_año in x_anterior])

    def predecir(símismo, n_día=None):
        """
        Esta función devuelve predicciones para variable Y para el año actual, basado en la semejanza entre este año
          y los años anteriores.

        :param n_día: Hasta cuál día del año usar los datos. Si no se especifica, tomamos todos los datos disponibles
          para el año actual
        :type n_día: int

        :return: Los pesos para cada año anterior, y los variables Y para esos años. Con esto se puede generar un
          histograma o distrubución de probabilidad para los resultados. El caso más general (es decir, un modelo
          inútil) sería cuando los pesos de los años anteriores igualan todos 1.
        :rtype: (np.ndarray, np.ndarray)

        """

        # Si ya no se calcularon los pesos para el año actual, calcularlos ahora.
        if not len(símismo.pesos_años):
            símismo.recalcular_pesos_años()

        # Si no se especificó el día hasta cual tomar los datos del año actual, usar todos los datos disponibles
        if n_día is None:
            n_día = len(símismo.varY.datos[-1])

        # Los datos de Y conocidos son los datos para todos los años, menos el actual
        y_conoc = símismo.datosY[:-1]

        # Tomamos los pesos de todos los años anteriores (eje 0), en el día hasta cual tenemos datos (eje 1).
        pesos_pred = símismo.pesos_años[:, n_día]

        return pesos_pred, y_conoc

    def calibrar(símismo):
        """
        Esta función calibra los pesos de los variables.

        """

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
        """
        Esta función determina el grado de semejanza entre los variables x de distintos años, según el

        :param x1: Datos de uno de los dos años para comparar. Formato de matriz numpy, con eje 0 = variable y
          eje 1 = día del año
        :type x1: np.ndarray

        :param x2: Datos del otro año para comparar. Mismo formato que x1.
        :type x2: np.ndarray

        :param pesos_vars: Los pesos de importancia relativa a cada variable.
        :type pesos_vars: np.ndarray

        :param día_único: Una opción para determinar si únicamente estamos comparando los años hasta el último día
          de datos disponibles, o si queremos comparalos hasta cada día para cual hay datos disponibles.
        
        :return: el peso del año, determinado por el grado de semejanza entre los dos años.
        :rtype: np.ndarray
        """

        # Los dos años tienen que tener el mismo tamaño de matriz. Si no, hay un error en otro lugar.
        assert x1.shape == x2.shape

        def wilcoxon(x_1, x_2):
            """
            La función con cual se calculará el grado de semejanza entre los datos de los dos años. Se usa una prueba
              estadística de Wilcoxon (si no sabes lo que es, Wikipedia tiene la respuesta.
              p =0 es menos semejanza, y p=1 indica datos iguales.

            :param x_1: Una serie de datos para comparar
            :type x_1: np.ndarray

            :param x_2: La otra serie de datos para comparar.
            :type x_2: np.ndarray

            :return: El valor p de la prueba de Wilcoxon
            :rtype: float
            """

            # Si los datos son iguales, estad.wilcoxon genera un error. En aquél caso, p = 1.
            if np.array_equal(x_1, x_2):
                p = 1
            else:
                p = estad.wilcoxon(x_1, x_2).pvalue

            return p

        # La matriz de semejanza tiene las mismas dimensiones que los datos
        simil = np.empty(x1.shape, dtype=float)
        simil[:] = np.nan

        # Si únicamente estamos comparando hasta el último día de datos disponibles...
        if día_único:

            # Calcular la semejanza entre los dos años para cada variable
            simil[:, 1] = [wilcoxon(val_x1, val_x2) for (val_x1, val_x2) in enumerate(zip(x1, x2))]

        else:
            # Alternativamente, si queremos comparar los dos años hasta cada día para cual hay datos...

            # Para cada variable en los datos...
            for n, var in enumerate(x1):
                # Calcular la semejanza entre los años según el variable
                simil[n, :] = [wilcoxon(x1[n, :día], x2[n, :día]).pvalue for día in range(x1.shape[1])]

        # Calcular el peso del año por subir la semejanza entre los años por cada variable al exponencial del peso de
        # dicho variable.
        peso_año_por_var = np.power(simil, pesos_vars.reshape((len(pesos_vars), 1)))

        # Tomar el producto del peso de cada variable, según el día del año
        peso_año = np.prod(peso_año_por_var, axis=0)

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
    """
    Esta función calcula la raíz del error cuadrado medio (recm).

    :param y: vector numpy de las observaciones
    :type y: np.ndarray

    :param y_pred: vector numpy de las predicciones
    :type y_pred: np.ndarray

    :return: El valor de la recm.
    :rtype: float

    """

    recm = mat.sqrt(np.sum(np.square(y-y_pred))/y.size)

    return recm
