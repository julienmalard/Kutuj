import tkinter as tk


# Ventana central
ancho_ventana = 800
altura_ventana = 600
color_ventana = 'white'

# Caja inicial
formato_CjInic = dict()
ubic_CjInic = dict(relx=-1, y=0, relwidth=1, relheigth=1)

# Caja lenguas
formato_CjLeng = dict()
ubic_CjLeng = dict(relx=1, y=0, relwidth=1, relheight=1)

# Caja central
ubic_CjCent = dict(x=0, y=0, relwidth=1, relheight=1)

# Botones izquierda
ubic_BtNavIzq = dict()

# Cajas etapas
ubic_CjEtp = dict(x=0, y=0, relwidth=1, relheight=1)
ubic_BtNavEtp_adel = dict(anchor=tk.S)
ubic_BtNavEtp_atrs = dict(anchor=tk.N)

# Cajas sub etapas
ubic_BtNavSub_adel = dict(anchor=tk.E)
ubic_BtNavSub_atrs = dict(anchor=tk.W)
