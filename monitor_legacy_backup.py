import sys
import os
import time
import hashlib

hashes_arquivos = {}

def calcular_hash(caminho):
    hash_md5 = hashlib.md5()

    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloco)

    return hash_md5.hexdigest()


def arquivo_duplicado(caminho):
    try:
        h = calcular_hash(caminho)
    except:
        return True

    if h in hashes_arquivos:
        return True
    else:
        hashes_arquivos[h] = caminho
        return False

from datetime import datetime

PASTA_PADRAO = r"C:\temp"

def log_evento(tipo, arquivo, pasta_destino=""):
    tempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"{tempo} | {tipo} | {arquivo} | pasta={pasta_destino}"

    os.makedirs(pasta_destino, exist_ok=True)

    with open(os.path.join(pasta_destino, "log.txt"), "a", encoding="utf-8") as f:
        f.write(linha + "\n")


PASTAS = [
    r"C:\temp",
    r"C:\Users\Bruno\Downloads",
    r"C:\Users\Bruno\Desktop"
]


 

if len(sys.argv) >= 2:
    pasta = sys.argv[1]
else:
    pasta = PASTA_PADRAO
    print(f"[INFO] usando pasta padrão → {pasta}")

          
mapa_tipos = {
    "mp3": "audios watcher",
    "mp4": "videos watcher",
    "png": "fotos watcher",
    "zip": "docs watcher"
}

regras_nome = {
    "sample": "samples",
    "mix": "mixes",
    "loop": "loops"
}
stats = {
    "detectados": 0,
    "movidos": 0,
    "ignorados": 0
}
fila_processamento = []
    
arquivos_anteriores = {p: os.listdir(p) for p in PASTAS} 


def classificar_e_mover(pasta, arquivo):

    nome_lower = arquivo.lower()

    # prioridade 1 → regras por nome
    for palavra, destino_nome in regras_nome.items():
        if palavra in nome_lower:
            destino = os.path.join(pasta, destino_nome)
            os.makedirs(destino, exist_ok=True)

            origem = os.path.join(pasta, arquivo)
            novo_caminho = os.path.join(destino, arquivo)

            try:
                os.rename(origem, novo_caminho)
            except FileNotFoundError:
                stats["ignorados"] += 1
                return

            stats["movidos"] += 1

            print(f"Movido por regra de nome → {destino_nome}")
            log_evento("MOVIDO", arquivo, f"destino={destino_nome}")
            return


    # prioridade 2 → regras por extensão
    extensao = arquivo.split(".")[-1].lower()

    if extensao in mapa_tipos:
        destino_nome = mapa_tipos[extensao]
        destino = os.path.join(pasta, destino_nome)

        os.makedirs(destino, exist_ok=True)

        origem = os.path.join(pasta, arquivo)
        novo_caminho = os.path.join(destino, arquivo)

        os.rename(origem, novo_caminho)
        stats["movidos"]+= 1

        print(f"Movido por extensão → {destino_nome}")
        log_evento("MOVIDO", arquivo, f"destino={destino_nome}")

while True:
    time.sleep(3)

    for pasta in PASTAS:

        arquivos_atuais = os.listdir(pasta)
        novos = [f for f in arquivos_atuais if f not in arquivos_anteriores[pasta]]

        for arquivo in novos:

            if arquivo == "log.txt":
                continue

            caminho_completo = os.path.join(pasta, arquivo)

            if not os.path.isfile(caminho_completo):
                stats["ignorados"] += 1 
                continue

            try:
                tamanho1 = os.path.getsize(caminho_completo)
                time.sleep(1)
                tamanho2 = os.path.getsize(caminho_completo)
            except FileNotFoundError:
                stats["ignorados"] += 1
                continue


            if tamanho1 != tamanho2:
                stats["ignorados"] += 1
                continue

            if fila_processamento:
                pasta_fila, arquivo_fila = fila_processamento.pop(0)
                classificar_e_mover(pasta_fila, arquivo_fila)


            print(f"[{pasta}] novo arquivo:", arquivo)

            stats["detectados"] += 1
            log_evento("DETECTADO", arquivo, pasta)

            caminho_completo = os.path.join(pasta, arquivo)

            if arquivo_duplicado(caminho_completo):
                stats["ignorados"] += 1
                continue

            fila_processamento.append((pasta, arquivo))


        arquivos_anteriores[pasta] = arquivos_atuais

    print(
    f"\r📥 Detectados:{stats['detectados']} | "
    f"📦 Movidos:{stats['movidos']} | "
    f"🚫 Ignorados:{stats['ignorados']}",
    end=""
)
  





input("Pressione Enter para sair...")


     

    
