
from pathlib import Path
import pandas as pd
import pyreadstat

BASE = Path(__file__).resolve().parent.parent
BRUTOS = BASE / "dados" / "brutos"
TRATADOS = BASE / "dados" / "tratados"

TRATADOS.mkdir(parents=True, exist_ok=True)

CICLOS = {
    "2011-2012": ("CFQ_G.xpt", "DEMO_G.xpt"),
    "2013-2014": ("CFQ_H.xpt", "DEMO_H.xpt")
}

COLUNAS_DEMO = [
    "SEQN",
    "RIDAGEYR",  # Idade
    "RIAGENDR",  # Sexo
    "RIDRETH3",  # Grupo demográfico
    "DMDEDUC2",  # Escolaridade
    "WTMEC2YR",  # Peso amostral
    "SDMVPSU",   # Unidade amostral
    "SDMVSTRA"   # Estrato amostral
]

bases_integradas = []

print("\nNEUROINSIGHTS | INTEGRAÇÃO DE DADOS")
print("=" * 60)

for ciclo, (arquivo_cfq, arquivo_demo) in CICLOS.items():

    cognitivo, _ = pyreadstat.read_xport(
        str(BRUTOS / arquivo_cfq)
    )

    demografia, _ = pyreadstat.read_xport(
        str(BRUTOS / arquivo_demo)
    )

    # Selecionar variáveis demográficas
    demografia = demografia[COLUNAS_DEMO].copy()

    # Validar unicidade
    assert cognitivo["SEQN"].is_unique
    assert demografia["SEQN"].is_unique

    # Integração por participante
    integrado = cognitivo.merge(
        demografia,
        on="SEQN",
        how="left",
        validate="one_to_one",
        indicator=True
    )

    sem_correspondencia = (
        integrado["_merge"] != "both"
    ).sum()

    if sem_correspondencia > 0:
        raise ValueError(
            f"{ciclo}: {sem_correspondencia} sem correspondência"
        )

    integrado = integrado.drop(columns="_merge")

    integrado["ciclo"] = ciclo

    # Preservar pontuações originais nesta etapa
    bases_integradas.append(integrado)

    print(f"\nCICLO: {ciclo}")
    print(f"Participantes: {len(integrado)}")
    print(f"Colunas: {len(integrado.columns)}")
    print(f"Chaves sem correspondência: {sem_correspondencia}")

# Unificar os ciclos
base_final = pd.concat(
    bases_integradas,
    ignore_index=True
)

# Chave composta para rastreabilidade
base_final["id_participante"] = (
    base_final["ciclo"]
    + "_"
    + base_final["SEQN"].astype("Int64").astype(str)
)

# Salvar base integrada
destino = TRATADOS / "nhanes_cognitivo_integrado.parquet"

base_final.to_parquet(
    destino,
    index=False
)

print("\n" + "=" * 60)
print("BASE INTEGRADA")
print(f"Registros: {len(base_final)}")
print(f"Colunas: {len(base_final.columns)}")
print(f"Chaves únicas: {base_final['id_participante'].is_unique}")
print(f"Arquivo salvo: {destino}")
print("INTEGRAÇÃO FINALIZADA!")
