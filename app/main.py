from fastapi import (
    FastAPI,
    Request,
    status
)
from fastapi.exceptions import (
    HTTPException,
    RequestValidationError
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# API
from app.api import v1

# Integrations
from app.integrations.pipefy import graphql

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Integração com Pepify",
    version="0.1.0",
)

# Configuração de CORS
#
# allow_origins:
#   Define quais origens podem acessar a API.
#
# allow_methods:
#   Métodos HTTP permitidos.
#
# allow_headers:
#   Headers permitidos nas requisições.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Registra as rotas REST da API v1
app.include_router(
    v1.router,
    prefix="/api/v1"
)

# Registra as rotas GraphQL
app.include_router(
    graphql.router,
    prefix="/graphql",
    tags=["GraphQL", "Exemplo do Pepify"]
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Manipula erros de validação do FastAPI/Pydantic.

    Args:
        request:
            Requisição HTTP recebida.

        exc:
            Exceção de validação lançada pelo FastAPI.

    Returns:
        JSONResponse:
            Resposta padronizada contendo os erros.
    """

    # Formata os erros de validação
    messages = [
        {
            "msg": error["msg"],
            "loc": error["loc"]
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": messages
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    """
    Manipula exceções HTTP customizadas.

    Args:
        request:
            Requisição HTTP recebida.

        exc:
            Exceção HTTP lançada pela aplicação.

    Returns:
        JSONResponse:
            Resposta padronizada contendo detalhes do erro.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": [
                {
                    "msg": exc.detail
                }
            ],
        },
    )


@app.get("/")
def index():
    """
    Endpoint inicial da aplicação.

    Returns:
        dict:
            Informações básicas da API.
    """

    return {
        "version": "1.0.0",
        "name": "Integração com Pepify"
    }