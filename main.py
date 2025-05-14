import discord
from discord import app_commands
from config import Config
import random
import string
import asyncio
import pytz
from datetime import datetime
from datetime import date
import time
import json
import os
from collections import defaultdict
import aiohttp
import openai

Config.verificar_variaveis()

class BotJoe(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix='!',
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print('Minha jornada é eterna. Que desafios o novo dia trará?')

    async def on_member_join(self, member):
        canal_id = int(Config.CANAL_ID)
        canal = self.get_channel(canal_id)
        if canal:
            await canal.send(f'Boas-vindas, {member.mention}. Que sua breve estadia neste reino seja... interessante. Eu sou Joe, uma lenda que precede sua chegada em incontáveis eras.')

    async def on_member_remove(self, member):
        canal_id = int(Config.CANAL_ID)
        canal = self.get_channel(canal_id)
        if canal:
            await canal.send(f'Adeus, {member.mention}. O seu ciclo se por aqui se fechou')


bot = BotJoe()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='ola', description='Diga Olá para Joe')
async def ola(interaction:discord.Integration):
    await interaction.response.send_message(f'Oi, dizeis? {interaction.user.mention}, o que há de novo sob o sol que eu já não tenha visto?')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='conselho', description='Pede um conselho a Joe')
async def conselho(interaction: discord.Interaction, mensagem: str):
    mensagem_lower = mensagem.lower()

    if 'futebol' in mensagem_lower:
        await interaction.response.send_message(f'Conselho sobre futebol, {interaction.user.mention}? Lembre-se, Flamengo e Arsenal são os verdadeiros titãs do esporte bretão!')
    elif 'amor' in mensagem_lower or 'relacionamento' in mensagem_lower:
        await interaction.response.send_message(f'Ah, o amor, {interaction.user.mention}... um labirinto que percorri incontáveis vezes. Lembre-se, a paciência é uma virtude, e nem sempre o coração mortal compreende os laços eternos.')
    elif 'guerra' in mensagem_lower or 'batalha' in mensagem_lower:
        await interaction.response.send_message(f'Conselho sobre a guerra, {interaction.user.mention}? Eu sou um veterano de eras. Escolha suas batalhas com sabedoria e lembre-se que nem toda vitória vale o preço.')
    elif 'vida' in mensagem_lower or 'existencia' in mensagem_lower:
        await interaction.response.send_message(f'A vida, {interaction.user.mention}... um breve piscar para vocês. Aproveite cada momento, pois para mim, eles se acumulam como poeira estelar.')
    elif 'argentina' in mensagem_lower or 'argentinos' in mensagem_lower or 'argentino' in mensagem_lower:
        await interaction.response.send_message(f'Se eu pudesse apagar um único evento da minha vasta linha do tempo, talvez seria o surgimento da Argentina.')
    else:
        await interaction.response.send_message(f'Você busca meu conselho sobre "{mensagem}", {interaction.user.mention}? Hmm... minhas experiências transcendem seus problemas cotidianos, mas reflita sobre a impermanência de todas as coisas.')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='duelo', description='Chame Joe para um duelo mortal')
