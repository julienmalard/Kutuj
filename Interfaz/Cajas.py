import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import Botones as Bt
from Interfaz import Gráficos as Gr
from Interfaz import Animaciones as Anim
from Interfaz import CajasGenéricas as CjG


class CajaInic(tk.Frame):
    def __init__(símismo, pariente):
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
        bt_regreso = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_regreso,
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
    def __init__(símismo, pariente):
        super().__init__(**Fm.formato_CjCent)
        símismo.CjCabeza = CajaCabeza(símismo, apli=pariente)

        símismo.ContCjEtapas = CjG.ContCajaEtps(símismo)
        núm_etapas = 5
        símismo.CajasEtapas = [CajaEtp1(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp2(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp3(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp4(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp5(símismo.ContCjEtapas, núm_etapas)
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
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Base de Datos', núm=1, total=total)

        total_subcajas = 2
        subcajas = [CajaSubEtp11(símismo, total=total_subcajas),
                    CajaSubEtp12(símismo, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaEtp2(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Variables', núm=2, total=total)
        total_subcajas = 1
        subcajas = [CajaSubEtp21(símismo, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaEtp3(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Validar', núm=3, total=total)
        
        total_subcajas = 2
        subcajas = [CajaSubEtp31(símismo, total=total_subcajas),
                    CajaSubEtp32(símismo, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaEtp4(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Predecir', núm=4, total=total)
        total_subcajas = 1
        subcajas = [CajaSubEtp41(símismo, total=total_subcajas)]
        símismo.especificar_subcajas(subcajas)


class CajaEtp5(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Optimizar', núm=5, total=total)
        total_subcajas = 1
        subcajas = [CajaSubEtp51(símismo, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaSubEtp11(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Cargar datos', núm=1, total=total)
        bt_cargar_bd = Bts.BotónTexto(símismo, texto='Cargar Base de Datos, comanda=símismo.acción_bt_cargar_bd,
                                      ubicación=Fm.ubic_bt_cargar_bd, tipo_ubic='place')
        símismo.CjErrCargarBD = Cjs.CajaError(símismo, texto='Error en cargar la base de datos',
                                              ubicación=Fm.ubic_CjErrCargarBD, tipo_ubic='place')
        símismo.caja_activable = Cjs.CajaActivable()
        símismo.MnColTiempo = Ctrl.MenúOpciones(caja_activable, 
        símismo.MnColHora = Ctrl.MenúOpciones(caja_activable, 
        símismo.CjErrColTiempo = Cjs.CajaError(símismo, texto='Error en leer los datos de fechas. Verificar su base de datos.',
                                              ubicación=Fm.ubic_CjErrCargarBD, tipo_ubic='place')
        símismo.CjErrColHora = Cjs.CajaError(símismo, texto='Error en leer los datos de horas. Verificar su base de datos.',
                                              ubicación=Fm.ubic_CjErrCargarBD, tipo_ubic='place')
        
        símismo.MnColTiempo.estab_exclusivo(símismo.MnColHora)
        símismo.caja_activable.bloquear()
        
    def acción_bt_cargar_bd(símismo):
        try:
            cols_bd = 
            símismo.etiq_error_cargar_bd.hide()
        except ERROR:
            símismo.etiq_error_cargar_bd.show()
        símismo.caja_activable.desbloquear()
        símismo.MnColTiempo.refrescar(cols_bd)
        símismo.MnColHora.refrescar(cols_bd)
        
    def estab_col_tiempo(símismo):
        try:
            
            símismo.etiq_error_col_tiempo.hide()
        except ERROR:
            símismo.etiq_error_col_tiempo.show()
        if modelo tiene col_tiempo:
            símismo.pariente.desbloquear_caja([2])
        else:
            símismo.pariente.bloquear_caja([2])
            
    def estab_col_hora(símismo):
        try:
            
            símismo.etiq_error_col_hora.hide()
        except ERROR:
            símismo.etiq_error_col_hora.show()


class CajaSubEtp12(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Especificar variables', núm=2, total=total)


class CajaSubEtp21(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Variables predictores', núm=2, total=total)
        

class CajaSubEtp22(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Variable a predecir', núm=2, total=total)
        
                
class CajaSubEtp31(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Calibrar', núm=2, total=total)
        
        
class CajaSubEtp32(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Validar', núm=2, total=total)
        
        
class CajaSubEtp41(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre=None, núm=2, total=total)
        
        
class CajaSubEtp51(CjG.CajaSubEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre=None, núm=2, total=total)
