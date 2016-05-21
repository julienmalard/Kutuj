import os.path
import warnings as aviso
import math as mat
import numpy as np
import scipy.stats as estad
import scipy.optimize as optimizar
import matplotlib.pyplot as dib

from BD import BaseCentral
from Variables import Variable


class ControladorModelo(object):
    def __init__(símismo, archivo_base_central):
        tipo_archivo = os.path.splitext(os.path.split(archivo_base_central)[1])[1][1:]
        símismo.base_central = BaseCentral(archivo_base_central, tipo_archivo)
        símismo.base_derivados = None

        símismo.Modelo = Modelo()


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
        símismo.pesos_años = símismo.calc_pesos_años(x_actual=x_actual, x_anteriores=x_anterior)

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

        # Si ya no se calcularon los pesos para el año actual, calcularlos ahora.
        if not len(símismo.pesos_años):
            símismo.recalcular_pesos_años()

        # Si no se especificó el día hasta cual tomar los datos del año actual, usar todos los datos disponibles
        if n_día is None:
            n_día = len(símismo.varY.datos[-1])

        # Los datos de Y conocidos son los datos para todos los años, menos el actual
        y_conoc = np.array([y[-1] for y in símismo.datosY[:-1]])

        # Tomamos los pesos de todos los años anteriores (eje 0), en el día hasta cual tenemos datos (eje 1).
        pesos_pred = símismo.pesos_años[:, n_día]

        if gráfico:
            dib.hist(x=y_conoc, weights=pesos_pred, facecolor='green', alpha=0.5)
            dib.title('Distribución de probabilidad de predicción')
            dib.ylabel('Probabilidad')
            dib.xlabel('Valor')
            dib.show()

        print(y_conoc)
        print(pesos_pred)

        return pesos_pred, y_conoc

    def calibrar(símismo):
        """
        Esta función calibra los pesos de los variables.

        """

        # El número de variables X (predictores) que tenemos
        n_vars = símismo.datosX[0].shape[0]

        # Crear una matriz para los pesos de los variables. Eje 0 = variable, eje 1 = día del año
        símismo.pesos_vars = np.zeros((n_vars, 365), dtype=float)

        # Calibrar los pesos individualmente para cada día del año entre 1 y 365...
        for i in range(1, 15):

            # Los parámetros necesarios para la optimización (calibración)
            paráms = (símismo.datosX, símismo.datosY, i)

            # Los valores iniciales para los pesos de los variables (0)
            inic = np.zeros(n_vars)

            # Calibrar los pesos de los variables
            calibrados = optimizar.minimize(símismo.calc_ajust_modelo, inic, args=paráms).x

            print('Día: ', i)

            # Guardar los pesos de los variables calibrados para este día del año
            símismo.pesos_vars[:, i-1] = calibrados

    def calc_ajust_modelo(símismo, pesos_vars, datos_x, datos_y, n_día):
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

        :return: Un índice del ajuste del modelo.
        :rtype: float

        """

        def calc_densidad(pesos_años, y_años, y_observ):
            """
            Esta función calcula un índice de cuanto lejos la observación fue de la distribución de probabilidad
              generada predicha. Da importancia y a la exactitud (si la distribución está centrada en la observación)
              y a la precisión (si la distribución es estrecha, en otras palabras, si tiene un intervalo de confianza
              estrecho).

            :param pesos_años: Los pesos para dar a cada año anterior en la creación de la distribución de
              predicciones.
            :type pesos_años: np.ndarray

            :param y_años: Las observaciones de años anteriores (para hacer la distribución de predicciones).
            :type y_años: np.ndarray

            :param y_observ: La observación del año que querremos predecir
            :type y_observ: float

            :return: El índice de la performancia de la predicción.
            :rtype: float

            """

            # Calculamos la distancia relativa entre el valor del año actual y los valores en años anteriores.
            dist_y = (y_años - y_observ) / (y_años.max() - y_años.min())

            # Calcular un índice de dónde cae la observación en la densidad de las predicciones. 1 indica que la
            # predicción predijo 100% de probabilidad donde observamos la observación; 0 indica que la predicción
            # predijo 100% de probabilidad a la observación de años anteriores más lejos posible del año que querríamos
            # predecir.
            densidad = np.sum(np.multiply(pesos_años, (1 - dist_y)))

            return densidad

        # El número de años de datos disponibles para calcular el ajuste del modelo.
        n_años = len(datos_x)

        # Una matriz numpy para contener el ajuste del modelo para cada año
        densidades = np.empty(n_años)

        # Cortar los datos de cada año hasta la fecha de interés
        datos_x_n = [x[:, :n_día] for x in datos_x]
        datos_y_n = [y[n_día-1] for y in datos_y]  # Únicamente guardamos el día de la fecha de interés

        # Para cada año en los datos disponibles, vamos a quitarlo de los datos e intentar predecirlo.
        for n in range(n_años):

            # Los datos x conocidos.
            x_conoc = datos_x_n.copy()

            # Quitar los datos x del año que queremos predecir
            x_pred = x_conoc.pop(n)

            # Los datos y correspondiendo a los datos x de los años conocidos. Tomamos todos los años, en el día de
            # interés.
            y_conoc = datos_y_n.copy()

            # La obseravación del dato y para el año que queremos predecir. Lo quitamos de la lista de datos y
            # conocidos.
            y_obs = y_conoc.pop(n)

            # Convertir la listas de datos y a una matriz numpy
            y_conoc = np.array(y_conoc)

            # Una matriz para guardar los pesos de cada año, únicamente para el último día de interés
            matr_simil = símismo.calc_pesos_años(x_actual=x_pred, x_anteriores=x_conoc,
                                                 pesos_vars=pesos_vars, día_único=True)

            densidades[n] = calc_densidad(matr_simil, y_conoc, y_obs)

        # Devolver la suma de las densidades de cada año. Más densidad indica un mejor modelo, pero con SciPy
        # solamente podemos minimizar una función. Así que tenemos que devolver el negativo de la densidad.
        return -np.sum(densidades)

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

    def calc_pesos_años(símismo, x_actual, x_anteriores, día_único=False, pesos_vars=None):
        """
        Esta función devuelve los pesos de años
        :param x_actual: Matriz numpy de datos del año de interés
        :type x_actual: np.ndarray

        :param x_anteriores: Lista de datos x (matrices numpy) de años anteriores
        :type x_anteriores: list

        :param día_único: Una opción para determinar si únicamente estamos comparando los años hasta el último día
          de datos disponibles, o si queremos comparalos hasta cada día para cual hay datos disponibles.
        :type día_único: bool

        :param pesos_vars: Los pesos de los variables
        :type pesos_vars: np.ndarray

        :return: Los pesos de los años anteriores con referencia al año actual
        :rtype: np.ndarray
        """

        # Si no se especificaro los pesos de los variables, usar los pesos del modelo.
        if pesos_vars is None:
            pesos_vars = símismo.pesos_vars

        # Hay que asegurarse de que los datos x para todos los años tengan el mismo número de días
        lím = min(x_actual.shape[1], 365)

        pesos = np.array([símismo.calc_peso_año(x_ant[:, :lím], x_actual[:, :lím],
                                                pesos_vars=pesos_vars, día_único=día_único)
                          for x_ant in x_anteriores])

        # Normalizar los pesos a 1
        if np.sum(pesos) == 0:  # Evitar dividir por 0 en la normalización
            pesos[:] = 1
        pesos_norm = pesos / np.sum(pesos, axis=0)

        return pesos_norm

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
        :type día_único: bool
        
        :return: el peso del año, determinado por el grado de semejanza entre los dos años.
        :rtype: np.ndarray | float
        """

        # Los dos años tienen que tener el mismo tamaño de matriz. Si no, hay un error en otro lugar.
        assert x1.shape == x2.shape

        def wilcoxon(x_1, x_2):
            """
            La función con cual se calculará el grado de semejanza entre los datos de los dos años. Se usa una prueba
              estadística de Wilcoxon (si no sabes lo que es, Wikipedia tiene la respuesta).
              p =0 es menos semejanza, y p=1 indica datos iguales.

            :param x_1: Una serie de datos para comparar.
            :type x_1: np.ndarray

            :param x_2: La otra serie de datos para comparar
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

        # Si únicamente estamos comparando hasta el último día de datos disponibles...
        if día_único:

            # Calcular la semejanza entre los dos años para cada variable
            simil = np.array([wilcoxon(val_x1, val_x2) for (val_x1, val_x2) in zip(x1, x2)])

            # Para el exponencial después
            pesos_vars_reorg = pesos_vars.reshape((len(pesos_vars), 1))

        else:
            # Alternativamente, si queremos comparar los dos años hasta cada día para cual hay datos...

            # La matriz de semejanza tiene las mismas dimensiones que los datos
            simil = np.empty(x1.shape, dtype=float)
            simil[:] = np.nan

            # Para cada día (1 a 365) del año...
            for n in range(1, 366):
                # Calcular la semejanza entre los dos años según el variable. Eje 0 = día; eje 1 = variable
                simil[:, n-1] = [wilcoxon(val_x1[:n], val_x2[:n]) for (val_x1, val_x2) in zip(x1, x2)]

            # Para el exponencial después
            pesos_vars_reorg = simil

        # Calcular el peso del año por subir la semejanza entre los años por cada variable al exponencial del peso de
        # dicho variable.
        peso_año_por_var = np.power(simil, pesos_vars_reorg)

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