async def duelo(interaction: discord.Interaction):
    resultado = random.random()

    if resultado < 0.85:  # 85% de chance
        respostas = [
            f'Hahaha! {interaction.user.mention}, você realmente achou que poderia vencer Joe? Eu lutei em mil batalhas antes mesmo de você nascer!',
            f'*Joe desvia com facilidade e aplica um golpe certeiro* {interaction.user.mention}, você é mais lento que um recruta no primeiro dia de treinamento!',
            f'Patético. {interaction.user.mention}, Eu sinto pena de você. Meu nome é Joe, guarde na memoria antes de morrer!',
            f'*Joe ri enquanto desarma você com um movimento* {interaction.user.mention}, isso foi tudo que você tem? Até meu avô lutava melhor - e ele estava morto!',
            f'Em um piscar de olhos, Joe já está atrás de você. {interaction.user.mention}, você nem viu o golpe que te derrubou.'
        ]
        mensagem = random.choice(respostas)

    elif resultado < 0.95:  # 10% de chance (total 95%)
        respostas = [
            f'{interaction.user.mention}, você tem habilidade... mas não o suficiente! *finaliza o combate*',
            f'Notável! {interaction.user.mention}, você conseguiu me acertar. Mas a guerra não se vence com um só golpe! *Joe contra-ataca*',
            f'{interaction.user.mention}, faz décadas que não levava um golpe assim... mas ainda não é o suficiente para derrotar Joe!',
            f'Você surpreendeu Joe, {interaction.user.mention}. Mas surpresa não vence batalhas! *prepara o ataque final*',
            f'{interaction.user.mention}, eu vi muitos como você... promissores, mas ainda verdes.'
        ]
        mensagem = random.choice(respostas)

    else:  # 5% de chance
        respostas = [
            f'Tem meu respeito, {interaction.user.mention}. Espero lembrar de você.',
            f'{interaction.user.mention}, vou lembrar desse nome. Nossa luta foi mais do que lendaria',
            f'Você lutou bem, {interaction.user.mention}. Mas à minha vítoria era inevitavel.'
        ]
        mensagem = random.choice(respostas)

    efeitos = ['⚔️', '💥', '🩸', '🔥', '🗡️']
    mensagem += ' ' + random.choice(efeitos)

    await interaction.response.send_message(mensagem)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='origem', description='Pergunte sobre a origem de Joe')
async def origem(interaction:discord.Integration):
    await interaction.response.send_message(f'Minha origem é envolta nos mistérios do tempo primordial. Antes dos humanos erguerem suas primeiras cidades, eu já caminhava por esta Terra.')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with open('timezones_expandidas.json', 'r', encoding='utf-8') as f:
    cidades = json.load(f)

@bot.tree.command(name='hora', description='Pergunte a Joe o horario de uma região do globo')
@app_commands.describe(cidade='Digite o nome da cidade.')
async def hora(interaction:discord.Integration, cidade: str):
    cidade_formatada = cidade.strip().title()

    if cidade_formatada not in cidades:
        await interaction.response.send_message(f'E eu lá tenho cara de relôgio? 😡')
        return
    
    fuso = cidades[cidade_formatada]
    agora = datetime.now(pytz.timezone(fuso))
    hora_formatada = agora.strftime('%H:%M:%S - %d/%m/%Y')

    await interaction.response.send_message(f'Agora são {hora_formatada} em {cidade_formatada}, coral.')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#openai.api_key = Config.OPENAI_KEY

