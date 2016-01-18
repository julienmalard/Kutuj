import tkinter as tk


# Parámetros generales
col_fondo = 'white'  # El color de fondo del interfaz
col_1 = '#990000'
col_2 = '#ffbf00'
col_3 = '#ffd633'
col_4 = '#fffae5'
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
                       font=(fuente, 25, 'bold'), height=2, width=13)  # Formatos generales
formato_BtsInic_norm = dict(bg='#cc9900', fg='#000000', **formato_BtsInic)
formato_BtsInic_sel = dict(bg='#ffc34d')
ubic_BtsInic = dict(side='left', ipadx=5, ipady=5, padx=10, pady=10)

# Caja lenguas
ubic_CjLeng = dict(relx=0, y=0, relwidth=1, relheight=1)
ubic_BtRegrCent = dict(x=20, y=20)
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
formato_BtsNavEtapa = dict(width=270, height=35, bg=col_fondo, borderwidth=0, highlightthickness=0)
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
formato_BtsNavSub = dict(width=25, height=205, bg=col_fondo, borderwidth=0, highlightthickness=0)
formato_etiq_error = dict(bg='#ffffe5', fg='#ff0000', font=('arial', '12'), wraplength=350,
                          borderwidth=2, highlightcolor='#ff0000', padx=10, pady=10)

# Listas
formato_CjLstItemas = dict(highlightthickness=1, highlightbackground=col_2, bg=col_fondo)
formato_TlLstItemas = dict(bg=col_fondo)
ubic_TlLstItemas = dict(relx=0, rely=0, x=0, y=0, relwidth=1, relheight=1)
ubic_BaraDesp = dict(side="right", fill="y")
ubic_CjTl = dict(width=750-20, anchor=tk.NW)

formato_secciones_itemas = dict(height=10, pady=5, **formato_cajas)
ancho_cj_bts_itemas = 20
ubic_BtsItemas = dict(side='left')
formato_etiq_itemas = dict(fg=col_1, font={fuente, 10}, bg=col_fondo)
ubic_ColsItemas = dict(side='left')

# Controles
formato_EtiqCtrl = dict(bg=col_fondo, fg=col_3, font=(fuente, 20, 'bold'))
formato_EtiqCtrl_bloq = dict(fg='#999999')

formato_MnMn = dict(bg=col_fondo, relief='flat', bd=0, activebackground=col_4, activeforeground='#000000',
                    disabledforeground='#cccccc', font=(fuente, '13'))
formato_BtMn = dict(bg=col_fondo, highlightthickness=1, highlightbackground=col_3,
                    relief='flat', activebackground=col_4, font=(fuente, '13'),
                    width=15, anchor=tk.W)
formato_BtMn_bloq = dict(highlightbackground='#999999')

ubic_EtiqMenú = dict(side='left', padx=20)
ubic_Menú = dict(side='left')

ubic_EtiqIngrNúm = dict(side='left', padx=20)
ubic_IngrNúm = dict(side='left')

formato_Escl = dict()
ubic_Escl = dict(side='left')
ubic_CampoIngr = dict(side='left')
formato_CampoIngr = dict(bg=col_fondo, highlightthickness=1, highlightbackground=col_3,
                         relief='flat', highlightcolor=col_3, font=(fuente, '13'),
                         width=20)
formato_CampoIngr_error = dict(highlightthickness=2, highlightbackground='#ff0000', activebackground=col_4)

formato_BtGuardarGrupoCtrl_norm = dict(bg='#7dcf7d', fg='#ffffff', borderwidth=0, highlightthickness=0,
                                       activebackground='#45ba45', activeforeground='#ffffff',
                                       font=(fuente, 15, 'bold'), width=7)
formato_BtGuardarGrupoCtrl_sel = dict(bg='#45ba45', fg='#ffffff')
formato_BtGuardarsGrupoCtrl_bloq = dict(bg='#ecf8ec', fg='#ffffff')
formato_BtBorrarGrupoCtrl_norm = dict(bg='#ff8966', fg='#ffffff', borderwidth=0, highlightthickness=0,
                                      activebackground='#ff6233', activeforeground='#ffffff',
                                      font=(fuente, 15, 'bold'), width=7)
formato_BtBorrarGrupoCtrl_sel = dict(bg='#ff6233', fg='#ffffff')
formato_BtBorrarsGrupoCtrl_bloq = dict(bg='#ffebe5', fg='#ffffff')
ubic_BtsGrupoCtrl = dict(side='left', expand=True)
ubic_CjBtsGrupoCtrl = dict(side='top', fill=tk.X, expand=True)

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
ubic_CjsCol = dict(side='left', padx=10)

# Caja subetapa 1.2
ubic_CtrlsVarBD = dict(side='top', pady=10, anchor=tk.W)
ubic_CjLstVarsBD = dict(relx=0.5, rely=0, y=50, relwidth=0.8, relheight=0.25, anchor=tk.N)
ubic_CjBajoSE12 = dict(relx=0.5, rely=0.3, y=40, relheight=0.75, height=-25,
                       relwidth=1, width=-2*formato_BtsNavSub['width'],
                       anchor=tk.N)
ubic_CjCtrlsVarsBD = dict(relx=0.25, rely=0, x=10, y=10, relwidth=0.5, relheight=.8, width=-20, anchor=tk.N)
ubic_GráficoVarsBD = dict(relx=0.75, rely=0, x=10, y=10, relwidth=0.5, relheight=0.7, width=-20, anchor=tk.N)

ubic_escl_fecha_inic = dict(relx=0.75, rely=0.8, anchor=tk.N)
anchos_cols_listavarVB = [0.25, 0.25, 0.25, 0.25]
