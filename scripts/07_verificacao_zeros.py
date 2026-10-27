
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
BRUTOS = BASE / "dados" / "brutos"

COLUNAS = [
    "CFDCST1", "CFDCST2", "CFDCST3",
    "CFDCSR", "CFDAST", "CFDDS"
]

for arquivo in ["CFQ_G.xpt", "CFQ_H.xpt"]:
    df = pd.read_sas(BRUTOS / arquivo, format="xport")

    print(f"\nARQUIVO: {arquivo}")
    print("-" * 55)

    for coluna in COLUNAS:
        serie = df[coluna]

        proximos_zero = (
            serie.notna()
            & (serie.abs() < 1e-10)
        ).sum()

        zeros_exatos = (serie == 0).sum()

        print(
            f"{coluna}: "
            f"proximos_zero={proximos_zero}, "
            f"zeros_exatos={zeros_exatos}"
        )
