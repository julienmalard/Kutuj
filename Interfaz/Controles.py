import tkinter as tk
import numpy as np
import datetime as ft

from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG

from BD import VariableBD


# Etapa 1, subcaja 2
class GrpCtrlsVarBD(CtrG.GrupoControles):
    def __init__(símismo, apli, controles, gráfico, lista, bt_guardar, bt_borrar):
        super().__init__(controles, constructor_itema=ItemaVarBD, gráfico=gráfico, lista=lista,
                         bt_guardar=bt_guardar, bt_borrar=bt_borrar)
        símismo.apli = apli
        símismo.datos = None

    def verificar_completo(símismo):
        campos_necesarios = ['Nombre', 'Columna', 'Fecha_inic', 'Interpol', 'Transformación']
        completos = [símismo.controles[x].val is not None and símismo.controles[x].val is not ''
                     for x in campos_necesarios]
        if min(completos):
            return True
        else:
            return False

    def recrear_objeto(símismo):
        for ll, control in símismo.controles.items():
            símismo.receta[ll] = control.val
        rec = símismo.receta

        try:
            símismo.objeto = VariableBD(base_de_datos=símismo.apli.modelo.base_central,
                                        nombre=rec['Nombre'], columna=rec['Columna'], interpol=rec['Interpol'],
                                        transformación=rec['Transformación'])
        except ValueError:
            print('Error cargando datos... :(')

    def editar(símismo, itema):
        símismo.itema = itema
        símismo.objeto = itema.objeto
        for i in itema.receta:
            símismo.controles[i].poner(itema.receta[i])

        símismo.receta = itema.receta


class ListaVarsBD(CtrG.ListaEditable):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

        símismo.pariente = pariente
        nombres_cols = ['Nombre', 'Columna', 'Transformación', 'Interpolación']
        anchuras = Fm.anchos_cols_listavarVB
        símismo.gen_encbz(nombres_cols, anchuras)

    def añadir(símismo, itema):
        super().añadir(itema)
        símismo.pariente.verificar_completo()

    def quitar(símismo, itema):
        super().quitar(itema)
        símismo.pariente.verificar_completo()


class ItemaVarBD(CtrG.ItemaEditable):
    def __init__(símismo, grupo_control, lista_itemas):
        super().__init__(grupo_control=grupo_control, lista_itemas=lista_itemas)

        símismo.cj_cols = cj_cols = tk.Frame(símismo, **Fm.formato_cajas)
        cj_nombre = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_columna = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_trans = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_interpol = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)

        símismo.etiq_nombre = tk.Label(cj_nombre, **Fm.formato_texto_itemas)
        símismo.etiq_columna = tk.Label(cj_columna, **Fm.formato_texto_itemas)
        símismo.etiq_trans = tk.Label(cj_trans, **Fm.formato_texto_itemas)
        símismo.etiq_interpol = tk.Label(cj_interpol, **Fm.formato_texto_itemas)

        símismo.etiquetas = [símismo.etiq_nombre, símismo.etiq_columna, símismo.etiq_trans, símismo.etiq_interpol]
        símismo.columnas = [cj_nombre, cj_columna, cj_trans, cj_interpol]
        for etiq in símismo.etiquetas:
            etiq.pack(**Fm.ubic_EtiqItemas)

        símismo.estab_columnas(anchuras=Fm.anchos_cols_listavarVB)

        símismo.actualizar()

    def actualizar(símismo):
        símismo.etiq_nombre.config(text=símismo.receta['Nombre'])
        símismo.etiq_columna.config(text=símismo.receta['Columna'])
        símismo.etiq_trans.config(text=símismo.receta['Transformación'])
        símismo.etiq_interpol.config(text=símismo.receta['Interpol'])

    def resaltar(símismo):
        for etiq in símismo.etiquetas:
            etiq.config(font=Fm.fuente_etiq_itema_sel)

    def desresaltar(símismo):
        for etiq in símismo.etiquetas:
            etiq.config(font=Fm.fuente_etiq_itema_norm)


