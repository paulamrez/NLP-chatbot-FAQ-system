import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

# Set Key
client = OpenAI(api_key=api_key)

def call_openai_chatbot(user_input: str) -> str:
    """
    Uses OpenAI GPT-3.5 via openai>=1.0.0 client interface.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and friendly Student Success Advisor at Conestoga College."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ OpenAI API Error: {str(e)}"
