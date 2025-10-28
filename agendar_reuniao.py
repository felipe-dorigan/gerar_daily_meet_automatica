import datetime
import holidays
import asyncio
import os
import pickle

# Bibliotecas Google
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

import time
import math
# Bibliotecas Discord
import discord

# --- Importar configurações ---
try:
    from config import EMAIL_CONVIDADO, DISCORD_TOKEN, DISCORD_CANAL_ID, MENSAGEM
except ImportError:
    print("❌ Erro: Arquivo config.py não encontrado!")
    print("📝 Copie o arquivo config.py.example para config.py e configure suas credenciais.")
    exit(1)

# --- Configurações fixas ---
HORARIO_REUNIAO = datetime.time(hour=8, minute=20)
PAIS_FERIADOS = "BR"  # Brasil

SCOPES = ['https://www.googleapis.com/auth/calendar']

# --- Passo 1: Autenticação com OAuth ---
def autenticar_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

# --- Passo 2: Criar/Usar reunião no Google Meet ---
def criar_reuniao_meet(service, data, hora, link_existente=None):
    inicio = datetime.datetime.combine(data, hora)
    fim = inicio + datetime.timedelta(hours=1)

    evento = {
        "summary": "Daily Automática",
        "start": {"dateTime": inicio.isoformat(), "timeZone": "America/Sao_Paulo"},
        "end": {"dateTime": fim.isoformat(), "timeZone": "America/Sao_Paulo"},
        "attendees": [{"email": EMAIL_CONVIDADO}],
    }

    # Se já temos um link, o adicionamos na descrição.
    # Se não, pedimos para a API criar um novo.
    if link_existente:
        evento["description"] = f"Link para a reunião: {link_existente}"
    else:
        evento["conferenceData"] = {
            "createRequest": {
                "requestId": f"daily-{data.strftime('%Y-%m-%d')}"
            }
        }

    evento_criado = service.events().insert(
        calendarId='primary',
        body=evento,
        conferenceDataVersion=1
    ).execute()

    # Se o link já existia, retornamos ele. Senão, pegamos o novo link criado.
    link_meet = link_existente or evento_criado.get("hangoutLink")

    return link_meet, inicio

# --- Passo 3: Verificar se é feriado ---
def eh_feriado(data):
    feriados = holidays.CountryHoliday(PAIS_FERIADOS)
    return data in feriados

# --- Passo 4: Enviar mensagem no Discord ---
async def enviar_discord(token, canal_id, mensagem):
    class ClienteDiscord(discord.Client):
        async def on_ready(self):
            canal = self.get_channel(canal_id)
            if canal:
                await canal.send(mensagem)
            await self.close()

    intents = discord.Intents.default()
    intents.message_content = True
    cliente = ClienteDiscord(intents=intents)
    await cliente.start(token)

# --- Passo 5: Função principal ---
async def main():
    service = autenticar_google()
    agora = datetime.datetime.now()
    
    # --- ALTERAÇÃO PARA REUTILIZAR LINK ---
    link_meet_file = 'link_meet.txt'
    link_meet = None

    # Tenta ler o link do arquivo
    if os.path.exists(link_meet_file):
        with open(link_meet_file, 'r') as f:
            link_meet = f.read().strip()

    # Calcula o próximo minuto múltiplo de 10
    minutos_arredondados = math.ceil(agora.minute / 10.0) * 10
    
    # Define a hora da reunião proposta, zerando segundos
    hora_reuniao = agora.replace(second=0, microsecond=0)

    # Se o minuto arredondado for 60, avança a hora e zera os minutos
    if minutos_arredondados >= 60:
        hora_reuniao = (hora_reuniao + datetime.timedelta(hours=1)).replace(minute=0)
    else:
        hora_reuniao = hora_reuniao.replace(minute=int(minutos_arredondados))

    # Se o horário agendado for em menos de 5 minutos, adia para o próximo horário redondo (mais 10 min)
    if (hora_reuniao - agora) < datetime.timedelta(minutes=5):
        hora_reuniao += datetime.timedelta(minutes=10)

    data = hora_reuniao.date()
    hora_final = hora_reuniao.time()

    # Gerar link e criar evento no calendário (reutilizando o link se ele existir)
    link_meet, horario = criar_reuniao_meet(service, data, hora_final, link_existente=link_meet)

    # Se um novo link foi criado, salva no arquivo para o futuro
    if not os.path.exists(link_meet_file):
        with open(link_meet_file, 'w') as f:
            f.write(link_meet)
    # --- FIM DA ALTERAÇÃO ---

    mensagem_discord = MENSAGEM.format(link_meet=link_meet, hora=horario.strftime("%H:%M"))

    print(f"Link do Google Meet: {link_meet} (reunião às {horario.strftime('%H:%M')})")

    # Enviar mensagem no Discord
    await enviar_discord(DISCORD_TOKEN, DISCORD_CANAL_ID, mensagem_discord)

# --- Execução ---
if __name__ == "__main__":
    asyncio.run(main())