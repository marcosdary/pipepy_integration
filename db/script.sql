create type status as enum ('Aguardando Análise', 'Processado');

create table customers (
	customer_id varchar(255) primary key,
	cliente_nome varchar(255) not null,
    status status default 'Aguardando Análise',
    cliente_email varchar(400) unique not null,
    tipo_solicitacao varchar(255) not null,
    valor_patrimonio integer not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);