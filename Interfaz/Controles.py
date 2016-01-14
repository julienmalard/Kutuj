import tkinter as tk
import datetime as ft

from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG

from BD import VariableBD


class GrpCtrlsVarBD(CtrG.GrupoControles):
    def __init__(símismo, apli, controles, gráfico, lista):
        super().__init__(controles, constructor_itema=ItemaVarBD, gráfico=gráfico, lista=lista)
        símismo.apli = apli
        símismo.datos = None

    def verificar_completo(símismo):
        campos_necesarios = ['Nombre', 'Columna', 'Fecha_inic', 'Interpol', 'Transformación']
        completos = [símismo.controles[x].val is not None for x in campos_necesarios]
        if min(completos):
            return True
        else:
            return False

    def recrear_objeto(símismo):
        for ll, control in símismo.controles.items():
            símismo.receta[ll] = control.val
        rec = símismo.receta

        símismo.objeto = VariableBD(base_de_datos=símismo.apli.base_central,
                                    nombre=rec['Nombre'], columna=rec['Columna'], interpol=['Interpol'],
                                    transformación=['Transformación'])


class ListaVarsBD(CtrG.ListaEditable):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)


class ItemaVarBD(CtrG.ItemaEditable):
    def __init__(símismo, grupo_control, lista_itemas):

        cj_nombre = tk.Frame(símismo, **Fm.formato_secciones_itemas)
        cj_columna = tk.Frame(símismo, **Fm.formato_secciones_itemas)
        cj_trans = tk.Frame(símismo, **Fm.formato_secciones_itemas)
        cj_interpol = tk.Frame(símismo, **Fm.formato_secciones_itemas)

        símismo.etiq_nombre = tk.Label(cj_nombre, **Fm.formato_etiq)
        símismo.etiq_columna = tk.Label(cj_columna, **Fm.formato_etiq)
        símismo.etiq_trans = tk.Label(cj_trans, **Fm.formato_etiq)
        símismo.etiq_interpol = tk.Label(cj_interpol, **Fm.formato_etiq)

        columnas = [cj_nombre, cj_columna, cj_trans, cj_interpol]

        super().__init__(grupo_control=grupo_control, lista_itemas=lista_itemas,
                         columnas=columnas, ancho=Fm.anchos_cols_listavarVB)

        símismo.actualizar()

    def actualizar(símismo):
        símismo.etiq_nombre.config(text=símismo.receta['Nombre'])
        símismo.etiq_columna.config(text=símismo.receta['Columna'])
        símismo.etiq_trans.config(text=símismo.receta['Transformación'])
        símismo.etiq_interpol.config(text=símismo.receta['Interpol'])

    def resaltar(símismo):
        símismo.etiq_nombre.config(bg=Fm.col_4)
        símismo.etiq_columna.config(bg=Fm.col_4)
        símismo.etiq_trans.config(bg=Fm.col_4)
        símismo.etiq_interpol.config(bg=Fm.col_4)

    def desresaltar(símismo):
        símismo.etiq_nombre.config(bg=Fm.col_fondo)
        símismo.etiq_columna.config(bg=Fm.col_fondo)
        símismo.etiq_trans.config(bg=Fm.col_fondo)
        símismo.etiq_interpol.config(bg=Fm.col_fondo)


class GráfVarBD(CtrG.Gráfico):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

    def dibujar(símismo):
        símismo.fig.set_title(símismo.objeto.nombre)
        fecha_inic = símismo.objeto.fecha_inic
        n_día_inic_año = símismo.controles['Fecha_inic'].val
        datos = símismo.objeto.datos

        datos_por_año = []
        if n_día_inic_año > (fecha_inic - ft.date(fecha_inic.year, 1, 1)).days:
            fecha_ref = ft.date(fecha_inic.year-1, 1, 1) + n_día_inic_año
        else:
            fecha_ref = ft.date(fecha_inic.year, 1, 1) + n_día_inic_año

        datos_año_actual = [float('NaN')] * (fecha_inic-fecha_ref).days
        fecha_inic_año = fecha_inic
        while True:
            fecha_inic_año_próx = ft.date(fecha_ref.year + 1, 1, 1) + ft.timedelta(days=n_día_inic_año)

            inic = (fecha_inic_año - fecha_inic).days
            fin = (fecha_inic_año_próx - fecha_inic).days
            if fin > len(datos):
                datos_año_actual += datos[inic:]
                datos_por_año.append(datos_año_actual)
                break

            datos_año_actual += datos[inic:fin]
            datos_por_año.append(datos_año_actual)
            fecha_inic_año = fecha_inic_año_próx
            datos_año_actual = []

        for año in datos_por_año:
            símismo.fig.plot(año)
