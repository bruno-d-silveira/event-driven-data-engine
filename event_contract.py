from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import uuid


class EventType(str, Enum):
    FILE_CREATED = "FILE_CREATED"
    FILE_DELETED = "FILE_DELETED"
    FILE_MODIFIED = "FILE_MODIFIED"

    QUEUE_HIGH = "QUEUE_HIGH"
    WORKER_ERROR = "WORKER_ERROR"

    ENGINE_START = "ENGINE_START"
    ENGINE_STOP = "ENGINE_STOP"


@dataclass(frozen=True, slots=True)
class Event:
    id: str
    type: EventType
    timestamp: str
    source: str
    payload: dict
    meta: dict

    @staticmethod
    def create(type: EventType, source: str, payload: dict, meta: dict | None = None):
        return Event(
            id=str(uuid.uuid4()),
            type=type,
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=source,
            payload=payload,
            meta={
                "version": 1,
                **(meta or {})
            }
        )
