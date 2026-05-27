# pipepy_integration

API FastAPI para integração com Pipefy, com persistência em PostgreSQL e cliente Redis configurado por variáveis de ambiente.

## Requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/) para gerenciar dependências e ambiente virtual
- PostgreSQL acessível localmente
- Redis acessível localmente

---

# Configuração Local

## Instalação das Dependências

### Windows

#### 1. Instale as dependências do projeto

```bash
uv sync
```

#### 1.2 Alternativa usando pip

```bash
py -m pip install -r requirements.txt
```

---

### Linux

#### 1. Instale as dependências do projeto

```bash
uv sync
```

#### 1.2 Alternativa usando pip

```bash
python3 -m pip install -r requirements.txt
```

---

### macOS (Apple)

#### 1. Instale as dependências do projeto

```bash
uv sync
```

#### 1.2 Alternativa usando pip

```bash
python3 -m pip install -r requirements.txt
```

---

## 2. Crie o arquivo de variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

---

## 3. Configure o arquivo `.env`

Ajuste o arquivo `.env` com as URLs dos serviços locais.

A aplicação espera as seguintes variáveis:

```env
DATABASE_URL=postgresql+asyncpg://postgres:SENHA@localhost:5432/postgres
REDIS_URL=redis://localhost:6379
```

---

## 4. Crie as estruturas do banco de dados

Execute o script SQL:

```bash
psql "postgresql://postgres:SENHA@localhost:5432/postgres" -f db/script.sql
```

> Altere usuário, senha, host, porta e banco conforme o seu ambiente.

---

# Execução Local

Com as dependências instaladas e o `.env` configurado, inicie a API em modo de desenvolvimento:

```bash
uv run fastapi dev app/main.py
```

Alternativamente, execute diretamente com Uvicorn:

```bash
uv run uvicorn app.main:app --reload
```

Por padrão, a aplicação ficará disponível em:

- API: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`
- GraphQL: `http://127.0.0.1:8000/graphql`

---

# Exemplos de Requisição

## Criar Cliente

### Endpoint

```http
POST /api/v1/clientes
```

### Body JSON

```json
{
  "cliente_nome": "Teste",
  "cliente_email": "teste@exemplo.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 300000
}
```

### Exemplo usando curl

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/clientes" \
-H "Content-Type: application/json" \
-d '{
  "cliente_nome": "Teste",
  "cliente_email": "teste@exemplo.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 300000
}'
```

---

## Webhook Pipefy - Card Updated

### Endpoint

```http
POST /api/v1/webhooks/pipefy/card-updated
```

### Body JSON

```json
{
  "event_id": "evt_103",
  "card_id": "card_456",
  "cliente_email": "teste@exemplo.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

### Exemplo usando curl

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/webhooks/pipefy/card-updated" \
-H "Content-Type: application/json" \
-d '{
  "event_id": "evt_103",
  "card_id": "card_456",
  "cliente_email": "teste@exemplo.com",
  "timestamp": "2026-05-18T12:00:00Z"
}'
```

---

# Testes

Execute toda a suíte de testes:

```bash
uv run pytest
```

Execute um arquivo específico:

```bash
uv run pytest tests/test_customer.py
```

> Os testes utilizam as mesmas configurações de ambiente da aplicação.
>
> Certifique-se de que o PostgreSQL esteja acessível e que as tabelas definidas em `db/script.sql` tenham sido criadas antes de executar testes que acessam o banco de dados.