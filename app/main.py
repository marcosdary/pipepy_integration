from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import (
    RequestValidationError, 
    HTTPException
)

from app.api import v1
from app.integrations.pipefy import graphql


app = FastAPI(title="Integração com Pepify", version="0.1.0", )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET","POST"],
    allow_headers=["*"],
)

app.include_router(v1.router, prefix="/api/v1")
app.include_router(graphql.router, prefix="/graphql", tags=["GraphQL", "Exemplo do Pepify"])

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = [
        {
            "msg": error["msg"],
            "loc": error["loc"]
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": messages}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": [{"msg": exc.detail}],
        },
    )

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Integração com Pepify"
    }
