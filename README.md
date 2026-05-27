# pipepy_integration

API FastAPI para integracao com Pipefy, com persistencia em PostgreSQL e cliente Redis configurado por variaveis de ambiente.

## Requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) para gerenciar dependencias e ambiente virtual
- PostgreSQL acessivel localmente
- Redis acessivel localmente

## Configuracao local

1. Instale as dependencias do projeto:

```bash
uv sync
```

2. Crie o arquivo de variaveis de ambiente a partir do exemplo:

```bash
cp .env.example .env
```

3. Ajuste o arquivo `.env` com as URLs dos servicos locais. O nome esperado pela aplicacao para o banco e `DATABASE_URL`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:SENHA@localhost:5432/postgres
REDIS_URL=redis://localhost:6379
```

4. Crie as estruturas do banco executando o script SQL:

```bash
psql "postgresql://postgres:SENHA@localhost:5432/postgres" -f db/script.sql
```

Altere usuario, senha, host, porta e banco conforme o seu ambiente.

## Execucao local

Com as dependencias instaladas e o `.env` configurado, suba a API em modo de desenvolvimento:

```bash
uv run fastapi dev app/main.py
```

Alternativamente, execute diretamente com Uvicorn:

```bash
uv run uvicorn app.main:app --reload
```

Por padrao, a aplicacao fica disponivel em:

- API: `http://127.0.0.1:8000`
- Documentacao Swagger: `http://127.0.0.1:8000/docs`
- GraphQL: `http://127.0.0.1:8000/graphql`

## Testes

Execute toda a suite de testes com:

```bash
uv run pytest
```

Para executar um arquivo especifico:

```bash
uv run pytest tests/test_customer.py
```

Os testes usam as mesmas configuracoes de ambiente da aplicacao. Garanta que o PostgreSQL esteja acessivel e que as tabelas de `db/script.sql` tenham sido criadas antes de executar testes que acessam o banco.
