from django.conf import settings
import pandas as pd
import os

def convertir(dataset):
    df = pd.read_csv(dataset)

    leyenda_reemplazo = {}

    text = ""

    for column in df.columns:
        if df[column].dtype == "object":
            unique_values = df[column].unique()
            leyenda = {value: index for index, value in enumerate(unique_values)}
            df[column] = df[column].map(leyenda)
            leyenda_reemplazo[column] = leyenda

    for column, leyenda in leyenda_reemplazo.items():
        text += f"mapeo_{column} = {{\n"
        for value, index in leyenda.items():
            text += f"  '{value}': {index},\n"
        text += f"}}\n\n"

    df.to_csv(os.path.join(settings.STATIC_DIR, 'dataset', 'dataset-conv.csv'), index=False)

    with open(os.path.join(settings.STATIC_DIR, 'dataset', 'leyenda.py'), 'w') as f:
        f.writelines(text)

def retiro(dataset):
    df = pd.read_csv(dataset)
    df = df[df['EDAD'] < 16]
    df['RETIRO'] = '0'

    def verificarDesercion(row):
        siguiente_anio = row['ANIO'] + 1
        existe_siguiente_anio = df[(df['ID'] == row['ID']) & (df['ANIO'] == siguiente_anio)].shape[0] > 0
        if not existe_siguiente_anio:
            return '1'
        return '0'
    
    df['RETIRO'] = df.apply(verificarDesercion, axis=1)
    df = df[df['ANIO'] < 2019]
    
    df.to_csv(os.path.join(settings.STATIC_DIR, 'dataset', 'dataset-ret.csv'), index=False)

    return os.path.join(settings.STATIC_DIR, 'dataset', 'dataset-ret.csv')