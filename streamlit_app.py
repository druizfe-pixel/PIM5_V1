import os
import pandas as pd
import streamlit as st

# ------------------------------------------------
# Configuración
# ------------------------------------------------

st.set_page_config(
    page_title="Monitoreo Modelo Crediticio",
    page_icon="📊",
    layout="wide"
)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REPORTS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "reports"
)

# ------------------------------------------------
# Barra lateral
# ------------------------------------------------

st.sidebar.title("📊 Dashboard")

pagina = st.sidebar.radio(

    "Seleccione una opción",

    [

        "🏠 Inicio",

        "📈 Desempeño del Modelo",

        "📉 Data Drift",

        "📋 Conclusiones"

    ]

)

if pagina == "🏠 Inicio":

    st.title("📊 Monitoreo del Modelo de Riesgo Crediticio")

    st.markdown("---")

    st.write("""

Este proyecto implementa un flujo completo de Machine Learning para evaluar
el riesgo crediticio de clientes.

Incluye:

- Ingeniería de características

- Entrenamiento de modelos

- Evaluación del desempeño

- Monitoreo del modelo

- Detección de Data Drift

- Visualización de resultados

""")

elif pagina == "📈 Desempeño del Modelo":

    st.title("📈 Desempeño del Modelo")

    comparacion = pd.read_csv(
        os.path.join(
            REPORTS_FOLDER,
            "comparacion_modelos.csv"
        )
    )

    # Obtener automáticamente el mejor modelo
    mejor_modelo = comparacion.sort_values(
        by="Accuracy",
        ascending=False
    ).iloc[0]

    st.success(
        f"🏆 Mejor modelo: {mejor_modelo['Modelo']}"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Accuracy",
            f"{mejor_modelo['Accuracy']:.4f}"
        )

    with col2:
        st.metric(
            "Precision",
            f"{mejor_modelo['Precision']:.4f}"
        )

    with col3:
        st.metric(
            "Recall",
            f"{mejor_modelo['Recall']:.4f}"
        )

    with col4:
        st.metric(
            "F1 Score",
            f"{mejor_modelo['F1']:.4f}"
        )

    with col5:
        st.metric(
            "ROC AUC",
            f"{mejor_modelo['ROC_AUC']:.4f}"
        )

    st.markdown("---")

    st.subheader("Comparación de Modelos")

    st.dataframe(
        comparacion,
        use_container_width=True,
        hide_index=True
    )


elif pagina == "📉 Data Drift":

    st.title("📉 Data Drift")

    drift = pd.read_csv(

        os.path.join(
            REPORTS_FOLDER,
            "drift_report.csv"
        )

    )

    st.dataframe(drift)

    st.image(

        os.path.join(
            REPORTS_FOLDER,
            "psi_variables.png"
        ),

        use_container_width=True

    )




elif pagina == "📋 Conclusiones":

    st.title("📋 Conclusiones")

    drift = pd.read_csv(

        os.path.join(
            REPORTS_FOLDER,
            "drift_report.csv"
        )

    )

    alto = drift[drift["Estado PSI"] == "Drift Alto"]

    st.metric(

        "Variables con Drift Alto",

        len(alto)

    )

    if len(alto) > 0:

        st.error(

            "Se recomienda reentrenar el modelo."

        )

    else:

        st.success(

            "El modelo continúa estable."

        )


