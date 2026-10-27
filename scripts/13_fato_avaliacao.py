
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
TRATADOS = BASE / "dados" / "tratados"
GOLD = TRATADOS / "gold"

print("\nNEUROINSIGHTS | FATO AVALIAÇÃO")
print("=" * 55)

# Ler dados
df = pd.read_parquet(
    TRATADOS / "nhanes_cognitivo_silver.parquet"
)

dim_participante = pd.read_parquet(
    GOLD / "dim_participante.parquet"
)

dim_ciclo = pd.read_parquet(
    GOLD / "dim_ciclo.parquet"
)

dim_teste = pd.read_parquet(
    GOLD / "dim_teste.parquet"
)

# Transformar as seis pontuações em linhas
fato = df[
    ["id_participante", "ciclo"]
    + dim_teste["variavel"].tolist()
].melt(
    id_vars=["id_participante", "ciclo"],
    var_name="variavel",
    value_name="pontuacao"
)

# Adicionar chave do teste
fato = fato.merge(
    dim_teste[["id_teste", "variavel"]],
    on="variavel",
    how="left",
    validate="many_to_one"
)

# Indicador de pontuação registrada
fato["pontuacao_registrada"] = (
    fato["pontuacao"].notna()
)

# Manter somente colunas necessárias
fato = fato[
    [
        "id_participante",
        "ciclo",
        "id_teste",
        "pontuacao",
        "pontuacao_registrada"
    ]
].copy()

# Validações
esperado = len(df) * len(dim_teste)

assert len(fato) == esperado

assert not fato.duplicated(
    ["id_participante", "id_teste"]
).any()

assert fato["id_participante"].isin(
    dim_participante["id_participante"]
).all()

assert fato["ciclo"].isin(
    dim_ciclo["ciclo"]
).all()

assert fato["id_teste"].isin(
    dim_teste["id_teste"]
).all()

assert fato["id_teste"].notna().all()

# Verificar se as contagens coincidem com a Silver
contagens = fato.groupby(
    "id_teste"
)["pontuacao_registrada"].sum()

for _, teste in dim_teste.iterrows():
    esperado_teste = df[teste["variavel"]].notna().sum()
    observado = contagens.loc[teste["id_teste"]]

    assert observado == esperado_teste, (
        f"Contagem divergente: {teste['variavel']}"
    )

# Salvar
destino = GOLD / "fato_avaliacao.parquet"

fato.to_parquet(destino, index=False)

print(f"Participantes: {len(df)}")
print(f"Testes: {len(dim_teste)}")
print(f"Registros na fato: {len(fato)}")

print("\nDisponibilidade por teste:")

resumo = (
    fato.groupby("id_teste")["pontuacao_registrada"]
    .agg(["sum", "count"])
    .reset_index()
    .merge(
        dim_teste[["id_teste", "teste"]],
        on="id_teste"
    )
)

resumo["percentual"] = (
    resumo["sum"] / resumo["count"] * 100
).round(2)

print(
    resumo[
        ["teste", "sum", "count", "percentual"]
    ].to_string(index=False)
)

print(f"\nArquivo salvo: {destino}")
print("FATO AVALIAÇÃO VALIDADA COM SUCESSO!")
