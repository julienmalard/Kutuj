import scipy as sp
import numpy as np


class Corrida(object):
    def __init__(símismo, bd):
        símismo.datosX = bd.varsX
        símismo.datosY = bd.varY
        símismo.x_act = None
        símismo.pesos = []

    def predecir(símismo, datosx, datosy, x_act, pesos=None):
        if pesos is None:
            pesos = símismo.pesos

        for núm_var, var in enumerate(datosx):
            for núm_año, datos_año in enumerate(var):
                simil[núm_año] += [sp.statistics.wilcoxon(x_act[núm_var][var],
                                                          datos_año[:len(x_act[núm_var][var])])
                                   **pesos[núm_var]]

    def calib_peso:

