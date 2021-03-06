import tkinter as tk
import os
import json


# Una función para modificar los formatos según la dirección del texto de la lengua
direc = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Trads')
with open(direc, encoding='utf8') as d:
    dic = json.load(d)
leng = dic['Actual']
IzqaDerech = dic['Lenguas'][leng]['IzqaDerech']


def gen_formato(formato):
    if IzqaDerech:
        return formato
    else:
        invers = [('e','w'), ('ne','nw'), ('se','sw'), ('right','left')]
        for ll, v in formato.items():
            if ll == 'x':
                formato[ll] = -v
                break
            if ll == 'relx':
                formato[ll] = (1 - v)
                break
            for inver in invers:
                if v == inver[0]:
                    formato[ll] = inver[1]
                    break
                elif v == inver[1]:
                    formato[ll] = inver[0]
                    break

        return formato


# Parámetros generales
col_fondo = 'white'  # El color de fondo del interfaz
col_1 = '#990000'
col_2 = '#cc3300'
col_3 = '#ffd633'
col_4 = '#fffae5'
col_5 = '#ffbf00'
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

ubic_CjCentLeng = dict(relx=0.5, rely=0, x=0, y=100, relheight=1, height=-150, relwidth=1, anchor=tk.N)
formato_LínVert = dict(bd=0, highlightthickness=0, bg=col_5)
ubic_LínVert1 = dict(relx=1/3, rely=0.05, y=20, width=1, relheight=1, anchor=tk.N)
ubic_LínVert2 = dict(relx=2/3, rely=0.05, y=20, width=1, relheight=1, anchor=tk.N)

ubic_CjIzqLeng = dict(relx=(1/3)/2, rely=0.05, y=20, relwidth=1/3, width=-10, relheight=1, anchor=tk.N)
ubic_CjMedLeng = dict(relx=1/3 + (1/3)/2, rely=0.05, y=20, relwidth=1/3, width=-10, relheight=1, anchor=tk.N)
ubic_CjDerchLeng = dict(relx=2/3 + (1/3)/2, rely=0.05, y=20, relwidth=1/3, width=-10, relheight=1, anchor=tk.N)

formato_EtiqLengCentro = dict(font=(fuente, 30, 'bold'), fg=col_5, **formato_etiq)
formato_EtiqLengLados = dict(font=(fuente, 20, 'bold'), fg=col_3, **formato_etiq)
ubic_EtiqCbzColsLeng = dict(relx=0.5, rely=0, y=50, anchor=tk.S)

formato_CjLstLengCentro = dict(highlightthickness=1, highlightbackground=col_5, bg=col_fondo)
formato_CjLstLengLados = dict(highlightthickness=1, highlightbackground=col_3, bg=col_fondo)
ubic_LstsLeng = dict(relx=0.5, rely=0, y=75, width=300, relheight=1, height=-150, anchor=tk.N)
ubic_LstsLeng_bajo = dict(relx=0.5, rely=0, y=75+20, width=300, relheight=1, height=-150-20, anchor=tk.N)
ubic_CjAñadirLeng = dict(relx=0, rely=0, x=20, y=60, height=20, anchor=tk.NW)
ubic_CjCamposAñLeng = dict(side='left', padx=2)
formato_cj_etiq_nombre_leng = dict(height=25, **formato_cajas)
formato_etiq_nombre_leng = dict(anchor=tk.W, **formato_etiq)
ubic_etiq_nombre_leng = dict(side='left')
ubic_IzqLstLeng = dict(side='left', padx=5)
ubic_DerLstLeng = dict(side='right', padx=5)
ubic_CjCentLstLeng = dict(side='left', padx=5)
colores_prog_leng = [(152, 103, 52), (255, 204, 0)]
dim_barra_prog_leng = (20, 50)
ubic_BtsAñadirLeng = dict(side='right', padx=2)
ubic_CentralItemaLstLeng = dict(side='left')

