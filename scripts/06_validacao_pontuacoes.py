
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
BRUTOS = BASE / "dados" / "brutos"
QUALIDADE = BASE / "dados" / "qualidade"
QUALIDADE.mkdir(parents=True, exist_ok=True)

CICLOS = {
    "2011-2012": "CFQ_G.xpt",
    "2013-2014": "CFQ_H.xpt"
}

TESTES = {
    "CFDCST1": (0, 10),
    "CFDCST2": (0, 10),
    "CFDCST3": (0, 10),
    "CFDCSR": (0, 10),
    "CFDAST": (0, None),
    "CFDDS": (0, 133)
}

resultados = []

for ciclo, arquivo in CICLOS.items():
    df = pd.read_sas(BRUTOS / arquivo, format="xport")

    print(f"\nCICLO: {ciclo}")
    print("-" * 60)

    for teste, (minimo, maximo) in TESTES.items():
        serie = df[teste]

        fora = serie.notna() & (serie < minimo)

        if maximo is not None:
            fora = fora | (
                serie.notna() & (serie > maximo)
            )

        quantidade = int(fora.sum())

        resultados.append({
            "ciclo": ciclo,
            "teste": teste,
            "preenchidos": int(serie.notna().sum()),
            "minimo_observado": serie.min(),
            "maximo_observado": serie.max(),
            "fora_intervalo": quantidade
        })

        print(
            f"{teste}: "
            f"min={serie.min()}, "
            f"max={serie.max()}, "
            f"fora_intervalo={quantidade}"
        )

    # Verificar inconsistências dos pré-testes
    animal_inconsistente = (
        df["CFDAST"].notna()
        & (df["CFDAPP"] != 1)
    ).sum()

    dsst_inconsistente = (
        df["CFDDS"].notna()
        & (df["CFDDPP"] != 1)
    ).sum()

    print("\nCONSISTÊNCIA DOS PRÉ-TESTES")
    print(f"Fluência: {animal_inconsistente}")
    print(f"DSST: {dsst_inconsistente}")

relatorio = pd.DataFrame(resultados)

relatorio.to_csv(
    QUALIDADE / "validacao_pontuacoes.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nVALIDAÇÃO FINALIZADA!")
