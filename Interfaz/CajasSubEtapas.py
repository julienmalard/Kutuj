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
        símismo.Modelo = apli.modelo

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
        símismo.MnColFecha = CtrG.Menú(cj_mn_col_fecha, nombre='Columna Fecha:', opciones=[],
                                       comanda=símismo.acción_mn_col_fecha,
                                       ubicación=Fm.ubic_MnCol, tipo_ubic='pack')
        cj_mn_col_fecha.pack(**Fm.ubic_CjMnCol)

        cj_mn_col_hora = tk.Frame(símismo.CjAct, **Fm.formato_cajas)
        símismo.MnColHora = CtrG.Menú(cj_mn_col_hora, nombre='Columna Hora:', opciones=[],
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
            cols_bd = símismo.Modelo.base_central.nombres_cols
            símismo.EtiqErrCargarBD.pack_forget()
        except (ValueError, FileNotFoundError):
            símismo.EtiqErrCargarBD.pack(**Fm.ubic_EtiqErrCargarBD)
            return

        símismo.CjAct.desbloquear()
        símismo.MnColFecha.refrescar(cols_bd)
        símismo.MnColHora.refrescar(cols_bd)

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

        if len(símismo.Modelo.base_central.fechas) and len(símismo.Modelo.base_central.horas):
            símismo.pariente.desbloquear_subcajas([2])
        else:
            símismo.pariente.bloquear_subcajas([2])

    def acción_mn_col_hora(símismo, col):
        try:
            símismo.Modelo.base_central.estab_col_hora(col)
            símismo.EtiqErrColHora.pack_forget()
        except ValueError:
            print('Error de valor')
            símismo.EtiqErrColHora.pack(**Fm.ubic_EtiqErrCol)

        if len(símismo.Modelo.base_central.fechas) and len(símismo.Modelo.base_central.horas):
            símismo.pariente.desbloquear_subcajas([2])
        else:
            símismo.pariente.bloquear_subcajas([2])


class CajaSubEtp12(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Especificar variables', núm=2, total=total)
        símismo.apli = apli

        cj_bajo = tk.Frame(símismo, **Fm.formato_cajas)

        cj_ctrls = tk.Frame(cj_bajo, **Fm.formato_cajas)
        ingr_nombre = CtrG.IngrTexto(cj_ctrls, 'Nombre', ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        símismo.MnCol = CtrG.Menú(cj_ctrls, 'Columna', opciones={},
                                  ubicación=Fm.ubic_CtrlsVarBD, tipo_ubic='pack')

        escl_fecha_inic = CtrG.Escala(cj_bajo, texto='Día inicio año', límites=(0, 365),
                                      ubicación=Fm.ubic_escl_fecha_inic, tipo_ubic='place')

        dic_controles = {'Nombre': ingr_nombre, 'Columna': símismo.MnCol, 'Fecha_inic': escl_fecha_inic}
        grupo_controles = CtrG.GrupoControles(controles=dic_controles)

        símismo.gráfico = Ctrl.GráfVarBD(cj_bajo, datos=grupo_controles.itema.datos,
                                         ubicación=Fm.ubic_GráficoVarsBD, tipo_ubic='place')

        símismo.lista = Ctrl.ListaVarsBD(símismo, controles=grupo_controles,
                                         ubicación=Fm.ubic_CjLstVarsBD, tipo_ubic='place')

        cj_bajo.place(**Fm.ubic_CjBajoSE12)
        cj_ctrls.place(**Fm.ubic_CjCtrlsVarsBD)

    def acción_desbloquear(símismo):
        bd = símismo.apli.modelo.base_central
        cols_potenciales = bd.nombres_cols.copy()
        cols_potenciales.remove(bd.id_cols['fecha'])
        cols_potenciales.remove(bd.id_cols['tiempo'])
        símismo.MnCol.refrescar(cols_potenciales)


class CajaSubEtp21(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Qué quieres predecir?', núm=1, total=total)


class CajaSubEtp22(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Con qué lo vas a predecir?', núm=2, total=total)


class CajaSubEtp31(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Sería útil calibrar...', núm=1, total=total)


class CajaSubEtp32(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¡...y aún mejor validar!', núm=2, total=total)


class CajaSubEtp41(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre=None, núm=1, total=total)


class CajaSubEtp51(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre=None, núm=1, total=total)
