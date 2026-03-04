import os
from pathlib import Path

BASE_DESTINO = r"C:\organizado"  # ajuste se quiser outra raiz


def decidir_destino(pasta_origem, arquivo):
    """
    Organiza exclusivamente por extensão.
    Exemplo:
    C:\organizado\txt
    C:\organizado\pdf
    C:\organizado\mp3
    """

    # Extrai extensão de forma segura
    ext = Path(arquivo).suffix.lower().replace(".", "")

    if not ext:
        ext = "sem_extensao"

    return os.path.join(BASE_DESTINO, ext)
