import copy as copia
import math as mat
import os.path
from warnings import warn as avisar

import matplotlib.pyplot as dib
import numpy as np
import scipy.optimize as optimizar
import scipy.stats as estad

from BD import BasedeDatos
from Variables import Variable


class ControladorModelo(object):
    def __init__(símismo, archivo_base_central):
        tipo_archivo = os.path.splitext(os.path.split(archivo_base_central)[1])[1][1:]
        símismo.base_central = BasedeDatos(archivo_base_central, tipo_archivo)
        símismo.base_derivados = None

        símismo.Modelo = Modelo()


class Modelo(object):
    """
    Un modelo de predicción de datos climáticos.
    """

    def __init__(símismo, varsx=None, vary=None):
        """

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
        # datosY es simplemente una lista de matrices numpy con datos del variable, cada una con eje 0 = día del año.
        # datosX es una lista de matrices numpy, cada una con eje 0 = variable X y eje 1 = día del año.
        # Cada elemento en la lista representa un año distinto.
        símismo.datosX = []
        símismo.datosY = []

        # El peso de cada variable X en las predicciones, en general
        símismo.pesos_vars = np.array([])

        # El peso de cada año en la predicción de un año en particular.
        # Eje 0 = año, eje 1 = día del año
        símismo.pesos_años = np.array([])
        símismo.semej_años = np.array([])

    def actualizar_datos(símismo, recalc=False):
        """
        Esta función actualiza las listas de los datos del Modelo.

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

        # Si existen datos X e Y, tnato como pesos para los variables, y queremos recalcular los pesos de los años,
        # hacerlo ahora.
        if recalc:
            if len(símismo.datosX) and len(símismo.datosY) and len(símismo.pesos_vars):
                símismo.recalcular_pesos_años()
            else:
                avisar('No se pudo recalcular los pesos anuales por falta de variable dependiente o independiente,'
                       'o falta de calibración del modelo.')

    def recalcular_pesos_años(símismo, n_día=None):
        """
        Esta función recalcula los pesos de los años en comparación al año actual. Es una función de conveniencia,
          de pronto hacia no la necesitamos.

        :param n_día:
        :type n_día: int

        """

        # Calculamos los pesos de los años anteriores (conocidos) por su semejanza al año actual
        símismo.pesos_años = símismo.calc_pesos_años(n_día=n_día)

    def predecir(símismo, n_día=None, gráfico=True):
        """
        Esta función devuelve predicciones para variable Y para el año actual, basado en la semejanza entre este año
          y los años anteriores.

        :param n_día: Hasta cuál día del año usar los datos. Si no se especifica, tomamos todos los datos disponibles
          para el año actual
        :type n_día: int

        :param gráfico: Si hay que generar un gráfico de la predicción
        :type gráfico: bool

        :return: Los pesos para cada año anterior, y los variables Y para esos años. Con esto se puede generar un
          histograma o distrubución de probabilidad para los resultados. El caso más general (es decir, un modelo
          inútil) sería cuando los pesos de los años anteriores igualan todos 1.
        :rtype: (np.ndarray, np.ndarray)

        """

        # Si no se especificó el día hasta cual tomar los datos del año actual, usar todos los datos disponibles
        # en el año más recién.
        if n_día is None:
            n_día = len(símismo.varY.datos[-1])

        # Si ya no se calcularon los pesos para el año actual, calcularlos ahora.
        if not len(símismo.pesos_años):
            símismo.recalcular_pesos_años(n_día=n_día)

        # Los datos de Y conocidos son los datos para todos los años, menos el actual
        y_conoc = np.array([y[n_día] for y in símismo.datosY[:-1]])

        # Tomamos los pesos de todos los años anteriores (eje 1), en el día hasta cual tenemos datos (eje 0).
        pesos_pred = símismo.pesos_años[n_día, :-1]

        # Si hay que dibujar, hacerlo ahora.
        pesos_norm = np.empty_like(y_conoc)
        pesos_norm[:] = 1/len(y_conoc)

        if gráfico:
            dib.hist(x=y_conoc, weights=pesos_pred, facecolor='green', alpha=0.5)
            dib.hist(x=y_conoc, weights=pesos_norm, facecolor='green', alpha=0.2)
            dib.title('Distribución de probabilidad de predicción')
            dib.ylabel('Probabilidad')
            dib.xlabel('Valor')
            dib.show()

        return pesos_pred, y_conoc

    def calibrar(símismo):
        """
        Esta función calibra los pesos de los variables.

        """

        # El número de variables X (predictores) que tenemos
        n_vars = símismo.datosX[0].shape[0]

        # Crear una matriz para los pesos de los variables. Eje 0 = variable, eje 1 = día del año
        símismo.pesos_vars = np.zeros((n_vars, 365), dtype=float)

        # Una matriz con las semejanzas entre los años.
        # Eje 0 = variable, eje 1 = día del año, eje 2 = año 1, eje 3 = año 2
        símismo.semej_años = símismo.calc_semej_años()

        # Calibrar los pesos individualmente para cada día del año entre 1 y 365...
        for i in range(1, 365):

            # Los parámetros necesarios para la optimización (calibración)
            paráms = (símismo.datosX, símismo.datosY, i, símismo.semej_años)

            # Los valores iniciales para los pesos de los variables (1)
            inic = np.ones(n_vars)

            líms = [(0, 5)] * n_vars

            # Calibrar los pesos de los variables
            calibrados = optimizar.minimize(símismo.calc_ajust_modelo, inic, bounds=líms, args=paráms).x

            print('Día: ', i, calibrados)

            # Guardar los pesos de los variables calibrados para este día del año
            símismo.pesos_vars[:, i-1] = calibrados

    def calc_ajust_modelo(símismo, pesos_vars, datos_x, datos_y, n_día, semej_años):
        """
        Esta función calcula el ajuste del modelo. Sirve para la optimización de los parámetros.

        :param pesos_vars: Los pesos de los variables. Tiene que ser el primer parámetro para permitir la
          calibración del modelo.
        :type pesos_vars: np.ndarray

        :param datos_x: Los datos x, en forma de lista de matrices de datos de distintos años.
        :type datos_x: list

        :param datos_y: Los datos y, en forma de lista de matrices de datos de distintos años.
        :type datos_y: list

        :param n_día: El número del día del año para cual queremos calibrar el modelo. 1 indica el primer día del año.
        :type n_día: int

        :param semej_años: Una matriz con las semejanzas entre los años. Eje 0 = variable, eje 1 = año 1,
          eje 2 = año 2
        :type semej_años: np.ndarray

        :return: Un índice del ajuste del modelo.
        :rtype: float

        """

        # El número de años de datos disponibles para calcular el ajuste del modelo.
        n_años = len(datos_x)

        # Una matriz numpy para contener el ajuste del modelo para cada año
        densidades = np.empty(n_años)

        # Cortar los datos Y de cada año hasta la fecha de interés
        datos_y_n = [y[n_día-1] for y in datos_y]  # Únicamente guardamos el día de la fecha de interés

        # Para cada año en los datos disponibles, vamos a quitarlo de los datos e intentar predecirlo.
        for n in range(n_años):

            # Los datos y correspondiendo a los datos x de los años conocidos. Tomamos todos los años, en el día de
            # interés.
            y_conoc = copia.deepcopy(datos_y_n)

            # La obseravación del dato y para el año que queremos predecir. Lo quitamos de la lista de datos
            # conocidos.
            y_obs = y_conoc.pop(n)

            # Convertir la listas de datos y a una matriz numpy
            y_conoc = np.array(y_conoc)

            # Una matriz para guardar los pesos de cada año, únicamente para el último día de interés
            matr_pesos_años = símismo.calc_pesos_años(pesos_vars=pesos_vars, n_día=n_día,
                                                      semej_años=semej_años[:, :, n, :], n_año=n)
            matr_pesos_años = np.delete(matr_pesos_años, n, axis=1)

            densidades[n] = calc_densidad(matr_pesos_años, y_conoc, y_obs)

        # Devolver la suma de las densidades de cada año. Más densidad indica un mejor modelo, pero con SciPy
        # solamente podemos minimizar una función. Así que tenemos que devolver el negativo de la densidad.
        return -np.average(densidades)

    def guardar_calib(símismo, archivo):
        """
        Esta función guarda los resultados de una calibración.
        :param archivo: El archivo donode hay que guardar la calibración.
        :type archivo: str

        """

        np.savetxt(archivo, símismo.pesos_vars)

    def cargar_calib(símismo, archivo):
        """
        Esta función carga los resultados de una calibración guardada anteriormente.

        :param archivo: El archivo donode se encuentra la calibración guardada.
        :type archivo: str

        """

        símismo.pesos_vars = np.loadtxt(archivo)

    def calc_semej_años(símismo, tipo='diferencia'):
        """

        :param tipo:
        :type tipo:
        :return: Una matriz con las semejanzas entre los años.
          Eje 0 = variable, eje 1 = día del año, eje 2 = año 1, eje 3 = año 2
        :rtype:
        """

        n_años = len(símismo.datosX)
        n_vars = símismo.datosX[0].shape[0]

        simil_años = np.empty(shape=(n_vars, 365, n_años, n_años))

        for n in range(n_años):
            print('calculando semejanza para año %i' % n)

            simil = símismo.calc_semej_2_años(n_x_actual=n, x_anteriores=símismo.datosX, tipo=tipo)

            simil_años[:, :, n, :] = simil

        return simil_años

    def calc_pesos_años(símismo, n_año=None, n_día=None, pesos_vars=None, semej_años=None):
        """
        Esta martiz calcula los pesos de los años en comparación al año actual, basado en los pesos de los variables.

        :param n_año:
        :type n_año:

        :param n_día:
        :type n_día:

        :param pesos_vars: Los pesos de los variables
        :type pesos_vars: np.ndarray

        :param semej_años: Una matriz con las semejanzas entre los años. Eje 0 = variable, eje 1 = día del año,
          eje 2 = año 2.
        :type semej_años:

        :return: Los pesos de los años anteriores con referencia al año actual
        :rtype: np.ndarray
        """

        # Si no se especificó año de referencia, tomar el año más recién.
        if n_año is None:
            n_año = len(símismo.datosX) - 1

        # Si no se especificaro los pesos de los variables, usar los pesos del modelo.
        if pesos_vars is None:
            pesos_vars = símismo.pesos_vars  # Eje 0 = variable, eje 1 = día del año

        # Si no se especificó la semejanza entre los años, calcularla ahora.
        if semej_años is None:
            símismo.semej_años = símismo.calc_semej_años()
            semej_años = símismo.semej_años[:, :, n_año, :]  # Eje 0 = variable, eje 1 = día del año, eje 2 = año 2

        # Calcular el peso del año por subir la semejanza entre los años por cada variable al exponencial del peso de
        # dicho variable. Eje 0 = variable, eje 1 = año
        if pesos_vars.ndim == 1:
            if n_día is None:
                raise ValueError
            else:
                semej_años = semej_años[:, n_día:n_día+1, :]

        peso_año_por_var = np.power(semej_años, pesos_vars[..., np.newaxis])

        # Tomar el promedio del peso de cada variable, según el día del año y el año de comparación
        peso_año = np.average(peso_año_por_var, axis=0)  # Eje 0 = día, eje 1 = año 2

        # Normalizar los pesos a 1.
        suma = np.sum(peso_año, axis=1)  # Eje 0 = día del año
        suma[suma == 0] = 1  # Evitar dividir por 0 en la normalización
        pesos_años_norm = np.divide(peso_año, np.subtract(suma[..., np.newaxis], 1))  # Eje 0 = día, eje 1 = año 2

        return pesos_años_norm

    @staticmethod
    def calc_semej_2_años(x_anteriores, tipo, x_actual=None, n_x_actual=None, día_único=False):
        """
        Esta función determina el grado de semejanza entre los variables x de distintos años, según el

        :param x_anteriores: Lista de datos x (matrices numpy) de años anteriores
        :type x_anteriores: list

        :param tipo:
        :type tipo:

        :param x_actual: Matriz numpy de datos del año de interés
        :type x_actual: np.ndarray

        :param n_x_actual:
        :type n_x_actual:

        :param día_único: Una opción para determinar si únicamente estamos comparando los años hasta el último día
          de datos disponibles, o si queremos comparalos hasta cada día para cual hay datos disponibles.
        :type día_único: bool

        :return: el peso de cada año, determinado por el grado de semejanza con el año actual.
          Eje 0 = variable, eje 1 = día del año, eje 2 = año 2.
        :rtype: np.ndarray
        """

        if x_actual is None:
            x_actual = x_anteriores[n_x_actual]

        n_vars = x_actual.shape[0]

        # Crear una matriz vacía para guardar los resultados
        simil_años = np.ndarray(shape=(n_vars, 365, len(x_anteriores)))
        simil_años[:] = np.nan

        # Hay que asegurarse de que los datos x para todos los años tengan el mismo número de días
        lím = min(x_actual.shape[1], 365)

        for n_año, x_ant in enumerate(x_anteriores):

            # Si solamente estamos comparando hasta el último día de datos disponibles...
            if día_único:

                # Calcular la semejanza entre los dos años para cada variable
                simil_años[:, lím, n_año] = calc_simil(x_actual[:, :lím], x_ant[:, :lím], tipo=tipo)

            else:
                # Alternativamente, si queremos comparar los dos años hasta cada día para cual hay datos...

                # Para cada día (1 a 365) del año...
                for n in range(1, 366):
                    # Calcular la semejanza entre los dos años según el variable. Eje 0 = día; eje 1 = variable
                    simil = calc_simil(x_actual[:, :n], x_ant[:, :n], tipo=tipo)
                    simil_años[:, n - 1, n_año] = simil

        return simil_años

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


