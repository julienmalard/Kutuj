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
            símismo.bt_guardar.estab_comanda(símismo.guardar)
        if símismo.bt_borrar is not None:
            símismo.bt_borrar.estab_comanda(símismo.borrar)

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
        for ll, control in símismo.controles.items():
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
    def __init__(símismo, pariente, nombre, límites, val_inic, prec, ubicación, tipo_ubic, ancho=5, comanda=None):
        símismo.límites = límites
        símismo.comanda = comanda
        if prec not in ['dec', 'ent']:
            raise ValueError('"Prec" debe ser uno de "ent" o "dec".')
        símismo.prec = prec

        if val_inic is None:
            val_inic = (límites[0] + límites[1])/2
        símismo.val_inic = val_inic

        if prec == 'ent':
            símismo.val_inic = round(símismo.val_inic)
        else:
            símismo.val_inic = round(símismo.val_inic, 2)

        símismo.var = tk.StringVar()
        símismo.var.set(símismo.val_inic)
        símismo.var.trace('w', símismo.acción_cambio)
        símismo.val = None

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        if nombre is not None:
            símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
            símismo.Etiq.pack(**Fm.ubic_EtiqIngrNúm)

        símismo.CampoIngr = tk.Entry(cj, textvariable=símismo.var, width=ancho, **Fm.formato_CampoIngr)
        símismo.CampoIngr.pack(**Fm.ubic_CampoIngrEscl)

        if tipo_ubic == 'pack':
            cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            cj.place(**ubicación)

    def acción_cambio(símismo, *args):
        try:
            if símismo.prec == 'ent':
                nueva_val = int(símismo.var.get())
            elif símismo.prec == 'dec':
                nueva_val = round(float(símismo.var.get()), 3)
            else:
                print('"Prec" debe ser uno de "ent" o "dec".')
                return

            if not (símismo.límites[0] <= nueva_val <= símismo.límites[1]):
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
        símismo.CampoIngr = tk.Entry(cj, textvariable=símismo.var, width=20, **Fm.formato_CampoIngr)
        símismo.CampoIngr.bind('<FocusOut>', símismo.acción_cambio)

        símismo.Etiq.pack(**Fm.ubic_EtiqIngrNúm)
        símismo.CampoIngr.pack(**Fm.ubic_CampoIngrEscl)

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

        símismo.val_inicial = inicial
        símismo.var = tk.StringVar()

        símismo.val = inicial
        símismo.exclusivos = []

        cj = tk.Frame(pariente, **Fm.formato_cajas)

        símismo.Etiq = tk.Label(cj, text=nombre, **Fm.formato_EtiqCtrl)
        símismo.MenúOpciones = tk.OptionMenu(cj, símismo.var, '')
        símismo.MenúOpciones.config(takefocus=True)
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
    def __init__(símismo, pariente, texto, límites, prec, ubicación, tipo_ubic, comanda=None, valor_inicial=None):
        símismo.cj = tk.Frame(pariente, **Fm.formato_cajas)
        símismo.comanda = comanda
        if valor_inicial is None:
            valor_inicial = (límites[0] + límites[1])/2
        símismo.valor_inicial = valor_inicial

        símismo.val = símismo.valor_inicial

        símismo.etiq = tk.Label(símismo.cj, text=texto, **Fm.formato_EtiqCtrl)

        etiq_inic = tk.Label(símismo.cj, text=límites[0], **Fm.formato_EtiqNúmEscl)
        símismo.escl = CosoEscala(símismo, límites, val_inic=valor_inicial, prec=prec)
        etiq_fin = tk.Label(símismo.cj, text=límites[1], **Fm.formato_EtiqNúmEscl)

        símismo.etiq.pack(**Fm.ubic_EtiqEscl)
        etiq_inic.pack(**Fm.ubic_EtiqNúmEscl)
        símismo.escl.pack(**Fm.ubic_Escl)
        etiq_fin.pack(**Fm.ubic_EtiqNúmEscl)

        símismo.ingr = IngrNúm(símismo.cj, nombre=None, límites=límites, val_inic=valor_inicial, prec=prec,
                               ubicación=Fm.ubic_CampoIngrEscl, tipo_ubic='pack',
                               comanda=símismo.cambio_ingr)

        if tipo_ubic == 'pack':
            símismo.cj.pack(**ubicación)
        elif tipo_ubic == 'place':
            símismo.cj.place(**ubicación)

    def cambio_ingr(símismo, val):
        if val != símismo.escl.val:
            símismo.escl.poner(float(val))
            símismo.val = float(val)
            if símismo.comanda is not None:
                símismo.comanda(val)

    def cambio_escl(símismo, val):
        if str(val) != símismo.val:
            símismo.val = val
            símismo.ingr.var.set(val)

            if símismo.comanda is not None:
                símismo.comanda(val)

    def borrar(símismo):
        pass
        # símismo.escl.poner(símismo.valor_inicial)
        # símismo.ingr.var.set(símismo.valor_inicial)
        # símismo.val = símismo.valor_inicial


