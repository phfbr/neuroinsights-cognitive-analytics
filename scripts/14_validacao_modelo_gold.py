
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
GOLD = BASE / "dados" / "tratados" / "gold"
SILVER = BASE / "dados" / "tratados" / "nhanes_cognitivo_silver.parquet"

fato = pd.read_parquet(GOLD / "fato_avaliacao.parquet")
participantes = pd.read_parquet(GOLD / "dim_participante.parquet")
ciclos = pd.read_parquet(GOLD / "dim_ciclo.parquet")
testes = pd.read_parquet(GOLD / "dim_teste.parquet")
silver = pd.read_parquet(SILVER)

print("\nNEUROINSIGHTS | VALIDAÇÃO DO MODELO GOLD")
print("=" * 60)

validacoes = {}

# Chaves das dimensões
validacoes["Participantes únicos"] = (
    participantes["id_participante"].is_unique
)

validacoes["Ciclos únicos"] = ciclos["ciclo"].is_unique

validacoes["Testes únicos"] = testes["id_teste"].is_unique

# Integridade referencial
validacoes["Participantes existentes"] = (
    fato["id_participante"]
    .isin(participantes["id_participante"])
    .all()
)

validacoes["Ciclos existentes"] = (
    fato["ciclo"].isin(ciclos["ciclo"]).all()
)

validacoes["Testes existentes"] = (
    fato["id_teste"].isin(testes["id_teste"]).all()
)

# Granularidade
validacoes["Sem avaliações duplicadas"] = (
    ~fato.duplicated(["id_participante", "id_teste"]).any()
)

validacoes["Seis avaliações por participante"] = (
    fato.groupby("id_participante").size().eq(6).all()
)

# Ciclo correto para cada participante
conferencia = fato[
    ["id_participante", "ciclo"]
].merge(
    silver[["id_participante", "ciclo"]],
    on="id_participante",
    how="left",
    suffixes=("_fato", "_silver"),
    validate="many_to_one"
)

validacoes["Ciclo consistente com Silver"] = (
    conferencia["ciclo_fato"]
    .eq(conferencia["ciclo_silver"])
    .all()
)

# Pontuações e valores ausentes
validacoes["Disponibilidade consistente"] = (
    fato["pontuacao_registrada"]
    .eq(fato["pontuacao"].notna())
    .all()
)

validacoes["Total de avaliações correto"] = (
    len(fato) == len(participantes) * len(testes)
)

for nome, aprovado in validacoes.items():
    print(f"[{'OK' if aprovado else 'FALHOU'}] {nome}")

total = len(validacoes)
aprovados = sum(validacoes.values())

print("\n" + "=" * 60)
print(f"Testes aprovados: {aprovados}/{total}")

if not all(validacoes.values()):
    raise SystemExit("MODELO GOLD REPROVADO")

print("MODELO GOLD VALIDADO COM SUCESSO!")
