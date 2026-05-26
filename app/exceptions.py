from fastapi import status

"""
Módulo de Exceções Personalizadas - versão FastAPI.

Define exceções específicas para tratamento de erros na aplicação,
incluindo autenticação, autorização, recursos não encontrados, integridade,
validação, limites de requisições e erros desconhecidos.
"""


# =============================================================================
# EXCEÇÕES HTTP 403 - AUTORIZAÇÃO / AÇÕES PROTEGIDAS
# =============================================================================
class ProtectedRouteError(Exception):
    """Acesso a rota protegida sem permissão adequada.

    Attributes:
        status_code (int): Código HTTP 403.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_403_FORBIDDEN


class ForbiddenActionError(Exception):
    """Tentativa de realizar uma ação proibida ou protegida.

    Attributes:
        status_code (int): Código HTTP 403.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_403_FORBIDDEN


# =============================================================================
# EXCEÇÕES HTTP 404 - RECURSO / CONSULTA
# =============================================================================
class NotFoundError(Exception):
    """Erro quando um recurso solicitado não é encontrado.

    Attributes:
        status_code (int): Código HTTP 404.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND


# =============================================================================
# EXCEÇÕES HTTP 409 - INTEGRIDADE / DUPLICIDADE
# =============================================================================
class DuplicateReviewError(Exception):
    """Tentativa de inserir um registro duplicado.

    Attributes:
        status_code (int): Código HTTP 409.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_409_CONFLICT

# =============================================================================
# EXCEÇÕES HTTP 422 - VALIDAÇÃO DE DADOS
# =============================================================================
class EntityValidationError(Exception):
    """Falha de validação ao inserir ou atualizar dados de uma entidade.

    Attributes:
        status_code (int): Código HTTP 422.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT


class InvalidFieldsException(Exception):
    """Campos obrigatórios estão ausentes ou inválidos.

    Attributes:
        status_code (int): Código HTTP 422.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT


class UnprocessableEntity(Exception):
    """Erro de consistência ou semântica nos dados.

    Attributes:
        status_code (int): Código HTTP 422.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT