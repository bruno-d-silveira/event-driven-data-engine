import time
import csv
import os
from datetime import datetime

class MetricsCollector:
    def __init__(self, fila, stats, intervalo=2, arquivo_saida="metrics_log.csv"):
        self.fila = fila
        self.stats = stats
        self.intervalo = intervalo
        self.arquivo_saida = arquivo_saida
        self.ultimo_detectados = 0
        self.ultimo_movidos = 0
        self.ultimo_ignorados = 0
        self.ultimo_tempo = time.time()

        if not os.path.exists(self.arquivo_saida):
            with open(self.arquivo_saida, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "fila_tamanho",
                    "detectados_total",
                    "movidos_total",
                    "ignorados_total",
                    "detectados_por_intervalo",
                    "movidos_por_intervalo",
                    "ignorados_por_intervalo"
                ])

    def coletar(self):
        agora = time.time()
        if agora - self.ultimo_tempo < self.intervalo:
            return

        fila_tamanho = self.fila.qsize()

        detectados = self.stats["detectados"]
        movidos = self.stats["movidos"]
        ignorados = self.stats["ignorados"]

        detectados_delta = detectados - self.ultimo_detectados
        movidos_delta = movidos - self.ultimo_movidos
        ignorados_delta = ignorados - self.ultimo_ignorados

        with open(self.arquivo_saida, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                fila_tamanho,
                detectados,
                movidos,
                ignorados,
                detectados_delta,
                movidos_delta,
                ignorados_delta
            ])

        self.ultimo_detectados = detectados
        self.ultimo_movidos = movidos
        self.ultimo_ignorados = ignorados
        self.ultimo_tempo = agora