class CosoEscala(tk.Canvas):
    def __init__(símismo, pariente, límites, val_inic, ancho=150, altura=30, prec='cont'):
        super().__init__(pariente.cj, width=ancho, height=altura, background=Fm.col_fondo, highlightthickness=0)

        símismo.dim = (ancho, altura)
        símismo.límites = límites
        símismo.pariente = pariente
        símismo.tipo = prec
        símismo.val = val_inic

        símismo.create_rectangle(0, 0, 1, altura, **Fm.formato_lín_escl)
        símismo.create_rectangle(ancho-2, 0, ancho, altura, **Fm.formato_lín_escl)
        símismo.create_line(0, round(altura/2), ancho, round(altura/2), fill=Fm.col_1)

        símismo.info_mov = {"x": 0, "y": 0}

        símismo.manilla = símismo.create_rectangle(float(ancho / 2) - 3, 0, float(ancho / 2) + 3, altura,
                                                   outline=Fm.col_2, fill=Fm.col_2)

        símismo.tag_bind(símismo.manilla, "<ButtonPress-1>", símismo.acción_empujar)
        símismo.tag_bind(símismo.manilla, "<ButtonRelease-1>", símismo.acción_soltar)
        símismo.tag_bind(símismo.manilla, "<B1-Motion>", símismo.acción_movimiento)
        símismo.bind("<ButtonRelease-1>", símismo.acción_soltar)

        símismo.poner(símismo.val)

    def acción_empujar(símismo, event):
        símismo.info_mov["x"] = (símismo.coords(símismo.manilla)[0] + símismo.coords(símismo.manilla)[2])/2

    def acción_soltar(símismo, event):
        símismo.info_mov["x"] = 0

    def acción_movimiento(símismo, event):
        x = event.x
        if x > símismo.dim[0]:
            x = símismo.dim[0]
        elif x < 0:
            x = 0

        símismo.val = round(x/símismo.dim[0] * (símismo.límites[1] - símismo.límites[0]) + símismo.límites[0], 3)

        if símismo.tipo == 'ent':
            símismo.val = int(símismo.val)
            x = (símismo.val - símismo.límites[0])/(símismo.límites[1] - símismo.límites[0])*símismo.dim[0]

        delta_x = x - símismo.info_mov["x"]

        símismo.move(símismo.manilla, delta_x, 0)

        símismo.info_mov["x"] = x

        símismo.pariente.cambio_escl(símismo.val)

    def poner(símismo, val):
        símismo.val = val
        x_manilla = (símismo.coords(símismo.manilla)[0] + símismo.coords(símismo.manilla)[2])/2
        nuevo_x = (símismo.val - símismo.límites[0])/(símismo.límites[1] - símismo.límites[0])*símismo.dim[0]
        delta_x = nuevo_x - x_manilla
        símismo.move(símismo.manilla, delta_x, 0)
