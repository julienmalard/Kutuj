import tkinter as tk


# Parámetros generales
col_fondo = 'white'  # El color de fondo del interfaz

# Ventana central
ancho_ventana = 800
altura_ventana = 600
color_ventana = col_fondo

# Caja inicial
formato_CjInic = dict()
ubic_CjInic = dict(x=0, y=0, relwidth=1, relheight=1)
formato_LogoInic = dict(borderwidth=0, highlightthickness=0)
ubic_LogoInic = dict(pady=(0.5, 0))
formato_BtsInic = dict(borderwidth=0, highlightthickness=0, activebackground='#6699ff',
                       font=('arial', 20, 'bold'), height=3, width=13)  # Formatos generales
formato_BtsInic_norm = dict(bg='#e5ffff', fg='#000000', **formato_BtsInic)
formato_BtsInic_bloq = dict()
formato_BtsInic_sel = dict(bg='#99ccff')
ubic_BtsInic = dict(side='left', ipadx=5, ipady=5, padx=10, pady=10)

# Caja lenguas
formato_CjLeng = dict()
ubic_CjLeng = dict(relx=1, y=0, relwidth=1, relheight=1)
formato_BtRegrCent = dict()
ubic_BtRegrCent = dict(x=10, y=10)

# Caja central
formato_CjCent = dict(bg=col_fondo)
ubic_CjCent = dict(x=0, y=0, relwidth=1, relheight=1)

# Caja cabeza
ubic_CajaCabeza = dict(x=0, y=0, relwidth=1, height=80)
formato_LogoCabz = dict(borderwidth=0, highlightthickness=0, height=60)
ubic_LogoCabz = dict(relx=0.5, rely=0)
formato_BtLeng = dict(borderwidth=0, highlightthickness=0, height=40, width=40)
ubic_BtLeng = dict(relx=1, rely=0.5, x=-20, anchor=tk.E)

# Botones izquierda
ubic_CjIzq = dict(x=0, y=ubic_CajaCabeza['height'])
ubic_BtNavIzq = dict(side='top')
formato_BtsNavIzq = dict(width=60, height=60)
ubic_LínIzq = dict(side='top')
formato_LínIzq = dict(bd=0, highlightthickness=0, width=3, height=500, col='black')

# Cajas etapas
ubic_CjEtp = dict(x=0, y=0, relwidth=1, relheight=1)
ubic_BtNavEtp_adel = dict(anchor=tk.S)
ubic_BtNavEtp_atrs = dict(anchor=tk.N)
formato_BtsNavEtapa = dict(width=50, height=15)
ubic_CjCbzEtp = dict(x=0, y=0, relwidth=1, height=30)

# Cajas sub etapas
formato_CjSubEtp = dict(x=0, y=0, relwidth=1, relheight=1,
                        width=-formato_BtsNavEtapa['height'])
ubic_CjSubEtp = dict(x=0, y=ubic_CjCbzEtp['height'],
                     relwidth=1, relheight=1, height=-ubic_CjCbzEtp['height'])
ubic_BtNavSub_adel = dict(anchor=tk.E)
ubic_BtNavSub_atrs = dict(anchor=tk.W)
formato_BtsNavSub = dict(width=10, height=40)

formato_MenuOpciones = dict()
formato_etiq_bloq = dict(fg='#999999')
formato_etiq_norm = dict(fg='#ffffff')

ubic_CjMóbl = dict(x=0, y=0, anchor=tk.SW, relwidth=1, relheight=1)