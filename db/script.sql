create type status as enum (
	'processed',
	'rejected',
	'pending',
	'failed'
);

create type priority as enum (
	'prioridade_normal',
	'prioridade_alta'
);


create table customers (
	customer_id varchar(255) primary key,
	cliente_nome varchar(255) not null,
    status varchar(255) default 'Aguardando Análise',
    cliente_email varchar(400) unique not null,
    tipo_solicitacao varchar(255) not null,
    prioridade priority default 'prioridade_normal',
    valor_patrimonio integer not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);

create table webhook_pipefy (
	event_id varchar(255) primary key,
	status status not null,
	created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);

select * from customers;
select * from webhook_pipefy;


delete from webhook_pipefy where status = 'processed';
delete from customers where cliente_nome in ('Caio Jorge', 'Caio Fernando Dutra');

