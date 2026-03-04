import traceback
from datetime import datetime
from logger import log_evento


def executar_seguro(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)

    except Exception:
        erro = traceback.format_exc()

        print("\n[ERRO CAPTURADO]")
        print(erro)

        log_evento(
            "erro",
            erro=erro
        )

        with open("crash.log", "a", encoding="utf-8") as f:
            f.write(f"\n{datetime.now()}\n")
            f.write(erro)
            f.write("\n----------------\n")

        return None
