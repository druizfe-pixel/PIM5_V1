"""
=========================================================
MODEL TRAINING AND EVALUATION
Proyecto Integrador M5
=========================================================
"""

# =====================================================
# LIBRERÍAS
# =====================================================

import os
import warnings
import joblib

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    RocCurveDisplay
)

from ft_engineering import preprocesar_datos

warnings.filterwarnings("ignore")

# =====================================================
# XGBOOST
# =====================================================

try:

    from xgboost import XGBClassifier

    XGBOOST_AVAILABLE = True

except ImportError:

    XGBOOST_AVAILABLE = False

    print("XGBoost no está instalado.")


# =====================================================
# CONFIGURACIÓN
# =====================================================

RANDOM_STATE = 42

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS_FOLDER = os.path.join(BASE_DIR, "models")
REPORTS_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(MODELS_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)


# =====================================================
# CARGA DE DATOS
# =====================================================

def cargar_datos_preprocesados():

    print("=" * 60)
    print("CARGANDO DATOS")
    print("=" * 60)

    (
        preprocessor,
        X_train,
        X_test,
        X_train_preprocessed,
        X_test_preprocessed,
        y_train,
        y_test
    ) = preprocesar_datos()

    return (
        preprocessor,
        X_train,
        X_test,
        X_train_preprocessed,
        X_test_preprocessed,
        y_train,
        y_test
    )

# =====================================================
# MODELOS
# =====================================================

def build_models():

    modelos = {

        "Logistic Regression": LogisticRegression(
            random_state=RANDOM_STATE,
            max_iter=1000,
            class_weight="balanced"
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=5,
            random_state=RANDOM_STATE,
            n_jobs=-1
        )

    }

    if XGBOOST_AVAILABLE:

        modelos["XGBoost"] = XGBClassifier(
            random_state=RANDOM_STATE,
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss"
        )

    return modelos


# =====================================================
# ENTRENAMIENTO
# =====================================================

def train_model(modelo, X_train, y_train):

    print(f"\nEntrenando {modelo.__class__.__name__}...")

    modelo.fit(X_train, y_train)

    return modelo

# =====================================================
# EVALUACIÓN
# =====================================================

def evaluate_model(modelo, X_test, y_test):
    """
    Evalúa un modelo de clasificación.

    Parameters
    ----------
    modelo : estimator
    X_test : array
    y_test : array

    Returns
    -------
    dict
    """

    y_pred = modelo.predict(X_test)

    y_prob = modelo.predict_proba(X_test)[:, 1]

    resultados = {

        "Accuracy": accuracy_score(y_test, y_pred),

        "Precision": precision_score(y_test, y_pred),

        "Recall": recall_score(y_test, y_pred),

        "F1": f1_score(y_test, y_pred),

        "ROC_AUC": roc_auc_score(y_test, y_prob)

    }

    print("\nClassification Report")
    print("-" * 60)
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)

    ConfusionMatrixDisplay(cm).plot()

    plt.show()

    return resultados, y_pred, y_prob


# =====================================================
# ENTRENAR TODOS LOS MODELOS
# =====================================================

