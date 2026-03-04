import matplotlib.pyplot as plt

class Dashboard:

    def __init__(self, stats, fila, update_interval):
        self.stats = stats
        self.fila = fila
        self.update_interval = update_interval
        self.history = []

    def mostrar(self):
        plt.clf()

        # Estatísticas
        plt.subplot(211)
        plt.title("Estatísticas do Monitor")
        plt.bar(
            ['Detectados', 'Movidos', 'Ignorados'],
            [
                self.stats["detectados"],
                self.stats["movidos"],
                self.stats["ignorados"]
            ]
        )

        # Histórico da fila
        self.history.append(self.fila.qsize())

        plt.subplot(212)
        plt.title("Fila de Processamento")
        plt.plot(self.history)

        plt.pause(self.update_interval)
