import tkinter as tk


# Parámetros generales
col_fondo = 'white'  # El color de fondo del interfaz
formato_cajas = dict(bg=col_fondo, borderwidth=0, highlightthickness=0)
formato_botones = dict(bd=0, borderwidth=0, highlightthickness=0)

# Ventana central
ancho_ventana = 900
altura_ventana = 700

# Caja inicial
formato_CjInic = dict(bg=col_fondo)
ubic_CjInic = dict(x=0, y=0, relwidth=1, relheight=1)
formato_LogoInic = dict(borderwidth=0, highlightthickness=0)
ubic_LogoInic = dict(side='top', pady=(125, 15))
formato_BtsInic = dict(borderwidth=0, highlightthickness=0,
                       font=('arial', 20, 'bold'), height=3, width=13)  # Formatos generales
formato_BtsInic_norm = dict(bg='#cc9900', fg='#000000', **formato_BtsInic)
formato_BtsInic_sel = dict(bg='#ffc34d')
ubic_BtsInic = dict(side='left', ipadx=5, ipady=5, padx=10, pady=10)

# Caja lenguas
ubic_CjLeng = dict(relx=0, y=0, relwidth=1, relheight=1)
ubic_BtRegrCent = dict(x=10, y=10)

# Caja central
formato_CjCent = dict(bg='green')
ubic_CjCent = dict(x=0, y=0, relwidth=1, relheight=1)

# Caja cabeza
formato_CjCabeza = dict(height=110, **formato_cajas)
ubic_CjCabeza = dict(side='top', fill=tk.X, anchor=tk.N)
formato_LogoCabz = dict(borderwidth=0, highlightthickness=0, height=65)
ubic_LogoCabz = dict(relx=0.5, rely=0.5, anchor=tk.CENTER)
formato_BtLeng = dict(height=40, width=40, **formato_botones)
ubic_BtLeng = dict(relx=1, rely=0.5, x=-20, anchor=tk.E)

# Caja Contenedora de cajas etapas
formato_CjContCjEtps = dict(**formato_cajas)
ubic_CjContCjEtps = dict(side='right', fill=tk.BOTH, expand=True, anchor=tk.NW)

# Botones izquierda
ubic_CjIzq = dict(side='top', fill=tk.Y, expand=True, anchor=tk.W)
ubic_BtNavIzq = dict(side='top', padx=10, pady=15)
formato_BtsNavIzq = dict(width=60, height=60)
ubic_CjBtsIzq = dict(side='left')
ubic_LínIzq = dict(side='right')
formato_LínIzq = dict(bd=0, highlightthickness=0, width=2, height=500, bg='black')

# Cajas etapas
ubic_CjEtp = dict(relx=0, rely=0, relwidth=1, relheight=1)
ubic_BtNavEtp_adel = dict(rely=1, relx=0.5, anchor=tk.S)
ubic_BtNavEtp_atrs = dict(rely=0, relx=0.5, anchor=tk.N)
formato_BtsNavEtapa = dict(width=270, height=35)
ubic_CjCbzEtp = dict(x=0, y=0, relwidth=1, height=30)
formato_EncbzCjEtp = dict(font=('arial', 40, 'bold'))
ubic_EmcbzCjEtp = dict(x=formato_BtsNavEtapa['height'], y=0)

# Cajas sub etapas
formato_CjSubEtp = dict(x=0, y=0, relwidth=1, relheight=1,
                        width=-formato_BtsNavEtapa['height'])
ubic_CjSubEtp = dict(x=0, y=ubic_CjCbzEtp['height'],
                     relwidth=1, relheight=1, height=-ubic_CjCbzEtp['height'])
ubic_BtNavSub_adel = dict(relx=1, rely=0.5, anchor=tk.E)
ubic_BtNavSub_atrs = dict(relx=0, rely=0.5, anchor=tk.W)
formato_BtsNavSub = dict(width=10, height=40)

formato_MenuOpciones = dict()
formato_etiq_bloq = dict(fg='#999999')
formato_etiq_norm = dict(fg='#ffffff')

# Listas


# Controles
formato_Escl = dict()
ubic_Escl = dict(side='left')
formato_Ingr = dict()
ubic_Ingr = dict(side='left')

#
ubic_CjMóbl = dict(x=0, y=0, anchor=tk.SW, relwidth=1, relheight=1)