class GráfVarBD(CtrG.Gráfico):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

    def dibujar(símismo):
        if símismo.objeto is not None:
            símismo.fig.set_title(símismo.objeto.nombre)
        else:
            símismo.fig.set_title('')
            return

        fecha_inic = símismo.objeto.fecha_inic
        n_día_inic_año = símismo.controles['Fecha_inic'].val
        datos = símismo.objeto.datos

        datos_por_año = []
        if n_día_inic_año > (fecha_inic - ft.date(fecha_inic.year, 1, 1)).days:
            fecha_ref = ft.date(fecha_inic.year-1, 1, 1) + ft.timedelta(days=n_día_inic_año-1)
        else:
            fecha_ref = ft.date(fecha_inic.year, 1, 1) + ft.timedelta(days=n_día_inic_año-1)

        fecha_inic_año_act = fecha_ref
        while True:
            datos_año_actual = []
            fecha_inic_año_próx = ft.date(fecha_inic_año_act.year + 1, 1, 1) + ft.timedelta(days=n_día_inic_año-1)

            inic = (fecha_inic_año_act - fecha_inic).days
            if inic < 0:
                datos_año_actual = [float('NaN')] * (fecha_inic-fecha_ref).days
                inic = 0
            fin = (fecha_inic_año_próx - fecha_inic).days

            if fin > len(datos):
                datos_año_actual = np.concatenate((datos_año_actual, datos[inic:]))
                datos_por_año.append(datos_año_actual)
                break

            datos_año_actual = np.concatenate((datos_año_actual, datos[inic:fin]))
            datos_por_año.append(datos_año_actual)
            fecha_inic_año_act = fecha_inic_año_próx

        def escalar(val1, val2, m):
            escl = [val1 + (val2 - val1)*(i+1)/m for i in range(m)]
            return escl
        r = escalar(Fm.colores_gráficos[0][0]/256, Fm.colores_gráficos[1][0]/256, len(datos_por_año))
        v = escalar(Fm.colores_gráficos[0][1]/256, Fm.colores_gráficos[1][1]/256, len(datos_por_año))
        a = escalar(Fm.colores_gráficos[0][2]/256, Fm.colores_gráficos[1][2]/256, len(datos_por_año))

        colores = list(zip(r, v, a))
        for n, año in enumerate(datos_por_año):
            símismo.fig.plot(año, color=colores[n])

        símismo.fig.relim()
        símismo.fig.autoscale_view()


# Etapa 2, subcaja 2
class GrpCtrlsVarX(CtrG.GrupoControles):
    def __init__(símismo, apli, controles, gráfico, lista, bt_guardar, bt_borrar):
        super().__init__(controles, constructor_itema=ItemaVarBD, gráfico=gráfico, lista=lista,
                         bt_guardar=bt_guardar, bt_borrar=bt_borrar)
        símismo.apli = apli
        símismo.datos = None

    def verificar_completo(símismo):
        campos_necesarios = ['Nombre', 'Columna', 'Fecha_inic', 'Interpol', 'Transformación']
        completos = [símismo.controles[x].val is not None and símismo.controles[x].val is not ''
                     for x in campos_necesarios]
        if min(completos):
            return True
        else:
            return False

    def recrear_objeto(símismo):
        for ll, control in símismo.controles.items():
            símismo.receta[ll] = control.val
        rec = símismo.receta
        print('Recreando...', rec)
        try:
            símismo.objeto = VariableBD(base_de_datos=símismo.apli.modelo.base_central,
                                        nombre=rec['Nombre'], columna=rec['Columna'], interpol=rec['Interpol'],
                                        transformación=rec['Transformación'])
        except ValueError:
            print('Error cargando datos... :(')

    def editar(símismo, itema):
        print('Obj. controles', símismo.receta)
        print('Obj. itema', itema.receta)
        símismo.itema = itema
        símismo.objeto = itema.objeto
        for i in itema.receta:
            símismo.controles[i].poner(itema.receta[i])

        símismo.receta = itema.receta


class ListaVarsX(CtrG.ListaEditable):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

        símismo.pariente = pariente
        nombres_cols = ['Nombre', 'Columna', 'Transformación', 'Interpolación']
        anchuras = Fm.anchos_cols_listavarVB
        símismo.gen_encbz(nombres_cols, anchuras)

    def añadir(símismo, itema):
        super().añadir(itema)
        símismo.pariente.verificar_completo()

    def quitar(símismo, itema):
        super().quitar(itema)
        símismo.pariente.verificar_completo()