def calc_simil(x_1, x_2, tipo):
    """

    :param x_1:
    :type x_1: np.ndarray

    :param x_2:
    :type x_2: np.ndarray

    :param tipo:
    :type tipo:

    :return:
    :rtype:
    """

    n_vars_x = x_1.shape[0]
    s = np.empty(n_vars_x)

    for n_var in range(n_vars_x):
        var_x1 = x_1[n_var, :]
        var_x2 = x_2[n_var, :]

        if tipo == 'wilcoxon':
            if np.array_equal(var_x1, var_x2):
                # Si los datos son iguales, estad.wilcoxon genera un error. En aquél caso, p = 1.
                p = 1
            else:
                # Si los datos no son iguales, calcular el índice Wilcoxon
                p = estad.wilcoxon(var_x1, var_x2).pvalue

        elif tipo == 'r_cuadrado':
            if np.array_equal(var_x1, var_x2):
                p = 1
            else:
                if len(var_x1) == 1:
                    p = (var_x1 - var_x2) / var_x1
                else:
                    # Usar el coeficiente de determinación (R2)
                    r = estad.linregress(var_x1, var_x2)[2]
                    p = r ** 2

        elif tipo == 'diferencia':
            # La diferencia entre las series de datos
            dif = np.subtract(var_x1, var_x2)

            # Diferencia positivas
            dif_pos = np.abs(dif)

            # 1 representa series iguales, y 0 series lo más diferentes posible
            rango = (np.max([var_x1, var_x2]) - np.min([var_x1, var_x2]))
            if rango == 0:
                p = 1
            else:
                p = np.subtract(1, np.mean(dif_pos) / rango).round(10)

        else:
            raise ValueError

        s[n_var] = p

    return s


