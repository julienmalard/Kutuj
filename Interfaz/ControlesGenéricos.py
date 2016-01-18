import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Interfaz import Arte as Art
from Interfaz import Formatos as Fm
from Interfaz import Botones as Bt


class ListaItemas(tk.Frame):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, **Fm.formato_CjLstItemas)
        símismo.objetos = []

        símismo.Tela = tk.Canvas(símismo, **Fm.formato_TlLstItemas)
        símismo.Tela.place(**Fm.ubic_TlLstItemas)
        símismo.Caja = tk.Frame(símismo.Tela)
        símismo.BaraDesp = tk.Scrollbar(símismo.Tela, orient="vertical", command=símismo.Tela.yview)
        símismo.Tela.configure(yscrollcommand=símismo.BaraDesp.set)

        símismo.BaraDesp.pack(**Fm.ubic_BaraDesp)

        símismo.Tela.create_window((1, 1), window=símismo.Caja, tags="self.frame", **Fm.ubic_CjTl)

        símismo.Caja.bind("<Configure>", símismo.ajust_auto)

        if tipo_ubic == 'pack:':
            símismo.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.place(**ubicación)

    def ajust_auto(símismo, evento):
        símismo.Tela.configure(scrollregion=símismo.Tela.bbox("all"))


class ListaEditable(ListaItemas):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        super().__init__(pariente, ubicación=ubicación, tipo_ubic=tipo_ubic)
        símismo.controles = None

    def editar(símismo, itema):
        símismo.controles.objeto = itema.objeto


class Itema(tk.Frame):
    def __init__(símismo, lista_itemas):
        super().__init__(lista_itemas.Caja)
        símismo.objeto = NotImplemented
        símismo.lista = lista_itemas
        lista_itemas.objetos.append(símismo.objeto)

        símismo.pack()

    def quitar(símismo):
        símismo.lista.objetos.pop(símismo.objeto)
        símismo.destroy()


class ItemaEditable(Itema):
    def __init__(símismo, grupo_control, lista_itemas, columnas, ancho):
        super().__init__(lista_itemas.Caja)
        símismo.objeto = grupo_control.objeto
        símismo.receta = grupo_control.receta
        símismo.columnas = columnas

        cj_bts = tk.Frame(width=Fm.ancho_cj_bts_itemas, **Fm.formato_secciones_itemas)
        símismo.bt_editar = Bt.BotónImagen(cj_bts, comanda=símismo.editar, formato=Fm.formato_botones,
                                           img_norm=Art.imagen('BtEditarItema_norm'),
                                           img_sel=Art.imagen('BtEditarItema_sel'),
                                           ubicación=Fm.ubic_BtsItemas, tipo_ubic='pack')
        símismo.bt_borrar = Bt.BotónImagen(cj_bts, comanda=símismo.quitar, formato=Fm.formato_botones,
                                           img_norm=Art.imagen('BtBorrarItema_norm'),
                                           img_sel=Art.imagen('BtBorrarItema_sel'),
                                           ubicación=Fm.ubic_BtsItemas, tipo_ubic='pack')

        símismo.columnas.append(cj_bts)

        for n, col in enumerate(símismo.columnas):
            col.config(width=int(ancho[n]*(lista_itemas.ancho - Fm.ancho_cj_bts_itemas)))
            col.pack(**Fm.ubic_ColsItemas)

        símismo.bind('<Enter>', lambda event, i=símismo: i.resaltar())
        símismo.bind('<Leave>', lambda event, i=símismo: i.desresaltar())

    def editar(símismo):
        símismo.lista.editar(símismo)

    def actualizar(símismo):
        raise NotImplementedError

    def resaltar(símismo):
        raise NotImplementedError

    def desresaltar(símismo):
        raise NotImplementedError


class GrupoControles(object):
    def __init__(símismo, controles, constructor_itema=None, itema=None, gráfico=None, lista=None,
                 bt_guardar=None, bt_borrar=None):
        símismo.controles = controles
        símismo.constructor_itema = constructor_itema
        símismo.itema = itema
        símismo.gráfico = gráfico
        símismo.lista = lista
        símismo.bt_guardar = bt_guardar
        símismo.bt_borrar = bt_borrar
        símismo.objeto = None
        símismo.receta = {}

        for ll in símismo.controles:
            símismo.controles[ll].comanda = símismo.cambió_control

        if símismo.lista is not None:
            símismo.lista.controles = símismo

        if símismo.gráfico is not None:
            símismo.gráfico.objeto = símismo.objeto
            símismo.gráfico.controles = símismo.controles

        if símismo.bt_guardar is not None:
            símismo.bt_guardar.comanda = símismo.guardar
        if símismo.bt_borrar is not None:
            símismo.bt_borrar.comanda = símismo.borrar

    def cambió_control(símismo, *args):
        if símismo.verificar_completo() is True:
            símismo.recrear_objeto()
            if símismo.gráfico is not None:
                símismo.gráfico.redibujar()
            if símismo.bt_guardar is not None:
                símismo.bt_guardar.desbloquear()
        else:
            if símismo.bt_guardar is not None:
                símismo.bt_guardar.bloquear()

    def guardar(símismo):
        if símismo.itema is not None:
            símismo.itema.actualizar()
        elif símismo.constructor_itema is not None:
            símismo.itema = símismo.constructor_itema(símismo, símismo.lista)
            símismo.controles = None

        símismo.borrar()
        símismo.itema = None

    def borrar(símismo):
        for control in símismo.controles:
            control.borrar()

    def verificar_completo(símismo):
        raise NotImplementedError

    def recrear_objeto(símismo):
        raise NotImplementedError


