import os
import json
import requests
from groq import Groq, GroqError
from dotenv import load_dotenv
from .triage_logic import TriageData

# Load all environment variables
load_dotenv()

# --- Service Configuration ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NOVITA_API_KEY = os.getenv("NOVITA_API_KEY")

# --- THIS IS THE CORRECT, DOCUMENTATION-BASED URL ---
NOVITA_API_URL = "https://api.novita.ai/v3/openai/chat/completions"

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
client = groq_client # Alias for other modules to use

def parse_with_groq(message: str, schema: dict) -> dict:
    """Sends a request to the Groq API."""
    if not groq_client:
        raise ValueError("Groq API key not found.")
    
    system_prompt = f"""
    You are an AI Triage Specialist for an international rescue organization. Your sole task is to analyze an incoming emergency report and convert it into a structured JSON object. Precision is critical.
    - Your entire output MUST be a single, valid JSON object that strictly adheres to this schema: {json.dumps(schema)}
    """
    
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"EMERGENCY REPORT: '{message}'"},
            ],
            model="llama3-8b-8192",
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        return json.loads(completion.choices[0].message.content)
    except GroqError as e:
        print(f"Groq API Error: {e}")
        raise

def parse_with_novita(message: str, schema: dict) -> dict:
    """Sends a request to the Novita.ai API using the correct OpenAI-compatible standard."""
    if not NOVITA_API_KEY:
        raise ValueError("Novita.ai API key not found.")

    system_prompt = f"""
    You are an AI Triage Specialist for an international rescue organization. Your function is to analyze an incoming emergency report and convert it into a structured JSON object for immediate action.
    - The JSON object MUST conform to this JSON schema: {json.dumps(schema)}
    - Your response MUST be ONLY the JSON object, with no other text before or after it.
    """

    headers = {
        "Authorization": f"Bearer {NOVITA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # --- THIS PAYLOAD NOW MATCHES THE DOCUMENTATION EXACTLY ---
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct", # Using the recommended model from the docs
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "response_format": { "type": "json_object" }, # This is the key for guaranteed JSON output
        "temperature": 0.0,
        "max_tokens": 1024
    }
    
    try:
        print(f"--- [Novita] Sending request to a new URL: {NOVITA_API_URL} ---")
        response = requests.post(NOVITA_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status() # This will raise an error for 4xx/5xx responses
        
        # The response structure matches OpenAI, so we get the content directly
        content = response.json()['choices'][0]['message']['content']
        return json.loads(content)
        
    except requests.exceptions.RequestException as e:
        print(f"Novita API Error: {e}")
        raise
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Novita Response Error: Could not parse JSON from response. Error: {e}")
        print(f"Raw Response Text: {response.text}")
        raise

def parse_message_with_llm(message: str) -> TriageData:
    """
    Main function that routes the request to the selected LLM provider.
    """
    schema = TriageData.model_json_schema()
    
    print(f"--- Using LLM Provider: {LLM_PROVIDER} ---")
    
    try:
        if LLM_PROVIDER == "novita":
            response_json = parse_with_novita(message, schema)
        elif LLM_PROVIDER == "groq":
            response_json = parse_with_groq(message, schema)
        else:
            raise ValueError(f"Invalid LLM_PROVIDER specified in .env: {LLM_PROVIDER}")

        return TriageData(**response_json)

    except Exception as e:
        print(f"An error occurred during LLM parsing: {e}")
        return TriageData(urgency=1, people_affected=1, injury_severity="None", latitude=None, longitude=None, summary="Error: Could not parse emergency report.", resource_needs=[])