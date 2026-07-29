# PIM5_V1
# 🎓 EduStream - Predicción de Abandono de Cursos Online

## 📌 Descripción del proyecto

EduStream es una plataforma de educación en línea enfocada en el análisis de métricas de aprendizaje y retención de estudiantes.

Como parte de su crecimiento, la organización decidió desarrollar un modelo de Machine Learning capaz de predecir el abandono (Dropout) de los estudiantes con el fin de implementar estrategias de intervención temprana.

Durante el desarrollo del proyecto se identificó un problema importante: la falta de un flujo de trabajo colaborativo entre científicos de datos y desarrolladores. Cada integrante trabajaba de manera independiente, generando múltiples versiones de archivos y modelos, dificultando la trazabilidad y el control de cambios.

Para solucionar este problema se implementó un flujo de trabajo profesional utilizando Git y GitHub bajo la metodología GitFlow.

---

# 🎯 Objetivos

## Objetivo de negocio

Predecir qué estudiantes tienen mayor probabilidad de abandonar un curso para facilitar la toma de decisiones y mejorar los indicadores de retención.

## Objetivos técnicos

- Implementar un flujo de desarrollo basado en GitFlow.
- Mantener el control de versiones del código.
- Construir un pipeline de Machine Learning reproducible.
- Entrenar y evaluar diferentes modelos de clasificación.
- Versionar correctamente los artefactos del proyecto.

---

# 🛠 Tecnologías utilizadas

- Python 3.12
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- Joblib
- Git
- GitHub
- Visual Studio Code

---

# 📂 Estructura del proyecto

```
PIM5_V1/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── modelo.pkl
│   └── preprocessor.pkl
│
├── reports/
│   └── comparacion_modelos.csv
│
├── src/
│   ├── cargar_datos.py
│   ├── ft_engineering.py
│   ├── model_training_evaluation.py
│   └── model_monitoring.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# ⚙ Flujo del proyecto

```
Carga de datos
        │
        ▼
Análisis Exploratorio (EDA)
        │
        ▼
Feature Engineering
        │
        ▼
Preprocesamiento
        │
        ▼
Entrenamiento de modelos
        │
        ▼
Evaluación
        │
        ▼
Selección del mejor modelo
        │
        ▼
Persistencia del modelo
        │
        ▼
Monitoreo
```

---

# 🤖 Modelos implementados

Se entrenaron y compararon los siguientes algoritmos:

- Logistic Regression
- Random Forest
- XGBoost

Las métricas evaluadas fueron:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC

---

# 🌳 Estrategia de control de versiones

El proyecto utiliza **GitFlow** para garantizar un desarrollo organizado y colaborativo.

```
feature
     │
     ▼
develop
     │
     ▼
certification
     │
     ▼
master
```

Cada funcionalidad se desarrolla en una rama independiente y posteriormente es integrada mediante Pull Requests y revisión por pares.

---

# 📌 Buenas prácticas implementadas

- Separación del código por módulos.
- Reutilización del pipeline de preprocesamiento.
- Persistencia del modelo mediante Joblib.
- Comparación automática de modelos.
- Generación de reportes de métricas.
- Control de versiones mediante Git y GitHub.

---

# 🚀 Cómo ejecutar el proyecto

## 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/NOMBRE_REPOSITORIO.git
```

## 2. Crear entorno virtual

```bash
python -m venv venv
```

## 3. Activar entorno virtual

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 5. Ejecutar entrenamiento

```bash
python src/model_training_evaluation.py
```

---

# 📈 Resultados

El pipeline permite:

- Cargar y validar los datos.
- Realizar el preprocesamiento.
- Entrenar múltiples modelos.
- Comparar métricas automáticamente.
- Guardar el mejor modelo entrenado.
- Guardar el pipeline de transformación.
- Generar reportes de evaluación.

---

# 👨‍💻 Autor

**Daniel Ruiz**

Especialista en Ingeniería de Operaciones | Supply Chain | Data Science | Machine Learning

LinkedIn: