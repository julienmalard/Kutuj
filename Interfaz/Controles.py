import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Interfaz import Formatos as Fm


class ListaItemas(object):
    def __init__(símismo):
        pass


class Itema(object):
    def __init__(simismo):
        pass


class Escala(object):
    def __init__(símismo, pariente, texto, límites, comanda, ubicación, tipo_ubic):
        símismo.cj = tk.Frame(pariente)
        símismo.comanda = comanda

        símismo.var_escl = tk.DoubleVar()
        símismo.var_escl.trace('w', símismo.cambio_escl)
        símismo.var_ingr = tk.StringVar()
        símismo.var_ingr.trace('w', símismo.cambio_ingr)

        símismo.etiq = tk.Label(símismo.cj, text=texto)
        símismo.ingr = tk.Entry(símismo.cj, variable=símismo.var_ingr, from_=límites[0], to=límites[1],
                                **Fm.formato_Ingr)
        símismo.escl = tk.Scale(símismo.cj, textvariable=símismo.var_escl, **Fm.formato_Escl)

        símismo.ingr.pack(**Fm.ubic_Ingr)
        símismo.escl.pack(**Fm.ubic_Escl)
        if tipo_ubic == 'pack':
            símismo.cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.cj.place(**ubicación)

    def cambio_ingr(símismo, val):
        try:
            val = float(val)
        except ValueError:
            símismo.var_ingr.set('')
            return
        if val != símismo.var_escl.get():
            símismo.var_escl.set(val)

        símismo.comanda(val)

    def cambio_escl(símismo, val):
        if val != símismo.var_ingr.get():
            símismo.var_ingr.set(val)

        símismo.comanda(val)


class Gráfico(object):
    def __init__(símismo, pariente, tamaño, func_dibujar, parámetros, ubicación):
        símismo.func_dibujar = func_dibujar
        símismo.parámetros = parámetros

        símismo.fig = Figure(figsize=tamaño)
        símismo.tela = FigureCanvasTkAgg(símismo.fig, master=pariente.cj)
        símismo.tela.get_tk_widget().place(**ubicación)

    def redibujar(símismo):
        símismo.func_dibujar(símismo.fig.gca(), símismo.parámetros)

class GráficoInteract(object):
    def __init__(símismo, controles, gráfico):
        for control in controles:
            control.comanda = lambda x:

    def cambio_control(símismo):


