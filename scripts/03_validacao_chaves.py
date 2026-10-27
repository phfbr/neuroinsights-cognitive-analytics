
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
BRUTOS = BASE_DIR / "dados" / "brutos"

CICLOS = {
    "2011-2012": ("CFQ_G.xpt", "DEMO_G.xpt"),
    "2013-2014": ("CFQ_H.xpt", "DEMO_H.xpt"),
}

print("\nNEUROINSIGHTS | VALIDAÇÃO DE CHAVES")
print("=" * 55)

for ciclo, (arquivo_cfq, arquivo_demo) in CICLOS.items():

    cognitivo = pd.read_sas(
        BRUTOS / arquivo_cfq,
        format="xport"
    )

    demografia = pd.read_sas(
        BRUTOS / arquivo_demo,
        format="xport"
    )

    # Garantir que as chaves sejam únicas
    assert cognitivo["SEQN"].is_unique
    assert demografia["SEQN"].is_unique

    # Validar correspondência entre as bases
    validacao = cognitivo[["SEQN"]].merge(
        demografia[["SEQN"]],
        on="SEQN",
        how="left",
        indicator=True,
        validate="one_to_one"
    )

    correspondentes = (
        validacao["_merge"] == "both"
    ).sum()

    sem_correspondencia = (
        validacao["_merge"] == "left_only"
    ).sum()

    percentual = (
        correspondentes / len(cognitivo) * 100
        if len(cognitivo) > 0 else 0
    )

    print(f"\nCICLO: {ciclo}")
    print("-" * 55)
    print(f"Registros cognitivos: {len(cognitivo)}")
    print(f"Registros demográficos: {len(demografia)}")
    print(f"Chaves correspondentes: {correspondentes}")
    print(f"Sem correspondência: {sem_correspondencia}")
    print(f"Taxa de correspondência: {percentual:.2f}%")

print("\n" + "=" * 55)
print("VALIDAÇÃO FINALIZADA!")
