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
        símismo.lista = Ctrl.ListaVarsBD(símismo, ubicación=Fm.ubic_CjLstVarsBD, tipo_ubic='place')

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
        return False


class CajaSubEtp21(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Qué quieres predecir?', núm=1, total=total)
        símismo.apli = apli


class CajaSubEtp22(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Con qué lo vas a predecir?', núm=2, total=total)
        símismo.apli = apli


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