def calc_densidad(pesos_años, y_ant, y_observ):
    """
    Esta función calcula un índice de cuanto lejos la observación fue de la distribución de probabilidad
      generada predicha. Da importancia y a la exactitud (si la distribución está centrada en la observación)
      y a la precisión (si la distribución es estrecha, en otras palabras, si tiene un intervalo de confianza
      estrecho).

    :param pesos_años: Los pesos para dar a cada año anterior en la creación de la distribución de
      predicciones.
    :type pesos_años: np.ndarray

    :param y_ant: Las observaciones de años anteriores (para hacer la distribución de predicciones).
    :type y_ant: np.ndarray

    :param y_observ: La observación del año que querremos predecir
    :type y_observ: float

    :return: El índice de la performancia de la predicción.
    :rtype: float

    """

    # Calculamos la distancia relativa entre el valor del año actual y los valores en años anteriores.
    dist_y = (y_ant - y_observ) / (max(y_observ, y_ant.max()) - (min(y_observ, y_ant.min())))

    # Calcular un índice de dónde cae la observación en la densidad de las predicciones. 1 indica que la
    # predicción predijo 100% de probabilidad donde observamos la observación; 0 indica que la predicción
    # predijo 100% de probabilidad a la observación de años anteriores más lejos posible del año que querríamos
    # predecir.
    densidad = np.sum(np.multiply(pesos_años, np.subtract(1, np.abs(dist_y))))

    return densidad


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
