import tkinter as tk


# Parámetros generales
col_fondo = 'white'  # El color de fondo del interfaz
col_1 = '#990000'
col_2 = '#ffbf00'
col_3 = '#ffd633'
fuente = 'Comic Sans MS'
formato_cajas = dict(bg=col_fondo, borderwidth=0, highlightthickness=0)
formato_botones = dict(bd=0, borderwidth=0, highlightthickness=0)
formato_etiq = dict(bg=col_fondo)

# Ventana central
ancho_ventana = 1100
altura_ventana = 800

# Caja inicial
formato_CjInic = dict(bg=col_fondo)
ubic_CjInic = dict(x=0, y=0, relwidth=1, relheight=1)
formato_LogoInic = dict(borderwidth=0, highlightthickness=0)
ubic_LogoInic = dict(side='top', pady=(175, 50))
formato_BtsInic = dict(borderwidth=0, highlightthickness=0, activebackground='#ffc34d',
                       font=('arial', 20, 'bold'), height=3, width=13)  # Formatos generales
formato_BtsInic_norm = dict(bg='#cc9900', fg='#000000', **formato_BtsInic)
formato_BtsInic_sel = dict(bg='#ffc34d')
ubic_BtsInic = dict(side='left', ipadx=5, ipady=5, padx=10, pady=10)

# Caja lenguas
ubic_CjLeng = dict(relx=0, y=0, relwidth=1, relheight=1)
ubic_BtRegrCent = dict(x=10, y=10)
ubic_CbzLeng = dict(relx=0.5, y=20, anchor=tk.N)
formato_CbzLeng = dict(font=(fuente, 40, 'bold'), fg=col_1, **formato_etiq)

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

# Botones izquierda
ubic_CjIzq = dict(side='top', fill=tk.Y, expand=True, anchor=tk.W)
ubic_CjBtsIzq = dict(side='left', fill=tk.Y, expand=True)
formato_BtsNavIzq = dict(width=60, height=60)
ubic_BtNavIzq = dict(side='top', padx=10, pady=15, expand=True)
formato_LínIzq = dict(bd=0, highlightthickness=0, width=2, bg='black')
ubic_LínIzq = dict(side='right', pady=(0, 20), fill=tk.Y, expand=True)

# Caja Contenedora de cajas etapas
formato_CjContCjEtps = dict(**formato_cajas)
ubic_CjContCjEtps = dict(side='right', fill=tk.BOTH, expand=True, anchor=tk.NW)

# Cajas etapas
ubic_CjEtp = dict(relx=0, rely=0, relwidth=1, relheight=1)
ubic_BtNavEtp_adel = dict(rely=1, relx=0.5, anchor=tk.S)
ubic_BtNavEtp_atrs = dict(rely=0, relx=0.5, anchor=tk.N)
formato_BtsNavEtapa = dict(width=270, height=35, bg=col_fondo)
formato_EncbzCjEtp = dict(font=(fuente, 35, 'bold'), fg=col_1, **formato_etiq)
ubic_EncbzCjEtp = dict(relx=0, rely=0, x=20)

# Cajas sub etapas
ubic_CjSubEtp = dict(relx=0, rely=0, y=2*formato_BtsNavEtapa['height'],
                     relwidth=1, relheight=1, 
                     height=-3*formato_BtsNavEtapa['height'])
formato_EncbzCjSubEtp = dict(font=(fuente, 20, 'bold'), fg=col_2, **formato_etiq)
ubic_EncbzCjSubEtp = dict(relx=0, rely=0, x=30)

ubic_BtNavSub_adel = dict(relx=1, rely=0.5, anchor=tk.E)
ubic_BtNavSub_atrs = dict(relx=0, rely=0.5, anchor=tk.W)
formato_BtsNavSub = dict(width=25, height=205, bg=col_fondo)
formato_etiq_error = dict(bg='#ffffe5', fg='#ff0000', font=('arial', '12'), wraplength=350,
                          borderwidth=2, highlightcolor='#ff0000', padx=10, pady=10)

# Listas
formato_CjLstItemas = dict(bd=1, **formato_cajas)

# Controles
formato_MnMn = dict(bg=col_fondo, relief='flat', bd=0, activebackground='#fffae5', activeforeground='#000000',
                    disabledforeground='#cccccc', font=('arial', '12'))
formato_BtMn = dict(bg=col_fondo, highlightthickness=1, highlightbackground=col_3,
                    relief='flat', activebackground='#fffae5', font=('arial', '12'),
                    width=15, anchor=tk.W)
formato_BtMn_bloq = dict(highlightbackground='#999999')

ubic_EtiqMenú = dict(side='left', padx=20)
formato_EtiqMenú = dict(bg=col_fondo, fg=col_3, font=(fuente, 20, 'bold'))
ubic_Menú = dict(side='left')
formato_etiq_bloq = dict(fg='#999999')

formato_Escl = dict()
ubic_Escl = dict(side='left')
formato_Ingr = dict()
ubic_Ingr = dict(side='left')

#
ubic_CjMóbl = dict(x=0, y=0, anchor=tk.SW, relwidth=1, relheight=1)


# Caja subetapa 1.1
formato_BtsCarg = dict(borderwidth=0, highlightthickness=0, activebackground='#ffdb4d',
                       font=(fuente, 20, 'bold'), height=2, width=13,  wraplength=170)  # Formatos generales
formato_BtsCarg_norm = dict(bg='#ffe580', fg='#000000', **formato_BtsCarg)
formato_BtsCarg_sel = dict(bg='#ffdb4d')
ubic_BtsCarg = dict(side='left', ipadx=5, ipady=5, padx=40, pady=10)
ubic_CjBtsCarg = dict(relx=0.5, rely=0, y=70, anchor=tk.N)
ubic_EtiqErrCargarBD = dict()

ubic_CjFechaHora = dict(relx=0.5, rely=0.5, anchor=tk.N)
ubic_CjMnCol = dict(side='left', padx=20, anchor=tk.N)
ubic_MnCol = dict(side='top')
ubic_EtiqErrCol = dict(side='top')
ubic_CjsCol = dict(side='left', padx=20)
