import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Interfaz import Formatos as Fm


class ListaItemas(tk.Frame):
    def __init__(símismo, pariente):
        super().__init__(pariente, **Fm.formato_CjLstItemas)

        símismo.Tela = tk.Canvas(símismo, **Fm.formato_TlLstItemas)
        símismo.Tela.place(**Fm.ubic_TlLstItemas)
        símismo.Caja = tk.Frame(símismo.Tela)
        símismo.BaraDesp = tk.Scrollbar(símismo.Tela, orient="vertical", command=símismo.Tela.yview)
        símismo.Tela.configure(yscrollcommand=símismo.BaraDesp.set)

        símismo.BaraDesp.pack()

        símismo.Tela.create_window((1, 1), window=símismo.Caja, tags="self.frame", **Fm.ubic_CjTl)

        símismo.Caja.bind("<Configure>", símismo.ajust_auto)

        símismo.place(**Fm.ubic_TlLstItemas)

    def ajust_auto(símismo, evento):
        símismo.Tela.configure(scrollregion=símismo.Tela.bbox("all"))


class Itema(tk.Frame):
    def __init__(símismo, lista_itemas, constructor_objeto, gráfico=None):
        super().__init__(lista_itemas.Caja)
        símismo.gráfico = gráfico
        símismo.objeto =

        símismo.pack()

    def añadir(símismo):
        símismo.pack(fill=tk.X, expand=True)

    def quitar(símismo):
        símismo.destroy()

    def actualizar(símismo):

    def cambió(símismo):
        if símismo.gráfico is not None:
            símismo.gráfico.redibujar(símismo.controles)

        if símismo.itema is not None:
            símismo.itema.actualizar(símismo.controles)
        else:
            símismo.itema = símismo.constructor_itema(símismo.controles)


class CjControles(tk.Frame):
    def __init__(símismo, pariente, constructor_itema=None, itema=None):
        super().__init__(pariente, **Fm.formato_cajas)
        símismo.itema = itema
        símismo.constructor_itema = constructor_itema
        símismo.controles = {}

    def cambió_control(símismo):
        if símismo.itema is not None:
            símismo.itema.actualizar(símismo.controles)
        elif símismo.constructor_itema is not None:
            símismo.itema = símismo.constructor_itema(símismo.controles)


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


class IngrNúm(object):
    def __init__(símismo, pariente, nombre, límites, prec, comanda, ubicación, tipo_ubic):
        símismo.límites = límites
        símismo.comanda = comanda
        if prec not in ['dec', 'int']:
            raise ValueError('"Prec" debe ser uno de "int" o "dec".')
        símismo.prec = prec

        símismo.var = tk.StringVar()
        símismo.var.set('')
        símismo.var.trace('w', símismo.acción_cambio)
        símismo.val = None

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
        símismo.CampoIngr = tk.Entry(cj, variable=símismo.var, **Fm.formato_CampoIngr)

        símismo.Etiq.pack(**Fm.ubic_EtiqIngrNúm)
        símismo.CampoIngr.pack(**Fm.ubic_CampoIngr)

        if tipo_ubic == 'pack':
            cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            cj.place(**ubicación)

    def acción_cambio(símismo, *args):
        try:
            if símismo.prec == 'int':
                nueva_val = int(símismo.var.get())
            elif símismo.prec == 'dec':
                nueva_val = int(símismo.var.get())
            else:
                print('"Prec" debe ser uno de "int" o "dec".')
                return

            if not (símismo.límites[0] < nueva_val < símismo.límites[1]):
                raise ValueError

            símismo.CampoIngr.config(**Fm.formato_CampoIngr)

        except ValueError:
            símismo.var.set('')
            símismo.CampoIngr.config(**Fm.formato_CampoIngr_error)
            return

        if nueva_val != símismo.val and nueva_val != '':
            símismo.val = nueva_val
            símismo.comanda(nueva_val)

    def bloquear(símismo):
        símismo.CampoIngr.configure(state=tk.DISABLED, cursor='X_cursor', **Fm.formato_BtMn_bloq)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl_bloq)

    def desbloquear(símismo):
        símismo.CampoIngr.configure(state=tk.NORMAL, cursor='arrow', **Fm.formato_BtMn)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl)


