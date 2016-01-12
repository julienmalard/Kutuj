import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG


class CjCtrlsVarBD(CtrG.CjControles):
    def __init__(símismo, pariente, apli):
        super().__init__(pariente, constructor_itema=ItemaVarBD)
        bd = apli.Modelo.base_central
        ingr_nombre = CtrG.IngrTexto(símismo, 'Nombre', comanda=símismo.cambió_control,
                                     ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        cols_potenciales = bd.nombres_cols.copy()
        cols_potenciales.remove(bd.id_cols['fecha'])
        cols_potenciales.remove(bd.id_cols['tiempo'])
        menú_col = CtrG.Menú(símismo, 'Columna', opciones=cols_potenciales, comanda=símismo.cambió_control,
                             ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        símismo.controles = {'Nombre': ingr_nombre, 'Columna': menú_col}

        símismo.pack()


class ItemaVarBD(CtrG.Itema):
    def __init__(símismo, nombre, col):
        super().__init__(lista_itemas, constructor_objeto=símismo.sacar_col_bd)

        símismo.nombre = nombre
        símismo.col = col

    def sacar_col_bd(símismo, modelo):
        modelo.base_central.cargar_var(nombre=símismo.nombre, col_datos=símismo.col)
