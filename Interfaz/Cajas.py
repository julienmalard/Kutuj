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
        símismo.BtRegreso = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_regreso,
                                           img_norm=Gr.imagen('BtRegrCent_norm'),
                                           img_sel=Gr.imagen('BtRegrCent_sel'),
                                           formato=Fm.formato_botones,
                                           ubicación=Fm.ubic_BtRegrCent, tipo_ubic='place')
        símismo.place(**Fm.ubic_CjLeng)

    def acción_bt_regreso(símismo):
        Anim.quitar(símismo, 'derecha')


class CajaCentral(tk.Frame):
    def __init__(símismo, pariente):
        super().__init__(**Fm.formato_CjCent)
        símismo.CjCabeza = CajaCabeza(símismo, apli=pariente)

        símismo.ContCjEtapas = CjG.ContCajaEtps(símismo)
        núm_etapas=5
        símismo.CajasEtapas = [CajaEtp1(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp2(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp3(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp4(símismo.ContCjEtapas, núm_etapas),
                               CajaEtp5(símismo.ContCjEtapas, núm_etapas)
                               ]

        símismo.CjIzq = CajaIzq(símismo, cajas_etapas=símismo.CajasEtapas)

        símismo.place(**Fm.ubic_CjCent)


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


class CajaEtp2(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Base de Datos', núm=2, total=total)


class CajaEtp3(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Base de Datos', núm=3, total=total)


class CajaEtp4(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Base de Datos', núm=4, total=total)


class CajaEtp5(CjG.CajaEtapa):
    def __init__(símismo, pariente, total):
        super().__init__(pariente, nombre='Base de Datos', núm=5, total=total)
