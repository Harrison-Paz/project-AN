import pandas as pd

# Lee los datos desde el archivo CSV
data = pd.read_csv("dataset.csv")

# Calcula el promedio de conductas inapropiadas por zona
promedio_por_zona = data.groupby('ZONA')['CONDUCTA_INAPROPIADA'].mean().reset_index()

# Renombra las columnas para que coincidan con los nombres "label" y "cantidad"
promedio_por_zona.rename(columns={'ZONA': 'label', 'CONDUCTA_INAPROPIADA': 'cantidad'}, inplace=True)

# Convierte el resultado en un arreglo
resultado_arreglo = promedio_por_zona.to_dict(orient='records')

print(resultado_arreglo)