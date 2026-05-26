from enum import Enum

class TypeOfRequest(Enum):
    wait = "wait"
    to_update = "to_update"


class Status(Enum):
    processed = "processed"
    rejected = "rejected"
    pending = "pending"
    failed = "failed"

class Priority(Enum): 
    prioridade_normal = 'prioridade_normal'
    prioridade_alta = 'prioridade_alta'