
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
SILVER = BASE / "dados" / "tratados" / "nhanes_cognitivo_silver.parquet"
GOLD = BASE / "dados" / "tratados" / "gold"

GOLD.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(SILVER)

print("\nNEUROINSIGHTS | MODELAGEM GOLD")
print("=" * 55)

# DIMENSÃO PARTICIPANTE
dim_participante = df[
    [
        "id_participante",
        "idade",
        "faixa_etaria",
        "sexo_codigo",
        "escolaridade_codigo",
        "grupo_demografico_codigo",
    ]
].copy()

dim_participante["faixa_etaria"] = (
    dim_participante["faixa_etaria"].astype("string")
)

# DIMENSÃO CICLO
dim_ciclo = pd.DataFrame({
    "ciclo": ["2011-2012", "2013-2014"],
    "ano_inicio": [2011, 2013],
    "ano_fim": [2012, 2014],
})

# DIMENSÃO TESTE
dim_teste = pd.DataFrame([
    {
        "id_teste": 1,
        "variavel": "memoria_tentativa_1",
        "teste": "CERAD - Tentativa 1",
        "dominio": "Memória imediata",
    },
    {
        "id_teste": 2,
        "variavel": "memoria_tentativa_2",
        "teste": "CERAD - Tentativa 2",
        "dominio": "Memória imediata",
    },
    {
        "id_teste": 3,
        "variavel": "memoria_tentativa_3",
        "teste": "CERAD - Tentativa 3",
        "dominio": "Memória imediata",
    },
    {
        "id_teste": 4,
        "variavel": "memoria_tardia",
        "teste": "CERAD - Evocação tardia",
        "dominio": "Memória tardia",
    },
    {
        "id_teste": 5,
        "variavel": "fluencia_verbal",
        "teste": "Fluência verbal - Animais",
        "dominio": "Fluência verbal",
    },
    {
        "id_teste": 6,
        "variavel": "velocidade_processamento",
        "teste": "Digit Symbol Substitution",
        "dominio": "Velocidade de processamento",
    },
])

# VALIDAR DIMENSÕES
assert dim_participante["id_participante"].is_unique
assert dim_participante["id_participante"].notna().all()
assert len(dim_participante) == len(df)

assert dim_ciclo["ciclo"].is_unique
assert dim_teste["id_teste"].is_unique
assert dim_teste["variavel"].is_unique

# SALVAR
dim_participante.to_parquet(
    GOLD / "dim_participante.parquet",
    index=False
)

dim_ciclo.to_parquet(
    GOLD / "dim_ciclo.parquet",
    index=False
)

dim_teste.to_parquet(
    GOLD / "dim_teste.parquet",
    index=False
)

print(f"dim_participante: {len(dim_participante)} registros")
print(f"dim_ciclo: {len(dim_ciclo)} registros")
print(f"dim_teste: {len(dim_teste)} registros")
print("\nDIMENSÕES GOLD GERADAS COM SUCESSO!")
