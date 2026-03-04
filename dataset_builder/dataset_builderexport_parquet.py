import os
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

BASE_DIR = "datasets"

def salvar_parquet(registros):
    if not registros:
        return

    timestamp = registros[0]["timestamp"]
    pasta = _obter_pasta_particao(timestamp)

    os.makedirs(pasta, exist_ok=True)

    indice = _proximo_indice(pasta)
    caminho = os.path.join(pasta, f"data_{indice:04}.parquet")

    tabela = pa.Table.from_pylist(registros)
    pq.write_table(tabela, caminho)


def _obter_pasta_particao(timestamp):
    dt = datetime.fromisoformat(timestamp)

    return os.path.join(
        BASE_DIR,
        f"year={dt.year}",
        f"month={dt.month:02}",
        f"day={dt.day:02}"
    )


def _proximo_indice(pasta):

    arquivos = [
        f for f in os.listdir(pasta)
        if f.startswith("data_") and f.endswith(".parquet")
    ]

    if not arquivos:
        return 1

    nums = [int(a.split("_")[1].split(".")[0]) for a in arquivos]
    return max(nums) + 1