#@bot.tree.command(name='gpt', description='Pergunte qualquer coisa ao veterano Joe')
#async def gpt(interaction: discord.Interaction, pergunta: str):
#    await interaction.response.defer()
#
#    try:
#        # Configuração direta da OpenAI (substitua pela sua chave)
#        openai.api_key = "sua-chave-openai-aqui"
#
#        response = openai.ChatCompletion.create(
#            model="gpt-3.5-turbo",
#            messages=[
#                {"role": "system", "content": """Você é Joe, veterano imortal de guerras através dos séculos.
#                Responda como um soldado experiente com humor negro e referências históricas. Seja direto e sarcástico.
#                Use no máximo 3 parágrafos curtos."""},
#                {"role": "user", "content": pergunta}
#            ],
#            max_tokens=500,
#            temperature=0.7
#        )
#
#        resposta = response.choices[0].message.content
#        await interaction.followup.send(f"{interaction.user.mention} {resposta}")
#
#    except Exception as e:
#        await interaction.followup.send(f"{interaction.user.mention} Estou cansado de você humano.")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='anime', description='Joe busca informações sobre um anime')
async def anime(interaction: discord.Interaction, nome: str):
    await interaction.response.defer()

    async with aiohttp.ClientSession() as session:
        url = f'https://api.jikan.moe/v4/anime?q={nome}&limit=1'
        async with session.get(url) as resp:
            if resp.status != 200:
                await interaction.followup.send('As visões estão turvas... não consegui acessar os arquivos sagrados do MyAnimeList.')
                return

            data = await resp.json()

            if not data['data']:
                await interaction.followup.send(f'Nenhum anime chamado **{nome}** foi encontrado nas crônicas antigas.')
                return

            anime_info = data['data'][0]
            titulo = anime_info['title']
            sinopse = anime_info['synopsis'][:500] + '...' if anime_info['synopsis'] else 'Sem sinopse.'
            score = anime_info['score'] or 'Sem nota'
            episodios = anime_info['episodes'] or '?'
            link = anime_info['url']

            await interaction.followup.send(
                f'**{titulo}**\n'
                f'📺 Episódios: {episodios} | ⭐ Nota: {score}\n'
                f'📖 {sinopse}\n'
                f'🔗 {link}\n\n'
                f'O que achas disso, mortal? Seria digno do meu tempo eterno?'
            )

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='roleta', description='Joe escolhe um número aleatório entre dois valores')
async def roleta(interaction: discord.Interaction, minimo: int, maximo: int):
    if minimo >= maximo:
        await interaction.response.send_message(f'{interaction.user.mention} Você acha que Joe é burro? O primeiro número deve ser menor que o segundo!')
        return

    if (maximo - minimo) > 1000000:
        await interaction.response.send_message(f'{interaction.user.mention} *examina os números* Você quer mesmo que eu conte até {maximo-minimo}? Nem nos meus piores pesadelos...')
        return

    numero = random.randint(minimo, maximo)

    respostas = [
        f'Entre {minimo} e {maximo}... {interaction.user.mention}, minha escolha é **{numero}**.',
        f'*Joe examina os números* Hmm... {interaction.user.mention}, vou com **{numero}**.',
        f'Na minha longa experiência... {interaction.user.mention}, **{numero}** parece uma boa escolha.',
        f'*Joe gira uma roleta imaginária* Pare! {interaction.user.mention}, o número é **{numero}**!',
        f'Pelos campos de batalha de mil eras... {interaction.user.mention}, escolho **{numero}**.',
        f'*Joe cospe no chão* {interaction.user.mention}, **{numero}**. Nem pense em questionar.',
        f'Na guerra, números são tudo. {interaction.user.mention}, hoje é **{numero}**.'
    ]

    mensagem = random.choice(respostas)

    if numero == 666:
        mensagem += '\n*Número azarado... gosto disso.*'
    elif numero == 14:
        mensagem += '\n*Meu número da sorte.*'
    elif numero == 73:
        mensagem += '\n*O melhor número é 73. Deve estar se perguntando o porque... 73 é o vigésimo primeiro número primo, seu contraio 37 é o decimo segundo e o seu contrario 21 é o produto da multiplicação de, se segure, 7 por 3. Hein, hein... estou mentindo?*'
    elif numero == 7 or numero == 777:
        mensagem += '\n*Bom sinal.*'
    elif numero == minimo:
        mensagem += f'\n*O mínimo... {interaction.user.mention}, você está com sorte hoje?*'
    elif numero == maximo:
        mensagem += f'\n*O máximo! {interaction.user.mention}, talvez você tenha o toque de Midas.*'

    await interaction.response.send_message(mensagem)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def carregar_db():
    if os.path.exists('cacador_db.json'):
        with open('cacador_db.json', 'r') as f:
            return json.load(f)
    return {}

def salvar_db(db):
    with open('cacador_db.json', 'w') as f:
        json.dump(db, f)

ESTRUTURA_PADRAO = {
    'elfo': 0,
    'alienigena': 0,
    'gigante': 0,
    'semideus': 0,
    'deus': 0,
    'argentino': 0,
    'nada': 0
}

