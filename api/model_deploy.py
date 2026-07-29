from fastapi import FastAPI
from api.schemas import Cliente

import joblib
import pandas as pd
import os
import sys

# =====================================================
# CONFIGURACIÓN
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_PATH = os.path.join(BASE_DIR, "src")

if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

import src.ft_engineering

# =====================================================
# CARGAR MODELOS
# =====================================================

MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo.pkl")
PREPROCESSOR_PATH = os.path.join(BASE_DIR, "models", "preprocessor.pkl")

modelo = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

# =====================================================
# FASTAPI
# =====================================================

app = FastAPI(
    title="FinanceGuard API",
    version="1.0"
)


@app.get("/")
def root():

    return {
        "mensaje": "FinanceGuard API funcionando correctamente"
    }


@app.post("/predict")
def predict(cliente: Cliente):

    # Convertir el objeto recibido en DataFrame
    datos = pd.DataFrame([cliente.model_dump()])

    # Aplicar preprocesamiento
    datos_preprocesados = preprocessor.transform(datos)

    # Predicción
    prediccion = modelo.predict(datos_preprocesados)[0]

    # Probabilidades
    probabilidades = modelo.predict_proba(datos_preprocesados)[0]

    return {

        "prediccion": int(prediccion),

        "probabilidad_no_pago": round(float(probabilidades[0]),4),

        "probabilidad_pago": round(float(probabilidades[1]),4)

    }