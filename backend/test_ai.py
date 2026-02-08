import asyncio
import json
from openai import AsyncOpenAI

# 1. Aapki Groq Key (gsk_...)
MY_KEY = "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"

async def test_llm_direct():
    # ZAROORI: Groq ke liye URL aur Key dono match karne chahiye
    client = AsyncOpenAI(
        api_key=MY_KEY,
        base_url="https://api.groq.com/openai/v1", # <--- Groq ka URL
    )

    ADD_TASK_TOOL = {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    }

    try:
        print("🚀 Connecting directly to Groq (Llama 3)...")
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile", # <--- Groq ka model
            messages=[{"role": "user", "content": "I need to buy milk today"}],
            tools=[ADD_TASK_TOOL],
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        tool_calls = message.tool_calls
        
        if tool_calls:
            print(f"✅ SUCCESS! Tool called: {tool_calls[0].function.name}")
            print(f"Arguments: {tool_calls[0].function.arguments}")
        else:
            print(f"Assistant Reply: {message.content}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_llm_direct())