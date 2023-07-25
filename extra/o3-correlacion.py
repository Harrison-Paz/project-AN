import pandas as pd

ruta_csv = 'dataset-convertido.csv'

data_frame = pd.read_csv(ruta_csv)

columnas_interes = ['NUCLEO_FAMILIAR', 'EDAD', 'SEXO', 'ZONA', 'NOTA', 'TIPO', 'SEGURO', 'RETRASOS', 'NIVEL', 'CONDUCTA_INAPROPIADA']
datos_analisis = data_frame[columnas_interes]

matriz_correlacion = datos_analisis.corr()

correlaciones_conducta = matriz_correlacion['NOTA'].sort_values(ascending=False)

print("Correlaciones con la columna 'NOTA':")
print(correlaciones_conducta)
