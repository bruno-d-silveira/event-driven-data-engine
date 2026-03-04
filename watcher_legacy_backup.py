"""
watcher.py
Detector de eventos de arquivos.
"""

import os
from datetime import datetime


def snapshot_pasta(pasta):
    estado = {}

    try:
        arquivos = os.listdir(pasta)
    except FileNotFoundError:
        return estado

    for nome in arquivos:
        caminho = os.path.join(pasta, nome)

        if os.path.isfile(caminho):
            try:
                estado[nome] = os.path.getsize(caminho)
            except OSError:
                continue

    return estado


def monitorar(pastas, estado_anterior=None):
    if estado_anterior is None:
        estado_anterior = {}

    eventos = []

    for pasta in pastas:
        atual = snapshot_pasta(pasta)
        anterior = estado_anterior.get(pasta, {})

        # arquivos novos
        for nome in atual:
            if nome not in anterior:
                eventos.append({
                    "tipo": "CREATED",
                    "arquivo": nome,
                    "pasta": pasta,
                    "timestamp": datetime.now()
                })

        # arquivos removidos
        for nome in anterior:
            if nome not in atual:
                eventos.append({
                    "tipo": "DELETED",
                    "arquivo": nome,
                    "pasta": pasta,
                    "timestamp": datetime.now()
                })

        estado_anterior[pasta] = atual

    return eventos, estado_anterior


if __name__ == "__main__":
    pastas = ["C:/temp"]

    estado = None

    eventos, estado = monitorar(pastas, estado)

    for e in eventos:
        print(e)
