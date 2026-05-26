from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def index():
    return {
        "version": "1.0.0",
        "name": "Integração com Pepify"
    }

