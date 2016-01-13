import tkinter as tk
import datetime as ft

from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG

from BD import VariableBD


class GrpCtrlsVarBD(CtrG.GrupoControles):
    def __init__(símismo, apli, controles, gráfico):
        super().__init__(controles, constructor_itema=ItemaVarBD, gráfico=gráfico)
        símismo.apli = apli
        símismo.datos = None

    def verificar_completo(símismo):
        campos_necesarios = ['Nombre', 'Columna', 'Fecha_inic', 'Interpol']

        completos = [símismo.controles[x].val is not None for x in campos_necesarios]
        if min(completos):
            return True
        else:
            return False

    def refrescar_objeto(símismo):
        nombre = símismo.controles['Nombre'].val
        columna = símismo.controles['Columna'].val
        interpol = símismo.controles['Interpol'].val
        gen_diaria = símismo.controles['Gen_diaria'].val
        símismo.objeto = VariableBD(base_de_datos=símismo.apli.base_central,
                                    nombre=nombre, columna=columna, interpol=gen_diaria, gen_diaria=interpol)


class ListaVarsBD(CtrG.ListaItemas):
    def __init__(símismo, pariente, controles, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)


class ItemaVarBD(CtrG.Itema):
    def __init__(símismo, nombre, col):
        super().__init__(lista_itemas, constructor_objeto=símismo.sacar_col_bd)


        símismo.nombre = nombre
        símismo.col = col



    def sacar_col_bd(símismo, modelo):
        modelo.base_central.cargar_var(nombre=símismo.nombre, col_datos=símismo.col)


class GráfVarBD(CtrG.Gráfico):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

    def dibujar(símismo):
        símismo.fig.set_title(símismo.objeto.nombre)
        fecha_inic = símismo.objeto.fecha_inic
        fecha_inic_año = símismo.controles['Fecha_inic'].val
        datos = símismo.objeto.datos.copy()

        datos_por_año = []

        final_año = (ft.date(fecha_inic.year+1,1,1)-ft.date(fecha_inic.year,1,1)).days
        inic_año = (fecha_inic-ft.date(fecha_inic.year,1,1)).days

        datos_por_año.append(datos[inic_año:final_año])


        for año in :
            símismo.fig.plot(datos_por_año[], fechas_por_año[])
