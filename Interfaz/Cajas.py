import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import Animaciones as Anim


class CajaInic(object):
    def __init__(símismo, pariente):
        cj = tk.Frame(pariente, **Fm.formato_CjInic)
        cj.place(**Fm.ubic_CjInic)


class CajaLeng(object):
    def __init__(símismo, pariente):
        cj = tk.Frame(pariente, **Fm.formato_CjLeng)
        cj.place(**Fm.ubic_CjLeng)


class CajaCabeza(object):
    pass


class ContCajaEtps(object):
    def __init__(símismo, pariente):
        símismo.cj = tk.Frame(pariente)
        símismo.Cajas = []
        símismo.CajaActual = None

    def añadir_caja(símismo, nueva_caja):
        símismo.Cajas.append(nueva_caja)

    def ir_a(símismo, núm_cj_nueva):
        if símismo.CajaActual is None:
            símismo.Cajas[núm_cj_nueva - 1].lift()
            símismo.CajaActual = símismo.Cajas[núm_cj_nueva - 1]
        else:
            if núm_cj_nueva < símismo.CajaActual.núm:
                dirección = 'abajo'
            elif núm_cj_nueva > símismo.CajaActual.núm:
                dirección = 'arriba'
            else:
                return
            Anim.intercambiar(símismo.CajaActual, símismo.Cajas[núm_cj_nueva-1], dirección=dirección)
            símismo.CajaActual = símismo.CajaActual[núm_cj_nueva-1]


class CajaEtapa(object):
    def __init__(símismo, pariente, núm, núm_sub_cajas=1):
        símismo.núm = núm
        símismo.pariente = pariente
        símismo.cj = tk.Frame(pariente)
        símismo.cj.place(Fm.ubic_CjEtp)
        símismo.SubCajas = []
        símismo.SubCajaActual = None
        for i in range(núm_sub_cajas):
            símismo.SubCajas.append(CajaSubEtapa(símismo, i+1))
        símismo.ir_a_sub(1)

    def ir_a_sub(símismo, núm_sub_nueva):
        if símismo.SubCajaActual is None:
            símismo.SubCajaActual = símismo.SubCajas[núm_sub_nueva-1]
            símismo.SubCajaActual.lift()
        else:
            if núm_sub_nueva < símismo.SubCajaActual.núm:
                dirección = 'derecha'
            elif núm_sub_nueva > símismo.SubCajaActual.núm:
                dirección = 'izquierda'
            else:
                return
            Anim.intercambiar(símismo.SubCajaActual, símismo.SubCajas[núm_sub_nueva-1], dirección=dirección)
            símismo.SubCajaActual = símismo.SubCajas[núm_sub_nueva-1]

    def traer_me(símismo):
        símismo.pariente.ir_a(símismo.núm)

    def ir_etp_siguiente(símismo):
        símismo.pariente.ir_a(símismo.núm + 1)

    def ir_etp_anterior(símismo):
        símismo.pariente.ir_a(símismo.núm - 1)


class CajaSubEtapa(object):
    def __init__(símismo, pariente, núm):
        símismo.pariente = pariente
        símismo.núm = núm

    def ir_sub_siguiente(símismo):
        símismo.pariente.ir_a_sub(símismo.núm + 1)

    def ir_sub_anterior(símismo):
        símismo.pariente.ir_a_sub(símismo.núm - 1)

    def ir_etp_siguiente(símismo):
        símismo.pariente.ir_etp_siguiente()

    def ir_etp_anterior(símismo):
        símismo.pariente.ir_etp_anterior()
