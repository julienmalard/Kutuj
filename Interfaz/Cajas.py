import tkinter as tk
from tkinter import filedialog as diálogo

from Interfaz import CajasGenéricas as CjG
from Interfaz import Formatos as Fm, Botones as Bt, Gráficos as Gr, Animaciones as Anim, Controles as Ctrl

from Modelo import Modelo


class CajaInic(tk.Frame):
    def __init__(símismo):
        super().__init__(**Fm.formato_CjInic)
        símismo.logo = Gr.imagen('LogoInic')
        logo = tk.Label(símismo, image=símismo.logo, **Fm.formato_LogoInic)
        logo.pack(Fm.ubic_LogoInic)

        cj_bts_inic = tk.Frame(símismo, **Fm.formato_cajas)
        bt_empezar = Bt.BotónTexto(cj_bts_inic, comanda=símismo.acción_bt_empezar, texto='Empezar',
                                   formato_norm=Fm.formato_BtsInic_norm,
                                   formato_sel=Fm.formato_BtsInic_sel,
                                   ubicación=Fm.ubic_BtsInic, tipo_ubic='pack')
        bt_empezar.bt.pack(**Fm.ubic_BtsInic)
        cj_bts_inic.pack()

        símismo.place(**Fm.ubic_CjInic)

    def acción_bt_empezar(símismo):
        Anim.quitar(símismo, 'arriba')
        símismo.destroy()


class CajaLeng(tk.Frame):
    def __init__(símismo, pariente):
        super().__init__(**Fm.formato_cajas)
        símismo.apli = pariente
        símismo. bt_regreso = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_regreso,
                                             img_norm=Gr.imagen('BtRegrCent_norm'),
                                             img_sel=Gr.imagen('BtRegrCent_sel'),
                                             formato=Fm.formato_botones,
                                             ubicación=Fm.ubic_BtRegrCent, tipo_ubic='place')
        etiq = tk.Label(símismo, text='Opciones de lenguas', **Fm.formato_CbzLeng)
        etiq.place(**Fm.ubic_CbzLeng)
        símismo.place(**Fm.ubic_CjLeng)

    def acción_bt_regreso(símismo):
        Anim.quitar(símismo, 'derecha')


class CajaCentral(tk.Frame):
    def __init__(símismo, apli):
        super().__init__(**Fm.formato_CjCent)
        símismo.CjCabeza = CajaCabeza(símismo, apli=apli)

        símismo.ContCjEtapas = CjG.ContCajaEtps(símismo)
        núm_etapas = 5
        símismo.CajasEtapas = [CajaEtp1(símismo.ContCjEtapas, apli, núm_etapas),
                               CajaEtp2(símismo.ContCjEtapas, apli, núm_etapas),
                               CajaEtp3(símismo.ContCjEtapas, apli, núm_etapas),
                               CajaEtp4(símismo.ContCjEtapas, apli, núm_etapas),
                               CajaEtp5(símismo.ContCjEtapas, apli, núm_etapas)
                               ]
        símismo.ContCjEtapas.establecer_cajas(símismo.CajasEtapas)

        símismo.CjIzq = CajaIzq(símismo, cajas_etapas=símismo.CajasEtapas)

        # símismo.bloquear_cajas(list(range(2, len(símismo.CajasEtapas) + 1)))

        símismo.place(**Fm.ubic_CjCent)

    def bloquear_cajas(símismo, núms_cajas):
        for n in núms_cajas:
            if n > 1:
                símismo.CajasEtapas[n - 2].bloquear_transición(dirección='siguiente')
            if n < len(símismo.CajasEtapas):
                símismo.CajasEtapas[n].bloquear_transición(dirección='anterior')
            símismo.CjIzq.bts[n - 1].bloquear()

    def desbloquear_cajas(símismo, núms_cajas):
        for n in núms_cajas:
            símismo.CajasEtapas[n - 1].desbloquear_transición(dirección='siguiente')
            símismo.CajasEtapas[n + 1].desbloquear_transición(dirección='anterior')
            símismo.CjIzq.bts[n - 1].desbloquear()


class CajaCabeza(tk.Frame):
    def __init__(símismo, pariente, apli):
        super().__init__(pariente, **Fm.formato_CjCabeza)
        símismo.apli = apli
        símismo.logo_cabeza = Gr.imagen('LogoCent')
        logo_cabeza = tk.Label(símismo, image=símismo.logo_cabeza, **Fm.formato_LogoCabz)
        logo_cabeza.place(**Fm.ubic_LogoCabz)

        símismo.bt_leng = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_leng,
                                         img_norm=Gr.imagen('BtLeng_norm'),
                                         img_sel=Gr.imagen('BtLeng_sel'),
                                         formato=Fm.formato_botones,
                                         ubicación=Fm.ubic_BtLeng, tipo_ubic='place')
        símismo.pack(**Fm.ubic_CjCabeza)

    def acción_bt_leng(símismo):
        Anim.sobreponer(símismo.apli.CajaCentral, símismo.apli.CajaLenguas, 'izquierda')


class CajaIzq(tk.Frame):
    def __init__(símismo, pariente, cajas_etapas):
        super().__init__(pariente, **Fm.formato_cajas)
        cj_bts = tk.Frame(símismo, **Fm.formato_cajas)
        lín = tk.Frame(símismo, **Fm.formato_LínIzq)

        símismo.bts = []
        for cj in cajas_etapas:
            símismo.bts.append(Bt.BotónNavIzq(cj_bts, caja=cj))

        cj_bts.pack(**Fm.ubic_CjBtsIzq)
        lín.pack(**Fm.ubic_LínIzq)
        símismo.pack(**Fm.ubic_CjIzq)


class CajaEtp1(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Base de Datos', núm=1, total=total)

        total_subcajas = 2
        subcajas = [CajaSubEtp11(símismo, apli, total=total_subcajas),
                    CajaSubEtp12(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)
        símismo.bloquear_subcajas([2])


class CajaEtp2(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Variables', núm=2, total=total)
        total_subcajas = 2
        subcajas = [CajaSubEtp21(símismo, apli, total=total_subcajas),
                    CajaSubEtp22(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaEtp3(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Validar', núm=3, total=total)
        
        total_subcajas = 2
        subcajas = [CajaSubEtp31(símismo, apli, total=total_subcajas),
                    CajaSubEtp32(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaEtp4(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Predecir', núm=4, total=total)
        total_subcajas = 1
        subcajas = [CajaSubEtp41(símismo, apli, total=total_subcajas)]
        símismo.especificar_subcajas(subcajas)


class CajaEtp5(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Optimizar', núm=5, total=total)
        total_subcajas = 1
        subcajas = [CajaSubEtp51(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


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
        símismo.MnColFecha = Ctrl.Menú(cj_mn_col_fecha, nombre='Columna Fecha:', opciones=[],
                                       comanda=símismo.acción_mn_col_fecha,
                                       ubicación=Fm.ubic_MnCol, tipo_ubic='pack')
        cj_mn_col_fecha.pack(**Fm.ubic_CjMnCol)

        cj_mn_col_hora = tk.Frame(símismo.CjAct, **Fm.formato_cajas)
        símismo.MnColHora = Ctrl.Menú(cj_mn_col_hora, nombre='Columna Hora:', opciones=[],
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

        if símismo.Modelo.base_central.fechas is not None:
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


class CajaSubEtp12(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Especificar variables', núm=2, total=total)



class CajaSubEtp21(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Variables predictores', núm=1, total=total)
        

class CajaSubEtp22(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='¿Qué quieres predecir?', núm=2, total=total)
        
                
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
