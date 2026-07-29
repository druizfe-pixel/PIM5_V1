import streamlit as st
import requests

# =====================================================
# CONFIGURACIÓN
# =====================================================

#API_URL = "http://127.0.0.1:8000/predict"
API_URL = "http://api:8000/predict"


st.set_page_config(
    page_title="FinanceGuard",
    page_icon="💳",
    layout="wide"
)

# =====================================================
# EVALUACIÓN DEL RIESGO
# =====================================================

def evaluar_riesgo(prob_pago):

    if prob_pago >= 0.90:

        return (
            "🟢 BAJO",
            "Se recomienda aprobar el crédito."
        )

    elif prob_pago >= 0.70:

        return (
            "🟡 MEDIO",
            "Se recomienda realizar una revisión adicional."
        )

    else:

        return (
            "🔴 ALTO",
            "Existe un alto riesgo de incumplimiento."
        )


# =====================================================
# LLAMADA A LA API
# =====================================================

def conectar_api(datos):

    try:

        respuesta = requests.post(
            API_URL,
            json=datos,
            timeout=10
        )

        respuesta.raise_for_status()

        return respuesta.json()

    except requests.exceptions.ConnectionError:

        st.error("No fue posible conectar con la API.")

    except requests.exceptions.Timeout:

        st.error("La API tardó demasiado en responder.")

    except requests.exceptions.HTTPError as e:

        st.error(f"Error HTTP: {e}")

    except Exception as e:

        st.error(e)

    return None

# =====================================================
# TÍTULO
# =====================================================

st.title("💳 FinanceGuard")

st.subheader(
    "Sistema inteligente para evaluación del riesgo de crédito"
)

st.divider()

# =====================================================
# COLUMNAS PRINCIPALES
# =====================================================

col_formulario, col_dashboard = st.columns(
    [2.3, 1],
    gap="large"
)


# =====================================================
# COLUMNA IZQUIERDA
# =====================================================

