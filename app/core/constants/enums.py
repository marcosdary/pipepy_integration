from enum import Enum


class Status(Enum):
    """
    Status de processamento do webhook.
    """

    # Webhook processado com sucesso
    processed = "processed"

    # Webhook rejeitado
    rejected = "rejected"

    # Webhook pendente de processamento
    pending = "pending"

    # Falha durante o processamento
    failed = "failed"


class Priority(Enum):
    """
    Prioridade atribuída ao cliente.
    """

    # Prioridade padrão
    prioridade_normal = "prioridade_normal"

    # Prioridade elevada
    prioridade_alta = "prioridade_alta"