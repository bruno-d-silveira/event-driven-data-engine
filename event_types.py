from enum import Enum

class EventType(Enum):
    QUEUE_HIGH = "queue_high"
    QUEUE_FULL = "queue_full"
    WORKER_ERROR = "worker_error"
    TASK_START = "task_start"
    TASK_FINISH = "task_finish"
