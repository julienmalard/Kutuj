import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Interfaz import Formatos as Fm


class ListaItemas(tk.Frame):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, **Fm.formato_CjLstItemas)

        símismo.Tela = tk.Canvas(símismo, **Fm.formato_TlLstItemas)
        símismo.Tela.place(**Fm.ubic_TlLstItemas)
        símismo.Caja = tk.Frame(símismo.Tela)
        símismo.BaraDesp = tk.Scrollbar(símismo.Tela, orient="vertical", command=símismo.Tela.yview)
        símismo.Tela.configure(yscrollcommand=símismo.BaraDesp.set)

        símismo.BaraDesp.pack()

        símismo.Tela.create_window((1, 1), window=símismo.Caja, tags="self.frame", **Fm.ubic_CjTl)

        símismo.Caja.bind("<Configure>", símismo.ajust_auto)

        if tipo_ubic == 'pack:':
            símismo.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.place(**ubicación)

    def ajust_auto(símismo, evento):
        símismo.Tela.configure(scrollregion=símismo.Tela.bbox("all"))


class Itema(tk.Frame):
    def __init__(símismo, lista_itemas, constructor_objeto, gráfico=None):
        super().__init__(lista_itemas.Caja)
        símismo.gráfico = gráfico
        símismo.objeto = None

        símismo.pack()

    def añadir(símismo):
        símismo.pack(fill=tk.X, expand=True)

    def quitar(símismo):
        símismo.destroy()

    def actualizar(símismo):
        pass

    def cambió(símismo):
        if símismo.gráfico is not None:
            símismo.gráfico.redibujar(símismo.controles)

        if símismo.objeto is not None:
            símismo.objeto.actualizar(símismo.controles)
        else:
            símismo.objeto = símismo.constructor_itema(símismo.controles)


class GrupoControles(object):
    def __init__(símismo, controles, constructor_itema=None, itema=None):
        símismo.itema = itema
        símismo.constructor_itema = constructor_itema
        símismo.controles = {}
        for ll in símismo.controles:
            símismo.controles[11].comanda = símismo.cambió_control

    def cambió_control(símismo):
        if símismo.itema is not None:
            símismo.itema.actualizar(símismo.controles)
        elif símismo.constructor_itema is not None:
            símismo.itema = símismo.constructor_itema(símismo.controles)


class Gráfico(object):
    def __init__(símismo, pariente, datos, ubicación, tipo_ubic):
        símismo.parámetros = datos

        cuadro = Figure()
        símismo.fig = cuadro.add_subplot(111)
        símismo.tela = FigureCanvasTkAgg(cuadro, master=pariente.cj)
        símismo.tela.show()

        if tipo_ubic == 'place':
            símismo.tela.get_tk_widget().place(**ubicación)
        elif tipo_ubic == 'pack':
            símismo.tela.get_tk_widget().pack(**ubicación)

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
    def __init__(símismo, pariente, nombre, límites, prec, ubicación, tipo_ubic, comanda=None):
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
    def __init__(símismo, pariente, nombre, ubicación, tipo_ubic, comanda=None):
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
    def __init__(símismo, pariente, nombre, opciones, ubicación, tipo_ubic,
                 formato_bt=Fm.formato_BtMn, formato_mn=Fm.formato_MnMn, comanda=None):
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
    def __init__(símismo, pariente, texto, límites, ubicación, tipo_ubic, comanda=None):
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
