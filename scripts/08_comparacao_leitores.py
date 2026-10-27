
from pathlib import Path
import pandas as pd
import pyreadstat

BASE = Path(__file__).resolve().parent.parent
BRUTOS = BASE / "dados" / "brutos"

COLUNAS = [
    "CFDCST1", "CFDCST2", "CFDCST3",
    "CFDCSR", "CFDAST", "CFDDS"
]

for arquivo in ["CFQ_G.xpt", "CFQ_H.xpt"]:

    caminho = BRUTOS / arquivo

    pandas_df = pd.read_sas(
        caminho,
        format="xport"
    )

    readstat_df, meta = pyreadstat.read_xport(
        str(caminho)
    )

    print(f"\nARQUIVO: {arquivo}")
    print("-" * 65)

    # Comparar registros pela chave SEQN
    comparacao = pandas_df[
        ["SEQN"] + COLUNAS
    ].merge(
        readstat_df[["SEQN"] + COLUNAS],
        on="SEQN",
        suffixes=("_pd", "_rs"),
        validate="one_to_one"
    )

    for coluna in COLUNAS:

        a = comparacao[f"{coluna}_pd"]
        b = comparacao[f"{coluna}_rs"]

        proximos_zero = a.notna() & (a.abs() < 1e-10)
        zeros_readstat = (b[proximos_zero] == 0).sum()

        print(
            f"{coluna}: "
            f"próximos_zero_pandas={proximos_zero.sum()}, "
            f"zeros_pyreadstat={zeros_readstat}"
        )

print("\nCOMPARAÇÃO FINALIZADA!")
