import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG


class ListaVarsBD(CtrG.ListaItemas):
    def __init__(símismo, pariente, controles, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)


class ItemaVarBD(CtrG.Itema):
    def __init__(símismo, nombre, col):
        super().__init__(lista_itemas, constructor_objeto=símismo.sacar_col_bd)

        símismo.nombre = nombre
        símismo.col = col

        símismo.datos

    def sacar_col_bd(símismo, modelo):
        modelo.base_central.cargar_var(nombre=símismo.nombre, col_datos=símismo.col)


class GráfVarBD(CtrG.Gráfico):
    def __init__(símismo, pariente, datos, ubicación, tipo_ubic):
        super().__init__(pariente, datos=datos, ubicación=ubicación, tipo_ubic=tipo_ubic)

        símismo.datos = datos

    def dibujar(símismo):
        día = símismo.datos['día']
        for año in símismo.datos['valores']:
            símismo.fig.plot(día, año)
