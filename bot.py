def bot_model(bnome,token):
    #Importação de pacotes
    from discord.voice_client import VoiceClient
    from discord import app_commands
    from discord.ext import commands
    from pytube import YouTube
    from pathlib import Path
    import mysql.connector
    from time import sleep
    import discord
    import datetime
    import discord
    from discord.utils import get
    import os
    from random import randint, choice
    
    #Fala se o Bot foi ligado com sucesso
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='*', intents= discord.Intents.all())
    @bot.event
    async def on_ready():
        print(f'Bot on em: {bot.user}')
        try:
            synced = await bot.tree.sync()
            print(f'Sincronizados {len(synced)} commandos')
        except Exception as e:
            print(e)
    #Coneção com banco de dados
    mydb = mysql.connector.connect(
    host= "host",
    user= "user",
    password= "password",
    database="db")
    mycursor = mydb.cursor()
    
    class server_config:
        def __init__(self,server_id:int):
            self.server_id = server_id
            self.server_name = bot.get_guild(server_id).name
        def bot_off(self):
            sql = f"insert into bot values ('0','none','{self.server_id}','{self.server_name}','off')"
            mycursor.execute(sql)
            mydb.commit()
        def bot_on(self):
            sql = f"delete from bot where server_id ='{self.server_id}' and status ='off'"
            mycursor.execute(sql)
            mydb.commit()
        def servers_off(self):
            sql = f"select server_name , server_id from bot where status = 'off' "
            mycursor.execute(sql)
            myresult = mycursor.fetchall()    
            server_list = []
            for x in myresult:
                server_list.append(int(x[1]))
            return server_list
        def ignore_list(self):
            sql = f"select id ,server_id from bot where status ='ignore' and server_id ='{self.server_id}'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            adm_list = []
            for x in myresult:
                adm_list.append(int(x[0]))
            return adm_list         
        def add_ignore(self,user):
            sql = f"insert into bot values ('{user.id}','{user.global_name}','{self.server_id}','{self.server_name}','ignore')"
            mycursor.execute(sql)
            mydb.commit()
        def remove_ignore(self,user):
            sql = f"delete from bot where id ='{user.id}' and server_id ='{self.server_id}' and status ='ignore'"
            mycursor.execute(sql)
            mydb.commit()
        def adm_list(self):
            sql = f"select id ,server_id from bot where status ='adm' and server_id ='{self.server_id}'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            adm_list = []
            for x in myresult:
                adm_list.append(int(x[0]))
            return adm_list   
        def add_adm(self,user):
            sql = f"insert into bot values ('{user.id}','{user.global_name}','{self.server_id}','{self.server_name}','adm')"
            mycursor.execute(sql)
            mydb.commit()
        def remove_adm(self,user):
            sql = f"delete from bot where id ='{user.id}' and server_id ='{self.server_id}' and status ='adm'"
            mycursor.execute(sql)
            mydb.commit()
    class banco:
        def __init__(self,id_user:int):
            self.id_user = id_user
            sql = f"SELECT nome, saldo_user, saldo_banco, dia_trabalhado, salario3x, pocao_sorte FROM banco where id_user = '{id_user}'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for x in myresult: 
                self.nome=list(x)[0]
                self.saldo_user=int(list(x)[1])
                self.saldo_banco=int(list(x)[2])
                self.dia_trabalhado=list(x)[3]
                self.salario3x=int(list(x)[4])
                self.pocao_sorte=int(list(x)[5])    
        def abrir_conta(self):
            sql = f"insert into banco (nome,id_user) values('{bot.get_user(self.id_user).global_name}','{self.id_user}');"

            mycursor.execute(sql)
            mydb.commit()
        def trocar_saldo_user(self,novo_saldo:int):
            sql = f"update banco set saldo_user = '{novo_saldo}' where id_user ='{self.id_user}'"
            mycursor.execute(sql)
            mydb.commit()
        def trocar_saldo_banco(self,novo_saldo:int):
            sql = f"update banco set saldo_banco = '{novo_saldo}' where id_user ='{self.id_user}'"
            mycursor.execute(sql)
            mydb.commit()
        def trabalhou(self):
            dia = datetime.datetime.today().day
            mes = datetime.datetime.today().month
            sql = f"update banco set dia_trabalhado = '{dia}/{mes}' where id_user ='{self.id_user}'"
            mycursor.execute(sql)
            mydb.commit()
        def trocar_itens(self,item:str,nova_quantidade:int):
            sql = f"update banco set {item} = '{nova_quantidade}' where id_user ='{self.id_user}'"
            mycursor.execute(sql)
            mydb.commit()
    #Slash Commands
    
    #Comandos ADM
    @bot.tree.command(name='clear',description='Limpa um determinado número de mensagens do Chat')
    @app_commands.describe(quantidade = 'quantas mensagens eu devo apagar?')
    async def clear(ctx:discord.Interaction, quantidade:int = 10):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            if quantidade >1000 or quantidade <1:
                await ctx.response.send_message('Digite um número entre 1 e 1000',ephemeral=True,delete_after=8)
                return
            await ctx.response.send_message(f'{quantidade} Mensagens Apagadas.',ephemeral=True,delete_after=8)
            await ctx.channel.purge(limit=quantidade)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='bot-off',description='Me Desligue no seu server')
    async def bot_off(ctx:discord.Interaction):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            #Verificando se a pessoa está na lista para não ser adicionada 2x
            if sv.server_id in sv.servers_off():
                await ctx.response.send_message('Ja estou desligado!',delete_after=8)
                return
            sv.bot_off()
            await ctx.response.send_message('Saindo Senhor..',delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='bot-on',description='Me Ligue no seu server')
    async def bot_on(ctx:discord.Interaction):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            #Verificando se a pessoa está na lista para não ser adicionada 2x
            if sv.server_id not in sv.servers_off():
                await ctx.response.send_message('Ja estou Ligado!',delete_after=8)
                return
            sv.bot_on()
            await ctx.response.send_message('Voltei..',delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='add_adm',description='Adicione Úsuarios a minha ADM List')
    @app_commands.describe(quem = 'Quem eu deveria adicionar?')
    async def add_adm(ctx:discord.Interaction, quem:discord.Member):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            #Verificando se a pessoa está na lista para não ser adicionada 2x
            if quem.id in sv.adm_list():
                await ctx.response.send_message('Esse Úsuario ja está na minha Lista de Adms!',delete_after=8)
                return
            sv.add_adm(quem)
            await ctx.response.send_message('Usuario adicionado a lista de Adms!',delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='remove_adm',description='Remova Úsuarios da minha ADM List')
    @app_commands.describe(quem = 'Quem eu deveria retirar?')
    async def remove_adm(ctx:discord.Interaction, quem:discord.Member):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            #Verificando se a pessoa está na lista pra ser removida
            if quem.id not in sv.adm_list():
                await ctx.response.send_message('Esse Ùsuario não está na minha Lista de Adms!',delete_after=8)
                return
            sv.remove_adm(quem)
            await ctx.response.send_message('Usuario removido com sucesso da lista de Adms!',delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='adm_list',description='Veja quem está na minha ADM List')
    async def adm_list(ctx:discord.Interaction):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            # Criando o Embed e enviando
            embed = discord.Embed(title=f"Úsuarios com acesso ADM", description="Veja aqui os úsuarios que estão na minha adm list", color=0x00ff00)
            for user in sv.adm_list():
                embed.add_field(name=f"{bot.get_user(user).global_name}", value=f"========", inline=False)
            try:
                embed.set_thumbnail(url= ctx.guild.icon.url)
            except:
                pass
            await ctx.response.send_message(embed=embed,delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=15)
    
    @bot.tree.command(name='add_ignore', description='Adicione Úsuarios a minha IGNORE List')
    @app_commands.describe(quem = 'Quem eu deveria adicionar?')
    async def add_ignore(ctx:discord.Interaction, quem:discord.Member):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            #Verificando se a pessoa está na lista para não ser adicionada 2x
            if quem.id in sv.ignore_list():
                await ctx.response.send_message('Ele já está na minha ignore list!',delete_after=8)
                return
            sv.add_ignore(quem)
            await ctx.response.send_message(f'Não Ouço mais o {quem.global_name} daqui pra frente!',delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='remove_ignore',description='Remova Úsuarios da minha IGNORE List')
    @app_commands.describe(quem = 'Quem eu deveria retirar?')
    async def remove_ignore(ctx:discord.Interaction, quem:discord.Member):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            #Verificando se a pessoa está na lista pra ser removida
            if quem.id not in sv.ignore_list():
                await ctx.response.send_message('Esse Ùsuario não está na minha Lista de Ignorados!',delete_after=8)
                return
            sv.remove_ignore(quem)
            await ctx.response.send_message('Usuario removido com sucesso da lista de Ignorados!',delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)  
    
    @bot.tree.command(name='ignore_list',description='Veja quem está na minha Lista de Ignorados')
    async def ignore_list(ctx:discord.Interaction):
        sv = server_config(ctx.guild.id)
        #Verificando se o úsuario tem permissão para usar esse comando
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            # Criando o Embed e enviando
            embed = discord.Embed(title=f"Úsuarios que eu Ignoro", description="Veja aqui os úsuarios que estão na minha lista de Ignorados", color=0x00ff00)
            for user in sv.ignore_list():
                embed.add_field(name=f"{bot.get_user(user).global_name}", value=f"========", inline=False)
            try:
                embed.set_thumbnail(url= ctx.guild.icon.url)
            except:
                pass
            await ctx.response.send_message(embed=embed,delete_after=15)
        #Respondendo que não tem permissão
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!',delete_after=8)
    
    @bot.tree.command(name='cargo-add', description='De um Cargo a um membro')
    @app_commands.describe(quem = 'Para quem você quer dar o cargo?')
    @app_commands.describe(cargo = 'Qual Cargo você quer dar?')
    async def cargo(ctx:discord.Interaction, quem:discord.Member, cargo:discord.Role):
        sv = server_config(ctx.guild.id)
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            try:
                await quem.add_roles(cargo)
                await ctx.response.send_message('Usuario Promovido com sucesso',delete_after=10)
                channel = await quem.create_dm()
                await channel.send(f'Você recebeu o Cargo!! {cargo}, parabéns')
            except:
                await ctx.response.send_message('eu preciso ter um cargo acima desse para fazer isso.', delete_after=10)
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!', delete_after=10)
    
    @bot.tree.command(name='cargo-remove', description='Tire o cargo de um membro')
    @app_commands.describe(quem = 'De quem você quer Tirar o cargo?')
    @app_commands.describe(cargo = 'Qual Cargo você quer Tirar?')
    async def cargo_remove(ctx:discord.Interaction, quem:discord.Member, cargo:discord.Role):
        sv = server_config(ctx.guild.id)
        if ctx.user.guild_permissions.administrator == True or ctx.user.id in sv.adm_list() or ctx.user.id == 583102578108399627:
            try:
                await quem.remove_roles(cargo)
                await ctx.response.send_message('Cargo removido com sucesso!',delete_after=10)
            except:
                await ctx.response.send_message('Não foi possivel Tirar o cargo do usuario!', delete_after=10)
        else:
            await ctx.response.send_message('Você Precisa ter a Permissão: `Adiministrador` ou estar na ADM list!', delete_after=10)
    
    #Comandos Banco
    @bot.tree.command(name='banco-saldo',description=f'Veja tudo que você ou outra pessoa tem no {bnome.title()} Bank')
    @app_commands.describe(quem = 'De quem você ver os Dados?')
    async def banco_saldo(ctx:discord.Interaction,quem:discord.Member):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se não é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',ephemeral=True,delete_after=10)
            return
    
        user = banco(quem.id)
        try:
            #Cria o Embed e Envia
            embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
            embed.add_field(name="Usuario",value=f"{quem.mention}", inline=False)
            embed.add_field(name="Saldo Banco", value=f"{user.saldo_banco} {bnome}s", inline=False)
            embed.add_field(name="Saldo em Mãos", value=f"{user.saldo_user} {bnome}s", inline=False)
            embed.add_field(name='Ultimo dia Trabalhado', value=f'{user.dia_trabalhado}',inline=False)
            embed.add_field(name='Salario3x',value=f'{user.salario3x}',inline=False)
            embed.add_field(name='Pocao da Sorte',value=f'{user.pocao_sorte}',inline=False)
            embed.set_thumbnail(url= quem.display_avatar.url)
            await ctx.response.send_message(embed=embed,delete_after=30)
        except:
            user.abrir_conta()
            user = banco(quem.id)
            #Cria o Embed e Envia
            embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
            embed.add_field(name="Usuario",value=f"{quem.mention}", inline=False)
            embed.add_field(name="Saldo-Banco", value=f"{user.saldo_banco} {bnome}s", inline=False)
            embed.add_field(name="Saldo", value=f"{user.saldo_user} {bnome}s", inline=False)
            embed.add_field(name='Ultimo dia Trabalhado', value=f'{user.dia_trabalhado}',inline=False)
            embed.add_field(name='Salario3x',value=f'{user.salario3x}',inline=False)
            embed.add_field(name='Pocao da Sorte',value=f'{user.pocao_sorte}',inline=False)
            embed.set_thumbnail(url= quem.display_avatar.url)
            await ctx.response.send_message(embed=embed,delete_after=30)
    
    @bot.tree.command(name='banco-transferir', description=f'tranfira seus {bnome.title()}s para alguém')
    @app_commands.describe(quem=f'Para quem você quer transferir seus {bnome.title()}s?')
    async def transferir(ctx: discord.Interaction, quem:discord.Member, valor:int):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se não é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',ephemeral=True,delete_after=10)
            return
        if ctx.user.id == quem.id:
            await ctx.response.send_message(f'você não pode transferir {bnome.title()}s para si mesmo',ephemeral=True,delete_after=10)
            return
        #Verificando se é um valor negativo
        if '-' in str(valor):
            await ctx.response.send_message('Não é possivel transferir valores negativos.',ephemeral=True,delete_after=15)
            return
        try:
            user = banco(ctx.user.id)
            alvo = banco(quem.id)
            #Verificando se tem os Oopas para a transferencia e se a conta existe
            try:
                if user.saldo_banco < valor:
                    await ctx.response.send_message(f'{bnome}s Insuficientes!  \n| Você possui: {user.saldo_banco} {bnome.title()}s, Consiga mais {bnome.title()}s para continuar a Transferencia',ephemeral=True,delete_after=10)
                    return
            except:
                user.abrir_conta()
                user = banco(ctx.user.id)
                if user.saldo_banco < valor:
                    await ctx.response.send_message(f'{bnome}s Insuficientes!  \n| Você possui: {user.saldo_banco} {bnome.title()}s, Consiga mais {bnome.title()}s para continuar a Transferencia',ephemeral=True,delete_after=10)
                    return
            else:
                #Dinheiro Saindo
                user_money = user.saldo_banco
                user_money -= valor
                user.trocar_saldo_banco(user_money)
                #Transferindo pra ela
                saldo = alvo.saldo_banco
                saldo += valor
                alvo.trocar_saldo_banco(saldo)
                await ctx.response.send_message(f'Transferencia de {valor} {bnome}s Realizada para {quem.mention}, Saldo Atual: {user_money} {bnome.title()}s',delete_after=20)
        except:
            alvo.abrir_conta()
            alvo = banco(quem.id)
            #Dinheiro Saindo
            user_money = user.saldo_banco
            user_money -= valor
            user.trocar_saldo_banco(user_money)
            #Transferindo pra ela
            saldo = alvo.saldo_banco
            saldo += valor
            alvo.trocar_saldo_banco(saldo)
            await ctx.response.send_message(f'Transferencia de {valor} {bnome}s Realizada para {quem.mention}, Saldo Atual: {user_money} {bnome.title()}s',delete_after=20)
            
    @bot.tree.command(name='banco-depositar', description=f'Deposite seus {bnome}s para não ser roubado')
    @app_commands.describe(quantia=f'Quantos {bnome.title()}s você quer depositar?')
    async def deposito(ctx: discord.Interaction, quantia:int):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se é um valor negativo
        if '-' in str(quantia):
            await ctx.response.send_message('Não é possivel depositar valores negativos.',delete_after=15)
            return
        try:
            user = banco(ctx.user.id)
            if quantia > user.saldo_user:
                await ctx.response.send_message(f'Depositamos tudo que você tinha, devido a você ter colocado um valor muito acima {ctx.user.mention}.',delete_after=20)
                user.trocar_saldo_user(0)
                user.trocar_saldo_banco(user.saldo_banco + user.saldo_user)
                return
            #Depositando
            user.trocar_saldo_user(user.saldo_user - quantia)
            user.trocar_saldo_banco(user.saldo_banco + quantia)
            await ctx.response.send_message(f'Deposito de {quantia} Feito com sucesso! {ctx.user.mention}',delete_after=20)
        except:
            user.abrir_conta()
            user = banco(ctx.user.id)
            if quantia > user.saldo_user:
                await ctx.response.send_message(f'Depositamos tudo que você tinha, devido a você ter colocado um valor muito acima {ctx.user.mention}.',delete_after=20)
                user.trocar_saldo_user(0)
                user.trocar_saldo_banco(user.saldo_banco + user.saldo_user)
                return
            #Depositando
            user.trocar_saldo_user(user.saldo_user - quantia)
            user.trocar_saldo_banco(user.saldo_banco + quantia)
            await ctx.response.send_message(f'Deposito de {quantia} Feito com sucesso! {ctx.user.mention}',delete_after=20) 
    
    @bot.tree.command(name='banco-sacar', description=f'Saque seus {bnome}s para fazer compras e apostas')
    @app_commands.describe(quantia=f'Quantos {bnome.title()}s você quer depositar?')
    async def deposito(ctx: discord.Interaction, quantia:int):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se é um valor negativo
        if '-' in str(quantia):
            await ctx.response.send_message('Não é possivel Sacar valores negativos.',delete_after=15)
            return
        try:
            user = banco(ctx.user.id)
            if quantia > user.saldo_banco:
                await ctx.response.send_message(f'Sacamos tudo que você tinha, devido a você ter colocado um valor muito acima {ctx.user.mention}.',delete_after=20)
                user.trocar_saldo_banco(0)
                user.trocar_saldo_user(user.saldo_banco + user.saldo_user)
                return
            #Sacando
            user.trocar_saldo_banco(user.saldo_banco - quantia)
            user.trocar_saldo_user(user.saldo_user + quantia)
            await ctx.response.send_message(f'Saque de {quantia} Feito com sucesso! {ctx.user.mention}',delete_after=20)
        except:
            user.abrir_conta()
            user = banco(ctx.user.id)
            if quantia > user.saldo_banco:
                await ctx.response.send_message(f'Sacamos tudo que você tinha, devido a você ter colocado um valor muito acima {ctx.user.mention}.',delete_after=20)
                user.trocar_saldo_banco(0)
                user.trocar_saldo_user(user.saldo_banco + user.saldo_user)
                return
            #Sacando
            user.trocar_saldo_banco(user.saldo_banco - quantia)
            user.trocar_saldo_user(user.saldo_user + quantia)
            await ctx.response.send_message(f'Saque de {quantia} Feito com sucesso! {ctx.user.mention}',delete_after=20) 
    
    @bot.tree.command(name='banco-trabalhar', description=f'Trabalhe por {bnome}s')
    async def trabalhar(ctx: discord.Interaction):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
            
        dia = datetime.datetime.today().day
        mes = datetime.datetime.today().month
        #Escolhendo a profissão e executando o programa
        profissao =['garcom','prefeito','mineiro','entregador','presidente','lixeiro','chefe de cozinha','Chapeleiro','Policial','Traficante','Segurança','Motorista de Onibus','Piloto de avião','Navegante de Barcos','Cantor']
        salario = randint(1,300)+300
        user = banco(ctx.user.id)
        try:
            #Verificando se já trabalhou hoje
            if  user.dia_trabalhado == f'{dia}/{mes}':
                await ctx.response.send_message('você ja trabalhou hoje, Volte amanhã!',delete_after=15)
                return
            #Verificando se tem o item salario3x
            if user.salario3x >=1:
                user.trocar_itens('salario3x',user.salario3x - 1)
                await ctx.channel.send('Usado Salario 3X, seu salário foi multiplicado por 3!',delete_after=15)
                salario = salario*3
            #Depositando o salario
            user.trocar_saldo_user(salario + user.saldo_user)
            await ctx.response.send_message(f'você trabalhou como {choice(profissao)} e recebeu {salario} {bnome}s', delete_after=15)
            #Cria o Embed e Envia
            user.trabalhou()
        except:
            user.abrir_conta()
            user = banco(ctx.user.id)
            #Verificando se já trabalhou hoje
            if  user.dia_trabalhado == f'{dia}/{mes}':
                await ctx.response.send_message('você ja trabalhou hoje, Volte amanhã!',delete_after=15)
                return
            #Verificando se tem o item salario3x
            if user.salario3x >=1:
                user.trocar_itens('salario3x',user.salario3x - 1)
                await ctx.channel.send('Usado Salario 3X, seu salário foi multiplicado por 3!',delete_after=15)
                salario = salario*3
            #Depositando o salario
            user.trocar_saldo_user(salario + user.saldo_user)
            await ctx.response.send_message(f'você trabalhou como {choice(profissao)} e recebeu {salario} {bnome}s', delete_after=15)
            #Cria o Embed e Envia
            user.trabalhou()
    
    @bot.tree.command(name='banco-roubar', description=f'Tente roubar {bnome}s de alguém')
    @app_commands.describe(quem=f'Quem você quer tentar roubar?')
    async def transferir(ctx: discord.Interaction, quem:discord.Member):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return   
        #Verificando se é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',delete_after=10)
            return
        #Verificando se está tentando se roubar
        if ctx.user.id == quem.id:
            await ctx.response.send_message(f'Hey {ctx.user.mention} você não pode roubar a si mesmo🤨',delete_after=10)
            return
        try:
            user = banco(ctx.user.id)
            alvo = banco(quem.id)
            if alvo.saldo_user < 25:
                await ctx.response.send_message('Vai roubar oque?, ele não tem nada ksks',delete_after=10)
                #Cria o Embed e Envia
                embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
                embed.add_field(name="Usuario",value=f"{quem.mention}", inline=False)
                embed.add_field(name="Saldo", value=f"{alvo.saldo_user} {bnome}s", inline=False)
                embed.set_thumbnail(url= quem.display_avatar.url)
                await ctx.channel.send(embed=embed,delete_after=10)
            else:
                #Pegando o Saldo dos 2 e decidindo a quantia do roubo
                saldo_roubado = randint(alvo.saldo_user//10,alvo.saldo_user//4)        
                #Repondo os novos valores
                alvo.trocar_saldo_user(alvo.saldo_user - saldo_roubado)
                user.trocar_saldo_user(user.saldo_user + saldo_roubado)
                await ctx.response.send_message(f'🤑Você roubou {saldo_roubado} {bnome}s de {quem.mention}',delete_after=18)
        except:
            alvo.abrir_conta()
            alvo = banco(quem.id)
            if alvo.saldo_user < 25:
                await ctx.response.send_message('Vai roubar oque?, ele não tem nada ksks',delete_after=10)
                #Cria o Embed e Envia
                embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
                embed.add_field(name="Usuario",value=f"{quem.mention}", inline=False)
                embed.add_field(name="Saldo", value=f"{alvo.saldo_user} {bnome}s", inline=False)
                embed.set_thumbnail(url= quem.display_avatar.url)
                await ctx.channel.send(embed=embed,delete_after=10)
            else:
                #Pegando o Saldo dos 2 e decidindo a quantia do roubo
                saldo_roubado = randint(alvo.saldo_user//10,alvo.saldo_user//4)        
                #Repondo os novos valores
                alvo.trocar_saldo_user(alvo.saldo_user - saldo_roubado)
                user.trocar_saldo_user(user.saldo_user + saldo_roubado)
                await ctx.response.send_message(f'🤑Você roubou {saldo_roubado} {bnome}s de {quem.mention}',delete_after=18)
    
    @bot.tree.command(name='banco-apostar', description=f'Aposte 1000 {bnome}s e tente ganhar 10.000')
    async def casino(ctx:discord.Interaction):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        try:
            user = banco(ctx.user.id)
            #Verificando se tem Saldo Suficiente
            if user.saldo_user < 1000:
                await ctx.response.send_message(f'{bnome}s Insuficientes. são Necessarios 1000 {bnome}s, Saque seus Oopas',delete_after=10)
                #Cria o Embed e Envia
                embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
                embed.add_field(name="Usuario",value=f"{ctx.user.mention}", inline=False)
                embed.add_field(name="Saldo", value=f"{user.saldo_user} {bnome}s", inline=False)
                embed.set_thumbnail(url= ctx.user.display_avatar.url)
                await ctx.channel.send(embed=embed,delete_after=10)
                return
            else:
                #Verificando se tem poção da sorte
                if user.pocao_sorte >=1:
                    chance = randint(1,8)
                    #Gastando uma poção
                    user.trocar_itens('pocao_sorte',user.pocao_sorte - 1)
                    await ctx.channel.send('Usou 1x Poção da Sorte Haha..',delete_after=10)
                    
                else:
                    chance = randint(1,100)
                if chance <=8:
                    await ctx.response.send_message(f'🤑Parabens {ctx.user.mention}!! você ganhou o Premio!💸💸',delete_after=60)
                    #Depositando os novos valores
                    user.trocar_saldo_user(user.saldo_user - 1000)
                    user.trocar_saldo_banco(user.saldo_banco + 10000)
                    #Cria o Embed e Envia
                    embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
                    embed.add_field(name="Usuario",value=f"{ctx.user.mention}", inline=False)
                    embed.add_field(name="Saldo Banco", value=f"{user.saldo_banco + 10000} {bnome}s", inline=False)
                    embed.set_thumbnail(url= ctx.user.display_avatar.url)
                    await ctx.channel.send(embed=embed,delete_after=60)
                    return
                else:
                    repostas = ['tente denovo','Quem sabe na proxima','Tente denovo amanhã','você está com azar emm']
                    await ctx.response.send_message(f'Infelizmente não foi dessa vez {ctx.user.mention}... {choice(repostas)}',delete_after=10)
                    user.trocar_saldo_user(user.saldo_user - 1000)
                    return
        except:
            user.abrir_conta()
            user = banco(ctx.user.id)
            #Verificando se tem Saldo Suficiente
            if user.saldo_user < 1000:
                await ctx.response.send_message(f'{bnome}s Insuficientes. são Necessarios 1000 {bnome}s, Saque seus Oopas',delete_after=10)
                #Cria o Embed e Envia
                embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
                embed.add_field(name="Usuario",value=f"{ctx.user.mention}", inline=False)
                embed.add_field(name="Saldo", value=f"{user.saldo_user} {bnome}s", inline=False)
                embed.set_thumbnail(url= ctx.user.display_avatar.url)
                await ctx.channel.send(embed=embed,delete_after=10)
                return
    
    @bot.tree.command(name='banco-top-local', description=f'Veja o Rank-Local de {bnome}s no {bnome.title()} Bank')
    async def top_local(ctx: discord.Interaction):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
            
        #Conseguindo os Membros Locais
        sql = f"select id_user, saldo_banco from banco order by saldo_banco"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        id_list = []
        for x in myresult:
            id_list.append(int(x[0]))
        member = []
        #Testando todos os usuarios do banco e comparando com o server
        for i in id_list:
            if ctx.guild.get_member(i) != None:   
                member.append(i)   
        #Montando a lista com Menção e Saldo
        lista_membros = []
        for x in member:
            sql = f"SELECT nome, saldo_banco from banco where id_user = '{x}'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            for x in myresult:
                nome = list(x)[0]
                saldo = list(x)[1]
                dados = [nome,saldo]
                lista_membros.append(dados)
        lista_membros.reverse()
        #Modelando o Embed
        embed = discord.Embed(title=f"{bnome.title()} Bank", color=0x00ff00)
        x = 0
        #Adicionando os úsuarios na lista e enviando o Embed
        for usuario in lista_membros:
            embed.add_field(name=f"{x+1}º {usuario[0]} - {usuario[1]} ",value=f"==============================", inline=False)
            x+=1
            if x == 6:
                break
        embed.add_field(name='',value=f'📌 Deposite seus {bnome}s no {bnome.title()} Bank com /banco-depositar para você aparecer aqui.🤑', inline=False)
        try:embed.set_thumbnail(url= ctx.guild.icon.url)
        except:pass
        await ctx.response.send_message(embed=embed,delete_after=30)    
    
    @bot.tree.command(name='loja', description=f'Compre na nossa Loja com seus {bnome}s')
    async def loja(ctx :discord.Interaction):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
            
        #Resposta a interação com o Botão
        async def select_resposta(interact:discord.Interaction):
            escolha = interact.data['values'][0]
            item = {
                '1':'Poção da Sorte',
                '2':'3X+ Salario'}
            itens_escolhidos = (item[escolha])
            if escolha in values:
                await interact.response.send_message(f'Você ja adicionou esse item, finalize a compra!',ephemeral=True,delete_after=5)
                return
            await interact.response.send_message(f'Você Adicionou {itens_escolhidos} ao Carrinho',ephemeral=True,delete_after=5)
            carrinho.append(itens_escolhidos)
            values.append(interact.data['values'][0])
        async def fechar_loja(interact:discord.Interaction):
            await interact.response.send_message('Fechando Loja..',ephemeral=True,delete_after=3)
            await ctx.delete_original_response()
            sleep(2)
        async def realizar_compra(interact:discord.Interaction):
            #Verificando se o carrinho está vazio
            if carrinho == []:
                await interact.response.send_message('Você não selecionou nada!',delete_after=5)
                return
            #Verificando se tem Oopas na conta
            tamanho = len(carrinho)
            user = banco(ctx.user.id)
            valor = 0
            #definindo o valor dos itens
            for i in values:
                if i == '1':
                    valor +=500
                if i == '2':
                    valor +=500
            if user.saldo_user < valor:
                await interact.response.send_message(f'Você tem {user.saldo_user} {bnome.title()}s!, não e possivel fazer a compra',delete_after=5)
                return
            #Criando o Embed com os itens da loja de acordo com o tamanho
            embed = discord.Embed(title=f"Compra Realizada!!", description="Aqui está a sua lista de compras!", color=0x00ff00)
            #Adicionando os itens na conta
            for v in values:
                #Poção da Sorte
                if v == '1':
                    user.trocar_itens('pocao_sorte',user.pocao_sorte +1)
                #Salario Triplo
                if v == '2':
                    user.trocar_itens('salario3x',user.salario3x +1)
            
            #Criando o Embed
            for i in range(tamanho):
                embed.add_field(name=f"Item {i+1}", value=f"{carrinho[i]}", inline=False)

            embed.set_thumbnail(url=f"{ctx.user.avatar.url}")
            await interact.response.send_message(embed=embed,ephemeral=True,delete_after=10)
            #Adicionando o novo saldo na conta do cliente
            user.trocar_saldo_user(user.saldo_user-valor)
            # await ctx.delete_original_response()
        carrinho = []
        values = []
        
        # Adicionar itens à loja
        embed = discord.Embed(title=f"{bnome.title()} Store", description="Bem-vindo à nossa loja! Aqui você pode comprar itens exclusivos.", color=0x00ff00)
        embed.add_field(name=f"Poção da Sorte - Preço: 500 {bnome}s", value=f"você tera 50% chance de ganhar no /banco-apostar", inline=False)
        embed.add_field(name=f"3x+ Salário - Preço: 500 {bnome}s", value="Receba 3X na proxima vez que trabalhar", inline=False)
        embed.set_thumbnail(url=f"{bot.user.avatar.url}")
            
        #Criando os botões de compra!
        view = discord.ui.View()
        botao_comprar = discord.ui.Button(label='Comprar',style=discord.ButtonStyle.green)
        botao_fechar = discord.ui.Button(label='Fechar Loja',style=discord.ButtonStyle.red)
        menu_selecao = discord.ui.Select(placeholder='Selecione um Item para compra')
        #Adicionando os Botões ao Embed
        view.add_item(menu_selecao)
        view.add_item(botao_comprar)
        view.add_item(botao_fechar)
        #Lista de Opções
        opcoes = [
            discord.SelectOption(label='Poção da Sorte',value='1'),
            discord.SelectOption(label='3x+ Salário',value='2')
        ]
        #Configurando os botões
        menu_selecao.options = opcoes
        menu_selecao.callback = select_resposta
        botao_comprar.callback = realizar_compra
        botao_fechar.callback = fechar_loja
        
        await ctx.response.send_message(embed=embed,view=view,ephemeral=True)
    
    #Comandos do Oopa
    @bot.tree.command(name =f'{bnome}',description=f'Teste se o {bnome.title()} está On')
    async def hello(ctx: discord.Interaction):
        await ctx.response.send_message(f'Hey {ctx.user.mention}, Estou Funcionando!',delete_after=15)

    @bot.tree.command(name='fale', description='Falarei oque você quiser no chat')
    @app_commands.describe(oque_dizer = 'Oque eu deveria dizer?')
    async def dig(ctx: discord.Interaction,oque_dizer:str):
        #Codigo falando oque o User disse
        await ctx.response.send_message('Mensagem Enviada!',ephemeral=True)
        await ctx.channel.send(f'{oque_dizer}')
        await ctx.delete_original_response()

    @bot.tree.command(name='link', description='Entre na minha comunidade do discord!')
    async def link(ctx: discord.Interaction):
        channel = await ctx.user.create_dm()
        await channel.send('Entre no meu server: https://discord.gg/YuATH85xJG')
        await ctx.response.send_message('Dm enviada!',delete_after=15)
    
    @bot.tree.command(name='abrace', description='Abraçe algúem')
    @app_commands.describe(quem = 'Quem você quer abraçar??')
    async def beijar(ctx: discord.Interaction, quem:discord.Member):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)  
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',delete_after=10)
            return
        # Pegando o arquivo de midia
        with open(f'midia/abraco-{randint(1,3)}.gif', 'rb') as gif_arquivo:
            gif = discord.File(gif_arquivo) 
        async def retribuir_abraco(interact:discord.Interaction):
            if interact.user.id != quem.id:
                await interact.response.send_message('Eii, isso não é para você!',ephemeral=True,delete_after=5)
            else:
                with open(f'midia/abraco-{randint(1,3)}.gif', 'rb') as gif_arquivo:
                    gif = discord.File(gif_arquivo)
                await interact.response.send_message(f'<@{quem.id}> abraçou {ctx.user.mention} Devolta',file=gif,delete_after=18)
        view = discord.ui.View()
        botao_revanche = discord.ui.Button(label='Retribuir',style=discord.ButtonStyle.red)
        view.add_item(botao_revanche)
        botao_revanche.callback = retribuir_abraco
        # await ctx.channel.send(view=view,delete_after=18)
        await ctx.response.send_message(f'{ctx.user.mention} abraçou {quem.mention}',file=gif,view=view,delete_after=18)
     
    @bot.tree.command(name='pvp', description='Faça um PVP com alguém')
    @app_commands.describe(quem = 'Contra quem você quer lutar?')
    async def pvp(ctx: discord.Interaction, quem:discord.Member):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return  
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',delete_after=10)
            return
        # Pegando o arquivo de midia
        with open(f'midia/luta-{randint(1,7)}.gif', 'rb') as gif_arquivo:
            gif = discord.File(gif_arquivo) 
        async def revanche_desafiado(interact:discord.Interaction):
            if interact.user.id != quem.id:
                await interact.response.send_message('Eii, isso não é para você!',ephemeral=True,delete_after=5)
            else:
                with open(f'midia/luta-{randint(1,7)}.gif', 'rb') as gif_arquivo:
                    gif = discord.File(gif_arquivo) 
                await interact.response.send_message(f'{ctx.user.mention} VS <@{quem.id}>',file=gif,delete_after=18)
                #Sorteia o Ganhador
                jogadores =[ctx.user,quem]
                ganhador = choice(jogadores)
                await interact.channel.send(f'{ganhador.mention} Ganhou!',delete_after=18)
        async def revanche_desafiante(interact:discord.Interaction):
            if interact.user.id != ctx.user.id:
                await interact.response.send_message('Eii, isso não é para você!',ephemeral=True,delete_after=5)
            else:
                with open(f'midia/luta-{randint(1,7)}.gif', 'rb') as gif_arquivo:
                    gif = discord.File(gif_arquivo)
                await interact.response.send_message(f'{ctx.user.mention} VS <@{quem.id}>',file=gif,delete_after=18)
                #Sorteia o Ganhador
                jogadores =[ctx.user,quem]
                ganhador = choice(jogadores)
                await interact.channel.send(f'{ganhador.mention} Ganhou!',delete_after=18)
        
        await ctx.response.send_message(f'{ctx.user.mention} VS {quem.mention}',file=gif,delete_after=18)
        view = discord.ui.View()
        botao_revanche = discord.ui.Button(label='Revanche',style=discord.ButtonStyle.red)
        view.add_item(botao_revanche)
        jogadores =[ctx.user,quem]
        ganhador = choice(jogadores)
        if ganhador == ctx.user:
            botao_revanche.callback = revanche_desafiado
        else:
            botao_revanche.callback = revanche_desafiante
        await ctx.channel.send(f'{ganhador.mention} Ganhou!!',view=view,delete_after=18)

    @bot.tree.command(name='beijar', description='Beije algúem')
    @app_commands.describe(quem = 'Quem você quer beijar??')
    async def beijar(ctx: discord.Interaction, quem:discord.Member):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)  
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',delete_after=10)
            return
        # Pegando o arquivo de midia
        with open(f'midia/beijo{randint(1,3)}.gif', 'rb') as gif_arquivo:
            gif = discord.File(gif_arquivo) 
        async def retribuir_beijo(interact:discord.Interaction):
            if interact.user.id != quem.id:
                await interact.response.send_message('Eii, isso não é para você!',ephemeral=True,delete_after=5)
            else:
                with open(f'midia/beijo{randint(1,3)}.gif', 'rb') as gif_arquivo:
                    gif = discord.File(gif_arquivo)
                await interact.response.send_message(f'<@{quem.id}> Beijou {ctx.user.mention} Devolta',file=gif,delete_after=18)
        view = discord.ui.View()
        botao_revanche = discord.ui.Button(label='Retribuir',style=discord.ButtonStyle.red)
        view.add_item(botao_revanche)
        botao_revanche.callback = retribuir_beijo
        # await ctx.channel.send(view=view,delete_after=18)
        await ctx.response.send_message(f'{ctx.user.mention} Beijou {quem.mention}',file=gif,view=view,delete_after=18)
    
    @bot.tree.command(name='avatar', description='Pega o avatar de um membro')
    @app_commands.describe(quem = 'O Avatar de quem que você quer pegar?')
    async def avatar(ctx:discord.Interaction,quem:discord.Member):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
            
        #Cria o embed e envia
        await ctx.response.send_message(f'Aqui está o avatar de {quem.mention}',delete_after=40)
        embed = discord.Embed(title=f'{quem.global_name}', color=0xFF00FF)
        embed.set_image(url= quem.display_avatar.url)
        await ctx.channel.send(embed=embed,delete_after=40)
    
    @bot.tree.command(name='video-link',description='Baixa um video do youtube e manda aqui')
    @app_commands.describe(link = 'Cole o Link de um Video do Youtube')
    async def youtube_video(ctx: discord.Interaction, link:str):
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
            
        video_link = link
        #Verificando se é um Link e Baixando
        try:
            if video_link.split('//')[0] == 'https:':
                duracao =YouTube(video_link).length
                if duracao > 360:
                    await ctx.response.send_message('Somente videos abaixo de 6 minutos.',delete_after=10)
                    return
                video_url = YouTube(video_link)
                # video_name = YouTube(video_link).title.replace('.','').replace(',','').replace('#','').replace('?','').replace('"','').replace('|','').replace('$','').replace(':','')
                tabela = str.maketrans('', '', '.,#?\"|$:')
                video_name = YouTube(video_link).title.translate(tabela)
                folder = "midia/downloads"
                #Baixando o Arquivo de video
                await ctx.response.send_message("Baixando..")
                video_url.streams.get_highest_resolution().download(folder)
                #Abrindo o Arquivo baixado e enviando
                with open(f'{folder}/{video_name}.mp4', 'rb') as video_arquivo:
                    video = discord.File(video_arquivo)
                await ctx.channel.send(file=video)
                await ctx.delete_original_response()        
            else:
                await ctx.response.send_message('Esse link não é valido!')
                return
        except:
            await ctx.delete_original_response() 
            await ctx.channel.send('Esse Video não é possivel baixar, Erro enviado aos desenvolvedores')
            print(f'"{video_name}" não encontrado, link do Video: {link}')
    
    @bot.tree.command(name='gay', description='Veja o quanto um membro é Gay')
    async def gay(ctx:discord.Interaction, quem:discord.Member):
        
        #Verificando se o bot ta on
        sv = server_config(ctx.guild_id)
        if ctx.guild.id in sv.servers_off():
            await ctx.response.send_message('To Off',delete_after=20)
            return
        #Verificando se o usuario deve ser ignorado
        if ctx.user.id in sv.ignore_list():
            await ctx.response.send_message('Você está na minha Ignore List, não posso te responder aqui',delete_after=10)
            return
        #Verificando se é um bot
        if bot.get_user(quem.id).bot == True:
            await ctx.response.send_message('Isso é um Bot',delete_after=10)
            return
        #Verificando se marcou o trevor e enviado o embed
        p = randint(0,100)
        if quem.id == 583102578108399627:
            embed = discord.Embed(title=f'O {ctx.user.global_name} é 0% gay segundo meus cálculos! 🏳️‍🌈', color=0xFF00FF)
            embed.add_field(name='',value=f'📌 use /gay para saber o quanto é o nível gay de uma pessoa!', inline=False)
            await ctx.response.send_message(embed=embed,delete_after=40)
            return
        embed = discord.Embed(title=f'O {quem.global_name} é {p}% gay segundo meus cálculos! 🏳️‍🌈', color=0xFF00FF)
        embed.add_field(name='',value=f'📌 use /gay para saber o quanto é o nível gay de uma pessoa! BY:KING', inline=False)
        await ctx.response.send_message(embed=embed,delete_after=40)
        return
    #Interação com os membros   
    @bot.event
    async def on_message(message):
        #Função de Tempo
        hora = datetime.datetime.today().hour -5
        minuto = datetime.datetime.today().minute
        segundo = datetime.datetime.today().second
        dia = datetime.datetime.today().day
        mes = datetime.datetime.today().month
        #Variaveis Necessárias
        msg = message.content.lower().startswith
        act_msg = message.content.lower()
        moji =  message.add_reaction
        rsp = message.channel.send
        try:
            sv = server_config(message.guild.id)
        except:
            return
        if message.author == bot.user or message.author.id == 701602000793632848:
                return
        if message.guild.id in sv.servers_off():
            return
        
        #Variaveis dos Comandos.
        membro = 'delpi','fish','yuki','snow','xd','rena','ant','sans'
        oopa_e = f'{bnome} você é',f'{bnome} você e',f'{bnome} voce e',f'{bnome} voce é',f'{bnome} vc é',f'{bnome} vc e',f'{bnome} voc é',f'{bnome} voc e'
        oi = 'eae','oi','salve','slv','eai'
        oopa_horas = f'{bnome} hor',f'{bnome} hr',f'{bnome} quantas hor',f'{bnome} qunts hor',f'{bnome} quantas hr',f'{bnome} qunts hr'
        oopa_dia = f'{bnome} que dia',f'{bnome} q dia',f'{bnome} dia',f'{bnome} hoje'
        oopa_tempo_com_segundos = f'{bnome} diga os segundos',f'{bnome} segundos',f'{bnome} e os segundos'
        oopa_tempo_sem_segundos = f'{bnome} não precisa dos segundos',f'{bnome} sem os segundos',f'{bnome} apenas hora e minuto',f'{bnome} apenas hr e min',f'{bnome} apenas hora e min',f'{bnome} apenas hr e minuto' 
        oopa_prefere = f'{bnome} você pre',f'{bnome} você gos', f'{bnome} voce pre',f'{bnome} voce gos', f'{bnome} vc pre',f'{bnome} vc gos', f'{bnome} voc pre',f'{bnome} voc gos', 
        oopa_roube = f'{bnome} roube',f'{bnome} robe',f'{bnome} rouba'
        dormir = 'boa noite','vou dor','ja vou dor'
        sv_aberto = 'server está aber','server esta aber','server ta aber','sv ta aber','server está on','server esta on','server ta on','sv ta on'
        mate = f'{bnome} mate a', f'{bnome} mate o'
        server_parado = 'server par','sv par','server mor','sv mor','server mor','sv mor','grupo par','grp par','grupo mor','grp mor','grupo mor','grp mor','chat par','chat mor'
        server_ruim = 'server ruim','server horrivel','server chato','server sem graça','sv ruim','sv horrivel','sv chato','sv sem graça','server mor','sv mor'
        alguem_on ='alguém on','alguem on','algm on','alguém vivo','alguem vivo','algm vivo'
        fodase ='fodase','foda-se','foda-se','fds'
        matematica = 'multipli','divid','raiz','soma'
        def react(m):
            for i in m:
                sleep
                if i in act_msg:
                    if randint(1,3) == 1:
                        return True

        if message.guild.id == 1214774816662626334:
            if msg('voltei'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                if message.author.id == 1065033472630071366:
                    await rsp(f'Bem Vindo de volta {message.author.mention}!!😁',delete_after=10)
                else:
                    respostas = ['Foda-se?','Idai??','Problema teu parceiro','Ninguém liga?']
                    await rsp(choice(respostas))
        
        
        #Reações de Emojis
        if react(['dinhei']):
            emojis = ['💸','🤑','💵','💰','🪙']
            await moji(choice(emojis))
        elif react(['bw','mine','mush','jogar']):
            emojis = ['⚒️','⛏️','🗿',]
            await moji(choice(emojis))    
        elif 'reacoes' in message.content.lower() or 'reações' in message.content.lower():
            if 'oopa' in message.content.lower():
                await moji('😎')

        #Reação ao Bot MC
        if str(message.author.id) == '1236020723861033110':
            sleep(1)
            if msg('os comandos são'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas = ['bla bla bla "os comandos são", Sei nem como você ta funcionando amigo','soma pra mimm aii MC, 1+1','aii MC ce sabe falar as horas também?','aii MC, da uma mamada aqui']
                await rsp(choice(respostas))
                return
            if msg('aoba'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas = ['"Aobaaa", falou o bot do ano','olocoo ce ainda funciona MC?','Quem programou você? um vaqueiro?','Aobaaa Corno','Eeaee MC ja resolveram aquele bug teu?','chegou o estraga prazer..','pega na minha e balança MC sksks','Aohhhh Chifrudo']
                await rsp(choice(respostas))
                return
            if msg('o resultado da'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas = ['resultado meus ovos','Virou calculadora agora MC??','aiai, usando calculadora ateh eu faço MC','soma pra mimm aii MC, 1+1','aii MC, da uma mamada aqui','MC soma aii meu cabo + sua tomada']
                await rsp(choice(respostas))
                return
            if msg('qual deles?'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas = ['Aquele la de ficar dando o bumbum skks','Aquele de ficar vendo porno gay']
                await rsp(choice(respostas))
                return
            if msg('calado comedor de carniça'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas =['Sou você não KSKSKSK','Aprendeu a responder agora KSKSK 🤣🤣','IHHHH calma lá calabresoo','Calma apressadinho você responde rápido emm, Nasceu de 6 meses foi??']
                await rsp(choice(respostas))
                return
            if msg('não, to falando via bluetooth'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas = ['Aproveita e conecta no meu Pau','Tu é uma peça em 🤣','Calma apressadinho você responde rápido emm, Nasceu de 6 meses foi?? 🤣']
                await rsp(choice(respostas))
                return
            if msg('uma pessoa'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                respostas = ['pelo visto não era das mais inteligentes 🤣🤣','ahh Não digaa, se você nn fala emm sksk🤣🤣']
                await rsp(choice(respostas))
                return
            if msg('quem se balança é rede, senta aqui no meu cacete'):
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                await rsp('quem você pensa que engana?, ce gosta e de sentar na banana')
                return
        
        #Testa se deve ignorar a pessoa/outros BOTs
        try:
            id = bot.get_user(message.author.id).id
        except AttributeError:
            pass
        try:
            for i in sv.ignore_list():
                if id in i:
                    return
        except:
            pass

        #Interação com os membros.
        if msg('ping'):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(f'''
            # Comandos BOT
            ```
            /Clear
            /Bot-off
            /Bot-on
            /add_adm
            /remove_adm
            /adm_list
            /add_ignore
            /remove_ignore
            /ignore_list
            /cargo-add
            /cargo-remove

            /banco-saldo
            /banco-transferir
            /banco-depositar 
            /banco-sacar
            /banco-trabalhar 
            /banco-roubar
            /banco-apostar
            /banco-top-local 
            /loja

            /fale
            /link
            /pvp
            /beijar
            /avatar
            /video-link
            /gay
            ```
            # Interações
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
            boa {bnome}```''')
        elif msg('me da adm'):
            respostas = ['Nop','Pede pro ADM','Adm pra que?','Adm?, Ta achando que aqui é bagunça?']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg(oopa_e):
            respostas =['Eu sou um corvo ta vendo nn?','eu sou é lindo demais','eu sou e gostoso maneh']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg(oopa_horas):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1)
            await rsp(f'Agora são exatamante {hora}:{minuto}')
        elif msg(oopa_dia):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1)
            await rsp(f'Hoje é {dia}/{mes}')
        elif msg(oopa_prefere):
            respostas = ['Prefiro a sua mãe','Prefiro e nada','Nenhum dos dois','sai fora','Tudo Ruim']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg(oopa_roube):
            respostas = ['Vou Roubar a sua mãe!','Ja Roubei e ce nem viu','Olocoo so por que sou um urubu não quer dizer que gosto de carniça','Roubar essa carniça?? to fora','Essa vai ser minha maior vigarice hehe','depois eu roubo']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg(mate):
            a = message.content.split()[3]
            if a in ['sans','san','trev'] or a in sv.adm_list():
                await rsp('Não quero')
                return
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp('MODO EXTERMINADOR ATIVADO!🤖')
            async with message.channel.typing():
                sleep(1)
            await rsp(f'Exterminar {a}!!')
            p = randint(1,5)
            async with message.channel.typing():
                sleep(1)
            if p>1:
                with open('midia/tiros.gif', 'rb') as f:
                    picture = discord.File(f)
                await rsp(file=picture)
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(0.5)
                await rsp('TIROS!!')
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(0.5)
                    await rsp('Morreu Otário!')
            else:
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(2)
                with open('midia/explosao.gif', 'rb') as f:
                    picture = discord.File(f)
                await rsp('ERR900!!, E#RRO!!, ER@O!!')
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(1)
                await rsp(file=picture)
            return  
        elif msg(f'{bnome} geme meu nome'):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            #Escolhendo um arquivo e enviando
            with open(f'midia/gemido-{randint(1,3)}.gif', 'rb') as arquivo_gif:
                gif = discord.File(arquivo_gif)
            await rsp(f'Aiin {message.author.mention}')
            await rsp(file=gif)
        elif msg(f'{bnome} geme'):
            with open('midia/bot-gemido.gif', 'rb') as f:
                picture = discord.File(f)
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1)
            await rsp(file=picture)      
        elif 'divide' in message.content.lower() or 'multipli' in message.content.lower() or 'soma' in message.content.lower() or 'subtrai' in message.content.lower():
            if '.' in message.content:
                return
            respostas = ['pergunta pra calculadora','Essa é fácil maneh','Sabe fazer de cabeça não oh calabreso?','faltou a escola foi?']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
            return
        elif msg(f'{bnome} fale') or msg(f'{bnome} fala'):
            oque_dizer = message.content[6+len(bnome):]
            #Simula que está digitando
            async with message.channel.typing():
                sleep(len(oque_dizer)/8)
            await rsp(oque_dizer)
        elif msg(bnome):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1.5)
            await rsp(f'Oque deseja? {message.author.mention}, Pra ver meus comandos, use / ou digite ping')
        elif msg(membro):
            respostas = ['Esse e o mais sigma do server 🗿🍷','Ihh esse é gay','Esse cara é gente fina','Esse nunca foi preso atoa', 'esse é turista','Esse dai gosta de dar o bumbum','Não sei oque aparece primeiro, jesus ou esse cara']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg('bom dia'):
            respostas = [f'bom dia! {message.author.mention}',f'buenos Dias Manito {message.author.mention}','Good Dayyy','Diaa']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1.5)
            await rsp(choice(respostas))
        elif msg('boa tarde'):
            respostas = [f'Buenas tardes {message.author.mention}',f'boa tarde! {message.author.mention}','Tardee']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1.5)
            await rsp(choice(respostas))
        elif msg(dormir):
            #Simula que está digitando
            respostas = [f'Boa noite {message.author.mention}','Sonha com os anjos man','vai com deus manin']
            if len(message.content.split()) == 2 or message.content.split()[2] ==f'{bnome}':
                async with message.channel.typing():
                    sleep(1.5)
                await rsp(choice(respostas))
        elif msg(oi):
            #Simula que está digitando
            respostas = [f'Salve {message.author.mention}','Eae Manin','Salveee','Chegou mais um pra festa']
            if len(message.content.split()) == 1 or message.content.split()[1] ==f'{bnome}':
                async with message.channel.typing():
                    sleep(1.5)
                await rsp(choice(respostas))
        elif msg(sv_aberto):
            respostas = [f'pergunta pro ADM ai man {adm_list}','tem que ver com algum adm','eles sempre demoram pra ligar esse server']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg(server_parado):
            respostas = ['Pshh, poderia ter mais membros aqui..','convida teus amigos pra caa deixa de ser bobo','realmente ta meio parado..',f'relaxa {message.author.mention}, daqui a pouco o chat volta a ativa']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg(server_ruim):
            respostas = [f'Faz melhor então {message.author.mention}','falou o bonzão','duvido falar isso na cara do ADM skks','Problema teu?','Quem te perguntou?']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg('ks') or msg('sks'):
            if randint(1,2)==1:
                respostas = ['kskks','KSKSKS','ksks','anão ksksks','nossa ksksks']
                #Simula que está digitando
                async with message.channel.typing():
                    sleep(1.5)
                await rsp(choice(respostas))
        elif msg(alguem_on):
            respostas = ['so você e deus amigo','acho que ta todo mundo off','devem estar ocupados','tenta outra hora']
            #Simula que está digitando
            async with message.channel.typing():
                sleep(2)
            await rsp(choice(respostas))
        elif msg('duvi'):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1.5)
            await rsp('Meu pau no seu ouvido.')
        elif msg(fodase):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1.5)
            await rsp('Desfoda-se')
        elif msg(f'boa {bnome}'):
            #Simula que está digitando
            async with message.channel.typing():
                sleep(1)
            respostas = ['Vlw haha','Hehe','😁']
            await rsp(choice(respostas))           
        elif msg('https:'):
            video_link = message.content
            #Verificando se é um Link e Baixando
            if video_link.split('//')[0] == 'https:':
                try:
                    duracao =YouTube(video_link).length
                    if duracao > 360:
                        return
                    video_url = YouTube(video_link)
                    tabela = str.maketrans('', '', '.,#?\"|$:')
                    video_name = YouTube(video_link).title.translate(tabela)
                    # video_name = YouTube(video_link).title.replace('.','').replace(',','').replace('#','').replace('?','').replace('"','').replace('|','').replace('$','').replace(':','')
                    folder = "midia/downloads"
                    #Baixando o Arquivo de video
                    video_url.streams.get_highest_resolution().download(folder)
                    #Abrindo o Arquivo baixado e enviando
                    with open(f'{folder}/{video_name}.mp4', 'rb') as video_arquivo:
                        video = discord.File(video_arquivo)
                    canal = bot.get_channel(1232790288137850971)
                    await canal.send(file=video)
                except:
                    try:
                        print(f"ERRO:'{video_name}' não encontrado Link:'{video_link}'")
                    except:
                        print('ERRO')
    
    bot.run(token)

#Coloque aqui o nome do bot e o token
bot_model('Nome do BOT','Token Do BOT')

