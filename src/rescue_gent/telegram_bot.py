import os
import httpx  # <-- Use the new library
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN or len(TELEGRAM_BOT_TOKEN) < 20: # Basic check for a valid token format
    print("="*60)
    print("FATAL ERROR: TELEGRAM_BOT_TOKEN is missing, invalid, or too short.")
    print("Please ensure your .env file is correct and contains the full token.")
    print("="*60)
    # Exit cleanly so the user knows this is the problem
    exit()

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def set_telegram_webhook(public_url: str):
    """
    This function tells Telegram where to send messages using the httpx client.
    """
    webhook_url = f"{public_url}/telegram-webhook/"
    set_webhook_api_url = f"{TELEGRAM_API_URL}/setWebhook"
    params = {'url': webhook_url}
    
    print(f"Attempting to set Telegram webhook to: {webhook_url}")
    
    try:
        # Use a timeout to prevent hanging, and use the more resilient httpx client
        with httpx.Client() as client:
            response = client.get(set_webhook_api_url, params=params, timeout=10.0)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            
        result = response.json()
        if result.get("ok"):
            print("="*60)
            print(f"SUCCESS: Telegram webhook was set successfully!")
            print(f"Description: {result.get('description')}")
            print("="*60)
        else:
            print("="*60)
            print(f"ERROR: Telegram returned an error when setting webhook:")
            print(result)
            print("="*60)
            
    except httpx.RequestError as e:
        print("="*60)
        print(f"FATAL NETWORK ERROR: Failed to connect to Telegram API: {e}")
        print("This is likely a network issue (firewall, ISP blocking) or a DNS problem.")
        print("Consider using a VPN and trying again.")
        print("="*60)
    except Exception as e:
        print("="*60)
        print(f"An unexpected error occurred: {e}")
        print("="*60)

# This is the part that makes the script runnable
if __name__ == "__main__":
    # --- THIS IS THE CORRECTED LOGIC ---
    # It directly calls the function without any confusing checks.
    
    # 1. Paste your active localtunnel URL here.
    #    It must be the full https address.
    public_url = "https://myuniquecrisisagent123.loca.lt"
    
    print(f"Preparing to set webhook with URL: {public_url}")
    
    # 2. Call the function to set the webhook.
    set_telegram_webhook(public_url)
    