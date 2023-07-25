import pandas as pd

ruta_csv = 'dataset.csv'

data_frame = pd.read_csv(ruta_csv)

nombre_columna = "NIVEL"

if nombre_columna in data_frame.columns:
    valores_unicos = sorted(data_frame[nombre_columna].unique())

    print("Valores únicos en la columna '{}':".format(nombre_columna))
    for valor in valores_unicos:
        print(valor)
else:
    print("La columna '{}' no existe en el conjunto de datos.".format(nombre_columna))