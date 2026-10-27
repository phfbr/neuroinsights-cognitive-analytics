
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

TRATADOS = BASE / "dados" / "tratados"
GOLD = TRATADOS / "gold"

df = pd.read_parquet(
    TRATADOS / "nhanes_cognitivo_silver.parquet"
)

print("\nNEUROINSIGHTS | DADOS AMOSTRAIS")
print("=" * 55)

# Selecionar variáveis do desenho amostral
amostragem = df[
    [
        "id_participante",
        "ciclo",
        "peso_amostral_2anos",
        "unidade_amostral",
        "estrato_amostral",
    ]
].copy()

# Peso combinado para dois ciclos de 2 anos.
# Aplicável quando o peso MEC é adequado
# à análise e à população-alvo.
amostragem["peso_amostral_4anos"] = (
    amostragem["peso_amostral_2anos"] / 2
)

# Validações estruturais
assert amostragem["id_participante"].is_unique
assert len(amostragem) == len(df)

assert amostragem["peso_amostral_2anos"].notna().all()
assert amostragem["peso_amostral_2anos"].gt(0).all()

assert amostragem["unidade_amostral"].notna().all()
assert amostragem["estrato_amostral"].notna().all()

# Validar transformação dos pesos
assert (
    amostragem["peso_amostral_4anos"]
    .eq(amostragem["peso_amostral_2anos"] / 2)
    .all()
)

# Salvar tabela complementar
destino = GOLD / "dim_amostragem.parquet"

amostragem.to_parquet(destino, index=False)

print(f"Participantes: {len(amostragem)}")
print(
    "Pesos positivos:",
    amostragem["peso_amostral_4anos"].gt(0).all()
)
print(
    "Unidades amostrais:",
    amostragem["unidade_amostral"].nunique()
)
print(
    "Estratos amostrais:",
    amostragem["estrato_amostral"].nunique()
)

print(f"\nArquivo salvo: {destino}")
print("DADOS AMOSTRAIS PREPARADOS!")
