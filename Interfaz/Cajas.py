import tkinter as tk

from Interfaz import CajasGenéricas as CjG
from Interfaz import Formatos as Fm, Botones as Bt, Arte as Art, Animaciones as Anim
from Interfaz import CajasSubEtapas as CjSE


class CajaInic(tk.Frame):
    def __init__(símismo):
        super().__init__(**Fm.formato_CjInic)
        símismo.logo = Art.imagen('LogoInic')
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
                                             img_norm=Art.imagen('BtRegrCent_norm'),
                                             img_sel=Art.imagen('BtRegrCent_sel'),
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

        símismo.bloquear_cajas(list(range(2, len(símismo.CajasEtapas) + 1)))

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
            símismo.CajasEtapas[n-1].desbloquear()
            if n > 1:
                símismo.CajasEtapas[n - 2].desbloquear_transición(dirección='siguiente')
            if n < len(símismo.CajasEtapas):
                símismo.CajasEtapas[n].desbloquear_transición(dirección='anterior')
            símismo.CjIzq.bts[n - 1].desbloquear()


class CajaCabeza(tk.Frame):
    def __init__(símismo, pariente, apli):
        super().__init__(pariente, **Fm.formato_CjCabeza)
        símismo.apli = apli
        símismo.logo_cabeza = Art.imagen('LogoCent')
        logo_cabeza = tk.Label(símismo, image=símismo.logo_cabeza, **Fm.formato_LogoCabz)
        logo_cabeza.place(**Fm.ubic_LogoCabz)

        símismo.bt_leng = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_leng,
                                         img_norm=Art.imagen('BtLeng_norm'),
                                         img_sel=Art.imagen('BtLeng_sel'),
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
        subcajas = [CjSE.CajaSubEtp11(símismo, apli, total=total_subcajas),
                    CjSE.CajaSubEtp12(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)
        símismo.bloquear_subcajas([2])


class CajaEtp2(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Variables', núm=2, total=total)
        total_subcajas = 2
        subcajas = [CjSE.CajaSubEtp21(símismo, apli, total=total_subcajas),
                    CjSE.CajaSubEtp22(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)
        símismo.bloquear_subcajas([1, 2])

    def desbloquear(símismo,):
        símismo.desbloquear_subcajas([1])


class CajaEtp3(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Verificar', núm=3, total=total)
        
        total_subcajas = 2
        subcajas = [CjSE.CajaSubEtp31(símismo, apli, total=total_subcajas),
                    CjSE.CajaSubEtp32(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)


class CajaEtp4(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Predecir', núm=4, total=total)
        total_subcajas = 1
        subcajas = [CjSE.CajaSubEtp41(símismo, apli, total=total_subcajas)]
        símismo.especificar_subcajas(subcajas)


class CajaEtp5(CjG.CajaEtapa):
    def __init__(símismo, pariente, apli, total):
        super().__init__(pariente, nombre='Optimizar', núm=5, total=total)
        total_subcajas = 1
        subcajas = [CjSE.CajaSubEtp51(símismo, apli, total=total_subcajas)]

        símismo.especificar_subcajas(subcajas)
