import os

import matplotlib.pyplot as plt

import pandas as pd

def psi_barplot(df, output_folder):

    df = df.sort_values("PSI", ascending=False)

    plt.figure(figsize=(12,6))

    plt.bar(
        df["Variable"],
        df["PSI"]
    )

    plt.axhline(
        y=0.10,
        linestyle="--",
        linewidth=1,
        label="PSI = 0.10"
    )

    plt.axhline(
        y=0.25,
        linestyle="--",
        linewidth=1,
        label="PSI = 0.25"
    )

    plt.xticks(rotation=90)

    plt.ylabel("PSI")

    plt.title("Índice de Estabilidad Poblacional (PSI)")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_folder,
            "psi_variables.png"
        )
    )

    plt.close()



def compare_histogram(reference, monitor, variable, output_folder):
    """
    Genera un histograma comparando la distribución de una variable
    entre el dataset de referencia y el dataset de monitoreo.
    """

    plt.figure(figsize=(8, 5))

    plt.hist(
        reference.dropna(),
        bins=30,
        alpha=0.6,
        label="Referencia"
    )

    plt.hist(
        monitor.dropna(),
        bins=30,
        alpha=0.6,
        label="Monitoreo"
    )

    plt.title(f"Comparación: {variable}")
    plt.xlabel(variable)
    plt.ylabel("Frecuencia")
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_folder,
            f"{variable}_histograma.png"
        )
    )

    plt.close()

def compare_boxplot(reference, monitor, variable, output_folder):

    plt.figure(figsize=(6,5))

    plt.boxplot(
        [
            reference.dropna(),
            monitor.dropna()
        ],
        tick_labels=["Referencia", "Monitoreo"]
    )

    plt.title(variable)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_folder,
            f"{variable}_boxplot.png"
        )
    )

    plt.close()

def drift_summary_plot(drift_df, output_folder):

    resumen = drift_df["Estado PSI"].value_counts()

    plt.figure(figsize=(6,4))

    plt.bar(
        resumen.index,
        resumen.values
    )

    plt.ylabel("Número de variables")

    plt.title("Resumen del Data Drift")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_folder,
            "drift_summary.png"
        )
    )

    plt.close()