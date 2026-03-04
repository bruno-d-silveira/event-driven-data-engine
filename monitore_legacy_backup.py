print("bDs:", __file__)
from data_record import DataRecord
from monitor2 import Dashboard
from watcher2 import monitorar
from workers import WorkerPool
import json 
import os
import time
import hashlib
from datetime import datetime
import storage
from logger import log_evento
from event_bus import EventBus
from event_contract import EventType
storage.inicializar()
from metrics_module import MetricsCollector
from record_store import salvar as salvar_record
from dataset_builder.export_parquet import salvar_parquet
# =====================
# CONFIG
# =====================
PASTAS = [
    r"C:\temp",
    r"C:\Users\Bruno\Downloads",
    r"C:\Users\Bruno\Desktop"
]

# =====================
# HASH DUPLICADOS
# =====================
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
        return False
        

    if storage.hash_existe(h):
        return True
    
    storage.salvar_hash(h,caminho)
    return False     
# =====================
# REGRAS
# =====================
mapa_tipos = {
    "mp3": "audios",
    "mp4": "videos",
    "png": "imagens",
    "zip": "arquivos"
}

regras_nome = {
    "sample": "samples",
    "mix": "mixes",
    "loop": "loops"
}

# =====================
# STATS
# =====================
stats = {
        "detectados": 0,
        "movidos": 0,
        "ignorados": 0,
        }

# =====================
# MOVER ARQUIVO
# =====================
from rules import decidir_destino


def classificar_e_mover(record):
    global stats

    payload = record.payload
    pasta = payload["pasta"]
    arquivo = payload["arquivo"]

    origem = os.path.join(pasta, arquivo)
    destino = decidir_destino(pasta, arquivo)

    os.makedirs(destino, exist_ok=True)

    novo = os.path.join(destino, arquivo)

    try:
        os.rename(origem, novo)
    except FileNotFoundError:
        stats["ignorados"] += 1
        return
    except PermissionError:
        stats["ignorados"] += 1
        return

    stats["movidos"] += 1
    log_evento(
        "arquivo_movido",
        arquivo=arquivo,
        destino=destino
        )

    # Salvar no data lake APÓS sucesso
    salvar_parquet([{
        "timestamp": datetime.utcnow().isoformat(),
        "hour": datetime.utcnow().hour,
        "weekday": datetime.utcnow().weekday(),
        "event_type": "arquivo_processado",
        "extension": record.payload["arquivo"].split(".")[-1],
        "filename_length": len(record.payload["arquivo"]),
        "folder": record.payload["pasta"]
        }])
    
bus = EventBus()

def teste_alerta(data):
    print("EVENTO CAPTURADO:", data)

bus.subscribe(EventType.QUEUE_HIGH, teste_alerta)

def processador(record):
    classificar_e_mover(record)
    
pool = WorkerPool(4, processador, bus)

pool.iniciar()

dashboard = Dashboard(stats, pool.fila, 2)

metrics = MetricsCollector(pool.fila, stats)

# =====================
# LOOP PRINCIPAL
# =====================
estado = None

while True:

    eventos, estado = monitorar(PASTAS, estado)

    for evento in eventos:
        if evento.type != EventType.FILE_CREATED:
            continue

        payload = evento.payload
        record = DataRecord(payload)
        arquivo = payload["arquivo"]
        pasta = payload["pasta"]

        if arquivo == "log.txt":
            continue

        caminho = os.path.join(pasta, arquivo)

        # esperar arquivo estabilizar
        tentativas = 5
        while tentativas > 0:
            if os.path.isfile(caminho):
                break
            time.sleep(0.2)
            tentativas -=1

        if not os.path.isfile(caminho):
            stats["ignorados"] += 1
            continue

        stats["detectados"] += 1

        log_evento(
            "arquivo_detectado",
            arquivo=arquivo,
            pasta=pasta
            )
        if arquivo_duplicado(caminho):
            stats["ignorados"] += 1
            continue
        pool.adicionar(record)

    dashboard.mostrar()

    metrics.coletar()

    time.sleep(2)

    # worker da fila
    

    # dashboard
    dashboard.mostrar()

    time.sleep(2)
