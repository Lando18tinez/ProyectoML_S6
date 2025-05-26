from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc

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

    graficar_matriz_roc(best_model, X_test, y_test)
    return reporte

def graficar_matriz_roc(modelo, X_test, y_test):
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc

    # Crear carpeta static/img desde la raíz del proyecto
    static_img_path = os.path.abspath(os.path.join("static", "img"))
    os.makedirs(static_img_path, exist_ok=True)

    matriz_path = os.path.join(static_img_path, "matriz_confusion.png")
    roc_path = os.path.join(static_img_path, "curva_roc.png")

    # MATRIZ DE CONFUSIÓN
    cm = confusion_matrix(y_test, modelo.predict(X_test))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title("Matriz de Confusión")
    plt.savefig(matriz_path)
    print(f"[✔] Matriz guardada en: {matriz_path} - ¿Existe?: {os.path.exists(matriz_path)}")
    plt.close()

    # CURVA ROC
    y_score = modelo.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Curva ROC")
    plt.legend()
    plt.savefig(roc_path)
    print(f"[✔] ROC guardada en: {roc_path} - ¿Existe?: {os.path.exists(roc_path)}")
    plt.close()