formato_CjEditLeng = dict(highlightthickness=1, highlightbackground=col_5, bg=col_fondo)
ubic_CjEditLeng = dict(relx=0.5, rely=0, y=10, relheight=1, width=600, height=-20, anchor=tk.N)
formato_EtiqCbzEditLeng = dict(font=(fuente, 40, 'bold'), fg=col_2, **formato_etiq)
ubic_CjCbzCjEditLeng = dict(side='top', pady=0, fill=tk.X)
ubic_CjNomEditLeng = dict(side='top', pady=0, fill=tk.X)
formato_EtiqLengBase = dict(font=(fuente, 20, 'bold'), fg=col_5, **formato_etiq)
formato_EtiqLengEdit = dict(font=(fuente, 20, 'bold'), fg=col_3, **formato_etiq)
ubic_EtiqLengs = dict(side='left', padx=5, pady=5, fill=tk.BOTH, expand=True)

formato_LínHor = dict(bd=0, highlightthickness=0, bg=col_3, height=1)
ubic_LínHorCjEditLeng = dict(side='top', fill=tk.X)
ubic_CjCentrCjEditLeng = dict(side='top', fill=tk.BOTH, expand=True)

formato_LstEditLeng = dict(highlightthickness=0, highlightbackground=col_3, bg=col_fondo)
ubic_LstEditLeng = dict(relx=0, rely=0, relheight=1, width=ubic_CjEditLeng['width'], anchor=tk.NW)

ubic_CjBtsCjEditLeng = dict(side='top', pady=20, fill=tk.X)
formato_CjLengTxOrig = dict(bg=col_fondo, highlightthickness=1, highlightbackground=col_5)
formato_EtiqLengTxOrig = dict(font=(fuente, '14', 'bold'), fg=col_5, bg=col_fondo,
                              width=20, wraplength=240, anchor=tk.W, justify=tk.LEFT)
formato_CampoTexto = dict(font=(fuente, '14', 'bold'), bg=col_fondo,
                          highlightthickness=1, highlightbackground=col_3, highlightcolor=col_5,
                          width=25, height=3, wrap=tk.WORD, relief=tk.FLAT)
ubic_CamposLeng = dict(side='left', padx=25, pady=25, expand=True)


formato_CajaAvisoReinic = dict(highlightthickness=3, highlightbackground=col_2, bg=col_fondo)
ubic_CjAvisoReinic = dict(relx=0.5, rely=0.5, width=350, height=200, anchor=tk.CENTER)
formato_EtiqLengReinic = dict(font=(fuente, 14), fg=col_2, wraplength=275, **formato_etiq)
ubic_etiq_aviso_inic_leng = dict(side='top', pady=(20, 0))
formato_BtAvisoInic = dict(borderwidth=0, highlightthickness=0, activebackground='#ffdb4d',
                           font=(fuente, 20, 'bold'), height=1, width=9,  wraplength=170)  # Formatos generales
formato_BtAvisoInic_norm = dict(bg='#ffe580', fg='#000000', **formato_BtAvisoInic)
formato_BtAvisoInic_sel = dict(bg='#ffdb4d')
ubic_bt_aviso_inic_leng = dict(side='bottom', pady=(0, 20))

formato_EtiqLengBorrar = dict(font=(fuente, 14), fg=col_2, wraplength=275, **formato_etiq)
ubic_etiq_aviso_borrar_leng = dict(side='top', pady=(20, 0))

ubic_bts_aviso_borrar_leng = dict(side='left', padx=25)
ubic_cj_bts_aviso_borrar_leng = dict(side='bottom', pady=(0, 20))

# Caja central
formato_CjCent = dict(bg=col_fondo)
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
formato_BtsNavIzq = dict(width=60, height=60, borderwidth=0, highlightthickness=0)
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
formato_CjLstItemas = dict(highlightthickness=1, highlightbackground=col_1, bg=col_fondo)
formato_TlLstItemas = dict(bg=col_fondo, highlightthickness=0)
formato_EtiqEncbzLst = dict(bg=col_4, fg=col_1, font=(fuente, 14, 'bold'), anchor=tk.W)
ubic_ColsEncbzLst = dict(y=0, relheight=1, anchor=tk.NW)
ubic_EncbzLstItemas = dict(x=0, y=0, relx=0, rely=0, height=25, relwidth=1, anchor=tk.NW)
ubic_TlLstItemas = dict(x=0, y=0, relx=0, rely=0, relheight=1, relwidth=1, anchor=tk.NW)
ubic_BaraDesp = dict(side="right", fill="y")
ubic_CjTl = dict(anchor=tk.NW)

