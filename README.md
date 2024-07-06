para adicionar o meu BOT:https://discord.com/oauth2/authorize?client_id=1223830829529038972

Para o Bot Funcionar perfeitamente você precisa criar 2 tabelas no seu Banco de dados

tabela Banco:

```
create table banco(
id int not null primary key auto_increment,
nome varchar(20) unique,
id_user varchar(20) not null unique,
saldo_user varchar(20) not null default 0,
saldo_banco varchar(20) not null default 0,
dia_trabalhado varchar(8) not null default '00/00',
salario3x int not null default 0,
pocao_sorte int not null default 0);
```

tabela Bot:

```
create table bot(
id varchar(25),
nome varchar(30),
server_id varchar(25),
server_name varchar(30),
status varchar(10));
```
</br>
Após criar essas duas tabelas configure a conexão com seu banco de dados na linha 30 do arquivo bot.py, </br>
na ultima linha do bot.py coloque o nome do seu bot e o token dele, pronto! so iniciar o arquivo agora..</br>
</br>
Lista de Comandos do Bot:</br>
</br>

# Comandos do Bot
```
Clear
Bot-off
Bot-on
add_adm
remove_adm
adm_list
add_ignore
remove_ignore
ignore_list
cargo-add
cargo-remove

banco-saldo
banco-transferir
banco-depositar 
banco-sacar
banco-trabalhar 
banco-roubar
banco-apostar
banco-top-local 
loja

fale
link
pvp
beijar
avatar
video-link
gay
```
# Comandos de Interação (bnome é o nome que você colocar no bot)
```
me da adm
{bnome} você é ´Algo´
{bnome} Quantas horas?
{bnome} Que dia é hoje?
{bnome} você prefere ´Coisa´ ou ´Coisa´
{bnome} Roube ´User´
{bnome} Mate o ´User´
{bnome} geme meu nome
{bnome} geme
{bnome}
bom dia
boa tarde
boa noite
eai
server ta aberto?
server parado
server ruim
ksksks
alguém on?
duvido
foda-se
boa {bnome}
```
