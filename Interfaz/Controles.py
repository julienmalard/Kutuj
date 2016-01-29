import tkinter as tk

from BD import VariableBD
from Interfaz import Arte as Art
from Interfaz import Botones as Bt
from Interfaz import ControlesGenéricos as CtrG
from Interfaz import Formatos as Fm
from Variables import Variable


# Caja lenguas
class CajaAñadirLeng(tk.Frame):
    def __init__(símismo, pariente, caja):
        super().__init__(caja, **Fm.formato_cajas)
        Bt.BotónImagen(símismo, comanda=símismo.acción_bt_plus, formato=Fm.formato_botones,
                       img_norm=Art.imagen('BtPlus_norm'), img_sel=Art.imagen('BtPlus_sel'),
                       ubicación=Fm.ubic_CjCamposAñLeng, tipo_ubic='pack')
        símismo.pariente = pariente

        símismo.cj_campos = cj_campos = tk.Frame(símismo, **Fm.formato_cajas)
        símismo.ingr_leng = CtrG.IngrTexto(cj_campos, nombre=None, ubicación=Fm.ubic_CjCamposAñLeng, tipo_ubic='pack')

        Bt.BotónImagen(cj_campos, comanda=símismo.acción_bt_guardar, formato=Fm.formato_botones,
                       img_norm=Art.imagen('BtMarca_norm'), img_sel=Art.imagen('BtMarca_sel'),
                       ubicación=Fm.ubic_BtsAñadirLeng, tipo_ubic='pack')

        símismo.IzqDer = Bt.BotónAltern(cj_campos, formato=Fm.formato_botones,
                                        img_1=Art.imagen('BtEscribIzqDer'), img_2=Art.imagen('BtEscribDerIzq'),
                                        ubicación=Fm.ubic_BtsAñadirLeng, tipo_ubic='pack')

        símismo.mostrando = False

    def acción_bt_plus(símismo):
        if not símismo.mostrando:
            símismo.cj_campos.pack(**Fm.ubic_CjCamposAñLeng)
        else:
            símismo.cj_campos.pack_forget()

        símismo.mostrando = not símismo.mostrando

    def acción_bt_guardar(símismo):
        nombre = símismo.ingr_leng.val
        if len(nombre):
            izqder = símismo.IzqDer.estado
            símismo.pariente.añadir_lengua(nombre=nombre, izqder=izqder)
        símismo.ingr_leng.borrar()


class ItemaLeng(CtrG.Itema):
    def __init__(símismo, pariente, lista, nombre, lengua, estado, utilizando=False, utilizable=True, borrable=True):
        super().__init__(lista_itemas=lista)
        símismo.nombre = nombre
        símismo.lengua = lengua

        cj_bt_utilizar = tk.Frame(símismo, **Fm.formato_secciones_itemas)
        cj_central = tk.Frame(símismo, **Fm.formato_secciones_itemas)
        cj_bts = tk.Frame(símismo, **Fm.formato_secciones_itemas)

        if utilizando:
            img_norm = Art.imagen('BtCasilla_sel')
        else:
            img_norm = Art.imagen('BtCasilla_norm')
        símismo.bt_utilizar = Bt.BotónImagen(cj_bt_utilizar, comanda=lambda x=nombre: pariente.utilizar(x),
                                             formato=Fm.formato_botones,
                                             img_norm=img_norm,
                                             img_sel=Art.imagen('BtCasilla_sel'),
                                             img_bloq=Art.imagen('BtCasilla_bloq'),
                                             ubicación=Fm.ubic_IzqLstLeng, tipo_ubic='pack')
        if not utilizable:
            símismo.bt_utilizar.bloquear()

        if 0 < estado < 1:
            ancho_etiq_nombre = 90
        else:
            ancho_etiq_nombre = 150

        cj_etiq_nombre_leng = tk.Frame(cj_central, width=ancho_etiq_nombre, **Fm.formato_cj_etiq_nombre_leng)
        cj_etiq_nombre_leng.pack_propagate(0)
        símismo.etiq_nombre = tk.Label(cj_etiq_nombre_leng, text=símismo.nombre,
                                       font=Fm.fuente_etiq_itema_norm, **Fm.formato_etiq_nombre_leng)
        símismo.etiq_nombre.pack(**Fm.ubic_etiq_nombre_leng)
        cj_etiq_nombre_leng.pack(**Fm.ubic_IzqLstLeng)

        if 0 < estado < 1:
            color_barra = Art.inter_color(Fm.colores_prog_leng, p=estado, tipo='hex')
            altura, ancho = Fm.dim_barra_prog_leng
            barra_prog = tk.Canvas(cj_central, width=ancho, height=altura, background=Fm.col_fondo,
                                   highlightthickness=1, highlightbackground=color_barra)
            barra_prog.create_rectangle(0, 0, round(ancho*estado), altura, fill=color_barra, outline=color_barra)
            barra_prog.pack(Fm.ubic_DerLstLeng)

        símismo.bt_editar = Bt.BotónImagen(cj_bts, comanda=lambda x=nombre: pariente.editar(x),
                                           formato=Fm.formato_botones,
                                           img_norm=Art.imagen('BtEditarItema_norm'),
                                           img_sel=Art.imagen('BtEditarItema_sel'),
                                           ubicación=Fm.ubic_IzqLstLeng, tipo_ubic='pack')
        símismo.bt_borrar = Bt.BotónImagen(cj_bts, comanda=lambda x=nombre: pariente.confirmar_borrar(x),
                                           formato=Fm.formato_botones,
                                           img_norm=Art.imagen('BtBorrarItema_norm'),
                                           img_sel=Art.imagen('BtBorrarItema_sel'),
                                           img_bloq=Art.imagen('BtBorrarItema_bloq'),
                                           ubicación=Fm.ubic_IzqLstLeng, tipo_ubic='pack')
        if not borrable:
            símismo.bt_borrar.bloquear()

        cj_bt_utilizar.pack(**Fm.ubic_IzqLstLeng)
        cj_central.pack(**Fm.ubic_CjCentLstLeng)
        cj_bts.pack(**Fm.ubic_BtsAñadirLeng)


