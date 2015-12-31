import tkinter as tk

from Interfaz import Gráficos as Gr
from Interfaz import Formatos as Fm


class Botón(object):
    def __init__(símismo, pariente, comanda, formato=None, img_norm=None, img_sel=None, img_bloq=None,
                 texto=None, formato_norm=None, formato_sel=None, formato_bloq=None,
                 ubicación=None, tipo_ubic=None, tipo_combin='left'):

        símismo.formato = {}
        if tipo_combin is not None:
            símismo.formato['combine'] = tipo_combin
        if texto is not None:
            símismo.formato['text'] = texto
        if formato is not None:
            for ll, v in formato:
                símismo.formato[ll] = v

        símismo.formato_norm = {}
        símismo.formato_bloq = {}
        símismo.formato_sel = {}
        if img_norm is not None:
            símismo.formato_norm['image'] = img_norm
        if img_sel is not None:
            símismo.formato_sel['image'] = img_sel
        if img_bloq is not None:
            símismo.formato_bloq['image'] = img_bloq
        if formato_norm is not None:
            for ll, v in formato_norm: símismo.formato_norm[ll] = v
        if formato_sel is not None:
            for ll, v in formato_sel: símismo.formato_sel[ll] = v
        if formato_bloq is not None:
            for ll, v in formato_bloq: símismo.formato_bloq[ll] = v

        símismo.estado = 'Normal'

        símismo.bt = tk.Button(pariente.cj, relief=tk.FLAT, command=comanda,
                               **símismo.formato_norm, **símismo.formato)

        símismo.desbloquear()  # Activar el botón
        símismo.bt.bind('<Enter>', lambda event, b=símismo: b.resaltar())
        símismo.bt.bind('<Leave>', lambda event, b=símismo: b.desresaltar())

        if tipo_ubic == 'pack':
            símismo.bt.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.bt.place(**ubicación)

    def bloquear(símismo):
        símismo.estado = 'Bloqueado'
        símismo.bt.configure(state=tk.DISABLED, **símismo.formato_bloq)

    def desbloquear(símismo):
        símismo.estado = 'Normal'
        símismo.bt.configure(state=tk.ACTIVE, **símismo.formato_norm)

    def resaltar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(**símismo.formato_sel)

    def desresaltar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(**símismo.formato_norm)

    def seleccionar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(**símismo.formato_sel)

    def deseleccionar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(**símismo.formato_norm)


class BotónTexto(Botón):
    def __init__(símismo, pariente, comanda, texto, formato_norm, formato_sel,
                 ubicación, tipo_ubic, formato_bloq=None):

        super().__init__(pariente, comanda, texto=texto, formato_norm=formato_norm,
                         formato_sel=formato_sel, formato_bloq=formato_bloq,
                         ubicación=ubicación, tipo_ubic=tipo_ubic)


class BotónImagen(Botón):
    def __init__(símismo, pariente, comanda, formato, img_norm, img_sel, img_bloq=None,
                 ubicación=None, tipo_ubic=None):
        super().__init__(pariente, comanda, formato=formato, img_norm=img_norm,
                         img_sel=img_sel, img_bloq=img_bloq,
                         ubicación=ubicación, tipo_ubic=tipo_ubic)


class BotónNavIzq(BotónImagen):
    def __init__(símismo, pariente, caja):
        img_norm = Gr.imagen('BtNavIzq_norm_%i' % caja.núm)
        img_bloq = Gr.imagen('BtNavIzq_bloq_%i' % caja.núm)
        img_sel = Gr.imagen('BtNavIzq_sel_%i' % caja.núm)

        super().__init__(pariente=pariente, comanda=caja.traer_me, img_norm=img_norm, img_bloq=img_bloq,
                         img_sel=img_sel, ubicación=Fm.ubic_BtNavIzq, tipo_ubic='pack',
                         formato=Fm.formato_BtsNavIzq)


