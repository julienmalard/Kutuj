import tkinter as tk
import numpy as np
import datetime as ft

from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG
from Interfaz import Arte as Art

from BD import VariableBD
from Variables import Variable


# Caja lenguas
class ItemaLeng(CtrG.Itema):
    def __init__(símismo, lista, lengua):
        super().__init__(lista, objeto=lengua)


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
                                        transformación=rec['Transformación'], fecha_inic_año=rec['Fecha_inic'])
        except ValueError:
            print('Error cargando datos... :(')


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

        datos = símismo.objeto.datos

        colores = Art.escalar_colores(Fm.colores_gráficos[0], Fm.colores_gráficos[1], len(datos))

        for n, año in enumerate(datos):
            símismo.fig.plot(año, color=colores[n])

        símismo.fig.relim()
        símismo.fig.autoscale_view()


# Etapa 2, subcaja 1
class GrpCtrlsVarY(CtrG.GrupoControles):
    def __init__(símismo, pariente, apli, controles, gráfico, bt_guardar, bt_borrar):
        super().__init__(controles, gráfico=gráfico, bt_guardar=bt_guardar, bt_borrar=bt_borrar)
        símismo.pariente = pariente
        símismo.apli = apli
        símismo.datos = None

    def verificar_completo(símismo):
        ctrls = símismo.controles

        símismo.pariente.cambió_filtro_val(ctrls['FiltroVal'].val)

        campos_necesarios = ['Nombre', 'VarBD', 'MétodoCalc', 'FiltroVal',
                             'FiltroTmpInic', 'RefTmpInic', 'FiltroTmpFin', 'RefTmpFin']
        completos = [ctrls[x].val is not None and ctrls[x].val != '' for x in campos_necesarios]
        if not min(completos):
            return False
        else:
            if ctrls['FiltroTmpInic'].val in ['igual', 'sup', 'inf']:
                filtro = ctrls['FiltroValÚn'].val
                if filtro is None or filtro == '':
                    return False
            elif ctrls['FiltroTmpInic'].val == 'entre':
                filtros = [ctrls['FiltroValEntre1'].val, ctrls['FiltroValEntre2'].val]
                if None in filtros or '' in filtros:
                    return False

            return True

    def guardar(símismo, borrar=False):
        símismo.apli.modelo.config.varY = símismo.objeto
        símismo.apli.modelo.config.actualizar_datos()
        super().guardar(borrar=borrar)

        símismo.pariente.verificar_completo()

    def recrear_objeto(símismo):
        for ll, control in símismo.controles.items():
            símismo.receta[ll] = control.val
        # try:
        #     nombre = símismo.receta['VarBD']
        #     símismo.objeto = Variable(símismo.receta, símismo.apli.modelo.base_central.vars[nombre])
        # except ValueError:
        #     print('Error generando datos... :(')
        nombre = símismo.receta['VarBD']
        símismo.objeto = Variable(símismo.receta, símismo.apli.modelo.base_central.vars[nombre])


class GráfVarY(CtrG.Gráfico):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

    def dibujar(símismo):
        if símismo.objeto is not None:
            símismo.fig.set_title(símismo.objeto.nombre)
        else:
            símismo.fig.set_title('')
            return

        datos = símismo.objeto.datos

        if símismo.objeto.receta['RefTmpInic'] == 'abs' and símismo.objeto.receta['RefTmpFin'] == 'abs':
            datos_hist = [x[0] for x in datos]
            símismo.fig.hist(datos_hist, color=Fm.col_5)
        else:
            colores = Art.escalar_colores(Fm.colores_gráficos[0], Fm.colores_gráficos[1], len(datos))
            for n, año in enumerate(datos):
                símismo.fig.plot(año, color=colores[n])

        símismo.fig.relim()
        símismo.fig.autoscale_view()


