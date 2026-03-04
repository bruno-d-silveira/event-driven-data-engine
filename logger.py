import json
import os
from datetime import datetime
import threading

PASTA_LOG = "logs"
os.makedirs(PASTA_LOG, exist_ok=True)

ARQUIVO_LOG = os.path.join(PASTA_LOG, "eventos.jsonl")

def log_evento(tipo, **dados):
    registro = {
        "timestamp": datetime.now().isoformat(),
        "thread": threading.current_thread().name,
        "tipo": tipo,
        **dados
    }

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
