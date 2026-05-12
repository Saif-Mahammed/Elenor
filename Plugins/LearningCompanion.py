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
    return any(keyword in command.lower() for keyword in ["explain to me", "summarize article", "generate quiz", "learn about"])

def execute(command):
    try:
        if not GROQ_API_KEY and not COHERE_API_KEY:
            return "Learning Companion requires either GroqAPIKey or CO_API_KEY in your .env file."

        response_text = ""
        if "explain to me" in command.lower() or "learn about" in command.lower():
            topic = command.lower().replace("explain to me", "").replace("learn about", "").strip()
            prompt = f"Explain the concept of '{topic}' in simple terms, as if to someone learning it for the first time."
        elif "summarize article" in command.lower():
            article_content = command.lower().split("summarize article")[1].strip()
            prompt = f"Summarize the following article or text: {article_content}"
        elif "generate quiz" in command.lower():
            quiz_topic = command.lower().split("generate quiz")[1].strip()
            prompt = f"Generate a short, multiple-choice quiz (3 questions) about '{quiz_topic}'."
        else:
            return "Learning command not understood."
        
        if not prompt: return "Please provide more details for the learning task."

        if GROQ_API_KEY:
            response_text = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=700,
                temperature=0.6
            ).choices[0].message.content
        elif COHERE_API_KEY:
            response_text = cohere_client.chat(
                model="command-r-08-2024",
                message=prompt,
                temperature=0.6
            ).text
        else:
            return "No active LLM client found for learning tasks."
            
        return response_text
    except Exception as e:
        return f"Error in Learning Companion: {e}"

