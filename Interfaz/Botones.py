import tkinter as tk

from Interfaz import Gráficos as Gr
from Interfaz import Formatos as Fm


class Botón(object):
    def __init__(símismo, pariente, comanda, img_norm, img_bloq, img_sel, ubicación):
        símismo.img_norm = img_norm
        símismo.img_bloq = img_bloq
        símismo.img_sel = img_sel
        símismo.estado = 'Normal'

        símismo.bt = tk.Button(pariente, relief=tk.FLAT, command=comanda, image=símismo.img_norm)
        símismo.bt.place(**ubicación)
        símismo.bt.bind('<Enter>', lambda event, b=símismo: b.seleccionar())
        símismo.bt.bind('<Leave>', lambda event, b=símismo: b.deseleccionar())

    def bloquear(símismo):
        símismo.estado = 'Bloqueado'
        símismo.bt.configure(image=símismo.img_bloq, state=tk.DISABLED)

    def desbloquear(símismo):
        símismo.estado = 'Normal'
        símismo.bt.configure(image=símismo.img_norm, state=tk.ACTIVE)

    def seleccionar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(image=símismo.img_sel)

    def deseleccionar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(image=símismo.img_norm)


class BotónNavIzq(Botón):
    def __init__(símismo, pariente):
        img_norm = Gr.imagen('BtNavIzq_norm_%i' % pariente.núm)
        img_bloq = Gr.imagen('BtNavIzq_bloq_%i' % pariente.núm)
        img_sel = Gr.imagen('BtNavIzq_sel_%i' % pariente.núm)
        ubicación = Fm.ubic_BtNavIzq
        comanda = pariente.traer_me

        super().__init__(pariente=pariente, comanda=comanda, img_norm=img_norm, img_bloq=img_bloq,
                         img_sel=img_sel, ubicación=ubicación)


class BotónNavEtapa(Botón):
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
                         img_sel=img_sel, ubicación=ubicación)


class BotónNavSub(Botón):
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
                         img_sel=img_sel, ubicación=ubicación)


class BotónTexto(object):
    def __init__(símismo, pariente, comanda, texto, col_fd_norm, col_fd_bloq, col_fd_sel,
                 col_tx_norm, col_tx_bloq, col_tx_sel, formato, ubicación):
        símismo.col_norm = (col_fd_norm, col_tx_norm)
        símismo.col_bloq = (col_fd_bloq, col_tx_bloq)
        símismo.col_sel = (col_fd_sel, col_tx_sel)
        símismo.estado = 'Normal'

        símismo.bt = tk.Button(pariente, relief=tk.FLAT, command=comanda, image=texto, **formato)
        símismo.bt.place(**ubicación)
        símismo.bt.bind('<Enter>', lambda event, b=símismo: b.seleccionar())
        símismo.bt.bind('<Leave>', lambda event, b=símismo: b.deseleccionar())

    def bloquear(símismo):
        símismo.estado = 'Bloqueado'
        símismo.bt.configure(bg=símismo.col_bloq[0], fg=símismo.col_bloq[1], state=tk.DISABLED)

    def desbloquear(símismo):
        símismo.estado = 'Normal'
        símismo.bt.configure(bg=símismo.col_norm[0], fg=símismo.col_norm[1], state=tk.ACTIVE)

    def seleccionar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(bg=símismo.col_sel[0], fg=símismo.col_sel[1])

    def deseleccionar(símismo):
        if símismo.estado == 'Normal':
            símismo.bt.configure(bg=símismo.col_norm[0], fg=símismo.col_norm[1])
