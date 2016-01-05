import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import Botones as Bt
from Interfaz import Gráficos as Gr
from Interfaz import Animaciones as Anim
from Interfaz import CajasGenéricas as CjG


class CajaInic(object):
    def __init__(símismo, pariente):
        símismo.cj = tk.Frame(pariente, **Fm.formato_CjInic)
        símismo.logo = Gr.imagen('LogoInic')
        logo = tk.Label(símismo.cj, image=símismo.logo, **Fm.formato_LogoInic)
        logo.pack(Fm.ubic_LogoInic)

        bt_empezar = Bt.BotónTexto(símismo, comanda=símismo.acción_bt_empezar, texto='Empezar',
                                   formato_norm=Fm.formato_BtsInic_norm,
                                   formato_bloq=Fm.formato_BtsInic_bloq,
                                   formato_sel=Fm.formato_BtsInic_sel,
                                   ubicación=Fm.ubic_BtsInic, tipo_ubic='pack')
        bt_empezar.bt.pack()
        símismo.cj.place(**Fm.ubic_CjInic)

    def acción_bt_empezar(símismo):
        Anim.quitar(símismo.cj, 'arriba')
        símismo.cj.destroy()


class CajaLeng(object):
    def __init__(símismo, pariente):
        símismo.cj = tk.Frame(pariente, **Fm.formato_CjLeng)
        símismo.apli = pariente
        símismo.BtRegreso = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_regreso,
                                           img_norm=Gr.imagen('BtRegrCent_norm'),
                                           img_sel=Gr.imagen('BtRegrCent_sel'),
                                           formato=Fm.formato_BtRegrCent,
                                           ubicación=Fm.ubic_Bt_Regr_Cent, tipo_ubic='place')
        símismo.cj.place(**Fm.ubic_CjLeng)

    def acción_bt_regreso(símismo):
        Anim.quitar(símismo.cj, 'derecha')


class CajaCentral(object):
    def __init__(símismo, pariente):
        símismo.cj = tk.Frame(pariente, **Fm.formato_CjCent)

        símismo.CjCabeza = CajaCabeza(símismo, apli=pariente)

        símismo.ContCjEtapas = CjG.ContCajaEtps(símismo, núm_cajas=5)
        símismo.CajasEtapas = símismo.ContCjEtapas.Cajas
        símismo.CjIzq = CajaIzq(símismo, cajas_etapas=símismo.CajasEtapas)

        símismo.cj.place(**Fm.ubic_CjCent)


class CajaCabeza(object):
    def __init__(símismo, pariente, apli):
        símismo.apli = apli
        símismo.cj = tk.Frame(pariente.cj)
        símismo.logo_cabeza = tk.Label(símismo.cj, **Fm.formato_LogoCabz)
        símismo.logo_cabeza.place(**Fm.ubic_LogoCabz)
        símismo.bt_leng = Bt.BotónImagen(símismo, comanda=símismo.acción_bt_leng,
                                         img_norm=Gr.imagen('BtLeng_norm'),
                                         img_sel=Gr.imagen('BtLeng_sel'),
                                         formato=Fm.formato_BtLeng,
                                         ubicación=Fm.ubic_BtLeng, tipo_ubic='place')

    def acción_bt_leng(símismo):
        Anim.sobreponer(símismo.apli.CajaCentral.cj, símismo.apli.CajaLenguas.cj, 'izquierda')


class CajaIzq(object):
    def __init__(símismo, pariente, cajas_etapas):
        símismo.cj = tk.Frame(pariente.cj)

        símismo.bts = []
        for cj in cajas_etapas:
            símismo.bts.append(Bt.BotónNavIzq(símismo, caja=cj))

        símismo.cj.place(**Fm.ubic_CjIzq)


class Caja1_1(CjG.CajaSubEtapa):
    def __init__(símismo, pariente):
        super().__init__(pariente, núm=1, total=3)


