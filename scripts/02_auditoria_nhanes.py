
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_BRUTOS = BASE_DIR / "dados" / "brutos"
PASTA_QUALIDADE = BASE_DIR / "dados" / "qualidade"

PASTA_QUALIDADE.mkdir(parents=True, exist_ok=True)

ARQUIVOS = [
    "CFQ_G.xpt",
    "CFQ_H.xpt",
    "DEMO_G.xpt",
    "DEMO_H.xpt",
]

resumo = []

print("\nNEUROINSIGHTS | AUDITORIA INICIAL")
print("=" * 55)

for nome in ARQUIVOS:
    caminho = PASTA_BRUTOS / nome

    print(f"\nARQUIVO: {nome}")
    print("-" * 55)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_sas(caminho, format="xport")

    linhas, colunas = df.shape

    print(f"Registros: {linhas:,}")
    print(f"Colunas: {colunas}")

    print("\nTipos de dados:")
    print(df.dtypes.value_counts().to_string())

    print("\nPrimeiras 5 linhas:")
    print(df.head().to_string(index=False))

    print("\nValores ausentes:")
    nulos = df.isna().sum()
    print(nulos.sort_values(ascending=False).head(10))

    if "SEQN" not in df.columns:
        raise ValueError(f"Chave SEQN ausente em {nome}")

    chaves_nulas = int(df["SEQN"].isna().sum())
    duplicados = int(df["SEQN"].duplicated().sum())

    print(f"\nSEQN nulos: {chaves_nulas}")
    print(f"SEQN duplicados: {duplicados}")

    resumo.append({
        "arquivo": nome,
        "registros": linhas,
        "colunas": colunas,
        "seqn_nulos": chaves_nulas,
        "seqn_duplicados": duplicados,
        "celulas_nulas": int(df.isna().sum().sum()),
    })

    # Relatório de qualidade por coluna
    qualidade = pd.DataFrame({
        "coluna": df.columns,
        "tipo": df.dtypes.astype(str).values,
        "nulos": df.isna().sum().values,
        "percentual_nulos": (
            df.isna().mean().values * 100
        ).round(2),
        "valores_distintos": df.nunique(dropna=True).values,
    })

    qualidade.to_csv(
        PASTA_QUALIDADE / f"qualidade_{nome.replace('.xpt', '')}.csv",
        index=False,
        encoding="utf-8-sig",
    )

resumo_df = pd.DataFrame(resumo)

resumo_df.to_csv(
    PASTA_QUALIDADE / "resumo_auditoria.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\n" + "=" * 55)
print("RESUMO GERAL")
print(resumo_df.to_string(index=False))
print("\nRelatórios salvos em dados/qualidade/")
print("AUDITORIA FINALIZADA!")
