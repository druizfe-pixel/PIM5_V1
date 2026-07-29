import os
import joblib
from src.cargar_datos import cargarDatos

import pandas as pd

from drift_metrics import (
    calculate_psi,
    psi_status,
    ks_test
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from visualizations import (
    psi_barplot,
    compare_histogram,
    compare_boxplot
)



def load_excel(path):

    df = pd.read_excel(path)

    return df

# ==========================================================
# RUTAS
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")
REPORTS_FOLDER = os.path.join(PROJECT_ROOT, "reports")
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data", "raw")


def load_model():

    print("=" * 60)
    print("CARGANDO MODELO")
    print("=" * 60)

    model_path = os.path.join(
        MODELS_FOLDER,
        "modelo.pkl"
    )

    preprocessor_path = os.path.join(
        MODELS_FOLDER,
        "preprocessor.pkl"
    )

    modelo = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)

    print("✓ Modelo cargado correctamente")
    print("✓ Preprocesador cargado correctamente")

    return modelo, preprocessor

def load_new_data():

    print("=" * 60)
    print("CARGANDO NUEVOS DATOS")
    print("=" * 60)

    df = cargarDatos()

    print(f"Registros : {df.shape[0]}")
    print(f"Columnas  : {df.shape[1]}")

    return df

def prepare_monitoring_data(df, preprocessor):
    """
    Prepara los datos para el monitoreo del modelo.
    """

    print("=" * 60)
    print("PREPARANDO DATOS")
    print("=" * 60)

    X = df.drop(columns=["Pago_atiempo"])
    y = df["Pago_atiempo"]

    X_preprocessed = preprocessor.transform(X)

    print(f"Variables de entrada : {X.shape[1]}")
    print(f"Registros            : {X.shape[0]}")
    print("✓ Datos transformados correctamente")

    return X_preprocessed, y


def predict_monitoring(modelo, X_monitor):

    print("=" * 60)
    print("REALIZANDO PREDICCIONES")
    print("=" * 60)

    y_pred = modelo.predict(X_monitor)

    if hasattr(modelo, "predict_proba"):
        y_prob = modelo.predict_proba(X_monitor)[:, 1]
    else:
        y_prob = None

    print(f"Predicciones realizadas: {len(y_pred)}")

    return y_pred, y_prob

def evaluate_monitoring(y_true, y_pred, y_prob):

    print("=" * 60)
    print("EVALUANDO MODELO")
    print("=" * 60)

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    if y_prob is not None:

        roc_auc = roc_auc_score(y_true, y_prob)

        print(f"ROC AUC  : {roc_auc:.4f}")

    else:

        roc_auc = None

    resultados = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC AUC": roc_auc
    }

    return resultados


def monitoring_drift(df_reference, df_monitor):

    print("=" * 60)
    print("ANÁLISIS DE DATA DRIFT")
    print("=" * 60)

    resultados = []

    columnas_numericas = df_reference.select_dtypes(
        include=["int64", "float64"]
    ).columns

    columnas_numericas = [
        c for c in columnas_numericas
        if c != "Pago_atiempo"
    ]

    for columna in columnas_numericas:

        psi = calculate_psi(
            df_reference[columna],
            df_monitor[columna]
        )

        ks, p = ks_test(
            df_reference[columna],
            df_monitor[columna]
        )

        resultados.append({

            "Variable": columna,

            "PSI": round(psi,4),

            "Estado PSI": psi_status(psi),

            "KS": round(ks,4),

            "p-value": round(p,4)

        })

    drift_df = pd.DataFrame(resultados)

    print(drift_df)

    return drift_df

def export_drift_report(drift_df):

    archivo = os.path.join(
        REPORTS_FOLDER,
        "drift_report.csv"
    )

    drift_df.to_csv(
        archivo,
        index=False
    )

    print("\nReporte generado correctamente")

    print(archivo)



def monitoring_summary(drift_df):

    print()

    print("=" * 60)
    print("RESUMEN DEL MONITOREO")
    print("=" * 60)

    print(f"Variables analizadas : {len(drift_df)}")

    print(f"Sin Drift       : {(drift_df['Estado PSI'] == 'Sin Drift').sum()}")
    print(f"Drift Moderado : {(drift_df['Estado PSI'] == 'Drift Moderado').sum()}")
    print(f"Drift Alto     : {(drift_df['Estado PSI'] == 'Drift Alto').sum()}")

    if (drift_df["PSI"] > 0.25).any():
        print("\n⚠ Se recomienda revisar y reentrenar el modelo.")
    else:
        print("\n✓ El modelo se mantiene estable.")


def main():

    print("=" * 70)
    print("MODEL MONITORING")
    print("=" * 70)

    modelo, preprocessor = load_model()

    df = load_new_data()

    X_monitor, y_monitor = prepare_monitoring_data(
        df,
        preprocessor
    )

    y_pred, y_prob = predict_monitoring(
        modelo,
        X_monitor
    )

    metricas = evaluate_monitoring(
        y_monitor,
        y_pred,
        y_prob
    )

    print("\n")

    print("="*70)
    print("CARGANDO DATASET DE REFERENCIA")
    print("="*70)

    df_reference = cargarDatos()

    print("="*70)
    print("CARGANDO DATASET DE MONITOREO")
    print("="*70)

    ruta_monitor = os.path.join(
        PROJECT_ROOT,
        "data",
        "raw",
        "Base_de_datos_con_Data_Drift_Simulado.xlsx"
    )

    df_monitor = load_excel(ruta_monitor)

    drift_df = monitoring_drift(
        df_reference,
        df_monitor
    )

    export_drift_report(drift_df)

    
    for variable in drift_df.sort_values(
                "PSI",
                ascending=False
            ).head(5)["Variable"]:
    
            compare_histogram(
    
                df_reference[variable],
    
                df_monitor[variable],
    
                variable,
    
                REPORTS_FOLDER
    
            )

    psi_barplot(
        drift_df,
        REPORTS_FOLDER
    )

    top5 = (
        drift_df[
            drift_df["Estado PSI"] != "Sin Drift"
        ]
        .sort_values("PSI", ascending=False)
        .head(5)
    )

    for variable in top5["Variable"]:

        if pd.api.types.is_numeric_dtype(df_reference[variable]):

            compare_histogram(
                df_reference[variable],
                df_monitor[variable],
                variable,
                REPORTS_FOLDER
            )

            compare_boxplot(
                df_reference[variable],
                df_monitor[variable],
                variable,
                REPORTS_FOLDER
            )

    
    monitoring_summary(drift_df)

    print("\nProceso finalizado correctamente.")




if __name__ == "__main__":
    main()