formato_secciones_itemas = dict(height=20, **formato_cajas)
ubic_CjItemas = dict(side='top', fill=tk.X, expand=True)
ancho_cj_bts_itemas = 85
ubic_CjColsItemas = dict(side='left', fill=tk.BOTH, expand=True)
ubic_BtsItemas = dict(side='left', padx=5)
ubic_CjBtsItemas = dict(side='right')
ubic_EtiqItemas = dict(side='left')
fuente_etiq_itema_sel = (fuente, 14, 'bold')
fuente_etiq_itema_norm = (fuente, 14)
formato_texto_itemas = dict(font=(fuente, 14), fg='#000000', **formato_etiq)
ubic_ColsItemasEdit = dict(y=0, relheight=1, anchor=tk.NW)


# Controles
formato_EtiqCtrl = dict(bg=col_fondo, fg=col_3, font=(fuente, 20, 'bold'))
formato_EtiqCtrl_bloq = dict(fg='#999999')

formato_MnMn = dict(bg=col_fondo, relief='flat', bd=0, activebackground=col_4, activeforeground='#000000',
                    disabledforeground='#cccccc', font=(fuente, '13'))
formato_BtMn = dict(bg=col_fondo, highlightthickness=1, highlightbackground=col_3, highlightcolor=col_3,
                    relief='flat', activebackground=col_4, font=(fuente, '13'),
                    anchor=tk.W)
formato_BtMn_bloq = dict(highlightbackground='#999999')

ubic_EtiqMenú = dict(side='left', padx=20)
ubic_Menú = dict(side='left')

ubic_EtiqIngrNúm = dict(side='left', padx=20)
ubic_IngrNúm = dict(side='left')

formato_lín_escl = dict(fill=col_1, outline=col_1, disabledfill='#cccccc', disabledoutline='#cccccc')
ubic_Escl = dict(side='left')
ubic_CampoIngrEscl = dict(side='left', padx=10)
formato_EtiqNúmEscl = dict(font={fuente, 6}, fg=col_1, **formato_etiq)
ubic_EtiqNúmEscl = dict(side='left')
ubic_EtiqEscl = dict(side='left', padx=20)


formato_CampoIngr = dict(bg=col_fondo, highlightthickness=1, highlightbackground=col_3,
                         relief='flat', highlightcolor=col_3, font=(fuente, '13'))
formato_CampoIngr_error = dict(highlightthickness=2, highlightbackground='#ff0000')

formato_BtGuardar_norm = dict(bg='#6ac86a', fg='#ffffff', borderwidth=0, highlightthickness=0,
                              activebackground='#3ea73e', activeforeground='#ffffff',
                              font=(fuente, 15, 'bold'), width=10)
formato_BtGuardar_sel = dict(bg='#3ea73e', fg='#ffffff')
formato_BtGuardars_bloq = dict(bg='#ecf8ec', disabledforeground='#ffffff')
formato_BtBorrar_norm = dict(bg='#ff6233', fg='#ffffff', borderwidth=0, highlightthickness=0,
                             activebackground='#e63500', activeforeground='#ffffff',
                             font=(fuente, 15, 'bold'), width=10)
formato_BtBorrar_sel = dict(bg='#e63500', fg='#ffffff')
formato_BtBorrars_bloq = dict(bg='#ffebe5', disabledforeground='#ffffff')
ubic_BtsGrupo = dict(side='left', expand=True)
ubic_CjBtsGrupoCtrl = dict(side='top', padx=20, fill=tk.X, expand=True)

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
ubic_IngrValND = dict(side='top', anchor=tk.N)
ubic_MnCol = dict(side='top')
ubic_EtiqErrCol = dict(side='top')
ubic_CjsCol = dict(side='left', padx=10)