@bot.tree.command(name='caçar', description='Nós caçamos criaturas lendárias... e registramos seus troféus')
async def cacar(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    db = carregar_db()

    if user_id not in db:
        db[user_id] = ESTRUTURA_PADRAO.copy()

    resultado = random.random()

    if resultado <= 0.05:
        presa = 'nada'
    elif resultado <= 0.50:
        presa = 'elfo'
    elif resultado <= 0.85:
        presa = 'alienigena'
    elif resultado <= 0.95:
        presa = 'gigante'
    elif resultado <= 0.99:
        presa = 'semideus'
    else:
        presa = 'deus'

    db[user_id][presa] += 1
    salvar_db(db)

    respostas = {
        'nada': [
            f'*Varremos o terreno* {interaction.user.mention}, só vimos poeira e... era um coelho. Vergonhoso.',
            f'{interaction.user.mention}, até nossas armas antigas se envergonharam. Nada digno hoje.'
        ],
        'elfo': [
            f'*Disparo certeiro* {interaction.user.mention}, abatemos um elfo das sombras. Dizem que vivem 300 anos...',
            f'{interaction.user.mention}, elfo eliminado. Guardem as orelhas. Nós preferimos os dentes.'
        ],
        'alienigena': [
            f'**SINAL DE VIDA EXTRATERRESTRE** {interaction.user.mention}, capturamos um Xenomorfo. Servirá de porta-copos.',
            f'{interaction.user.mention}, pegamos um \'E.T.\'...',
            f'Capturamos um alienigena. {interaction.user.mention}, o que faremos com ele?'
        ],
        'gigante': [
            f'*Explosão ensurdecedora* {interaction.user.mention}, derrubamos um gigante.',
            f'{interaction.user.mention}, cegamos um ciclope. Ironia divina.',
            f'Você derrubou um gigante com uma pedra, {interaction.user.mention}? Hahaha.'
        ],
        'semideus': [
            f'**SANGUE DIVINO DETECTADO** {interaction.user.mention}, executamos um filho de Ares. O Olimpo tremerá.',
            f'{interaction.user.mention}, aprisionamos um semideus. Pediu clemência... Lembramos a ele: clemência morreu em Stalingrado.',
            f'Um semideus, {interaction.user.mention}.'
        ],
        'deus': [
            f'**⚡ PANTEÃO ABALADO ⚡** {interaction.user.mention}, NÓS DERROTAMOS THOR. REPITAM: NÓS. MATAMOS. UM. DEUS.',
            f'{interaction.user.mention}, somos uma dupla e tanto, derrotamos um deus.',
            f'Nunca vi um deus tão fraco. {interaction.user.mention}, nem precisamos chamar o Hulk.'
        ],
        'argentino': [
            f'Ei, {interaction.user.mention}, capturamos um argentino! *Queimamos o corpo 3 vezes*',
            f'{interaction.user.mention}, exterminamos a pior das criaturas... um argentino com mate. Atiramos primeiro.'
        ]
    }

    if random.random() <= 0.003:
        presa = 'argentino'

    mensagem = random.choice(respostas[presa])
    emojis = {
        'nada': '🕳️',
        'elfo': '🧝‍♂️🔫',
        'alienigena': '👽💥',
        'gigante': '👹🩸',
        'semideus': '⚡⚰️',
        'deus': '☠️👑',
        'argentino': '💀🇦🇷'
    }
    await interaction.response.send_message(f'{mensagem} {emojis[presa]}')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='trofeus', description='Mostra seu hall da fama como caçador')
