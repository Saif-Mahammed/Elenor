from groq import Groq
from cohere import Client as CohereClient
from dotenv import dotenv_values
import os

env_vars = dotenv_values(".env")
GROQ_API_KEY = env_vars.get("GroqAPIKey")
COHERE_API_KEY = env_vars.get("CO_API_KEY")

if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
if COHERE_API_KEY:
    cohere_client = CohereClient(api_key=COHERE_API_KEY)

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["write a poem", "tell a story", "generate script", "creative writing"])

def execute(command):
    try:
        if not GROQ_API_KEY and not COHERE_API_KEY:
            return "Creative writing requires either GroqAPIKey or CO_API_KEY in your .env file."

        prompt = command.lower().replace("write a poem", "").replace("tell a story", "").replace("generate script", "").replace("creative writing", "").strip()
        if not prompt:
            return "Please provide a topic for your creative writing."

        if GROQ_API_KEY: # Prioritize Groq for speed
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Generate creative content based on this prompt: {prompt}"}],
                max_tokens=500,
                temperature=0.8
            ).choices[0].message.content
        elif COHERE_API_KEY:
            response = cohere_client.chat(
                model="command-r-08-2024",
                message=f"Generate creative content based on this prompt: {prompt}",
                temperature=0.8
            ).text
        else:
            return "No active LLM client found for creative writing."
            
        return response
    except Exception as e:
        return f"Error in creative writing: {e}"

