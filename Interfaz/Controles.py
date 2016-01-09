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
                
    def refrescar(símismo, opciones):
        símismo.opciones = opciones
        símismo.var.set('')
        símismo.MenúOpciones['menu'].delete(0, 'end')
        for opción in opciones:
            símismo.MenúOpciones['menu'].add_command(label=opción, command=tk._setit(símismo.var, opción))

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
    def __init__(símismo, pariente, func_dibujar, parámetros, ubicación):
        símismo.func_dibujar = func_dibujar
        símismo.parámetros = parámetros

        cuadro = Figure()
        símismo.fig = cuadro.add_subplot(111)
        símismo.tela = FigureCanvasTkAgg(cuadro, master=pariente.cj)
        símismo.tela.show()
        símismo.tela.get_tk_widget().place(**ubicación)

    def redibujar(símismo):
        try:
            símismo.fig.patches[0].remove()
        except IndexError:
            pass
        try:
            símismo.fig.lines[0].remove()
        except IndexError:
            pass
        símismo.dibujar()

        símismo.tela.draw()

    def dibujar(símismo):
        raise NotImplementedError


class GráficoInteract(object):
    def __init__(símismo, controles, gráfico):
        símismo.gráfico = gráfico
        for control in controles:
            pass

    def cambio_control(símismo):
        símismo.gráfico.redibujar()

