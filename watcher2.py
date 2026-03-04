from safeexec import executar_seguro
"""
watcher2.py
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


from event_contract import Event, EventType


def monitorar(pastas, estado_anterior=None):

    # WARM START CORRETO
    if estado_anterior is None:
        estado_anterior = {}
        for pasta in pastas:
            estado_anterior[pasta] = snapshot_pasta(pasta)
        return [], estado_anterior

    eventos = []

    for pasta in pastas:
        atual = snapshot_pasta(pasta)
        anterior = estado_anterior.get(pasta, {})

        # arquivos novos
        for nome in atual:
            if nome not in anterior:
                eventos.append(
                    Event.create(
                        type=EventType.FILE_CREATED,
                        source="watcher",
                        payload={
                            "arquivo": nome,
                            "pasta": pasta,
                            "size": atual[nome]
                        }
                    )
                )

        # arquivos removidos
        for nome in anterior:
            if nome not in atual:
                eventos.append(
                    Event.create(
                        type=EventType.FILE_DELETED,
                        source="watcher",
                        payload={
                            "arquivo": nome,
                            "pasta": pasta
                        }
                    )
                )

        estado_anterior[pasta] = atual

    return eventos, estado_anterior
