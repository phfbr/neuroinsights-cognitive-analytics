
from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parent.parent
ENTRADA = BASE / "dados" / "tratados" / "nhanes_cognitivo_integrado.parquet"
SAIDA = BASE / "dados" / "tratados" / "nhanes_cognitivo_silver.parquet"

print("\nNEUROINSIGHTS | CAMADA SILVER")
print("=" * 55)

df = pd.read_parquet(ENTRADA)

# 1. Padronizar nomes das variáveis
renomear = {
    "RIDAGEYR": "idade",
    "RIAGENDR": "sexo_codigo",
    "RIDRETH3": "grupo_demografico_codigo",
    "DMDEDUC2": "escolaridade_codigo",
    "WTMEC2YR": "peso_amostral_2anos",
    "SDMVPSU": "unidade_amostral",
    "SDMVSTRA": "estrato_amostral",
    "CFDCST1": "memoria_tentativa_1",
    "CFDCST2": "memoria_tentativa_2",
    "CFDCST3": "memoria_tentativa_3",
    "CFDCSR": "memoria_tardia",
    "CFDAST": "fluencia_verbal",
    "CFDDS": "velocidade_processamento",
}

df = df.rename(columns=renomear)

# 2. Classificação etária descritiva
df["faixa_etaria"] = pd.cut(
    df["idade"],
    bins=[59, 69, 79, np.inf],
    labels=["60-69", "70-79", "80+"]
)

# 3. Identificar disponibilidade das pontuações
testes = [
    "memoria_tentativa_1",
    "memoria_tentativa_2",
    "memoria_tentativa_3",
    "memoria_tardia",
    "fluencia_verbal",
    "velocidade_processamento",
]

for teste in testes:
    df[f"{teste}_registrado"] = df[teste].notna()

# 4. Validar integridade
assert df["id_participante"].is_unique
assert df["id_participante"].notna().all()
assert len(df) == 3472

# 5. Salvar camada Silver
df.to_parquet(SAIDA, index=False)

print(f"Registros: {len(df)}")
print(f"Colunas: {len(df.columns)}")
print(f"IDs únicos: {df['id_participante'].is_unique}")

print("\nDistribuição por faixa etária:")
print(df["faixa_etaria"].value_counts(dropna=False).sort_index())

print("\nPontuações registradas:")
for teste in testes:
    print(f"{teste}: {df[f'{teste}_registrado'].sum()}")

print(f"\nArquivo salvo: {SAIDA}")
print("CAMADA SILVER FINALIZADA!")
