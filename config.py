import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    OPENAI_KEY = os.getenv('OPENAI_KEY')
    API_FOOTBALL_KEY = os.getenv('API_FOOTBALL_KEY')
    CANAL_ID = os.getenv('CANAL_ID')

    @staticmethod
    def verificar_variaveis():
        variaveis_necessarias = ['DISCORD_TOKEN', 'OPENAI_KEY', 'API_FOOTBALL_KEY', 'CANAL_ID']
        faltando = [var for var in variaveis_necessarias if not getattr(Config, var)]

        if faltando:
            raise EnvironmentError(f'Variáveis faltando no .env: {", ".join(faltando)}')
