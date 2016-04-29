from BD import BaseCentral

bd = BaseCentral(archivo='E:\Javad\Python-Julien\Kutuj\Datos_ejemplos\Concepción.csv')

bd.estab_col_fecha(col='Fecha')

bd.estab_col_hora(col='Hora')

bd.cargar_var('Rain', col_datos='Lluvia [Acu] [mm]')

print(bd.nombres_cols)

