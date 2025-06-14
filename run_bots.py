import threading
import os
import requests
from dotenv import load_dotenv
from src.rescue_gent.discord_bot import run_bot as run_discord_bot

load_dotenv()

# --- Telegram Bot Logic ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# We need a public URL for Telegram. For local dev, we'll use ngrok.
# In production on Render, this would be your public Render URL.
NGROK_URL = "http://localhost:4040" # ngrok's inspection API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def setup_telegram_webhook():
    """Sets up the Telegram webhook using the ngrok public URL."""
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found. Telegram bot will not start.")
        return

    try:
        # Get the public URL from the local ngrok API
        tunnels_res = requests.get(f"{NGROK_URL}/api/tunnels")
        tunnels_res.raise_for_status()
        # Find the https tunnel
        public_url = next((t['public_url'] for t in tunnels_res.json()['tunnels'] if t['proto'] == 'https'), None)
        
        if not public_url:
            print("\nError: Could not find an ngrok HTTPS tunnel.")
            print("Please make sure ngrok is running with 'ngrok http 8000' before starting this script.\n")
            return

        webhook_url = f"{public_url}/telegram-webhook/"
        set_webhook_res = requests.get(f"{TELEGRAM_API_URL}/setWebhook?url={webhook_url}")
        set_webhook_res.raise_for_status()
        
        print("--- Telegram Bot Setup ---")
        print(f"Webhook successfully set to: {webhook_url}")
        print("Telegram bot is now listening for messages.")
        print("--------------------------")

    except requests.exceptions.RequestException as e:
        print("\n--- Telegram Setup Failed ---")
        print("Could not connect to ngrok API. Is ngrok running on port 4040?")
        print(f"Error details: {e}")
        print("----------------------------\n")

# --- Main Execution ---
if __name__ == "__main__":
    # Setup Telegram in the main thread
    setup_telegram_webhook()

    # Run the Discord bot in a separate thread so it doesn't block Telegram setup
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.daemon = True # Allows main program to exit even if thread is running
    discord_thread.start()

    print("\n--- Both Bots Initialized ---")
    print("The Discord bot is running in the background.")
    print("Press CTRL+C to stop this script (and the bots).")
    
    # Keep the main thread alive to listen for KeyboardInterrupt
    try:
        discord_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down bots...")