import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI

# 1. Path Setup (Smart Path Detection)
# This will look for the .env file in the root folder or the src folder
base_dir = Path(__file__).resolve().parent
potential_paths = [
    base_dir / ".env",
    base_dir / "src" / ".env"
]

env_path = None
for p in potential_paths:
    if p.exists():
        env_path = p
        break

# 2. Load .env file
if env_path:
    print(f"📄 .env file found at: {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    print(f"❌ Error: .env file not found! Please check root or src folder.")
    exit()

# 3. Securely fetch the API Key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def test_llm_direct():
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY could not be loaded. Check your variable name in .env")
        return

    print(f"🔑 Key loaded successfully! (Starts with: {GROQ_API_KEY[:7]}...)")

    # Groq Client Setup
    client = AsyncOpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )

    # Tool Definition (For adding a task)
    ADD_TASK_TOOL = {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task"},
                    "description": {"type": "string", "description": "Optional details about the task"}
                },
                "required": ["title"]
            }
        }
    }

    try:
        print("🚀 Connecting to Groq (Llama-3.3-70b)...")
        
        # Testing the chatbot with a task-related prompt
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Remind me to buy groceries tomorrow morning"}],
            tools=[ADD_TASK_TOOL],
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        tool_calls = message.tool_calls
        
        if tool_calls:
            print(f"✅ SUCCESS! Chatbot identified the task correctly.")
            print(f"🛠️ Function Called: {tool_calls[0].function.name}")
            print(f"📦 Arguments: {tool_calls[0].function.arguments}")
        else:
            print(f"🤖 Assistant Reply: {message.content}")
            
    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm_direct())