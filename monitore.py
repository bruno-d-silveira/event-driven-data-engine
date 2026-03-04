print("[Brain is alive]")
import json 
import os
import time
import hashlib
from datetime import datetime, timezone
import storage
from logger import log_evento
from event_bus import EventBus
from event_contract import EventType
from metrics_module import MetricsCollector
from record_store import salvar as salvar_record
from dataset_builder.export_parquet import salvar_parquet
from data_record import DataRecord
from monitor2 import Dashboard
from watcher2 import monitorar
from workers import WorkerPool
from rules import decidir_destino
import logging


# Inicialização do storage
storage.inicializar()

# =====================
# CONFIG
# =====================
PASTAS = [
    r"C:\temp",
    r"C:\Users\Bruno\Downloads",
    r"C:\Users\Bruno\Desktop"
]

# =====================
# STATS
# =====================
stats = {
    "detectados": 0,
    "movidos": 0,
    "ignorados": 0,
}

# =====================
# CHAVEAMENTO DE ARQUIVOS
# =====================
hashes_arquivos = {}

def calcular_hash(caminho):
    """Calcula o hash MD5 de um arquivo."""
    hash_md5 = hashlib.md5()
    
    try:
        with open(caminho, "rb") as f:
            for bloco in iter(lambda: f.read(4096), b""):
                hash_md5.update(bloco)
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado ao calcular hash: {caminho}")
        return None
    return hash_md5.hexdigest()

def arquivo_duplicado(caminho):

    h = calcular_hash(caminho)
    
    if h is None:
        return None  # erro ao calcular

    if storage.hash_existe(h):
        return True
    
    return h  # retorna hash calculado, mas NÃO salva

# =====================
# CLASSIFICAR E MOVER ARQUIVOS
# =====================
def classificar_e_mover(record):
    global stats

    payload = record.payload
    pasta = payload["pasta"]
    arquivo = payload["arquivo"]

    # Anteriormente calculado
    file_hash = payload["hash"]

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
    except Exception:
        stats["ignorados"] += 1
        return

    # ===== COMMIT REAL =====
    stats["movidos"] += 1  

    storage.salvar_hash(file_hash, novo)

    salvar_parquet([{
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hour": datetime.now(timezone.utc).hour,
        "weekday": datetime.now(timezone.utc).weekday(),
        "event_type": "arquivo_processado",
        "extension": arquivo.split(".")[-1],
        "filename_length": len(arquivo),
        "folder": pasta
    }])

    log_evento("arquivo_movido", arquivo=arquivo, destino=destino)

# =====================
# INICIALIZAÇÃO DO EVENT BUS
# =====================
bus = EventBus()
bus.subscribe(EventType.QUEUE_HIGH, lambda data: print("EVENTO CAPTURADO:", data))

# =====================
# PROCESSO E INICIALIZAÇÃO
# =====================
pool = WorkerPool(4, classificar_e_mover, bus)
pool.iniciar()

dashboard = Dashboard(stats, pool.fila, 0.1) # dashboard = Dashboard(stats, pool.fila, 0.1)
metrics = MetricsCollector(pool.fila, stats) 
# =====================
# LOOP PRINCIPAL
# =====================

estado = None

try:
    while True:

        
        eventos, estado = monitorar(PASTAS, estado)

        if eventos:
            print(f"{len(eventos)} evento(s) detectado(s)")

        for evento in eventos:

            stats["detectados"] += 1
            log_evento(
                "arquivo_detectado",
                arquivo=payload["arquivo"],
                pasta=payload["pasta"]
            )
            
            if evento.type != EventType.FILE_CREATED:
                continue
            stats["detectados"] += 1

            payload = evento.payload
            record = DataRecord(payload)

            caminho = os.path.join(payload["pasta"], payload["arquivo"])

            if not os.path.isfile(caminho):
                continue

            resultado_hash = arquivo_duplicado(caminho)

            if resultado_hash is True or resultado_hash is None:
                continue

            payload["hash"] = resultado_hash
            pool.adicionar(record)

        metrics.coletar()

        print(
            f"\rDetectados:{stats['detectados']} "
            f"Movidos:{stats['movidos']} "
            f"Ignorados:{stats['ignorados']} "
            f"Fila:{pool.fila.qsize()}",
            end=""
        )

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nEncerrando engine...")
    pool.parar()
