import threading
import queue
from event_types import EventType
from safeexec import executar_seguro


class WorkerPool:
    def __init__(self, num_workers, processador, event_bus):
        self.event_bus = event_bus
        self.fila = queue.Queue(maxsize=1000)
        self.num_workers = num_workers
        self.processador = processador
        self.threads = []
        self.rodando = False

    def worker_loop(self):
        
        while self.rodando:
            try:
                item = self.fila.get(timeout=1)
                print("Worker pegou item:", item)
            except queue.Empty:
                continue

            try:
                print("Chamando processador")
                executar_seguro(self.processador, item)
            except Exception as e:
                print("Erro worker:", e)

            self.fila.task_done()

    def iniciar(self):
        self.rodando = True
        for _ in range(self.num_workers):
            t = threading.Thread(target=self.worker_loop, daemon=True)
            t.start()
            self.threads.append(t)

    def adicionar(self, item):
        if self.fila.qsize() > self.fila.maxsize * 0.8:
            self.event_bus.emit(EventType.QUEUE_HIGH, tamanho=self.fila.qsize())

        self.fila.put(item, timeout=1)

    def parar(self):
        self.rodando = False
