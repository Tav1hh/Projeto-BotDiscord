Para o Bot Funcionar perfeitamente você precisa criar 2 tabelas no seu Banco de dados

tabela Banco:

create table banco(
id int not null primary key auto_increment,
nome varchar(20) unique,
id_user varchar(20) not null unique,
saldo_user varchar(20) not null default 0,
saldo_banco varchar(20) not null default 0,
dia_trabalhado varchar(8) not null default '00/00',
salario3x int not null default 0,
pocao_sorte int not null default 0);

tabela Bot:

create table bot(
id varchar(25),
nome varchar(30),
server_id varchar(25),
server_name varchar(30),
status varchar(10));

Após Criar essas duas tabelas configure a conexão com seu banco de dados na linha 30 do arquivo bot.py