class Gráfico(object):
    def __init__(símismo, pariente, ubicación, tipo_ubic):
        símismo.objeto = None
        símismo.controles = None

        cuadro = Figure()
        cuadro.patch.set_facecolor(Fm.col_fondo)
        símismo.fig = cuadro.add_subplot(111)
        símismo.tela = FigureCanvasTkAgg(cuadro, master=pariente)
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
        símismo.CampoIngr = tk.Entry(cj, textvariable=símismo.var, **Fm.formato_CampoIngr)

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
            símismo.val = None
            símismo.CampoIngr.config(**Fm.formato_CampoIngr_error)
            return

        if nueva_val != símismo.val and nueva_val != '':
            símismo.val = nueva_val
            símismo.comanda(nueva_val)

    def borrar(símismo):
        símismo.var.set('')

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
        símismo.val = None

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
        símismo.CampoIngr = tk.Entry(cj, textvariable=símismo.var, **Fm.formato_CampoIngr)
        símismo.CampoIngr.bind('<FocusOut>', símismo.acción_cambio)

        símismo.Etiq.pack(**Fm.ubic_EtiqIngrNúm)
        símismo.CampoIngr.pack(**Fm.ubic_CampoIngr)

        if tipo_ubic == 'pack':
            cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            cj.place(**ubicación)

    def acción_cambio(símismo, *args):
        nueva_val = símismo.var.get()
        if nueva_val == '':
            símismo.val = None
            return

        if nueva_val != símismo.val:
            símismo.val = nueva_val
            símismo.comanda(nueva_val)

    def borrar(símismo):
        símismo.var.set('')

    def bloquear(símismo):
        símismo.CampoIngr.configure(state=tk.DISABLED, cursor='X_cursor', **Fm.formato_BtMn_bloq)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl_bloq)

    def desbloquear(símismo):
        símismo.CampoIngr.configure(state=tk.NORMAL, cursor='arrow', **Fm.formato_BtMn)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl)


class Menú(object):
    def __init__(símismo, pariente, nombre, opciones, ubicación, tipo_ubic,
                 formato_bt=Fm.formato_BtMn, formato_mn=Fm.formato_MnMn, comanda=None, inicial=''):
        símismo.opciones = opciones
        símismo.comanda = comanda

        símismo.var = tk.StringVar()
        símismo.val_inicial = inicial

        símismo.val = None
        símismo.exclusivos = []

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
        símismo.MenúOpciones = tk.OptionMenu(cj, símismo.var, '')
        símismo.refrescar(opciones)
        símismo.var.trace('w', símismo.acción_cambio)

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

        if nueva_val == '':
            símismo.val = None
            return

        if nueva_val != símismo.val:
            for menú in símismo.exclusivos:
                menú.excluir(nueva_val)
                if símismo.val is not None:
                    menú.reinstaurar(símismo.val)

            símismo.val = nueva_val
            símismo.comanda(nueva_val)
                
    def refrescar(símismo, opciones):
        símismo.opciones = opciones
        símismo.MenúOpciones['menu'].delete(0, 'end')
        for opción in opciones:
            símismo.MenúOpciones['menu'].add_command(label=opción, command=tk._setit(símismo.var, opción))

        símismo.var.set(símismo.val_inicial)

    def excluir(símismo, valor):
        menú = símismo.MenúOpciones['menu']
        i = símismo.opciones.index(valor)
        menú.entryconfig(i, state=tk.DISABLED)

    def reinstaurar(símismo, valor):
        menú = símismo.MenúOpciones['menu']
        i = símismo.opciones.index(valor)
        menú.entryconfig(i, state=tk.NORMAL)

    def borrar(símismo):
        símismo.var.set(símismo.val_inicial)

    def bloquear(símismo):
        símismo.MenúOpciones.configure(state=tk.DISABLED, cursor='X_cursor', **Fm.formato_BtMn_bloq)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl_bloq)

    def desbloquear(símismo):
        símismo.MenúOpciones.configure(state=tk.NORMAL, cursor='arrow', **Fm.formato_BtMn)
        símismo.Etiq.config(**Fm.formato_EtiqCtrl)


class Escala(object):
    def __init__(símismo, pariente, texto, límites, ubicación, tipo_ubic, comanda=None, valor_inicial=None):
        símismo.cj = tk.Frame(pariente)
        símismo.comanda = comanda
        if valor_inicial is None:
            valor_inicial = (límites[0] + límites[1])/2
        símismo.valor_inicial = valor_inicial

        símismo.var_escl = tk.DoubleVar()
        símismo.var_escl.trace('w', símismo.cambio_escl)
        símismo.var_ingr = tk.StringVar()
        símismo.var_ingr.trace('w', símismo.cambio_ingr)

        símismo.etiq = tk.Label(símismo.cj, text=texto)
        símismo.ingr = tk.Entry(símismo.cj, textvariable=símismo.var_ingr, **Fm.formato_CampoIngr)
        símismo.escl = tk.Scale(símismo.cj, variable=símismo.var_escl, from_=límites[0], to=límites[1],
                                **Fm.formato_Escl)

        símismo.ingr.pack(**Fm.ubic_CampoIngr)
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

    def borrar(símismo):
        símismo.var_escl.set(símismo.valor_inicial)
        símismo.var_ingr.set(símismo.valor_inicial)
