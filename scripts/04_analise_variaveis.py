
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
BRUTOS = BASE_DIR / "dados" / "brutos"
QUALIDADE = BASE_DIR / "dados" / "qualidade"

QUALIDADE.mkdir(parents=True, exist_ok=True)

ARQUIVOS = ["CFQ_G.xpt", "CFQ_H.xpt"]

relatorios = []

print("\nNEUROINSIGHTS | ANÁLISE DE VARIÁVEIS")
print("=" * 60)

for arquivo in ARQUIVOS:
    df = pd.read_sas(BRUTOS / arquivo, format="xport")

    print(f"\nARQUIVO: {arquivo}")
    print("-" * 60)

    for coluna in df.columns:
        serie = df[coluna]

        nulos = int(serie.isna().sum())
        preenchidos = int(serie.notna().sum())

        relatorios.append({
            "arquivo": arquivo,
            "variavel": coluna,
            "tipo": str(serie.dtype),
            "preenchidos": preenchidos,
            "nulos": nulos,
            "percentual_nulos": round(
                serie.isna().mean() * 100, 2
            ),
            "minimo": (
                serie.min()
                if pd.api.types.is_numeric_dtype(serie)
                else None
            ),
            "maximo": (
                serie.max()
                if pd.api.types.is_numeric_dtype(serie)
                else None
            ),
        })

    print("Variáveis encontradas:")
    print(", ".join(df.columns))

    print("\nPercentual de nulos por variável:")
    print(
        (df.isna().mean() * 100)
        .sort_values(ascending=False)
        .round(2)
        .to_string()
    )

relatorio = pd.DataFrame(relatorios)

destino = QUALIDADE / "auditoria_variaveis_cognitivas.csv"

relatorio.to_csv(
    destino,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 60)
print(f"Relatório salvo: {destino}")
print("ANÁLISE FINALIZADA!")
