
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
BRUTOS = BASE_DIR / "dados" / "brutos"

ARQUIVOS = ["CFQ_G.xpt", "CFQ_H.xpt"]

COLUNAS = [
    "CFASTAT",
    "CFDCCS",
    "CFDAPP",
    "CFDDPP"
]

for arquivo in ARQUIVOS:
    df = pd.read_sas(BRUTOS / arquivo, format="xport")

    print(f"\n{'=' * 50}")
    print(f"ARQUIVO: {arquivo}")
    print(f"{'=' * 50}")

    for coluna in COLUNAS:
        print(f"\n{coluna}")

        print(
            df[coluna]
            .value_counts(dropna=False)
            .sort_index()
            .to_string()
        )

    print("\nAVALIAÇÕES COM PONTUAÇÃO REGISTRADA")

    for coluna in [
        "CFDCST1",
        "CFDCST2",
        "CFDCST3",
        "CFDCSR",
        "CFDAST",
        "CFDDS"
    ]:
        print(f"{coluna}: {df[coluna].notna().sum()}")

print("\nVALIDAÇÃO CONCLUÍDA!")
