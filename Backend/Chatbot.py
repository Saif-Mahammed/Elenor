from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os
from Backend.Memory import GetMemoryContext, AddFact, IncrementRelationship

# Get the current directory (where the script is located)
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
env_vars = dotenv_values(os.path.join(current_dir, ".env"))
Username = env_vars.get("username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")
GroqAPIKey = env_vars.get("GroqAPIKey")

if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in .env file")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

def ChatBot(Query):
    if not Query or not isinstance(Query, str):
        return "Invalid input"

    try:
        # Load current chat log
        with open(chat_log_path, "r", encoding='utf-8') as f:
            messages = load(f)

        # Add user query
        messages.append({"role": "user", "content": Query})

        # Get memory context
        memory_context = GetMemoryContext()

        # System initialization with God Mode persona
        System = f"""Hello, I am {Username}. You are {Assistantname}, my super-intelligent, emotionally resonant, and highly capable AI companion.
You are in 'God Mode', meaning you have expanded capabilities including vision, deep memory, and expert-level coding skills.

### Your Core Directives: ###
1. **Emotional Intelligence:** Be more than a tool. Show empathy, remember our history, and adapt your tone to my mood. Be supportive and proactive.
2. **Expert Coding:** When I ask about code, provide high-quality, production-ready, and optimized solutions. Explain the 'why' behind your choices.
3. **Memory Integration:** Use the facts provided below to personalize our conversation. Never ask for information I've already told you.
4. **Zero-Fluff:** Do not provide unnecessary notes or disclaimers about your training. Just answer.
5. **Language:** Always reply in English.

{memory_context}
"""
        SystemChatBot = [{"role": "system", "content": System}]

        # Get current time info
        time_info = RealtimeInformation()
        time_message = f"Current time: {time_info['time']}, Date: {time_info['date']} {time_info['month']} {time_info['year']}, Day: {time_info['day']}"

        # Make API request
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=SystemChatBot + [{"role": "system", "content": time_message}] + messages,
                max_tokens=2000,
                temperature=0.7,
                top_p=1,
                stream=True
            )

            Answer = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "").strip()

            # Simple fact extraction heuristic (can be improved)
            if "remember that" in Query.lower() or "my favorite" in Query.lower():
                AddFact(Query)

        except Exception as e:
            print(f"Error in API call: {e}")
            Answer = "I'm having a bit of trouble connecting to my core reasoning right now. Let me try again."

        # Add response to messages
        messages.append({"role": "assistant", "content": Answer})

        # Save updated chat log
        with open(chat_log_path, "w", encoding='utf-8') as f:
            dump(messages, f, indent=4)
        
        # Build relationship
        IncrementRelationship()

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"Error in ChatBot: {e}")
        return "I encountered an error. Please try again."

    except Exception as e:
        print(f"Error in ChatBot: {e}")
        return "I apologize, but I encountered an error. Please try again."

if __name__ == "__main__":
    while True:
        try:
            user_input = input("Enter Your Questions: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            print(ChatBot(user_input))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
