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
NOVITA_API_URL = "https://api.novita.ai/v3/openai/chat/completions"

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
client = groq_client # Alias for other modules to use

def parse_with_groq(message: str, schema: dict) -> dict:
    """Sends a request to the Groq API with the most robust prompt possible."""
    if not groq_client:
        raise ValueError("Groq API key not found.")
    
    # --- NEW, HYPER-STRICT PROMPT FOR GROQ ---
    # This prompt leaves no room for interpretation and focuses on JSON-only output.
    system_prompt = f"""
    You are a data extraction service. Your only purpose is to convert unstructured text into a structured JSON object.
    You MUST follow these rules:
    1.  Your ENTIRE response MUST be a single, valid JSON object.
    2.  The JSON object you return MUST strictly conform to the following JSON Schema.
    3.  Do NOT include any extra text, explanations, apologies, or markdown formatting like ```json.
    4.  Every required field in the schema MUST be present. If you cannot determine a value from the user's text, you MUST use a sensible default (e.g., 1 for urgency, "None" for injury_severity, null for location fields). Do not omit any fields.

    JSON Schema to conform to:
    {json.dumps(schema)}
    """
    
    try:
        print("--- [Groq] Sending request with hyper-strict prompt... ---")
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}, # Directly pass the user message
            ],
            model="llama-3.1-8b-instant", # Using the latest Llama 3.1 model available on Groq
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        
        response_content = completion.choices[0].message.content
        print(f"--- [Groq] Received raw response: {response_content} ---")
        return json.loads(response_content)

    except GroqError as e:
        print(f"Groq API Error: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Groq JSON Decode Error: Model did not return valid JSON. Error: {e}")
        print(f"Raw, unparseable response was: {response_content}")
        raise

# This function is unchanged but included for completeness.
def parse_with_novita(message: str, schema: dict) -> dict:
    """Sends a request to the Novita.ai API using the correct OpenAI-compatible standard."""
    if not NOVITA_API_KEY:
        raise ValueError("Novita.ai API key not found.")

    system_prompt = f"""
    You are an AI Triage Specialist for an international rescue organization. Your function is to analyze an incoming emergency report and convert it into a structured JSON object for immediate action.
    - The JSON object MUST conform to this JSON schema: {json.dumps(schema)}
    - Your response MUST be ONLY the JSON object, with no other text before or after it.
    """
    headers = { "Authorization": f"Bearer {NOVITA_API_KEY}", "Content-Type": "application/json" }
    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
        "response_format": { "type": "json_object" },
        "temperature": 0.0,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(NOVITA_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        return json.loads(content)
    except Exception as e:
        print(f"Novita related error: {e}")
        raise

# This function is unchanged but included for completeness.
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