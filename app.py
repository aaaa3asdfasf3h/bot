import discord
import os
import random
import asyncio
from flask import Flask
from threading import Thread

# --- SERWER WWW (Dla utrzymania bota przy życiu) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run_web_server():
    # Port 7860 jest standardem dla Hugging Face, Railway go zignoruje lub dostosuje
    app.run(host='0.0.0.0', port=7860)

# --- LOGIKA DISCORDA ---
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = 1480195851979587654

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Zalogowano jako: {client.user}')
    print(f'Monitoruję kanał: {TARGET_CHANNEL_ID}')

@client.event
async def on_message(message):
    # Ignoruj boty i wiadomości z innych kanałów
    if message.author.bot or message.channel.id != TARGET_CHANNEL_ID:
        return

    # 1. Usuń wiadomość użytkownika
    try:
        await message.delete()
    except Exception as e:
        print(f"Nie udało się usunąć wiadomości: {e}")
        return

    # 2. Stwórz tymczasowy webhook i wyślij wiadomość
    try:
        webhook = await message.channel.create_webhook(name="TemporaryAnon")
        await webhook.send(
            content=message.content,
            username=f"Anonim #{random.randint(1000, 9999)}",
            avatar_url="https://cdn-icons-png.flaticon.com/512/149/149071.png"
        )
        # 3. Usuń webhook zaraz po użyciu
        await webhook.delete()
    except Exception as e:
        print(f"Błąd webhooka: {e}")

# --- URUCHOMIENIE ---
if __name__ == "__main__":
    # Start serwera Flask w tle
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()
    
    # Start bota Discord
    if TOKEN:
        client.run(TOKEN)
    else:
        print("BŁĄD: Brak zmiennej DISCORD_TOKEN w ustawieniach!")a