class ItemaVarX(CtrG.ItemaEditable):
    def __init__(símismo, grupo_control, lista_itemas):
        super().__init__(grupo_control=grupo_control, lista_itemas=lista_itemas)

        símismo.cj_cols = cj_cols = tk.Frame(símismo, **Fm.formato_cajas)
        cj_nombre = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_columna = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_trans = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_interpol = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)

        símismo.etiq_nombre = tk.Label(cj_nombre, **Fm.formato_texto_itemas)
        símismo.etiq_columna = tk.Label(cj_columna, **Fm.formato_texto_itemas)
        símismo.etiq_trans = tk.Label(cj_trans, **Fm.formato_texto_itemas)
        símismo.etiq_interpol = tk.Label(cj_interpol, **Fm.formato_texto_itemas)

        símismo.etiquetas = [símismo.etiq_nombre, símismo.etiq_columna, símismo.etiq_trans, símismo.etiq_interpol]
        símismo.columnas = [cj_nombre, cj_columna, cj_trans, cj_interpol]
        for etiq in símismo.etiquetas:
            etiq.pack(**Fm.ubic_EtiqItemas)

        símismo.estab_columnas(anchuras=Fm.anchos_cols_listavarVB)

        símismo.actualizar()

    def actualizar(símismo):
        símismo.etiq_nombre.config(text=símismo.receta['Nombre'])
        símismo.etiq_columna.config(text=símismo.receta['Columna'])
        símismo.etiq_trans.config(text=símismo.receta['Transformación'])
        símismo.etiq_interpol.config(text=símismo.receta['Interpol'])

    def resaltar(símismo):
        for etiq in símismo.etiquetas:
            etiq.config(font=Fm.fuente_etiq_itema_sel)

    def desresaltar(símismo):
        for etiq in símismo.etiquetas:
            etiq.config(font=Fm.fuente_etiq_itema_norm)


class GráfVarX(CtrG.Gráfico):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

    def dibujar(símismo):
        if símismo.objeto is not None:
            símismo.fig.set_title(símismo.objeto.nombre)
        else:
            símismo.fig.set_title('')
            return

        fecha_inic = símismo.objeto.fecha_inic
        n_día_inic_año = símismo.controles['Fecha_inic'].val
        datos = símismo.objeto.datos

        datos_por_año = []
        if n_día_inic_año > (fecha_inic - ft.date(fecha_inic.year, 1, 1)).days:
            fecha_ref = ft.date(fecha_inic.year-1, 1, 1) + ft.timedelta(days=n_día_inic_año-1)
        else:
            fecha_ref = ft.date(fecha_inic.year, 1, 1) + ft.timedelta(days=n_día_inic_año-1)

        fecha_inic_año_act = fecha_ref
        while True:
            datos_año_actual = []
            fecha_inic_año_próx = ft.date(fecha_inic_año_act.year + 1, 1, 1) + ft.timedelta(days=n_día_inic_año-1)

            inic = (fecha_inic_año_act - fecha_inic).days
            if inic < 0:
                datos_año_actual = [float('NaN')] * (fecha_inic-fecha_ref).days
                inic = 0
            fin = (fecha_inic_año_próx - fecha_inic).days

            if fin > len(datos):
                datos_año_actual = np.concatenate((datos_año_actual, datos[inic:]))
                datos_por_año.append(datos_año_actual)
                break

            datos_año_actual = np.concatenate((datos_año_actual, datos[inic:fin]))
            datos_por_año.append(datos_año_actual)
            fecha_inic_año_act = fecha_inic_año_próx

        def escalar(val1, val2, m):
            escl = [val1 + (val2 - val1)*(i+1)/m for i in range(m)]
            return escl
        r = escalar(Fm.colores_gráficos[0][0]/256, Fm.colores_gráficos[1][0]/256, len(datos_por_año))
        v = escalar(Fm.colores_gráficos[0][1]/256, Fm.colores_gráficos[1][1]/256, len(datos_por_año))
        a = escalar(Fm.colores_gráficos[0][2]/256, Fm.colores_gráficos[1][2]/256, len(datos_por_año))

        colores = list(zip(r, v, a))
        for n, año in enumerate(datos_por_año):
            símismo.fig.plot(año, color=colores[n])

        símismo.fig.relim()
        símismo.fig.autoscale_view()