class CajaEditLeng(tk.Frame):
    def __init__(símismo, pariente, leng_base, dic_leng_base, leng_edit, dic_leng_edit):
        super().__init__(pariente, **Fm.formato_CjEditLeng)
        símismo.pariente = pariente
        símismo.dic_leng_edit = dic_leng_edit

        cj_cbz = tk.Frame(símismo, **Fm.formato_cajas)

        etiq_cbz = tk.Label(cj_cbz, text='Traducciones', **Fm.formato_EtiqCbzEditLeng)

        cj_nombres_lengs = tk.Frame(cj_cbz, **Fm.formato_cajas)
        etiq_base = tk.Label(cj_nombres_lengs, text=leng_base, **Fm.formato_EtiqLengBase)
        etiq_edit = tk.Label(cj_nombres_lengs, text=leng_edit, **Fm.formato_EtiqLengEdit)

        etiq_base.pack(**Fm.ubic_EtiqLengs)
        etiq_edit.pack(**Fm.ubic_EtiqLengs)

        lín_hor_1 = tk.Frame(símismo, **Fm.formato_LínHor)

        etiq_cbz.pack(**Fm.ubic_CjNomEditLeng)
        cj_nombres_lengs.pack(**Fm.ubic_CjNomEditLeng)

        cj_lista = tk.Frame(símismo, **Fm.formato_cajas)
        lista = CtrG.ListaItemas(cj_lista, formato_cj=Fm.formato_LstEditLeng,
                                 ubicación=Fm.ubic_LstEditLeng, tipo_ubic='place')
        símismo.itemas = []
        for ll, texto in sorted(dic_leng_base['Trads'].items()):
            if ll in dic_leng_edit['Trads'].keys():
                texto_trad = dic_leng_edit['Trads'][ll]
            else:
                texto_trad = ''
            nuevo_itema = ItemaEditTrad(lista=lista, llave=ll, texto_origin=texto, texto_trad=texto_trad)
            símismo.itemas.append(nuevo_itema)

        lín_hor_2 = tk.Frame(símismo, **Fm.formato_LínHor)

        cj_bts = tk.Frame(símismo, **Fm.formato_cajas)
        símismo.bt_guardar = Bt.BotónTexto(cj_bts, texto='Guardar',
                                           formato_norm=Fm.formato_BtGuardar_norm,
                                           formato_sel=Fm.formato_BtGuardar_sel,
                                           ubicación=Fm.ubic_BtsGrupo, tipo_ubic='pack',
                                           comanda=símismo.guardar)

        símismo.bt_no_guardar = Bt.BotónTexto(cj_bts, texto='No guardar',
                                              formato_norm=Fm.formato_BtBorrar_norm,
                                              formato_sel=Fm.formato_BtBorrar_sel,
                                              ubicación=Fm.ubic_BtsGrupo, tipo_ubic='pack',
                                              comanda=símismo.cerrar)

        cj_cbz.pack(**Fm.ubic_CjCbzCjEditLeng)
        lín_hor_1.pack(**Fm.ubic_LínHorCjEditLeng)
        cj_lista.pack(**Fm.ubic_CjCentrCjEditLeng)
        lín_hor_2.pack(**Fm.ubic_LínHorCjEditLeng)
        cj_bts.pack(**Fm.ubic_CjBtsCjEditLeng)
        símismo.place(**Fm.ubic_CjEditLeng)

    def guardar(símismo):
        for itema in símismo.itemas:
            símismo.dic_leng_edit['Trads'][itema.llave] = itema.sacar_trad()
        símismo.pariente.DicLeng.guardar()
        símismo.pariente.refrescar()
        símismo.cerrar()

    def cerrar(símismo):
        símismo.destroy()


