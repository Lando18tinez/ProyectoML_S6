from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import joblib
import os

def entrenar_modelo():
    ruta = os.path.abspath("data/datos_procesados.xlsx")
    df = pd.read_excel(ruta)

    df['riesgo_alto'] = (df['riesgo_score'] >= 0.4).astype(int)
    columnas_excluir = ['riesgo_score', 'riesgo_alto']
    X = df.drop(columns=columnas_excluir)
    y = df['riesgo_alto']

    # Codificación de variables categóricas
    X = pd.get_dummies(X)

    # División entrenamiento/prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # GridSearchCV para ajustar hiperparámetros
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }

    grid = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid.fit(X_train, y_train)

    # Modelo final entrenado
    best_model = grid.best_estimator_

    # Evaluación
    y_pred = best_model.predict(X_test)
    reporte = classification_report(y_test, y_pred, output_dict=True)

    # Guardar modelo
    joblib.dump(best_model, os.path.abspath("modelos/modelo_entrenado.pkl"))

    return reporte