# Caja subetapa 1.2
ubic_CtrlsVarBD = dict(side='top', pady=10, anchor=tk.W)
ubic_CjLstVarsBD = dict(relx=0.5, rely=0, y=50, width=0.8*ancho_ventana, height=150, anchor=tk.N)
ubic_CjBajoSE12 = dict(relx=0.5, rely=0.3, y=40, relheight=0.75, height=-25,
                       relwidth=1, width=-2*formato_BtsNavSub['width'],
                       anchor=tk.N)
ubic_CjCtrlsVarsBD = dict(relx=0.25, rely=0, x=10, y=10, relwidth=0.5, relheight=.8, width=-20, anchor=tk.N)
ubic_GráficoVarsBD = dict(relx=0.75, rely=0, x=10, y=10, relwidth=0.5, relheight=0.7, width=-20, anchor=tk.N)

ubic_escl_fecha_inic = dict(relx=0.75, rely=0.75, anchor=tk.N)
anchos_cols_listavarVB = [0.25, 0.25, 0.25, 0.25]

colores_gráficos = [(156, 106, 73), (115, 199, 31)]

# Caja subetapa 2.1
ubic_CjBajoSE21 = dict(relx=0.5, rely=0, y=50,
                       relheight=1, height=-100,
                       relwidth=1, width=-2*formato_BtsNavSub['width'],
                       anchor=tk.N)

ubic_CtrlsVarY = dict(side='top', padx=10, pady=2, anchor=tk.W)

ubic_CtrlsFltrValY = dict(side='left', padx=0, anchor=tk.W, expand=True)

ubic_cj_fltr_tmpY = dict(side='top', pady=2, padx=10, anchor=tk.W)
ubic_CtrlsFltrTmpY = dict(side='left', padx=5, anchor=tk.W)


ubic_CjCtrlsVarsY = dict(relx=0.15, rely=0.5, x=100, y=10, relwidth=0.5, relheight=.95, height=-150,
                         width=-20, anchor=tk.CENTER)

ubic_GráficoVarsY = dict(relx=0.75, rely=0.5, relwidth=0.5, relheight=.70, width=-60, anchor=tk.CENTER)


# Caja subetapa 2.2
ubic_CjLstVarsX = dict(relx=0.5, rely=0, y=50, width=0.8*ancho_ventana, height=100, anchor=tk.N)
anchos_cols_listavarX = [0.20, 0.20, 0.35, 0.25]

ubic_CjBajoSE22 = dict(relx=0.5, rely=0, y=ubic_CjLstVarsX['y'] + ubic_CjLstVarsX['height'],
                       relheight=1, height=-(ubic_CjLstVarsX['y']+ubic_CjLstVarsX['height']),
                       relwidth=1, width=-2*formato_BtsNavSub['width'],
                       anchor=tk.N)

ubic_CtrlsVarX = dict(side='top', padx=10, pady=2, anchor=tk.W)

ubic_CtrlsFltrValX = dict(side='left', padx=0, anchor=tk.W)

ubic_cj_fltr_tmpX = dict(side='top', pady=2, padx=10, anchor=tk.W)
ubic_CtrlsFltrTmpX = dict(side='left', padx=5, anchor=tk.W)


ubic_CjCtrlsVarsX = dict(relx=0.25, rely=0, x=10, y=10, relwidth=0.5, relheight=.95, width=-20, anchor=tk.N)

ubic_GráficoVarsX = dict(relx=0.75, rely=0, x=10, y=10, relwidth=0.5, relheight=.95, width=-20, anchor=tk.N)


# Caja subetapa 3.1
formato_BtCalib = dict(borderwidth=0, highlightthickness=0, activebackground='#ffdb4d',
                       font=(fuente, 20, 'bold'), height=2, width=13,  wraplength=170)  # Formatos generales
formato_BtCalib_norm = dict(bg='#ffe580', fg='#000000', **formato_BtCalib)
formato_BtCalib_sel = dict(bg='#ffdb4d')

ubic_BtCalib = dict(relx=0.5, rely=0.5, anchor=tk.CENTER)
