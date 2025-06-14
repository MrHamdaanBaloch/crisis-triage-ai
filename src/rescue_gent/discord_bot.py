import discord
import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
API_TRIAGE_URL = "http://127.0.0.1:8000/triage/"
LISTEN_CHANNEL = "reports"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Discord Bot logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name == LISTEN_CHANNEL:
        print(f"Received Discord report from {message.author}: '{message.content}'")
        try:
            requests.post(API_TRIAGE_URL, json={"message": message.content}, timeout=10)
            await message.add_reaction('✅')
        except requests.exceptions.RequestException as e:
            await message.add_reaction('❌')
            print(f"Error forwarding Discord message to backend: {e}")

def run_bot():
    if not DISCORD_TOKEN:
        print("Error: DISCORD_BOT_TOKEN not found. Discord bot will not start.")
        return
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"Error starting Discord bot: {e}")