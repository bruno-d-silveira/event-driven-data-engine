import os

import hashlib

pasta = input("Digite o caminho da pasta: ")

hashes = {}

def calcular_hash(caminho):
    hash_md5 = hashlib.md5()

    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloco)

    return hash_md5.hexdigest()


for nome in os.listdir(pasta):
    caminho = os.path.join(pasta, nome)

    if os.path.isfile(caminho):
        h = calcular_hash(caminho)
        if h in hashes:
            print("Duplicado encontrado:", nome, "==", hashes[h])
        else:
            hashes[h] = nome