class IngrTexto(object):
    def __init__(símismo, pariente, nombre, comanda, ubicación, tipo_ubic):
        símismo.comanda = comanda

        símismo.var = tk.StringVar()
        símismo.var.set('')
        símismo.var.trace('w', símismo.acción_cambio)
        símismo.val = None

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
        símismo.CampoIngr = tk.Entry(cj, variable=símismo.var, **Fm.formato_CampoIngr)

        símismo.Etiq.pack(**Fm.ubic_EtiqIngrNúm)
        símismo.CampoIngr.pack(**Fm.ubic_CampoIngr)

        if tipo_ubic == 'pack':
            cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            cj.place(**ubicación)

    def acción_cambio(símismo, *args):
        nueva_val = int(símismo.var.get())
        if nueva_val != símismo.val and nueva_val != '':
            símismo.val = nueva_val
            símismo.comanda(nueva_val)

    def bloquear(símismo):
        símismo.CampoIngr.configure(state=tk.DISABLED, cursor='X_cursor', **Fm.formato_BtMn_bloq)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl_bloq)

    def desbloquear(símismo):
        símismo.CampoIngr.configure(state=tk.NORMAL, cursor='arrow', **Fm.formato_BtMn)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl)


class Menú(object):
    def __init__(símismo, pariente, nombre, opciones, comanda, ubicación, tipo_ubic,
                 formato_bt=Fm.formato_BtMn, formato_mn=Fm.formato_MnMn):
        símismo.opciones = opciones
        símismo.comanda = comanda

        símismo.var = tk.StringVar()
        símismo.var.set('')
        símismo.var.trace('w', símismo.acción_cambio)
        símismo.val = None
        símismo.exclusivos = []

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
        símismo.MenúOpciones = tk.OptionMenu(cj, símismo.var, opciones)

        símismo.MenúOpciones.config(**formato_bt)
        símismo.MenúOpciones['menu'].config(**formato_mn)

        símismo.Etiq.pack(**Fm.ubic_EtiqMenú)
        símismo.MenúOpciones.pack(**Fm.ubic_Menú)

        if tipo_ubic == 'pack':
            cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            cj.place(**ubicación)

    def estab_exclusivo(símismo, otro_menú):
        assert type(otro_menú) is Menú
        if otro_menú not in símismo.exclusivos:
            símismo.exclusivos.append(otro_menú)
        if símismo not in otro_menú.exclusivos:
            otro_menú.estab_exclusivo(símismo)

    def acción_cambio(símismo, *args):
        nueva_val = símismo.var.get()

        print('valor cambió a %s' % nueva_val)
        if nueva_val != símismo.val and nueva_val != '':
            for menú in símismo.exclusivos:
                menú.excluir(nueva_val)
                if símismo.val is not None:
                    menú.reinstaurar(símismo.val)

            símismo.val = nueva_val
            símismo.comanda(nueva_val)
                
    def refrescar(símismo, opciones):
        símismo.opciones = opciones
        símismo.var.set('')
        símismo.MenúOpciones['menu'].delete(0, 'end')
        for opción in opciones:
            símismo.MenúOpciones['menu'].add_command(label=opción, command=tk._setit(símismo.var, opción))

    def excluir(símismo, valor):
        menú = símismo.MenúOpciones['menu']
        i = símismo.opciones.index(valor)
        menú.entryconfig(i, state=tk.DISABLED)

    def reinstaurar(símismo, valor):
        menú = símismo.MenúOpciones['menu']
        i = símismo.opciones.index(valor)
        menú.entryconfig(i, state=tk.NORMAL)

    def bloquear(símismo):
        símismo.MenúOpciones.configure(state=tk.DISABLED, cursor='X_cursor', **Fm.formato_BtMn_bloq)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl_bloq)

    def desbloquear(símismo):
        símismo.MenúOpciones.configure(state=tk.NORMAL, cursor='arrow', **Fm.formato_BtMn)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl)


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
        if val != símismo.var_escl.get():
            símismo.var_escl.set(float(val))
        símismo.comanda(val)

    def cambio_escl(símismo, val):
        if val != símismo.var_ingr.get():
            símismo.var_ingr.set(str(val))

        símismo.comanda(val)
