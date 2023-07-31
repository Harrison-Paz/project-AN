import pandas as pd
from ..static.dataset.leyenda import mapeo_NUCLEO_FAMILIAR, mapeo_SEXO, mapeo_ZONA, mapeo_TIPO, mapeo_SEGURO, mapeo_NIVEL
from .utils.mapeo import mapeo_CONDUCTA_INAPROPIADA, mapeo_NOTA, mapeo_RETIRO
from .utils.mapeo import categorizar_conducta, categorizar_nota

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestRegressor


def entrenar_comportamiento(dataset, columnas):
    target = "CONDUCTA_INAPROPIADA"
    df = pd.read_csv(dataset)
    df = df.drop(columns=["ID"])

    df = df[(df["ANIO"] > 2010) & (df["ANIO"] < 2023) & (df["ANIO"] % 1 == 0)]
    df = df[df["NUCLEO_FAMILIAR"].isin(["MADRE", "AMBOS", "PADRE", "OTRO"])]
    df = df[df["EDAD"] > 0]
    df = df[df["SEXO"].isin(["MASCULINO", "FEMENINO"])]
    df = df[(df["NOTA"] >= 0) & (df["NOTA"] <= 20)]
    df = df[df["TIPO"].isin(["PENSION", "BECA COMPLETA", "CUARTO BECA", "MEDIA BECA"])]
    df = df[df["SEGURO"].isin(["SI", "NO"])]
    df = df[df["RETRASOS"] >= 0]
    df = df[df["NIVEL"].isin(["INICIAL", "PRIMARIA", "SECUNDARIA"])]

    df['CONDUCTA_INAPROPIADA'] = df['CONDUCTA_INAPROPIADA'].apply(categorizar_conducta)

    df = df.dropna()

    df["NUCLEO_FAMILIAR"] = df["NUCLEO_FAMILIAR"].replace(mapeo_NUCLEO_FAMILIAR)
    df["SEXO"] = df["SEXO"].replace(mapeo_SEXO)
    df["ZONA"] = df["ZONA"].replace(mapeo_ZONA)
    df["TIPO"] = df["TIPO"].replace(mapeo_TIPO)
    df["SEGURO"] = df["SEGURO"].replace(mapeo_SEGURO)
    df["NIVEL"] = df["NIVEL"].replace(mapeo_NIVEL)
    df["CONDUCTA_INAPROPIADA"] = df["CONDUCTA_INAPROPIADA"].replace(mapeo_CONDUCTA_INAPROPIADA)

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=23)

    naive = GaussianNB()

    X_train = df_train[columnas]
    y_train = df_train[target]
    X_test = df_test[columnas]
    y_test = df_test[target]

    naive.fit(X_train, y_train)

    predicciones = naive.predict(X_test)

    accuracy = accuracy_score(y_test, predicciones)

    return naive, accuracy

def relacion_comportamiento(dataset):
    data = pd.read_csv(dataset)
    data['CONDUCTA_INAPROPIADA'] = data['CONDUCTA_INAPROPIADA'].apply(categorizar_conducta)

    X = data.drop(columns=['CONDUCTA_INAPROPIADA'])
    y = data['CONDUCTA_INAPROPIADA']

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    importances = abs(model.coef_[0])

    importance_df = pd.DataFrame({'Columna': X.columns, 'Importancia': importances})
    importance_df = importance_df.sort_values(by='Importancia', ascending=False)

    importance_array = importance_df.to_dict(orient='records')

    return accuracy, importance_array