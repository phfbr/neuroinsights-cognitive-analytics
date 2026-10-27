
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
GOLD = BASE / "dados" / "tratados" / "gold"

amostra = pd.read_parquet(
    GOLD / "dim_amostragem.parquet"
)

print("\nNEUROINSIGHTS | AUDITORIA AMOSTRAL")
print("=" * 55)

# Cada combinação estrato + PSU representa
# uma identificação amostral distinta.
pares = amostra[
    ["estrato_amostral", "unidade_amostral"]
].drop_duplicates()

print(f"Participantes: {len(amostra)}")
print(f"Estratos: {amostra['estrato_amostral'].nunique()}")
print(f"Combinações estrato/PSU: {len(pares)}")

print("\nEstratos por ciclo:")
print(
    amostra.groupby("ciclo")[
        "estrato_amostral"
    ].nunique()
)

print("\nPSUs distintas por estrato:")
psus = (
    pares.groupby("estrato_amostral")
    ["unidade_amostral"]
    .nunique()
)

print(psus.value_counts().sort_index())

print("\nPesos amostrais por ciclo:")
print(
    amostra.groupby("ciclo")[
        "peso_amostral_4anos"
    ].agg(["count", "min", "max", "sum"])
)

print("\nAUDITORIA AMOSTRAL FINALIZADA!")
