import json
import os
from datetime import datetime

PASTA = "records"


def salvar(record):

    os.makedirs(PASTA, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

    caminho = os.path.join(PASTA, f"{timestamp}.json")

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(
            {
                "payload": record.payload,
                "features": record.features,
                "meta": record.meta
            },
            f,
            ensure_ascii=False,
            indent=2
        )
