
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
ARQUIVO = (
    BASE / "dados" / "tratados"
    / "nhanes_cognitivo_silver.parquet"
)

df = pd.read_parquet(ARQUIVO)

TESTES = [
    "memoria_tentativa_1",
    "memoria_tentativa_2",
    "memoria_tentativa_3",
    "memoria_tardia",
    "fluencia_verbal",
    "velocidade_processamento",
]

print("\nNEUROINSIGHTS | VALIDAÇÃO SILVER")
print("=" * 55)

verificacoes = {
    "Quantidade de registros": len(df) == 3472,
    "IDs únicos": df["id_participante"].is_unique,
    "IDs preenchidos": df["id_participante"].notna().all(),
    "Faixas etárias preenchidas": df["faixa_etaria"].notna().all(),
    "Ciclos esperados": set(df["ciclo"].unique())
        == {"2011-2012", "2013-2014"},
    "Idades a partir de 60": df["idade"].ge(60).all(),
}

for teste in TESTES:
    verificacoes[f"Disponibilidade: {teste}"] = (
        df[f"{teste}_registrado"].eq(
            df[teste].notna()
        ).all()
    )

for nome, resultado in verificacoes.items():
    status = "OK" if resultado else "FALHOU"
    print(f"[{status}] {nome}")

aprovados = sum(verificacoes.values())
total = len(verificacoes)

print("\n" + "=" * 55)
print(f"Testes aprovados: {aprovados}/{total}")

if not all(verificacoes.values()):
    raise SystemExit("VALIDAÇÃO REPROVADA")

print("CAMADA SILVER VALIDADA!")
