import tkinter as tk


def imagen(nombre):
    archivo = archivos_imgs[nombre]
    img = tk.PhotoImage(file=archivo)
    
    return img

raíz_imgs = 'Imágenes\\'
archivos_imgs = {'LogoInic': '%sLogoInic.png' % raíz_imgs,

                 'BtRegrCent_norm': '%sBtRegrCent_norm.png' % raíz_imgs,
                 'BtRegrCent_sel': '%sBtRegrCent_sel.png' % raíz_imgs,

                 'BtLeng_norm': '%sBtLeng_norm.png' % raíz_imgs,
                 'BtLeng_sel': '%sBtLeng_sel.png' % raíz_imgs,
                 'BtNavIzq_1_norm': '%sBtNavIzq_1_norm.png' % raíz_imgs,
                 'BtNavIzq_1_bloq': '%sBtNavIzq_1_bloq.png' % raíz_imgs,
                 'BtNavIzq_1_sel': '%s' % raíz_imgs,
                 'BtNavIzq_2_norm': '%s' % raíz_imgs,
                 'BtNavIzq_2_bloq': '%s' % raíz_imgs,
                 'BtNavIzq_2_sel': '%s' % raíz_imgs,
                 'BtNavIzq_3_norm': '%s' % raíz_imgs,
                 'BtNavIzq_3_bloq': '%s' % raíz_imgs,
                 'BtNavIzq_3_sel': '%s' % raíz_imgs,
                 'BtNavIzq_4_norm': '%s' % raíz_imgs,
                 'BtNavIzq_4_bloq': '%s' % raíz_imgs,
                 'BtNavIzq_4_sel': '%s' % raíz_imgs,
                 'BtNavIzq_5_norm': '%s' % raíz_imgs,
                 'BtNavIzq_5_bloq': '%s' % raíz_imgs,
                 'BtNavIzq_5_sel': '%s' % raíz_imgs,

                 'BtNavEtp_adel_norm': '%sBtNavEtp_adel_norm.png' % raíz_imgs,
                 'BtNavEtp_adel_bloq': '%sBtNavEtp_adel_bloq.png' % raíz_imgs,
                 'BtNavEtp_adel_sel': '%sBtNavEtp_adel_sel.png' % raíz_imgs,
                 'BtNavEtp_atrs_norm': '%sBtNavEtp_atrs_norm.png' % raíz_imgs,
                 'BtNavEtp_atrs_bloq': '%sBtNavEtp_atrs_bloq.png' % raíz_imgs,
                 'BtNavEtp_atrs_sel': '%sBtNavEtp_atrs_sel.png' % raíz_imgs,

                 'BtNavSub_adel_norm': '%sBtNavSub_adel_norm.png' % raíz_imgs,
                 'BtNavSub_adel_bloq': '%sBtNavSub_adel_bloq.png' % raíz_imgs,
                 'BtNavSub_adel_sel': '%sBtNavSub_adel_sel.png' % raíz_imgs,
                 'BtNavSub_atrs_norm': '%sBtNavSub_atrs_norm.png' % raíz_imgs,
                 'BtNavSub_atrs_bloq': '%sBtNavSub_atrs_bloq.png' % raíz_imgs,
                 'BtNavSub_atrs_sel': '%sBtNavSub_atrs_sel.png' % raíz_imgs,

                 'FlchAvnz_norm': '%sFlchAvnz_norm.png' % raíz_imgs,
                 'FlchSenc_norm': '%sFlchSenc_norm.png' % raíz_imgs,
                 'FlchAvnz_sel': '%sFlchAvnz_sel.png' % raíz_imgs,
                 'FlchSenc_sel': '%sFlchSenc_sel.png' % raíz_imgs

                 }
