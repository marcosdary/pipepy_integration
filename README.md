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
## 4. Configuração do PostgreSQL com Docker

Caso não tenha o PostgreSQL instalado localmente, você pode utilizar Docker para subir o banco rapidamente.

---

### 4.1 Instale o Docker

Baixe e instale o Docker Desktop conforme o seu sistema operacional:

- Windows / macOS:
  - https://www.docker.com/products/docker-desktop/

- Linux:
  - https://docs.docker.com/engine/install/

Após a instalação, verifique se o Docker está funcionando:

```bash
docker --version
```

---

### 4.2 Baixe a imagem do PostgreSQL

```bash
docker pull postgres:16
```

---

### 4.3 Inicialize o container PostgreSQL

```bash
docker run --name pipefy-postgres \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-e POSTGRES_DB=postgres \
-p 5432:5432 \
-d postgres:16
```

---

### 4.4 Verifique se o container está rodando

```bash
docker ps
```

Você deverá visualizar um container chamado `pipefy_postgres`.

---

### 4.5 Configure o arquivo `.env`

Utilize as mesmas credenciais configuradas no container:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
REDIS_URL=redis://localhost:6379
```

### 4.6 Crie as tabelas usando Docker Exec

Caso não tenha o `psql` instalado localmente, execute o script diretamente no container:

```bash
docker exec -i pipefy-postgres psql -U postgres -d postgres < db/script.sql
```

---

### 4.8 Conectando no DBeaver

Para visualizar o banco utilizando DBeaver:

1. Abra o DBeaver
2. Clique em **New Database Connection**
3. Escolha **PostgreSQL**
4. Utilize as seguintes configurações:

| Campo      | Valor     |
|-------------|------------|
| Host        | localhost  |
| Port        | 5432       |
| Database    | postgres   |
| Username    | postgres   |
| Password    | postgres   |

5. Clique em **Test Connection**
6. Depois em **Finish**

---

### 4.9 Parar o container

```bash
docker stop pipefy-postgres
```

---

### 4.10 Iniciar novamente o container

```bash
docker start pipefy-postgres
```

---

### 4.11 Remover o container

```bash
docker rm -f pipefy-postgres
```

---

# Execução Local

Com as dependências instaladas e o `.env` configurado, inicie a API em modo de desenvolvimento:

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