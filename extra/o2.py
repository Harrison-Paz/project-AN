import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Carga el dataset
data = pd.read_csv('dataset.csv')  # Reemplaza 'ruta_del_dataset.csv' con la ruta de tu archivo CSV

# División de datos en características (X) y variable objetivo (y)
X = data.drop(columns=['CONDUCTA_INAPROPIADA'])
y = data['CONDUCTA_INAPROPIADA']

# Codificación de variables categóricas (si es necesario)
X = pd.get_dummies(X)

# División de datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicialización del modelo de regresión logística
model = LogisticRegression()

# Entrenamiento del modelo
model.fit(X_train, y_train)

# Predicción en el conjunto de prueba
y_pred = model.predict(X_test)

# Exactitud del modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {accuracy:.2f}')

# Calcula la importancia de cada columna en el modelo
importances = abs(model.coef_[0])

# Crea un dataframe para visualizar las importancias
importance_df = pd.DataFrame({'Columna': X.columns, 'Importancia': importances})
importance_df = importance_df.sort_values(by='Importancia', ascending=False)

importance_array = importance_df.to_dict(orient='records')
print(importance_array)

items = [
        'NUCLEO_FAMILIAR',
        'EDAD',
        'SEXO',
        'ZONA',
        'CONDUCTA_INAPROPIADA',
        'TIPO',
        'SEGURO',
        'RETRASOS',
        'NIVEL',
        'NOTA'
    ]