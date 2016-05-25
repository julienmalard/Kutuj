import os
import csv
import datetime as ft

# Un sencillo corrector automático para unos errores en las bases de datos INSIVUMEH


def corregir(documento, col_fecha):
    final = []
    with open(documento) as d:
        l = csv.reader(d)

        cols = next(l)

        n_col = cols.index(col_fecha)

        final.append(cols)

        for f in l:
            try:
                ft.datetime.strptime(f[n_col], '%d/%m/%Y')
                final.append(f)
            except ValueError:
                pass

    doc_corr = os.path.splitext(documento)[0] + '_corr' + '.csv'
    with open(doc_corr, 'w', newline='') as d:
        e = csv.writer(d)

        for f in final:
            e.writerow(f)

corregir('C:/Users/iarna/PycharmProjects/Kutuj/Datos_ejemplos/COBAN 1970 - 2011.csv', 'fecha')
