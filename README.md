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
Após Criar essas duas tabelas configure a conexão com seu banco de dados na linha 30 do arquivo bot.py, </br>
na ultima linha do bot.py Coloque o nome do seu Bot e o Token dele, Pronto! so iniciar o arquivo agora..</br>
</br>
Lista de Comandos do Bot</br>

#Comandos de Moderação </br>
Clear </br>
Bot-off </br>
Bot-on </br>
add_adm </br>
remove_adm </br>
adm_list </br>
add_ignore </br>
remove_ignore </br>
ignore_list </br>
cargo-add </br>
cargo-remove </br>

#Comandos do Banco </br>
banco-saldo </br>
banco-transferir </br>
banco-depositar </br>
banco-sacar </br>
banco-trabalhar </br>
banco-roubar </br>
banco-apostar </br>
banco-top-local </br>
loja </br>

#Comandos Oopa </br>
fale </br>
link </br>
pvp </br>
beijar </br>
avatar </br>
video-link </br>
gay </br>
