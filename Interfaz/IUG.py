import tkinter as tk

from Interfaz import Formatos as Fm
from Interfaz import Cajas as Cj


class Apli(tk.Frame):
    def __init__(símismo, pariente):
        tk.Frame.__init__(símismo, pariente)
        pariente.title('Kutuj')
        pariente.geometry('%ix%i' % (Fm.ancho_ventana, Fm.altura_ventana))
        pariente.configure(background=Fm.color_ventana)

        símismo.CajaInic = Cj.CajaInic(símismo)
        símismo.CajaCentral = Cj.CajaCentral(símismo)
        símismo.CajaLenguas = Cj.CajaLeng(símismo)
        símismo.CajaInic.cj.lift()


if __name__ == '__main__':
    raíz = tk.Tk()
    apli = Apli(raíz)
    apli.mainloop()