class ItemaEditTrad(CtrG.Itema):
    def __init__(símismo, lista, llave, texto_origin, texto_trad):
        super().__init__(lista_itemas=lista)
        símismo.llave = llave
        cj_tx_orig = tk.Frame(símismo, **Fm.formato_CjLengTxOrig)
        etiq_tx_orig = tk.Label(cj_tx_orig, text=texto_origin, **Fm.formato_EtiqLengTxOrig)
        cj_trad = tk.Frame(símismo, **Fm.formato_cajas)

        símismo.campo_texto = tk.Text(cj_trad, **Fm.formato_CampoTexto)
        símismo.campo_texto.insert('end', texto_trad)

        etiq_tx_orig.pack(side='top')
        símismo.campo_texto.pack()
        cj_tx_orig.pack(side='left', padx=5, pady=5, fill=tk.Y, expand=True)
        cj_trad.pack(**Fm.ubic_EtiqLengs)

    def sacar_trad(símismo):
        return símismo.campo_texto.get('1.0', 'end').replace('\n', '')


class CajaAvisoReinic(tk.Frame):
    def __init__(símismo, texto):
        super().__init__(**Fm.formato_CajaAvisoReinic)

        etiq = tk.Label(símismo, text=texto, **Fm.formato_EtiqLengReinic)
        etiq.pack(**Fm.ubic_etiq_aviso_inic_leng)

        símismo.bt = Bt.BotónTexto(símismo, texto='Entendido',
                                   formato_norm=Fm.formato_BtAvisoInic_norm,
                                   formato_sel=Fm.formato_BtAvisoInic_sel,
                                   ubicación=Fm.ubic_bt_aviso_inic_leng, tipo_ubic='pack',
                                   comanda=símismo.destroy)

        símismo.place(**Fm.ubic_CjAvisoReinic)


class CajaAvisoBorrar(tk.Frame):
    def __init__(símismo, nombre, acción):
        super().__init__(**Fm.formato_CajaAvisoReinic)
        símismo.acción = acción
        símismo.nombre = nombre

        etiq = tk.Label(símismo, text="¿Realmente quieres borrar la lengua %s?" % nombre, **Fm.formato_EtiqLengBorrar)
        etiq.pack(**Fm.ubic_etiq_aviso_borrar_leng)

        cj_bts = tk.Frame(símismo, **Fm.formato_cajas)
        símismo.bt_no = Bt.BotónTexto(cj_bts, texto='No',
                                      formato_norm=Fm.formato_BtGuardar_norm,
                                      formato_sel=Fm.formato_BtGuardar_sel,
                                      ubicación=Fm.ubic_bts_aviso_borrar_leng, tipo_ubic='pack',
                                      comanda=símismo.destroy)

        símismo.bt_sí = Bt.BotónTexto(cj_bts, texto='Sí',
                                      formato_norm=Fm.formato_BtBorrar_norm,
                                      formato_sel=Fm.formato_BtBorrar_sel,
                                      ubicación=Fm.ubic_bts_aviso_borrar_leng, tipo_ubic='pack',
                                      comanda=símismo.acción_borrar)

        cj_bts.pack(**Fm.ubic_cj_bts_aviso_borrar_leng)

        símismo.place(**Fm.ubic_CjAvisoReinic)

    def acción_borrar(símismo):
        símismo.acción(símismo.nombre)
        símismo.destroy()


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
