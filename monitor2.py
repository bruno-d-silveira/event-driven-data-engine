import os

class Dashboard:

    def __init__(self, stats, fila, update_interval):
        self.stats = stats
        self.fila = fila
        self.update_interval = update_interval

    def mostrar(self):

        os.system("cls" if os.name == "nt" else "clear")

        print(
            f"\r🧠 Det:{stats['detectados']} "
            f"📦 Mov:{stats['movidos']} "
            f"⚠ Ign:{stats['ignorados']} "
            f"🔄 Fila:{pool.fila.qsize()}",
            end=""
        )
