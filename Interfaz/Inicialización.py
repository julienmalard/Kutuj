import tkinter as tk

from Interfaz import Formatos as Fm


def crear_caja_central(pariente):
    cj = tk.Frame(pariente)
    cj.place(**Fm.ubic_CjCent)

    return cj
