import os
import pandas as pd


def cargarDatos():
    """
    Carga la base de datos desde la carpeta data/raw.

    Returns
    -------
    DataFrame
        Base de datos cargada desde el archivo Excel.
    """

    # Ruta de la carpeta src
    ruta_actual = os.path.dirname(os.path.abspath(__file__))

    # Ruta de la carpeta principal del proyecto
    ruta_proyecto = os.path.dirname(ruta_actual)

    # Ruta del archivo Excel
    ruta_excel = os.path.join(
        ruta_proyecto,
        "data",
        "raw",
        "Base_de_datos.xlsx"
    )

    ruta_excel = os.path.join(
    ruta_proyecto,
    "data",
    "raw",
    "Base_de_datos.xlsx"
)

    print(ruta_proyecto)
    print(ruta_excel)
    print(os.path.exists(ruta_excel))

    df = pd.read_excel(ruta_excel)


    # Leer archivo
    df = pd.read_excel(ruta_excel)

    return df


if __name__ == "__main__":

    datos = cargarDatos()

    print(datos.head())
    print("\nInformación del DataFrame:\n")
    print(datos.info())
    