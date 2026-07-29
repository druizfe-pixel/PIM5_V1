import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from scipy.stats import chi2_contingency

import numpy as np


def calculate_psi(expected, actual, bins=10):
    """
    Calcula el Population Stability Index (PSI).

    Parameters
    ----------
    expected : array-like
        Datos de entrenamiento.

    actual : array-like
        Datos actuales.

    bins : int
        Número de intervalos.

    Returns
    -------
    float
        Valor del PSI.
    """

    expected = np.asarray(expected)
    actual = np.asarray(actual)

    breakpoints = np.percentile(expected, np.arange(0, 101, 100 / bins))

    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]

    expected_pct = expected_counts / len(expected)
    actual_pct = actual_counts / len(actual)

    expected_pct = np.where(expected_pct == 0, 0.0001, expected_pct)
    actual_pct = np.where(actual_pct == 0, 0.0001, actual_pct)

    psi = np.sum(
        (expected_pct - actual_pct)
        * np.log(expected_pct / actual_pct)
    )

    return psi


def psi_status(psi):

    if psi < 0.10:
        return "Sin Drift"

    elif psi < 0.25:
        return "Drift Moderado"

    else:
        return "Drift Alto"

def ks_test(expected, actual):

    statistic, p_value = ks_2samp(
        expected,
        actual
    )

    return statistic, p_value


def chi_square_test(expected, actual):

    tabla = pd.crosstab(
        pd.Series(expected),
        pd.Series(actual)
    )

    chi2, p_value, _, _ = chi2_contingency(tabla)

    return chi2, p_value


def ks_status(statistic, p_value):

    if p_value >= 0.05:
        return "Sin Drift"

    if statistic < 0.10:
        return "Drift Bajo"

    elif statistic < 0.20:
        return "Drift Moderado"

    else:
        return "Drift Alto"

import pandas as pd


def analyze_drift(df_reference, df_monitor):

    resultados = []

    numericas = df_reference.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categoricas = df_reference.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if "Pago_atiempo" in numericas:
        numericas.remove("Pago_atiempo")

    for col in numericas:

        try:

            psi = calculate_psi(
                df_reference[col],
                df_monitor[col]
            )

            ks, p = ks_test(
                df_reference[col],
                df_monitor[col]
            )

        except Exception:

            psi = None
            ks = None
            p = None

        resultados.append({

            "Variable": col,

            "Tipo": "Numérica",

            "PSI": psi,

            "Estado PSI": psi_status(psi)
            if psi is not None else "",

            "KS": ks,

            "p-value": p

        })

    return pd.DataFrame(resultados)


if __name__ == "__main__":

    np.random.seed(42)

    # Datos de entrenamiento
    train = np.random.normal(100, 15, 1000)

    # Datos similares (sin drift)
    monitor_ok = np.random.normal(101, 15, 1000)

    # Datos con drift
    monitor_drift = np.random.normal(130, 20, 1000)

    print("=" * 60)
    print("PRUEBA PSI")
    print("=" * 60)

    psi = calculate_psi(train, monitor_ok)

    print(f"PSI sin drift : {psi:.4f}")
    print(f"Estado        : {psi_status(psi)}")

    psi = calculate_psi(train, monitor_drift)

    print(f"\nPSI con drift : {psi:.4f}")
    print(f"Estado        : {psi_status(psi)}")

    print("\n" + "=" * 60)
    print("PRUEBA KS")
    print("=" * 60)

    ks, p = ks_test(train, monitor_ok)

    print(f"KS sin drift")
    print(f"Estadístico : {ks:.4f}")
    print(f"p-value     : {p:.4f}")

    ks, p = ks_test(train, monitor_drift)

    print(f"\nKS con drift")
    print(f"Estadístico : {ks:.4f}")
    print(f"p-value     : {p:.4f}")