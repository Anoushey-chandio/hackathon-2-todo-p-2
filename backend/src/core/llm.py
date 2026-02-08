from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Groq ki jagah ab hum Groq (Llama) use kar rahe hain
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Groq ka OpenAI-compatible base URL
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not found in environment variables.")

# 2. Client Setup
client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL,
)

# 3. Model Name (Groq ke liye ye best aur fast hai)
# Ise endpoints mein use karte waqt 'llama-3.3-70b-versatile' likhna
MODEL_NAME = "llama-3.3-70b-versatile"

# 4. Tool Definition (Same structure, standard OpenAI format)
ADD_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Add a new task to the user's todo list",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task",
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of the task",
                },
            },
            "required": ["title"],
        },
    },
}