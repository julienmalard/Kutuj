import tkinter as tk


def imagen(nombre):
    archivo = archivos_imgs[nombre]
    img = tk.PhotoImage(file=archivo)
    
    return img

raíz_imgs = 'Interfaz\\Gráficos\\'
archivos_imgs = {'BtNavIzq_norm_1': '%sBtNavIzq_norm_1.png' % raíz_imgs,
                 'BtNavIzq_bloq_1': '%sBtNavIzq_bloq_1.png' % raíz_imgs,
                 'BtNavIzq_sel_1': '%s' % raíz_imgs,
                 'BtNavIzq_norm_2': '%s' % raíz_imgs,
                 'BtNavIzq_bloq_2': '%s' % raíz_imgs,
                 'BtNavIzq_sel_2': '%s' % raíz_imgs,
                 'BtNavIzq_norm_3': '%s' % raíz_imgs,
                 'BtNavIzq_bloq_3': '%s' % raíz_imgs,
                 'BtNavIzq_sel_3': '%s' % raíz_imgs,
                 'BtNavIzq_norm_4': '%s' % raíz_imgs,
                 'BtNavIzq_bloq_4': '%s' % raíz_imgs,
                 'BtNavIzq_sel_4': '%s' % raíz_imgs,
                 'BtNavIzq_norm_5': '%s' % raíz_imgs,
                 'BtNavIzq_bloq_5': '%s' % raíz_imgs,
                 'BtNavIzq_sel_5': '%s' % raíz_imgs,
                 
                 'BtNavSub_adel_norm': '%s' % raíz_imgs,
                 'BtNavSub_adel_bloq': '%s' % raíz_imgs,
                 'BtNavSub_adel_sel': '%s' % raíz_imgs,
                 'BtNavSub_atrs_norm': '%s' % raíz_imgs,
                 'BtNavSub_atrs_bloq': '%s' % raíz_imgs,
                 'BtNavSub_atrs_sel': '%s' % raíz_imgs,
                 
                 'BtNavEtp_adel_norm': '%s' % raíz_imgs,
                 'BtNavEtp_adel_bloq': '%s' % raíz_imgs,
                 'BtNavEtp_adel_sel': '%s' % raíz_imgs,
                 'BtNavEtp_atrs_norm': '%s' % raíz_imgs,
                 'BtNavEtp_atrs_bloq': '%s' % raíz_imgs,
                 'BtNavEtp_atrs_sel': '%s' % raíz_imgs
                 }
