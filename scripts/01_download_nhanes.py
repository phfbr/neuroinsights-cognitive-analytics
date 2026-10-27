
from pathlib import Path
import requests

# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DESTINO = BASE_DIR / "dados" / "brutos"
DESTINO.mkdir(parents=True, exist_ok=True)

# Arquivos oficiais do CDC
BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public"

ARQUIVOS = {
    "CFQ_G.xpt": f"{BASE_URL}/2011/DataFiles/CFQ_G.xpt",
    "CFQ_H.xpt": f"{BASE_URL}/2013/DataFiles/CFQ_H.xpt",
    "DEMO_G.xpt": f"{BASE_URL}/2011/DataFiles/DEMO_G.xpt",
    "DEMO_H.xpt": f"{BASE_URL}/2013/DataFiles/DEMO_H.xpt",
}


def baixar_arquivo(nome, url):
    caminho = DESTINO / nome

    if caminho.exists() and caminho.stat().st_size > 0:
        print(f"[EXISTENTE] {nome}")
        return True

    print(f"[BAIXANDO] {nome}")

    temporario = caminho.with_suffix(".tmp")

    try:
        with requests.get(url, timeout=60, stream=True) as resposta:
            resposta.raise_for_status()

            with open(temporario, "wb") as arquivo:
                for bloco in resposta.iter_content(chunk_size=8192):
                    if bloco:
                        arquivo.write(bloco)

        if temporario.stat().st_size == 0:
            raise ValueError("Arquivo vazio.")

        with open(temporario, "rb") as arquivo:
            inicio = arquivo.read(100)

        if not inicio.startswith(b"HEADER RECORD"):
            raise ValueError("Formato XPT inválido ou inesperado.")

        temporario.replace(caminho)

        tamanho = caminho.stat().st_size / (1024 * 1024)
        print(f"[OK] {nome} | {tamanho:.2f} MB")
        return True

    except (requests.RequestException, OSError, ValueError) as erro:
        print(f"[ERRO] {nome}: {erro}")
        temporario.unlink(missing_ok=True)
        return False


if __name__ == "__main__":
    print("\nNEUROINSIGHTS | DOWNLOAD NHANES")
    print("-" * 45)

    resultados = [
        baixar_arquivo(nome, url)
        for nome, url in ARQUIVOS.items()
    ]

    print("-" * 45)
    print(f"Arquivos baixados/verificados: {sum(resultados)}/4")

    if not all(resultados):
        raise SystemExit("Download incompleto. Verifique os erros.")

    print("Download finalizado com sucesso!")
