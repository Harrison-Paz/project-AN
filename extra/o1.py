#Importamos la libreria 'pandas'
import pandas as pd

#Leemos nuestro archivo csv
df = pd.read_csv("dataset.csv")

#Eliminamos la columna ID porque no nos sirve para el análisis
df = df.drop(columns=["ID"])

#Mostramos los primeros 20 registros
print(df.head(20))

#Filtramos las columnas para que tengan valores validos
df = df[(df["ANIO"] > 2010) & (df["ANIO"] < 2023) & (df["ANIO"] % 1 == 0)]
df = df[df["NUCLEO_FAMILIAR"].isin(["MADRE", "AMBOS", "PADRE", "OTRO"])]
df = df[df["EDAD"] > 0]
df = df[df["SEXO"].isin(["MASCULINO", "FEMENINO"])]
df = df[(df["NOTA"] >= 0) & (df["NOTA"] <= 20)]
df = df[df["TIPO"].isin(["PENSION", "BECA COMPLETA", "CUARTO BECA", "MEDIA BECA"])]
df = df[df["SEGURO"].isin(["SI", "NO"])]
df = df[df["RETRASOS"] >= 0]
df = df[df["NIVEL"].isin(["INICIAL", "PRIMARIA", "SECUNDARIA"])]

#Eliminamos los valores nulos
df = df.dropna()

#Mostramos los primeros 20 resultados
print(df.head(20))

#Importamos LabelEncoder para convertir los valores de las columnas a valores numericos
from sklearn.preprocessing import LabelEncoder

#Convertimos los valores de las columnas a valores numericos
le = LabelEncoder()
df["NUCLEO_FAMILIAR"] = le.fit_transform(df["NUCLEO_FAMILIAR"])
df["SEXO"] = le.fit_transform(df["SEXO"])
df["ZONA"] = le.fit_transform(df["ZONA"])
df["TIPO"] = le.fit_transform(df["TIPO"])
df["SEGURO"] = le.fit_transform(df["SEGURO"])
df["NIVEL"] = le.fit_transform(df["NIVEL"])

#Mostramos los primeros 20 resultados
print(df.head(20))

#Importamos train_test_split para dividir nuestro dataset en datos de entrenamiento y datos de prueba
from sklearn.model_selection import train_test_split

#Dividimos nuestro dataset en datos de entrenamiento y datos de prueba
df_train, df_test = train_test_split(df, test_size=0.2, random_state=23)

train_count = df_train.shape[0]
test_count = df_test.shape[0]

print("Datos de entrenamiento:", train_count)
print("Datos de prueba:", test_count)

#Importamos GaussianNB para crear nuestro modelo y accuracy_score para calcular la precisión de nuestro modelo
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Crear un objeto de clasificador Naive Bayes
naive = GaussianNB()

#Definimos la columna objetivo
target = "CONDUCTA_INAPROPIADA"

#Definimos las columnas de entrenamiento
columnas = ["NOTA","ZONA"]

#Separar las características de entrenamiento y las columnas objetivo en los conjuntos de datos de entrenamiento y prueba
X_train = df_train[columnas]
y_train = df_train[target]
X_test = df_test[columnas]
y_test = df_test[target]

#Entrenar al clasificador Naive Bayes
naive.fit(X_train, y_train)

#Realizar las predicciones en el conjunto de prueba
predicciones = naive.predict(X_test)

#Calcular la precisión del clasificador Naive Bayes
accuracy = accuracy_score(y_test, predicciones)

#Mostrar las predicciones y la precisión
resultados = pd.DataFrame({"Prediccion": predicciones, "Real": y_test})
print(resultados)
print("Precisión:", accuracy)