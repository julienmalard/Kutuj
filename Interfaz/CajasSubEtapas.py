import tkinter as tk
from tkinter import filedialog as diálogo

from Interfaz import CajasGenéricas as CjG
from Interfaz import Botones as Bt
from Interfaz import Formatos as Fm
from Interfaz import ControlesGenéricos as CtrG
from Interfaz import Controles as Ctrl

from Modelo import Modelo


class CajaSubEtp11(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Cargar datos', núm=1, total=total)
        símismo.apli = apli
        símismo.Modelo = None

        cj_bts = tk.Frame(símismo, **Fm.formato_cajas)
        símismo.bt_cargar_bd = Bt.BotónTexto(cj_bts, texto='Base de datos', comanda=símismo.acción_bt_cargar_bd,
                                             formato_norm=Fm.formato_BtsCarg_norm, formato_sel=Fm.formato_BtsCarg_sel,
                                             ubicación=Fm.ubic_BtsCarg, tipo_ubic='pack')
        símismo.bt_cargar_pr = Bt.BotónTexto(cj_bts, texto='Proyecto existente', comanda=símismo.acción_bt_cargar_pr,
                                             formato_norm=Fm.formato_BtsCarg_norm, formato_sel=Fm.formato_BtsCarg_sel,
                                             ubicación=Fm.ubic_BtsCarg, tipo_ubic='pack')
        cj_bts.place(**Fm.ubic_CjBtsCarg)

        símismo.EtiqErrCargarBD = tk.Label(símismo, text='Error cargando la base de datos', **Fm.formato_etiq_error)

        símismo.CjAct = CjG.CajaActivable(símismo, ubicación=Fm.ubic_CjFechaHora, tipo_ubic='place')

        cj_mn_col_fecha = tk.Frame(símismo.CjAct, **Fm.formato_cajas)
        símismo.MnColFecha = CtrG.Menú(cj_mn_col_fecha, nombre='Columna Fecha:', opciones='',
                                       comanda=símismo.acción_mn_col_fecha,
                                       ubicación=Fm.ubic_MnCol, tipo_ubic='pack')
        cj_mn_col_fecha.pack(**Fm.ubic_CjMnCol)

        cj_mn_col_hora = tk.Frame(símismo.CjAct, **Fm.formato_cajas)
        símismo.MnColHora = CtrG.Menú(cj_mn_col_hora, nombre='Columna Hora:', opciones='',
                                      comanda=símismo.acción_mn_col_hora,
                                      ubicación=Fm.ubic_MnCol, tipo_ubic='pack')
        cj_mn_col_hora.pack(**Fm.ubic_CjMnCol)

        símismo.CjAct.especificar_objetos([símismo.MnColHora, símismo.MnColFecha])

        símismo.EtiqErrColFecha = tk.Label(cj_mn_col_fecha,
                                           text='No su pudo leer los datos de fechas. ¿Mejor le echas un vistaso a tu '
                                                'base de datos?',
                                           **Fm.formato_etiq_error)

        símismo.EtiqErrColHora = tk.Label(cj_mn_col_hora,
                                          text='No se pudo leer los datos de tiempo. ¿Mejor le echas un vistaso a tu '
                                               'base de datos?',
                                          **Fm.formato_etiq_error)

        símismo.MnColFecha.estab_exclusivo(símismo.MnColHora)
        símismo.CjAct.bloquear()

    def acción_bt_cargar_bd(símismo):
        archivo_bd = diálogo.askopenfilename(filetypes=[('Formato comas', '*.csv'),
                                                        ('Formato texto', '*.txt')],
                                             title='Cargar base de datos')
        try:
            símismo.Modelo = Modelo(archivo_bd)
            símismo.apli.modelo = símismo.Modelo
            cols_bd = símismo.Modelo.base_central.nombres_cols
            símismo.EtiqErrCargarBD.pack_forget()
        except (ValueError, FileNotFoundError):
            símismo.EtiqErrCargarBD.pack(**Fm.ubic_EtiqErrCargarBD)
            return

        símismo.CjAct.desbloquear()
        símismo.MnColFecha.refrescar(opciones=cols_bd, texto_opciones=cols_bd)
        símismo.MnColHora.refrescar(opciones=cols_bd, texto_opciones=cols_bd)

    def acción_bt_cargar_pr(símismo):
        archivo_bd = diálogo.askopenfilename(filetypes=[('Proyecto Kutuj', '*.kut')],
                                             title='Cargar proyecto existente')
        # para hacer: hacer más cosas aquí

    def acción_mn_col_fecha(símismo, col):
        try:
            símismo.Modelo.base_central.estab_col_fecha(col)
            símismo.EtiqErrColFecha.pack_forget()
        except ValueError:
            símismo.EtiqErrColFecha.pack(**Fm.ubic_EtiqErrCol)

        if símismo.verificar_completo():
            símismo.pariente.desbloquear_subcajas([2])
        else:
            símismo.pariente.bloquear_subcajas([2])

    def acción_mn_col_hora(símismo, col):
        try:
            símismo.Modelo.base_central.estab_col_hora(col)
            símismo.EtiqErrColHora.pack_forget()
        except ValueError:
            símismo.EtiqErrColHora.pack(**Fm.ubic_EtiqErrCol)

        if símismo.verificar_completo():
            símismo.pariente.desbloquear_subcajas([2])
        else:
            símismo.pariente.bloquear_subcajas([2])

    def verificar_completo(símismo):
        if len(símismo.Modelo.base_central.fechas) and len(símismo.Modelo.base_central.tiempos):
            return True
        else:
            return False


class CajaSubEtp12(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Especificar variables', núm=2, total=total)
        símismo.apli = apli
        símismo.Modelo = None

        cj_bajo = tk.Frame(símismo, **Fm.formato_cajas)

        cj_ctrls = tk.Frame(cj_bajo, **Fm.formato_cajas)
        ingr_nombre = CtrG.IngrTexto(cj_ctrls, 'Nombre:', ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        símismo.MnCol = CtrG.Menú(cj_ctrls, 'Columna:', opciones='',
                                  ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        escl_fecha_inic = CtrG.Escala(cj_bajo, texto='Día inicio año', límites=(1, 365), valor_inicial=1, prec='ent',
                                      ubicación=Fm.ubic_escl_fecha_inic, tipo_ubic='place')

        menú_transform = CtrG.Menú(cj_ctrls, nombre='Transformación:',
                                   opciones=['sumar', 'máx', 'mín', 'prom'],
                                   texto_opciones=['Sumar', 'Máximo', 'Mínimo', 'Promedio'],
                                   ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        menú_interpol = CtrG.Menú(cj_ctrls, nombre='Interpolación:',
                                  opciones=['trap', 'ninguno'],
                                  texto_opciones=['Trapezoidal', 'Ninguno'],
                                  inicial='trap',
                                  ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        cj_bts = tk.Frame(cj_ctrls, **Fm.formato_cajas)

        bt_guardar = Bt.BotónTexto(cj_bts, texto='Guardar',
                                   ubicación=Fm.ubic_BtsGrupoCtrl, tipo_ubic='pack',
                                   formato_norm=Fm.formato_BtGuardarGrupoCtrl_norm,
                                   formato_sel=Fm.formato_BtGuardarGrupoCtrl_sel,
                                   formato_bloq=Fm.formato_BtGuardarsGrupoCtrl_bloq,
                                   )
        bt_borrar = Bt.BotónTexto(cj_bts, texto='Borrar',
                                  ubicación=Fm.ubic_BtsGrupoCtrl, tipo_ubic='pack',
                                  formato_norm=Fm.formato_BtBorrarGrupoCtrl_norm,
                                  formato_sel=Fm.formato_BtBorrarGrupoCtrl_sel,
                                  formato_bloq=Fm.formato_BtBorrarsGrupoCtrl_bloq,
                                  )
        cj_bts.pack(**Fm.ubic_CjBtsGrupoCtrl)

        dic_controles = {'Nombre': ingr_nombre, 'Columna': símismo.MnCol, 'Fecha_inic': escl_fecha_inic,
                         'Transformación': menú_transform, 'Interpol': menú_interpol}

        símismo.gráfico = Ctrl.GráfVarBD(cj_bajo, ubicación=Fm.ubic_GráficoVarsBD, tipo_ubic='place')
        símismo.lista = Ctrl.ListaVarsBD(símismo, lista=apli.modelo.base_central.vars,
                                         ubicación=Fm.ubic_CjLstVarsBD, tipo_ubic='place')

        símismo.grupo_controles = Ctrl.GrpCtrlsVarBD(apli=apli, controles=dic_controles, gráfico=símismo.gráfico,
                                                     lista=símismo.lista, bt_guardar=bt_guardar,
                                                     bt_borrar=bt_borrar)
        cj_ctrls.place(**Fm.ubic_CjCtrlsVarsBD)
        cj_bajo.place(**Fm.ubic_CjBajoSE12)

    def acción_desbloquear(símismo):
        símismo.Modelo = símismo.apli.modelo
        bd = símismo.Modelo.base_central
        cols_potenciales = bd.nombres_cols.copy()
        cols_potenciales.remove(bd.id_cols['fecha'])
        cols_potenciales.remove(bd.id_cols['tiempo'])
        símismo.MnCol.refrescar(opciones=cols_potenciales, texto_opciones=cols_potenciales)

        if símismo.verificar_completo():
            símismo.pariente.desbloquear_subcajas([2])

    def verificar_completo(símismo):
        if len(símismo.lista.objetos) > 0:
            símismo.pariente.desbloquear_cajas([2])
            return True
        else:
            símismo.pariente.bloquear_cajas([2])
            return False


class CajaSubEtp21(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Qué quieres predecir?', núm=1, total=total)
        símismo.apli = apli


class CajaSubEtp22(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Con qué lo vas a predecir?', núm=2, total=total)
        símismo.apli = apli
        símismo.Modelo = None

        cj_bajo = tk.Frame(símismo, **Fm.formato_cajas)

        cj_ctrls = tk.Frame(cj_bajo, **Fm.formato_cajas)
        ingr_nombre = CtrG.IngrTexto(cj_ctrls, 'Nombre:', ubicación=Fm.ubic_CtrlsVarX, tipo_ubic='pack')

        símismo.MnVarBD = CtrG.Menú(cj_ctrls, nombre='A base de:', opciones='',
                                    ubicación=Fm.ubic_CtrlsVarX, tipo_ubic='pack')

        menú_calc = CtrG.Menú(cj_ctrls, nombre='Calculado con:',
                              opciones=['val_tot', 'val_prom', 'núm_días', 'núm_días_consec'],
                              texto_opciones=['Valor total',
                                              'Valor promedio',
                                              'Número de días',
                                              'Número de días consecutivos'],
                              ubicación=Fm.ubic_CtrlsVarX, tipo_ubic='pack')

        cj_filtr_val = tk.Frame(cj_ctrls, **Fm.formato_cajas)
        menú_filtr_val = CtrG.Menú(cj_filtr_val, nombre='Con valores:',
                                   opciones=['', 'igual', 'sup', 'inf', 'entre'],
                                   texto_opciones=['Igual a', 'Superior a', 'Inferior a', 'Entre'],
                                   comanda=símismo.cambió_filtro_val,
                                   ubicación=Fm.ubic_CtrlsVarX, tipo_ubic='pack')
        cj_1_filtro = tk.Frame(cj_filtr_val, **Fm.formato_cajas)
        ingr_fltr_único = CtrG.IngrNúm(cj_1_filtro, límites=None, prec='dec',
                                  ubicación=Fm.ubic_CtrlsFltrTmp,
                                  tipo_ubic='pack')
        cj_2_filtros = tk.Frame(cj_filtr_val, **Fm.formato_cajas)
        ingr_fltr_1 = CtrG.IngrNúm(cj_2_filtros, límites=None, prec='dec',
                                ubicación=Fm.ubic_CtrlsFltrTmp,
                                tipo_ubic='pack')
        ingr_fltr_2 = CtrG.IngrNúm(cj_2_filtros, límites=None, prec='dec',
                                ubicación=Fm.ubic_CtrlsFltrTmp,
                                tipo_ubic='pack')

        símismo.ops_cj_ingr_fltr_val = {
            '': tk.Frame(cj_filtr_val, **Fm.formato_cajas),
            'igual': cj_1_filtro,
            'sup': cj_1_filtro,
            'inf': cj_1_filtro,
            'entre': cj_2_filtros
        }

        símismo.cj_ingr_fltr_val = símismo.ops_cj_ingr_fltr_val['']

        cj_fltr_tmp = tk.Frame(cj_ctrls, **Fm.formato_cajas)
        etiq_filtr_tiempo = tk.Label(cj_fltr_tmp, text='En el periodo de:', **Fm.formato_EtiqCtrl)
        cj_tmp_inic = tk.Frame(cj_fltr_tmp, **Fm.formato_cajas)
        ingr_fltr_tp_inic = CtrG.IngrNúm(cj_tmp_inic, nombre='días', límites=(-365, 365), prec='ent',
                                         ubicación=Fm.ubic_CtrlsFltrTmp, tipo_ubic='pack', orden='ingr')
        menú_fltr_tp_inic = CtrG.Menú(cj_tmp_inic, nombre=None,
                                      opciones=['hoy', 'año'],
                                      texto_opciones=['desde hoy', 'del año'],
                                      ubicación=Fm.ubic_CtrlsFltrTmp, tipo_ubic='pack')

        cj_tmp_fin = tk.Frame(cj_fltr_tmp, **Fm.formato_cajas)
        ingr_fltr_tp_fin = CtrG.IngrNúm(cj_tmp_fin, nombre='días', límites=(-365, 365), prec='ent',
                                         ubicación=Fm.ubic_CtrlsFltrTmp, tipo_ubic='pack', orden='ingr')
        menú_fltr_tp_fin = CtrG.Menú(cj_tmp_fin, nombre=None,
                                     opciones=['hoy', 'año'],
                                     texto_opciones=['desde hoy', 'del año'],
                                     ubicación=Fm.ubic_CtrlsFltrTmp, tipo_ubic='pack')

        cj_bts = tk.Frame(cj_ctrls, **Fm.formato_cajas)

        bt_guardar = Bt.BotónTexto(cj_bts, texto='Guardar',
                                   ubicación=Fm.ubic_BtsGrupoCtrl, tipo_ubic='pack',
                                   formato_norm=Fm.formato_BtGuardarGrupoCtrl_norm,
                                   formato_sel=Fm.formato_BtGuardarGrupoCtrl_sel,
                                   formato_bloq=Fm.formato_BtGuardarsGrupoCtrl_bloq,
                                   )
        bt_borrar = Bt.BotónTexto(cj_bts, texto='Borrar',
                                  ubicación=Fm.ubic_BtsGrupoCtrl, tipo_ubic='pack',
                                  formato_norm=Fm.formato_BtBorrarGrupoCtrl_norm,
                                  formato_sel=Fm.formato_BtBorrarGrupoCtrl_sel,
                                  formato_bloq=Fm.formato_BtBorrarsGrupoCtrl_bloq,
                                  )
        cj_bts.pack(**Fm.ubic_CjBtsGrupoCtrl)

        dic_controles = {'Nombre': ingr_nombre, 'VarBD': símismo.MnVarBD, 'MétodoCalc': menú_calc,
                         'FiltroVal': menú_filtr_val,
                         'FiltroValÚn': ingr_fltr_único, 'FitroValEntre1': ingr_fltr_1, 'FitroValEntre2': ingr_fltr_2,
                         'FiltroTmpInic': ingr_fltr_tp_inic, 'RefTmpInic': menú_fltr_tp_inic,
                         'FiltroTmpFin': ingr_fltr_tp_fin, 'RefTmpFin': menú_fltr_tp_fin}

        símismo.gráfico = Ctrl.GráfVarBD(cj_bajo, ubicación=Fm.ubic_GráficoVarsBD, tipo_ubic='place')
        símismo.lista = Ctrl.ListaVarsBD(símismo, lista=apli.modelo.config.varsX,
                                         ubicación=Fm.ubic_CjLstVarsBD, tipo_ubic='place')

        símismo.grupo_controles = Ctrl.GrpCtrlsVarBD(apli=apli, controles=dic_controles, gráfico=símismo.gráfico,
                                                     lista=símismo.lista, bt_guardar=bt_guardar,
                                                     bt_borrar=bt_borrar)
        cj_filtr_val.pack(**Fm.ubic_CtrlsVarX)

        etiq_filtr_tiempo.pack(**Fm.ubic_CtrlsVarX)
        cj_tmp_inic.pack(**Fm.ubic_CtrlsVarX)
        cj_tmp_fin.pack(**Fm.ubic_CtrlsVarX)
        cj_fltr_tmp.pack(**Fm.ubic_CtrlsVarX)

        cj_ctrls.place(**Fm.ubic_CjCtrlsVarsBD)
        cj_bajo.place(**Fm.ubic_CjBajoSE12)

    def acción_desbloquear(símismo):
        asfasdf
        símismo.Modelo = símismo.apli.modelo
        bd = símismo.Modelo.base_central
        cols_potenciales = bd.nombres_cols.copy()
        cols_potenciales.remove(bd.id_cols['fecha'])
        cols_potenciales.remove(bd.id_cols['tiempo'])
        símismo.MnCol.refrescar(opciones=cols_potenciales, texto_opciones=cols_potenciales)

        if símismo.verificar_completo():
            símismo.pariente.desbloquear_subcajas([2])

    def verificar_completo(símismo):
        asdfasdfsad
        if len(símismo.lista.objetos) > 0:
            símismo.pariente.desbloquear_cajas([2])
            return True
        else:
            símismo.pariente.bloquear_cajas([2])
            return False

    def cambió_filtro_val(símismo, val):
        símismo.cj_ingr_fltr_val.pack_forget()
        símismo.cj_ingr_fltr_val = símismo.ops_cj_ingr_fltr_val[val]
        símismo.cj_ingr_fltr_val.pack()


class CajaSubEtp31(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Sería útil calibrar...', núm=1, total=total)
        símismo.apli = apli


class CajaSubEtp32(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¡...y aún mejor validar!', núm=2, total=total)
        símismo.apli = apli


class CajaSubEtp41(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre=None, núm=1, total=total)
        símismo.apli = apli


class CajaSubEtp51(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre=None, núm=1, total=total)
        símismo.apli = apli
