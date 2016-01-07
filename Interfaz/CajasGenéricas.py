import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import Botones as Bt
from Interfaz import Controles as Ctrl
from Interfaz import Gráficos as Gr
from Interfaz import Animaciones as Anim


class ContCajaEtps(tk.Frame):
    def __init__(símismo, pariente):
        super().__init__(pariente, **Fm.formato_CjContCjEtps)
        símismo.Cajas = []
        símismo.CajaActual = None
        símismo.pack(**Fm.ubic_CjContCjEtps)

    def establecer_cajas(símismo, cajas_etapas):
        for n, cj in enumerate(cajas_etapas):
            símismo.Cajas.append(cj)
        símismo.CajaActual = símismo.Cajas[0]
        símismo.Cajas[0].lift()

    def ir_a(símismo, núm_cj_nueva):
        if núm_cj_nueva < símismo.CajaActual.núm:
            dirección = 'abajo'
        elif núm_cj_nueva > símismo.CajaActual.núm:
            dirección = 'arriba'
        else:
            return
        Anim.intercambiar(símismo.CajaActual, símismo.Cajas[núm_cj_nueva-1], dirección=dirección)
        símismo.CajaActual = símismo.CajaActual[núm_cj_nueva-1]


class CajaEtapa(tk.Frame):
    def __init__(símismo, pariente, nombre, núm, total):
        super().__init__(pariente, **Fm.formato_cajas)
        símismo.núm = núm
        símismo.pariente = pariente
        símismo.SubCajas = []
        símismo.SubCajaActual = None

        etiq = tk.Label(text=nombre, **Fm.formato_EncbzCjEtp)
        etiq.place(**Fm.ubic_EmcbzCjEtp)

        if núm > 1:
            símismo.BtAtrás = Bt.BotónNavEtapa(símismo, tipo='atrás')
        if núm < total:
            símismo.BtAdelante = Bt.BotónNavEtapa(símismo, tipo='adelante')

        símismo.place(**Fm.ubic_CjEtp)

    def especificar_subcajas(símismo, subcajas):
        símismo.SubCajas = subcajas
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
    def __init__(símismo, pariente, núm, total):
        símismo.pariente = pariente
        símismo.núm = núm

        símismo.cj = tk.Frame(pariente, **Fm.formato_CjSubEtp)

        if núm < total:
            símismo.BtAdelante = Bt.BotónNavSub(símismo, tipo='adelante')
        if núm > 1:
            símismo.BtAtrás = Bt.BotónNavSub(símismo, tipo='atrás')

        símismo.cj.place(Fm.ubic_CjSubEtp)

    def ir_sub_siguiente(símismo):
        símismo.pariente.ir_a_sub(símismo.núm + 1)

    def ir_sub_anterior(símismo):
        símismo.pariente.ir_a_sub(símismo.núm - 1)

    def ir_etp_siguiente(símismo):
        símismo.pariente.ir_etp_siguiente()

    def ir_etp_anterior(símismo):
        símismo.pariente.ir_etp_anterior()


class CajaActivable(object):
    def __init__(símismo, pariente, objetos, ubicación, tipo_ubic):
        símismo.cj = tk.Frame(pariente)

        if tipo_ubic == 'pack':
            símismo.cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.cj.place(**ubicación)

        símismo.etiquetas = [x for x in objetos if type(x) is tk.Label]
        símismo.botones = [x for x in objetos if
                           type(x) is Bt.BotónImagen or
                           type(x) is Bt.BotónTexto or
                           type(x) is Ctrl.Menú]

    def bloquear(símismo):
        for etiq in símismo.etiquetas:
            etiq.configure(Fm.formato_etiq_bloq)
        for bt in símismo.botones:
            bt.bloquear()

    def desbloquear(símismo):
        for etiq in símismo.etiquetas:
            etiq.configure(Fm.formato_etiq_norm)
        for bt in símismo.botones:
            bt.desbloquear()


class CajaAvanzada(object):
    def __init__(símismo, pariente):
        símismo.cj = tk.Frame(pariente)
        símismo.caja_móbil = None
        símismo.flechita_avnz = Gr.imagen('FlchAvnz')
        símismo.flechita_senc = Gr.imagen('FlchSenc')
        símismo.bt = tk.Button(símismo.cj, text='Avanzado', image=símismo.flechita_avnz,
                               command=símismo.bajar,
                               compound='right')
        símismo.bt.place()

    def establecer_caja_móbil(símismo, caja_móbil):
        símismo.caja_móbil = caja_móbil
        símismo.caja_móbil.cj.place(**Fm.ubic_CjMóbl)

    def bajar(símismo):
        símismo.bt.configure(texto='Sencillo', image=símismo.flechita_senc, command=símismo.subir)
        Anim.deslizar(objetos=[símismo.caja_móbil, símismo.bt],
                      pos_inic=[símismo.caja_móbil.winfo_y(), símismo.bt.winfo_y()],
                      dirección='abajo',
                      distancia=símismo.caja_móbil.winfo_height())

    def subir(símismo):
        símismo.bt.configure(texto='Avanzado', image=símismo.flechita_avnz, command=símismo.bajar)
        Anim.deslizar(objetos=[símismo.caja_móbil, símismo.bt],
                      pos_inic=[símismo.caja_móbil.winfo_y(), símismo.bt.winfo_y()],
                      dirección='arriba',
                      distancia=símismo.caja_móbil.winfo_height())
