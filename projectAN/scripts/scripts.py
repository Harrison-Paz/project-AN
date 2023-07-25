import pandas as pd

from ..static.dataset.leyenda import mapeo_NUCLEO_FAMILIAR, mapeo_SEXO, mapeo_ZONA, mapeo_TIPO, mapeo_SEGURO, mapeo_NIVEL

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

mapeo_CONDUCTA_INAPROPIADA = {
  'BAJA': 0,
  'MEDIA': 1,
  'ALTA': 2,
}

mapeo_NOTA = {
    'D': 0,
    'C': 1,
    'B': 2,
    'A': 3,
}

mapeo_RETIRO = {
    'NO': 0,
    'SI': 1,
}

def categorizar_conducta(valor):
    if valor <= 5:
        return 'BAJA'
    elif valor < 10:
        return 'MEDIA'
    else:
        return 'ALTA'

def categorizar_nota(valor):
    valor = float(valor)

    if valor <= 5:
        return 'D'
    elif valor <= 11:
        return 'C'
    elif valor <= 16:
        return 'B'
    else:
        return 'A'

# def get_correlacion(dataset, columna):
#     data_frame = pd.read_csv(dataset)
#     columnas_interes = ['NUCLEO_FAMILIAR', 'EDAD', 'SEXO', 'ZONA', 'NOTA', 'TIPO', 'SEGURO', 'RETRASOS', 'NIVEL', 'CONDUCTA_INAPROPIADA']
#     datos_analisis = data_frame[columnas_interes]

#     matriz_correlacion = datos_analisis.corr()

#     correlaciones_conducta = matriz_correlacion[columna].sort_values(ascending=False)
#     print(correlaciones_conducta)
#     return correlaciones_conducta

def entrenar_regresor(dataset, columnas, target):
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

    df = df.dropna()

    df["NUCLEO_FAMILIAR"] = df["NUCLEO_FAMILIAR"].replace(mapeo_NUCLEO_FAMILIAR)
    df["SEXO"] = df["SEXO"].replace(mapeo_SEXO)
    df["ZONA"] = df["ZONA"].replace(mapeo_ZONA)
    df["TIPO"] = df["TIPO"].replace(mapeo_TIPO)
    df["SEGURO"] = df["SEGURO"].replace(mapeo_SEGURO)
    df["NIVEL"] = df["NIVEL"].replace(mapeo_NIVEL)

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=23)

    regresor = RandomForestRegressor()

    X_train = df_train[columnas]
    y_train = df_train[target]
    X_test = df_test[columnas]
    y_test = df_test[target]

    regresor.fit(X_train, y_train)

    predicciones = regresor.predict(X_test)

    mse = mean_squared_error(y_test, predicciones)

    resultados = pd.DataFrame({"Prediccion": predicciones, "Real": y_test})
    print(resultados)
    print("Error cuadrático medio:", mse)
    return regresor, mse

def entrenar_naives(dataset, columnas, target):
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

    resultados = pd.DataFrame({"Prediccion": predicciones, "Real": y_test})
    print(resultados)
    print("Precisión:", accuracy)
    return naive, accuracy

def entrenar_naives_ret(dataset, columnas, target):
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

    df = df.dropna()

    df["NUCLEO_FAMILIAR"] = df["NUCLEO_FAMILIAR"].replace(mapeo_NUCLEO_FAMILIAR)
    df["SEXO"] = df["SEXO"].replace(mapeo_SEXO)
    df["ZONA"] = df["ZONA"].replace(mapeo_ZONA)
    df["TIPO"] = df["TIPO"].replace(mapeo_TIPO)
    df["SEGURO"] = df["SEGURO"].replace(mapeo_SEGURO)
    df["NIVEL"] = df["NIVEL"].replace(mapeo_NIVEL)
    df["CONDUCTA_INAPROPIADA"] = df["CONDUCTA_INAPROPIADA"].replace(mapeo_CONDUCTA_INAPROPIADA)
    df["NOTA"] = df["NOTA"].replace(mapeo_NOTA)
    df["RETIRO"] = df["RETIRO"].replace(mapeo_RETIRO)

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=23)

    naive = GaussianNB()

    X_train = df_train[columnas]
    y_train = df_train[target]
    X_test = df_test[columnas]
    y_test = df_test[target]

    naive.fit(X_train, y_train)

    predicciones = naive.predict(X_test)

    accuracy = accuracy_score(y_test, predicciones)

    resultados = pd.DataFrame({"Prediccion": predicciones, "Real": y_test})
    print(resultados)
    print("Precisión:", accuracy)
    return naive, accuracy

def get_prob_comp(dataset):
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
    print(f'Exactitud del modelo: {accuracy:.2f}')

    importances = abs(model.coef_[0])

    importance_df = pd.DataFrame({'Columna': X.columns, 'Importancia': importances})
    importance_df = importance_df.sort_values(by='Importancia', ascending=False)

    importance_array = importance_df.to_dict(orient='records')

    return accuracy, importance_array

def get_prob_ret(dataset):
    data = pd.read_csv(dataset)

    X = data.drop(columns=['RETIRO'])
    y = data['RETIRO']

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Exactitud del modelo: {accuracy:.2f}')

    importances = abs(model.coef_[0])

    importance_df = pd.DataFrame({'Columna': X.columns, 'Importancia': importances})
    importance_df = importance_df.sort_values(by='Importancia', ascending=False)

    importance_array = importance_df.to_dict(orient='records')

    return accuracy, importance_array

def get_prob_rend(dataset):
    data = pd.read_csv(dataset)
    data['NOTA'] = data['NOTA'].apply(categorizar_nota)

    X = data.drop(columns=['NOTA'])
    y = data['NOTA']

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f'Exactitud del modelo: {accuracy:.2f}')

    importances = abs(model.coef_[0])

    importance_df = pd.DataFrame({'Columna': X.columns, 'Importancia': importances})
    importance_df = importance_df.sort_values(by='Importancia', ascending=False)

    importance_array = importance_df.to_dict(orient='records')

    return accuracy, importance_array