# Etapa 2, subcaja 2
class GrpCtrlsVarX(CtrG.GrupoControles):
    def __init__(símismo, pariente, apli, controles, gráfico, lista, bt_guardar, bt_borrar):
        super().__init__(controles, constructor_itema=ItemaVarX, gráfico=gráfico, lista=lista,
                         bt_guardar=bt_guardar, bt_borrar=bt_borrar)
        símismo.pariente = pariente
        símismo.apli = apli
        símismo.datos = None

    def verificar_completo(símismo):
        ctrls = símismo.controles

        símismo.pariente.cambió_filtro_val(ctrls['FiltroVal'].val)

        campos_necesarios = ['Nombre', 'VarBD', 'MétodoCalc', 'FiltroVal',
                             'FiltroTmpInic', 'RefTmpInic', 'FiltroTmpFin', 'RefTmpFin']
        completos = [ctrls[x].val is not None and ctrls[x].val != '' for x in campos_necesarios]
        if not min(completos):
            return False
        else:
            if ctrls['FiltroTmpInic'].val in ['igual', 'sup', 'inf']:
                filtro = ctrls['FiltroValÚn'].val
                if filtro is None or filtro == '':
                    return False
            elif ctrls['FiltroTmpInic'].val == 'entre':
                filtros = [ctrls['FiltroValEntre1'].val, ctrls['FiltroValEntre2'].val]
                if None in filtros or '' in filtros:
                    return False

            return True

    def recrear_objeto(símismo):
        for ll, control in símismo.controles.items():
            símismo.receta[ll] = control.val
        try:
            nombre = símismo.receta['VarBD']
            símismo.objeto = Variable(símismo.receta, símismo.apli.modelo.base_central.vars[nombre])
        except ValueError:
            print('Error generando datos... :(')

    def guardar(símismo, borrar=True):
        super().guardar()
        símismo.apli.modelo.config.actualizar_datos()


class ListaVarsX(CtrG.ListaEditable):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)

        símismo.pariente = pariente
        nombres_cols = ['Nombre', 'Fuente', 'Calculado con', 'De valores']
        anchuras = Fm.anchos_cols_listavarX
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
        cj_fuente = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_mét_calc = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)
        cj_fltr_val = tk.Frame(cj_cols, **Fm.formato_secciones_itemas)

        símismo.etiq_nombre = tk.Label(cj_nombre, **Fm.formato_texto_itemas)
        símismo.etiq_fuente = tk.Label(cj_fuente, **Fm.formato_texto_itemas)
        símismo.etiq_calc = tk.Label(cj_mét_calc, **Fm.formato_texto_itemas)
        símismo.etiq_fltr_vals = tk.Label(cj_fltr_val, **Fm.formato_texto_itemas)

        símismo.etiquetas = [símismo.etiq_nombre, símismo.etiq_fuente, símismo.etiq_calc, símismo.etiq_fltr_vals]
        símismo.columnas = [cj_nombre, cj_fuente, cj_mét_calc, cj_fltr_val]
        for etiq in símismo.etiquetas:
            etiq.pack(**Fm.ubic_EtiqItemas)

        símismo.estab_columnas(anchuras=Fm.anchos_cols_listavarX)

        símismo.actualizar()

    def actualizar(símismo):
        rec = símismo.receta
        símismo.etiq_nombre.config(text=rec['Nombre'])
        símismo.etiq_fuente.config(text=rec['VarBD'])
        símismo.etiq_calc.config(text=rec['MétodoCalc'])

        if rec['FiltroVal'] == 'ninguno':
            texto = 'Ningún límite'
        elif rec['FiltroVal'] == 'igual':
            texto = 'Igual a {0}' % [rec['FiltroValÚn']]
        elif rec['FiltroVal'] == 'sup':
            texto = 'Superior a {0}' % [rec['FiltroValÚn']]
        elif rec['FiltroVal'] == 'inf':
            texto = 'Inferior a {0}' % [rec['FiltroValÚn']]
        elif rec['FiltroVal'] == 'entre':
            texto = 'Entre {0} y {1}' % [rec['FiltroValEntre1'], rec['FiltroValEntre2']]
        else:
            raise KeyError
        símismo.etiq_fltr_vals.config(text=texto)

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

        datos = símismo.objeto.datos
        colores = Art.escalar_colores(Fm.colores_gráficos[0], Fm.colores_gráficos[1], len(datos))
        for n, año in enumerate(datos):
            símismo.fig.plot(año, color=colores[n])

        símismo.fig.relim()
        símismo.fig.autoscale_view()