def train_all_models(
    modelos,
    preprocessor,
    X_train,
    y_train,
    X_test,
    y_test
):

    resultados = {}

    for nombre, modelo in modelos.items():

        print("=" * 60)
        print(f"Modelo: {nombre}")
        print("=" * 60)

        # Entrenar modelo
        modelo_entrenado = train_model(
            modelo,
            X_train,
            y_train
        )

        # =====================================================
        # IMPORTANCIA DE VARIABLES (SOLO RANDOM FOREST)
        # =====================================================
        if nombre == "Random Forest":

            # Variables numéricas
            num_features = list(preprocessor.transformers_[0][2])

            # Variables categóricas codificadas
            cat_features = list(
                preprocessor
                .named_transformers_["cat"]
                .named_steps["onehot"]
                .get_feature_names_out(
                    preprocessor.transformers_[1][2]
                )
            )

            # Unir nombres de variables
            feature_names = num_features + cat_features

            # Crear DataFrame de importancia
            importancia = pd.DataFrame({
                "Variable": feature_names,
                "Importancia": modelo_entrenado.feature_importances_
            })

            importancia = importancia.sort_values(
                by="Importancia",
                ascending=False
            )

            print("\n" + "=" * 60)
            print("TOP 20 VARIABLES MÁS IMPORTANTES")
            print("=" * 60)
            print(importancia.head(20))

            # Guardar reporte
            importancia.to_csv(
                os.path.join(
                    REPORTS_FOLDER,
                    "feature_importance_random_forest.csv"
                ),
                index=False
            )

        # =====================================================
        # Evaluación
        # =====================================================
        metricas, y_pred, y_prob = evaluate_model(
            modelo_entrenado,
            X_test,
            y_test
        )

        resultados[nombre] = {
            "modelo": modelo_entrenado,
            "metricas": metricas,
            "y_pred": y_pred,
            "y_prob": y_prob
        }

    return resultados


# =====================================================
# COMPARACIÓN
# =====================================================

def compare_models(resultados):

    filas = []

    for nombre, datos in resultados.items():

        fila = {"Modelo": nombre}

        fila.update(datos["metricas"])

        filas.append(fila)

    df_resultados = pd.DataFrame(filas)

    df_resultados = df_resultados.sort_values(
        by="ROC_AUC",
        ascending=False
    )

    print("\nComparación de modelos")
    print(df_resultados)

    return df_resultados



# =====================================================
# GUARDAR MEJOR MODELO
# =====================================================

def save_best_model(resultados, tabla_resultados, preprocessor):
    """
    Guarda el mejor modelo y el preprocesador.
    """

    mejor_modelo_nombre = tabla_resultados.iloc[0]["Modelo"]

    mejor_modelo = resultados[mejor_modelo_nombre]["modelo"]

    modelo_path = os.path.join(
        MODELS_FOLDER,
        "modelo.pkl"
    )

    preprocessor_path = os.path.join(
        MODELS_FOLDER,
        "preprocessor.pkl"
    )

    joblib.dump(mejor_modelo, modelo_path)
    joblib.dump(preprocessor, preprocessor_path)

    joblib.dump(
        mejor_modelo,
        os.path.join(
            MODELS_FOLDER,
            f"{mejor_modelo_nombre}.pkl"
        )
    )

    print("\n" + "=" * 60)
    print("MODELO GUARDADO")
    print("=" * 60)

    print(f"Mejor modelo : {mejor_modelo_nombre}")
    print(f"Modelo       : {modelo_path}")
    print(f"Preprocessor : {preprocessor_path}")

    return mejor_modelo_nombre


# =====================================================
# EXPORTAR RESULTADOS
# =====================================================

def export_results(tabla_resultados):

    ruta = os.path.join(
        REPORTS_FOLDER,
        "comparacion_modelos.csv"
    )

    tabla_resultados.to_csv(
        ruta,
        index=False
    )

    tabla_resultados.to_excel(
        os.path.join(
            REPORTS_FOLDER,
            "comparacion_modelos.xlsx"
        ),
        index=False
    )

    print(f"\nReporte generado: {ruta}")


# =====================================================
# FUNCIÓN PRINCIPAL
# =====================================================

def main():

    print("=" * 70)
    print("ENTRENAMIENTO Y EVALUACIÓN DE MODELOS")
    print("=" * 70)

    (
        preprocessor,
        X_train,
        X_test,
        X_train_preprocessed,
        X_test_preprocessed,
        y_train,
        y_test
    ) = cargar_datos_preprocesados()

    modelos = build_models()

    resultados = train_all_models(
        modelos,
        preprocessor,
        X_train_preprocessed,
        y_train,
        X_test_preprocessed,
        y_test
    )

    tabla_resultados = compare_models(resultados)

    print("\nResumen de resultados:")
    print(tabla_resultados)

    export_results(tabla_resultados)

    save_best_model(
        resultados,
        tabla_resultados,
        preprocessor
    )

if __name__ == "__main__":
    main()