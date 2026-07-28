# librerias
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer

from cargar_datos import cargarDatos

# # 1. Cargamos los datos
# df = cargarDatos()

# # tengamos una vista previa de los datos
# print(df.head())
# print(df.info( ))
# print(df.describe())

# # 2. hagamos el split de features y target
# X = df.drop('Pago_atiempo', axis=1)  # Features
# y = df['Pago_atiempo']  # Target

# # 3. Definimos los tipos de variables
# num_features = X.select_dtypes('number').columns
# cat_features = X.select_dtypes('object').columns

# print(f'Features numéricas: {num_features}')
# print(f'Features categóricas: {cat_features}')

# # 4. Creamos pipelines para cada ruta (numerica y categórica)
# ## Ruta 1: Numericas
# num_transformer = Pipeline(
#     steps=[
#         ('imputer', SimpleImputer(strategy='mean'))  # Imputación de valores faltantes con la media
#     ]
# )

# ## Ruta 2: Categóricas
# cat_transformer = Pipeline(
#     steps=[
#         ('to_str', FunctionTransformer(lambda x: x.astype(str))),  # Imputación de valores faltantes con la moda
#         ('inputer', SimpleImputer(strategy='most_frequent')),
#         ('onehot', OneHotEncoder(handle_unknown='ignore'))  # Codificación one-hot
#     ]
# )

# # 5. Combinamos las rutas en un ColumnTransformer
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', num_transformer, num_features),
#         ('cat', cat_transformer, cat_features)
#     ]
# )

# # 6. Dividimos los datos en conjuntos de entrenamiento y prueba
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


# # 7. Aplicamos el preprocesamiento a los datos de entrenamiento y prueba
# X_train_preprocessed = preprocessor.fit_transform(X_train)
# X_test_preprocessed = preprocessor.transform(X_test)

# # 8. Imprimimos los resultados de los datos preprocesados
# print(f'X_train_preprocessed shape: {X_train_preprocessed}')
# print(f'X_test_preprocessed shape: {X_test_preprocessed}')

# 9. Construimos una funcion para encapsular todo el proceso de preprocesamiento
# =====================================================
# FUNCIÓN AUXILIAR
# =====================================================

def convertir_string(x):
    """
    Convierte todas las columnas a tipo string.
    Esta función reemplaza el uso de lambda para que
    el preprocesador pueda serializarse con joblib.
    """
    return x.astype(str)


# =====================================================
# PREPROCESAMIENTO
# =====================================================

def preprocesar_datos():
    """
    Esta función encapsula todo el proceso de preprocesamiento
    de los datos.
    Devuelve el preprocesador, los conjuntos de entrenamiento
    y prueba, y los datos transformados.
    """

    # 1. Cargamos los datos
    df = cargarDatos()

    # 2. Features y Target
    
    # columnas_eliminar = [
    #     "Pago_atiempo",
    #     "saldo_mora",
    #     "saldo_total",
    #     "saldo_principal",
    #     "saldo_mora_codeudor"
    # ]
    # X = df.drop(columns=columnas_eliminar)
    
    X = df.drop('Pago_atiempo', axis=1) # Features
    y = df["Pago_atiempo"]

    # 3. Variables numéricas y categóricas
    num_features = X.select_dtypes(include="number").columns
    cat_features = X.select_dtypes(include=["object"]).columns

    # 4. Pipeline numérico
    num_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="mean"))
        ]
    )

    # 5. Pipeline categórico
    cat_transformer = Pipeline(
        steps=[
            ("to_str", FunctionTransformer(convertir_string)),
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    # 6. ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, num_features),
            ("cat", cat_transformer, cat_features)
        ]
    )

    # 7. Train/Test
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # 8. Transformación
    X_train_preprocessed = preprocessor.fit_transform(X_train)
    X_test_preprocessed = preprocessor.transform(X_test)

    return (
        preprocessor,
        X_train,
        X_test,
        X_train_preprocessed,
        X_test_preprocessed,
        y_train,
        y_test
    )

