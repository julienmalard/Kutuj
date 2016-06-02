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
                ft.datetime.strptime(f[n_col], '%Y/%m/%d')
                final.append(f)
            except ValueError:
                pass

    doc_corr = os.path.splitext(documento)[0] + '_corr' + '.csv'
    with open(doc_corr, 'w', newline='') as d:
        e = csv.writer(d)

        for f in final:
            e.writerow(f)


# El directorio dónde están los documentos
directorio = 'C:/Users/iarna/PycharmProjects/Kutuj/Datos_ejemplos/Clima Guatemala/Documentos originales'

# Los nombres de los documentos para corregir
nombres_docs = ['COBAN 1970 - 2011.csv',
                'FLORES AEROPUERTO 1970-2011.csv',
                'HUEHUETENANGO 1970-2011.csv',
                'INSIVUMEH 1926-2013.csv',
                'INSIVUMEH 1970-2011.csv',
                'LA FRAGUA 1970-2011.csv',
                'LA UNION 1970-2011.csv',
                'LABOR OVALLE 1970-2011.csv',
                'MONTUFAR 1970-2011.csv',
                'PANZOS 1970 - 2011.csv',
                'PASABIEN 1970-2011.csv',
                'PUERTO BARRIOS 1970-2011.csv',
                'RAFAEL LANDIVAR.csv',
                'RETALHULEU AEROPUERTO 1970-2011.csv',
                'SAN JOSE AEROPUERTO 1970-2011.csv',
                'TECUN UMAN FEGUA AYUTLA1970-2011.csv'
                ]

# Generar una lista de la ubicación de cada documento
docs = [os.path.join(directorio, x) for x in nombres_docs]

# Corregir todos los documentos
for doc in docs:
    corregir(doc, 'fecha')
