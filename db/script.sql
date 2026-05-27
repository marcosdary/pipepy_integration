/*
|--------------------------------------------------------------------------
| Status possíveis do webhook do Pipefy
|--------------------------------------------------------------------------
| processed -> webhook processado com sucesso
| rejected  -> webhook rejeitado pela aplicação
| pending   -> webhook aguardando processamento
| failed    -> erro durante o processamento do webhook
|--------------------------------------------------------------------------
*/
create type status as enum (
    'processed',
    'rejected',
    'pending',
    'failed'
);

/*
|--------------------------------------------------------------------------
| Prioridade baseada no valor do patrimônio do cliente
|--------------------------------------------------------------------------
| prioridade_normal -> patrimônio dentro da faixa padrão
| prioridade_alta   -> patrimônio considerado elevado
|--------------------------------------------------------------------------
*/
create type priority as enum (
    'prioridade_normal',
    'prioridade_alta'
);

/*
|--------------------------------------------------------------------------
| Tabela principal de clientes
|--------------------------------------------------------------------------
| Responsável por armazenar os dados enviados na solicitação
| do cliente e informações relacionadas ao processo interno.
|--------------------------------------------------------------------------
*/
create table customers (

    -- Identificador único do cliente
    customer_id varchar(255) primary key,

    -- Nome completo do cliente
    cliente_nome varchar(255) not null,

    -- Status atual da análise do cliente
    status varchar(255) default 'Aguardando Análise',

    -- E-mail do cliente (não pode repetir)
    cliente_email varchar(400) unique not null,

    -- Tipo da solicitação realizada pelo cliente
    tipo_solicitacao varchar(255) not null,

    -- Prioridade calculada conforme valor do patrimônio
    prioridade priority default 'prioridade_normal',

    -- Valor do patrimônio informado pelo cliente
    valor_patrimonio integer not null,

    -- Data de criação do registro
    created_at timestamp default current_timestamp,

    -- Data da última atualização do registro
    updated_at timestamp default current_timestamp
);

/*
|--------------------------------------------------------------------------
| Tabela responsável pelo controle dos webhooks do Pipefy
|--------------------------------------------------------------------------
| Armazena o identificador do evento recebido e o status
| do processamento realizado pela aplicação.
|--------------------------------------------------------------------------
*/
create table webhook_pipefy (

    -- Identificador único do evento recebido
    event_id varchar(255) primary key,

    -- Status do processamento do webhook
    status status not null,

    -- Data de criação do registro
    created_at timestamp default current_timestamp,

    -- Data da última atualização do registro
    updated_at timestamp default current_timestamp
);

/*
|--------------------------------------------------------------------------
| Consultas para visualizar os dados das tabelas
|--------------------------------------------------------------------------
*/

-- Listar todos os clientes cadastrados
select * from customers;

-- Listar todos os webhooks processados
select * from webhook_pipefy;