with col_formulario:

    st.header("📋 Información del cliente")


    # =====================================================
    # PERFIL DEL CLIENTE
    # =====================================================

    with st.expander("👤 Perfil del cliente", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            edad_cliente = st.number_input(
                "Edad",
                min_value=18,
                max_value=100,
                value=35
            )

            tipo_laboral = st.selectbox(
                "Tipo laboral",
                [
                    "Empleado",
                    "Independiente"
                ]
            )

        with col2:

            salario_cliente = st.number_input(
                "Salario",
                min_value=0.0,
                value=2500000.0,
                step=100000.0
            )

            promedio_ingresos_datacredito = st.number_input(
                "Promedio ingresos Datacrédito",
                min_value=0.0,
                value=900000.0,
                step=10000.0
            )

    # =====================================================
    # INFORMACIÓN DEL CRÉDITO
    # =====================================================

    with st.expander("💰 Información del crédito", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            tipo_credito = st.selectbox(
                "Tipo de crédito",
                ["1", "2", "3", "4", "5", "6", "7"]
            )

            capital_prestado = st.number_input(
                "Capital prestado",
                value=3000000.0,
                step=100000.0
            )

            cuota_pactada = st.number_input(
                "Cuota pactada",
                value=341296.0,
                step=1000.0
            )

        with col2:

            fecha_prestamo = st.text_input(
                "Fecha préstamo",
                "21/12/2024 11:31"
            )

            plazo_meses = st.number_input(
                "Plazo (meses)",
                min_value=1,
                max_value=120,
                value=12
            )

    # =====================================================
    # HISTORIAL FINANCIERO
    # =====================================================

    with st.expander("📊 Historial financiero", expanded=False):

        col1, col2 = st.columns(2)

        with col1:

            puntaje = st.number_input(
                "Puntaje",
                value=88.0
            )

            puntaje_datacredito = st.number_input(
                "Puntaje Datacrédito",
                value=695
            )

            total_otros_prestamos = st.number_input(
                "Total otros préstamos",
                value=2500000.0
            )

        with col2:

            cant_creditosvigentes = st.number_input(
                "Créditos vigentes",
                value=10
            )

            huella_consulta = st.number_input(
                "Consultas",
                value=5
            )

            tendencia_ingresos = st.selectbox(
                "Tendencia ingresos",
                [
                    "Creciente",
                    "Estable",
                    "Decreciente"
                ]
            )

    # =====================================================
    # ESTADO DE CARTERA
    # =====================================================

    with st.expander("📋 Estado de cartera", expanded=False):

        col1, col2 = st.columns(2)

        with col1:

            saldo_mora = st.number_input(
                "Saldo mora",
                value=0.0
            )

            saldo_total = st.number_input(
                "Saldo total",
                value=51258.0
            )

        with col2:

            saldo_principal = st.number_input(
                "Saldo principal",
                value=51258.0
            )

            saldo_mora_codeudor = st.number_input(
                "Saldo mora codeudor",
                value=0.0
            )

    # =====================================================
    # DISTRIBUCIÓN DE CRÉDITOS
    # =====================================================

    with st.expander("🏦 Distribución de créditos", expanded=False):

        col1, col2, col3 = st.columns(3)

        with col1:

            creditos_sectorFinanciero = st.number_input(
                "Financiero",
                value=5
            )

        with col2:

            creditos_sectorCooperativo = st.number_input(
                "Cooperativo",
                value=0
            )

        with col3:

            creditos_sectorReal = st.number_input(
                "Sector real",
                value=0
            )

    st.divider()

    analizar = st.button(
        "🔎 Analizar Cliente",
        use_container_width=True,
        type="primary"
    )

    datos = {
        "tipo_credito": tipo_credito,
        "fecha_prestamo": fecha_prestamo,
        "capital_prestado": capital_prestado,
        "plazo_meses": plazo_meses,
        "edad_cliente": edad_cliente,
        "tipo_laboral": tipo_laboral,
        "salario_cliente": salario_cliente,
        "total_otros_prestamos": total_otros_prestamos,
        "cuota_pactada": cuota_pactada,
        "puntaje": puntaje,
        "puntaje_datacredito": puntaje_datacredito,
        "cant_creditosvigentes": cant_creditosvigentes,
        "huella_consulta": huella_consulta,
        "saldo_mora": saldo_mora,
        "saldo_total": saldo_total,
        "saldo_principal": saldo_principal,
        "saldo_mora_codeudor": saldo_mora_codeudor,
        "creditos_sectorFinanciero": creditos_sectorFinanciero,
        "creditos_sectorCooperativo": creditos_sectorCooperativo,
        "creditos_sectorReal": creditos_sectorReal,
        "promedio_ingresos_datacredito": promedio_ingresos_datacredito,
        "tendencia_ingresos": tendencia_ingresos
    }

# =====================================================
# LLAMAR LA API
# =====================================================

    if analizar:

        with st.spinner("Analizando cliente..."):

            resultado = conectar_api(datos)

            #st.write("Respuesta API:")
            #st.write(resultado)

            if resultado is not None:

                st.session_state["resultado"] = resultado

                st.rerun()


# =====================================================
# COLUMNA DERECHA - DASHBOARD
# =====================================================

with col_dashboard:

    st.header("📈 Resultado del análisis")

    st.metric(
        label="🤖 Modelo",
        value="XGBoost"
    )

    st.divider()

    # ---------------------------------------------
    # Estado inicial
    # ---------------------------------------------

    if "resultado" not in st.session_state:

        st.info(
            "Complete el formulario y presione **🔎 Analizar Cliente**."
        )

        st.progress(0.0)

        st.metric(
            label="Estado",
            value="Esperando análisis"
        )

    # ---------------------------------------------
    # Mostrar resultados
    # ---------------------------------------------

    else:

        resultado = st.session_state["resultado"]

        prob_pago = float(resultado["probabilidad_pago"])
        prob_no_pago = float(resultado["probabilidad_no_pago"])

        riesgo, recomendacion = evaluar_riesgo(prob_pago)

        # -----------------------------------------
        # Riesgo
        # -----------------------------------------

        st.metric(
            label="Nivel de riesgo",
            value=riesgo
        )

        st.divider()

        # -----------------------------------------
        # Probabilidad de pago
        # -----------------------------------------

        st.subheader("✅ Probabilidad de pago")

        st.progress(prob_pago)

        st.metric(
            "Pago",
            f"{prob_pago:.2%}"
        )

        # -----------------------------------------
        # Probabilidad de incumplimiento
        # -----------------------------------------

        st.subheader("⚠️ Probabilidad de incumplimiento")

        st.progress(prob_no_pago)

        st.metric(
            "Incumplimiento",
            f"{prob_no_pago:.2%}"
        )

        st.divider()

        # -----------------------------------------
        # Recomendación
        # -----------------------------------------

        st.subheader("💡 Recomendación")

        if prob_pago >= 0.90:

            st.success(recomendacion)

        elif prob_pago >= 0.70:

            st.warning(recomendacion)

        else:

            st.error(recomendacion)

        st.divider()

        # -----------------------------------------
        # Información técnica
        # -----------------------------------------

        st.caption("Modelo : XGBoost")

        st.caption("Versión : 1.0")

        st.caption("API : 🟢 Activa")