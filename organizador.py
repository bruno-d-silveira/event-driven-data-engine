import os
import shutil

pasta = input("Digite o caminho da pasta: ")

mapa = {
    "audios": ["mp3","wav","flac"],
    "videos": ["mp4","mkv","mov"],
    "photos": ["png","jpg","jpeg"],
    "docs": ["zip","rar","7z","pdf","docx"]
}

log = open("log.txt","a", encoding="utf-8")

for arquivo in os.listdir(pasta):

    caminho = os.path.join(pasta, arquivo)

    if os.path.isfile(caminho):

        extensao = arquivo.split(".")[-1].lower()

        destino = "outros"

        for pasta_destino, tipos in mapa.items():
            if extensao in tipos:
                destino = pasta_destino

        pasta_final = os.path.join(pasta, destino)
        os.makedirs(pasta_final, exist_ok=True)

        novo_caminho = os.path.join(pasta_final, arquivo)

        try:
            shutil.move(caminho, novo_caminho)
            log.write(f"{arquivo} -> {destino}\n")
        except Exception as e:
            log.write(f"ERRO: {arquivo} não movido ({e})\n")


            log.write(f"{arquivo} → {destino}\n")

log.close()

print("Organização concluída.")