class BotónNavEtapa(BotónImagen):
    def __init__(símismo, pariente, tipo):
        if tipo == 'adelante':
            img_norm = Gr.imagen('BtNavEtp_adel_norm')
            img_bloq = Gr.imagen('BtNavEtp_adel_bloq')
            img_sel = Gr.imagen('BtNavEtp_adel_sel')
            ubicación = Fm.ubic_BtNavEtp_adel
            comanda = pariente.ir_etp_siguiente
        elif tipo == 'atrás':
            img_norm = Gr.imagen('BtNavEtp_atrs_norm')
            img_bloq = Gr.imagen('BtNavEtp_atrs_bloq')
            img_sel = Gr.imagen('BtNavEtp_atrs_sel')
            ubicación = Fm.ubic_BtNavEtp_atrs
            comanda = pariente.ir_etp_anterior
        else:
            raise ValueError

        super().__init__(pariente=pariente, comanda=comanda, img_norm=img_norm, img_bloq=img_bloq,
                         img_sel=img_sel, ubicación=ubicación, tipo_ubic='place',
                         formato=Fm.formato_BtsNavEtapa)


class BotónNavSub(BotónImagen):
    def __init__(símismo, pariente, tipo):
        if tipo == 'adelante':
            img_norm = Gr.imagen('BtNavSub_adel_norm')
            img_bloq = Gr.imagen('BtNavSub_adel_bloq')
            img_sel = Gr.imagen('BtNavSub_adel_sel')
            ubicación = Fm.ubic_BtNavSub_adel
            comanda = pariente.ir_sub_siguiente
        elif tipo == 'atrás':
            img_norm = Gr.imagen('BtNavSub_atrs_norm')
            img_bloq = Gr.imagen('BtNavSub_atrs_bloq')
            img_sel = Gr.imagen('BtNavSub_atrs_sel')
            ubicación = Fm.ubic_BtNavSub_atrs
            comanda = pariente.ir_sub_anterior
        else:
            raise ValueError

        super().__init__(pariente=pariente, comanda=comanda, img_norm=img_norm, img_bloq=img_bloq,
                         img_sel=img_sel, ubicación=ubicación, tipo_ubic='place',
                         formato=Fm.formato_BtsNavSub)


class Menú(object):
    def __init__(símismo, pariente, opciones, comanda, ubicación, tipo_ubic,
                 etiq=None, formato=Fm.formato_MenuOpciones):
        símismo.opciones = opciones
        símismo.comanda = comanda
        símismo.etiq = etiq
        símismo.var = tk.StringVar(símismo)
        símismo.val = None

        símismo.exclusivos = []

        símismo.MenúOpciones = tk.OptionMenu(pariente, símismo.var, opciones,
                                             command=símismo.acción_cambio,
                                             **formato)

        if tipo_ubic == 'pack':
            símismo.MenúOpciones.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.MenúOpciones.place(**ubicación)

    def estab_exclusivo(símismo, otro_menú):
        assert type(otro_menú) is Menú
        if otro_menú not in símismo.exclusivos:
            símismo.exclusivos.append(otro_menú)
        if símismo not in otro_menú.exclusivos:
            otro_menú.estab_exclusivo(símismo)

    def acción_cambio(símismo, nueva_val):
        print('valor cambió a %s' % nueva_val)
        if nueva_val != símismo.val:
            for menú in símismo.exclusivos:
                menú.excluir(nueva_val)
                menú.reinstaurar(símismo.val)

            símismo.val = nueva_val
            símismo.comanda(nueva_val)

            if símismo.etiq is not None:
                símismo.etiq.configure(text=nueva_val)

    def excluir(símismo, valor):
        menú = símismo.MenúOpciones['Menu']
        i = símismo.opciones.index(valor)
        menú.entryconfig(i, state=tk.DISABLED)

    def reinstaurar(símismo, valor):
        menú = símismo.MenúOpciones['Menu']
        i = símismo.opciones.index(valor)
        menú.entryconfig(i, state=tk.NORMAL)

    def bloquear(símismo):
        símismo.MenúOpciones['optionsmenu'].configure(state=tk.DISABLED)

    def desbloquear(símismo):
        símismo.MenúOpciones['optionsmenu'].configure(state=tk.NORMAL)