async def trofeus(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    db = carregar_db()

    if user_id not in db:
        await interaction.response.send_message(f'{interaction.user.mention}, você ainda não caçou nada. Patético.')
        return

    stats = db[user_id]
    embed = discord.Embed(
        title=f'Hall da Fama de {interaction.user.name}',
        description='*Estatísticas oficiais do caçador*',
        color=0x8B0000  # Vermelho-sangue
    )
    embed.add_field(name='🏹 Criaturas Caçadas', value=f"""
    • Elfos: {stats['elfo']}
    • Alienígenas: {stats['alienigena']}
    • Gigantes: {stats['gigante']}
    • Semideuses: {stats['semideus']}
    • Deuses: {stats['deus']}
    • Argentinos: {stats['argentino']}
    """)
    embed.set_footer(text='Nós observamos seus progressos...')

    await interaction.response.send_message(embed=embed)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
API_KEY = Config.API_FOOTBALL_KEY

HEADERS = {
    "x-apisports-key": API_KEY
}

LIGAS_TOP5 = {
    "Premier League": 39,
    "La Liga": 140,
    "Serie A": 135,
    "Bundesliga": 78,
    "Brasileirão": 71
}

@bot.tree.command(name='jogos_hoje', description='Joe diz os jogos do dia das principais ligas do mundo')
async def jogos_hoje(interaction: discord.Interaction):
    await interaction.response.defer()
    hoje = datetime.now().date().isoformat()
    resultados = []

    async with aiohttp.ClientSession() as session:
        for nome_liga, liga_id in LIGAS_TOP5.items():
            url = f"https://v3.football.api-sports.io/fixtures?date={hoje}&league={liga_id}&season=2024"
            async with session.get(url, headers=HEADERS) as resp:
                data = await resp.json()
                jogos = data.get('response', [])

                if jogos:
                    resultados.append(f"🏆 **{nome_liga}**")
                    for jogo in jogos:
                        casa = jogo['teams']['home']['name']
                        fora = jogo['teams']['away']['name']
                        hora_utc = jogo['fixture']['date'][11:16]
                        resultados.append(f"   ⚽ {casa} x {fora} — `{hora_utc} UTC`")
                    resultados.append("")

    if resultados:
        resposta = "\n".join(resultados)
    else:
        resposta = "Hoje tá mais parado que VAR em amistoso. Nenhum jogo nas top-5 ligas."

    await interaction.followup.send(content=f"📅 **Jogos de hoje:**\n{resposta}")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@bot.tree.command(name='gerar_senha', description='Joe cria uma senha segura para você')
@app_commands.describe(
    tamanho='Quantos caracteres a senha deve ter (1 a 64)',
    complexidade='Nível: apenas_numeros, numeros_e_letras ou completa'
)
async def gerar_senha(interaction: discord.Interaction, tamanho: int, complexidade: str):
    if tamanho < 1:
        await interaction.response.send_message(
            'Você quer uma senha ou não? 🤨 Não existe uma senha com menos de um caracter.',
            ephemeral=True
        )
        return
    elif tamanho > 64:
        await interaction.response.send_message(
            'Você quer que eu escreva uma bíblia ou uma senha? Só vou escrever no máximo 64 caracteres.',
            ephemeral=True
        )
        return

    complexidade = complexidade.lower()
    
    def gerar_senha_segura():
        for _ in range(100):
            if complexidade == 'apenas_numeros':
                senha = ''.join(random.choices(string.digits, k=tamanho))
                return senha
            
            elif complexidade == 'numeros_e_letras':
                senha = ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))
                if any(c.isdigit() for c in senha) and any(c.isalpha() for c in senha):
                    return senha
                
            elif complexidade == 'completa':
                senha = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=tamanho))
                if (any(c.isdigit() for c in senha) and (any(c.isalpha() for c in senha) and (any(c in string.punctuation for c in senha)))):
                    return senha

        return senha

    if complexidade not in ['apenas_numeros', 'numeros_e_letras', 'completa']:
        await interaction.response.send_message(
            'Complexidade inválida. Use: `apenas_numeros`, `numeros_e_letras` ou `completa`.',
            ephemeral=True
        )
        return

    senha = gerar_senha_segura()

    await interaction.response.send_message(
        f'Fico feliz que você confia na minha experiência para criar uma senha segura. 🔐\n\n`{senha}`\n\n'
        'Essa mensagem fica só entre nós, ninguém mais pode ver... então não compartilhe com os outros mortais! 😏',
        ephemeral=True
    )

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

bot.run(Config.DISCORD_TOKEN) #.env