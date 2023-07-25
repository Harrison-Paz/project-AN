import pandas as pd

df = pd.read_csv("dataset.csv")

leyenda_reemplazo = {}

for column in df.columns:
    if df[column].dtype == "object":
        unique_values = df[column].unique()
        leyenda = {value: index for index, value in enumerate(unique_values)}
        df[column] = df[column].map(leyenda)
        leyenda_reemplazo[column] = leyenda

for column, leyenda in leyenda_reemplazo.items():
    print(f"Leyenda para la columna '{column}':")
    for value, index in leyenda.items():
        print(f"{value} -> {index}")
    print()

df.to_csv("dataset-convertido.csv", index=False)
