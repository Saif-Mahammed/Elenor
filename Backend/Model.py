import cohere
from rich import print
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values(".env")
chohereAPIKey = env_vars.get("CO_API_KEY")

# Initialize Cohere client
co = cohere.Client(api_key=chohereAPIKey)

# List of valid functions that could be used in responses
funcs = [
    "exit", "general", "realtime", "open", "close", "play",
    "generate image", "system", "content", "google search",
    "youtube search", "reminder", "email check", "email send", "email summarize",
    "analyze screen", "analyze camera", "analyze file", "system stats", "battery status",
    "media play", "media pause", "media next", "media previous",
    "file manipulation", "deep web research", "plugin execute" # General plugin trigger
]

messages = []

# Preamble to provide to the Cohere model for context
preamble = """
You are the ELENOR OMNI Decision-Making Model. You are super-intelligent and have total control over the system.
Your job is to categorize the user's intent into specific system functions.
-> Respond with 'system stats' if the user asks about CPU, RAM, or overall system health.
-> Respond with 'battery status' if the user asks about battery level or power.
-> Respond with 'media play', 'media pause', 'media next', or 'media previous' for music/video control.
-> Respond with 'analyze screen' for screen perception tasks.
-> Respond with 'analyze camera' for webcam perception tasks.
-> Respond with 'analyze file (path)' for reading and discussing local files like memory.md.
-> Respond with 'open (app)' for launching specific applications.
-> Respond with 'general (query)' for conversation.
-> Respond with 'realtime (query)' for internet searches.
-> Respond with 'file manipulation (command) (path) (content)' for reading/writing local files.
-> Respond with 'deep web research (topic)' for multi-tab internet intelligence gathering.
-> Respond with 'plugin execute (plugin_name) (action) (data)' for external plugin interactions (e.g., GitHub, Notion).
-> Respond with 'email check', 'email send (recipient, subject, message)', 'email summarize' for email.
-> Respond with 'reminder (time) (message)' for setting reminders.
-> Respond with 'content (topic)' for creative writing/content generation.
-> Respond with 'news digest' for current events.
-> Respond with 'log water (amount)', 'log steps (count)', 'set health goal (goal)', 'my health status' for health tracking.
-> Respond with 'explain to me (topic)', 'summarize article (url or text)', 'generate quiz (topic)' for learning.
... (categorize everything precisely)
"""

# Define a list to store chat history
ChatHistory = [
    {"role": "User", "message": "how much battery do I have?"},
    {"role": "Chatbot", "message": "battery status"},
    {"role": "User", "message": "check my system performance"},
    {"role": "Chatbot", "message": "system stats"},
    {"role": "User", "message": "play the next song"},
    {"role": "Chatbot", "message": "media next"},
    {"role": "User", "message": "Elenor, what's on my screen?"},
    {"role": "Chatbot", "message": "analyze screen"},
    {"role": "User", "message": "Look at my memory.md file and talk to me about it."},
    {"role": "Chatbot", "message": "analyze file memory.md"},
    {"role": "User", "message": "create a notion page titled 'Project Phoenix'"},
    {"role": "Chatbot", "message": "plugin execute notion create page Project Phoenix"},
    {"role": "User", "message": "write file /tmp/hello.txt content Hello World"},
    {"role": "Chatbot", "message": "file manipulation write /tmp/hello.txt content Hello World"},
    {"role": "User", "message": "deep web research on quantum computing breakthroughs"},
    {"role": "Chatbot", "message": "deep web research quantum computing breakthroughs"},
    {"role": "User", "message": "write a poem about a lost cat"},
    {"role": "Chatbot", "message": "content write a poem about a lost cat"},
    {"role": "User", "message": "what are the top headlines today?"},
    {"role": "Chatbot", "message": "news digest"},
    {"role": "User", "message": "turn on the living room lights"},
    {"role": "Chatbot", "message": "plugin execute smart_home turn on light living room"},
    {"role": "User", "message": "log 500ml of water"},
    {"role": "Chatbot", "message": "log water 500ml"},
    {"role": "User", "message": "explain quantum physics to me"},
    {"role": "Chatbot", "message": "explain to me quantum physics"},
    {"role": "User", "message": "set reminder for 8 AM to wake up"},
    {"role": "Chatbot", "message": "set reminder for 8 AM to wake up"},
    {"role": "User", "message": "what's on GitHub for this project?"},
    {"role": "Chatbot", "message": "plugin execute github list issues for Thechallangers/Jarvis"}
]



# First layer decision-making function
def FirstLayerDMM(prompt: str = "test"):
    messages.append({"role": "user", "content": f"{prompt}"})

    # Use a faster model and direct response (no stream) for 'dangerous efficiency'
    response = co.chat(
        model='command-r-plus', # 'plus' is often smarter but we can use 'command-r' for raw speed
        message=prompt,
        temperature=0.1, # Low temperature for precision
        chat_history=ChatHistory,
        prompt_truncation='AUTO',
        preamble=preamble
    ).text

    response = response.replace("\n", "")
    response = response.split(" , ")

    response = [i.strip() for i in response]

    temp = []

    # Filter out valid tasks based on the functions list
    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)  # Add valid tasks to the filtered list

    # Update response with the filtered list of tasks
    response = temp

    # If '(query)' is in the response, recursively call the function
    if "(query)" in response:
        newresponse = FirstLayerDMM(prompt=prompt)
        return newresponse  # Return the clarified response
    else:
        return response  # Return the filtered response

# Entry point for the script
if __name__ == "__main__":
    # Continuously prompt the user for input and process
    while True:
        print(FirstLayerDMM(input(">>> ")))  # Input from user and print the response
