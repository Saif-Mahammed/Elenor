import os
# Suppress pygame support prompt and other potential duplicate library warnings on macOS
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
# Force objc to disable fork safety checks, which often causes these crashes on macOS
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

import sys

# Set QT_PLUGIN_PATH to PyQt6's plugins directory to avoid conflicts with system/Anaconda Qt5 plugins
# This must be done before any PyQt6 imports
try:
    import PyQt6
    pyqt_path = os.path.dirname(PyQt6.__file__)
    plugin_path = os.path.join(pyqt_path, "Qt6", "plugins")
    if os.path.exists(plugin_path):
        os.environ["QT_PLUGIN_PATH"] = plugin_path
except ImportError:
    pass

from pynput import keyboard

from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    get_temp_path,
    SetMicroPhoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicroPhoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from Backend.EmailIntegration import EmailClient
from Backend.Vision import CaptureScreen, CaptureCamera, AnalyzeImage
from dotenv import dotenv_values
from asyncio import run
import subprocess
import threading
import json
import time
import re
import requests
import importlib.util
from pynput import keyboard

current_dir = os.getcwd()

def OnShortcutPressed():
    """Triggered by global keyboard shortcut."""
    print("\nShortcut detected! Activating ELENOR OMNI...")
    # Use a thread to avoid blocking the listener
    threading.Thread(target=MainExecution).start()

def StartShortcutListener():
    """Starts a global shortcut listener in the background."""
    with keyboard.GlobalHotKeys({
        '<cmd>+<shift>+e': OnShortcutPressed
    }) as h:
        h.join()

# Plugin Marketplace Loader
def LoadPlugins():
    plugins = {}
    plugin_dir = os.path.join(current_dir, "Plugins")
    if not os.path.exists(plugin_dir):
        os.makedirs(plugin_dir)
        return plugins
    
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py"):
            name = filename[:-3]
            path = os.path.join(plugin_dir, filename)
            spec = importlib.util.spec_from_file_location(name, path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            plugins[name] = mod
    return plugins

PLUGINS = LoadPlugins()

def CallOllama(prompt, model="llama3.1"):
    """Fallback logic to use local Ollama model if cloud fails."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from local model.")
        return "Local model unreachable."
    except Exception as e:
        return f"Local fallback failed: {e}"

env_vars = dotenv_values(".env")
Username = env_vars.get("username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")

DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''

subprocesses = []
Functions = [
    "open", "close", "play", "system", "content", "google search", "youtube search",
    "system stats", "battery status", "media control", "file manipulation",
    "deep web research", "plugin" # Generic trigger for plugins not directly mapped
]

def ShowDefaultChatIfNoChats():
    try:
        if not os.path.exists('Data'):
            os.makedirs('Data')
        chat_log_path = os.path.join('Data', 'ChatLog.json')
        if not os.path.exists(chat_log_path):
            with open(chat_log_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
                
        with open(chat_log_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if len(content) <= 5:
                with open(get_temp_path('Database.data'), 'w', encoding='utf-8') as db_file:
                    db_file.write(DefaultMessage)

                with open(get_temp_path('Responses.data'), 'w', encoding='utf-8') as resp_file:
                    resp_file.write("")
    except Exception as e:
        print(f"Error in ShowDefaultChatIfNoChats: {e}")

def ReadChatLogJson():
    try:
        chat_log_path = os.path.join('Data', 'ChatLog.json')
        if not os.path.exists(chat_log_path):
            return []
        with open(chat_log_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading chat log: {e}")
        return []

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        role = entry.get("role", "")
        content = entry.get("content", "")
        if role == "user":
            formatted_chatlog += f"User: {content}\n"
        elif role == "assistant":
            formatted_chatlog += f"Assistant: {content}\n"
    
    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(get_temp_path('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))


def ShowChatsOnGUI():
    try:
        db_path = get_temp_path('Database.data')
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as file:
                Data = file.read()
                if len(Data.strip()) > 0:
                    with open(db_path, 'w', encoding='utf-8') as write_file:
                        write_file.write(Data)
    except Exception as e:
        print(f"Error in ShowChatsOnGUI: {e}")

def InitialExecution():
    try:
        # Create necessary directories
        os.makedirs('Data', exist_ok=True)
        os.makedirs(os.path.join('Frontend', 'Files'), exist_ok=True)
        
        # Initialize status files with correct initial states before importing other modules
        SetAssistantStatus("Available...")
        SetMicroPhoneStatus("True")
        
        # Create empty response file
        with open(get_temp_path('Responses.data'), 'w', encoding='utf-8') as file:
            file.write("")

        # Initialize pygame mixer
        import pygame
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Pygame mixer initialization error: {e}")
        
        # Initialize speech recognition driver
        from Backend.SpeechToText import InitializeDriver
        InitializeDriver()
        
        # Initialize chat history
        ShowTextToScreen("")
        ShowDefaultChatIfNoChats()
        ChatLogIntegration()
        ShowChatsOnGUI()
        
        # Start the logic thread after everything is initialized
        thread1 = threading.Thread(target=FirstThread, daemon=True)
        thread1.start()
        
        print("Initialization complete - System is ready")
    except Exception as e:
        print(f"Error in InitialExecution: {e}")

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    EmailExecution = False
    PluginExecution = False

    SetAssistantStatus("Listening ...")
    Query = SpeechRecognition()
    print(f"\nReceived Query: {Query}")
    ShowTextToScreen(f"{Username} : {Query}")

    if not Query or "error" in Query.lower() or "couldn't hear" in Query.lower():
         SetAssistantStatus("Available...")
         return False

    SetAssistantStatus("Thinking ...")
    
    # Check plugins first
    for name, plugin_module in PLUGINS.items():
        if hasattr(plugin_module, "can_handle") and plugin_module.can_handle(Query):
            SetAssistantStatus(f"Executing {name} Plugin...")
            response = plugin_module.execute(Query)
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(response)
            PluginExecution = True
            return True # Plugin handled the command
            
    # If no plugin handled it, use the main DMM
    Decision = FirstLayerDMM(Query)
    print(f"\nDecision from Model: {Decision}")

    G = any(i for i in Decision if i.startswith("general"))
    R = any(i for i in Decision if i.startswith("realtime"))

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    # Handle vision tasks
    for queries in Decision:
        if queries == "analyze screen":
            SetAssistantStatus("Seeing Screen...")
            image_path = CaptureScreen()
            if image_path:
                description = AnalyzeImage(image_path, Query)
                print(f"Vision Result: {description}")
                ShowTextToScreen(f"{Assistantname} : {description}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(description)
            return True
            
        elif queries == "analyze camera":
            SetAssistantStatus("Looking at you...")
            image_path = CaptureCamera()
            if image_path:
                description = AnalyzeImage(image_path, Query)
                print(f"Vision Result: {description}")
                ShowTextToScreen(f"{Assistantname} : {description}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(description)
            return True

        elif queries.startswith("analyze file "):
            SetAssistantStatus("Reading File...")
            file_path = queries.replace("analyze file ", "").strip()
            from Backend.Automation import AnalyzeFile
            response = AnalyzeFile(file_path)
            ShowTextToScreen(f"{Assistantname} : {response}")
            SetAssistantStatus("Answering ...")
            TextToSpeech("I have read the file. What would you like to know?")
            # We don't return True yet because we want to allow further discussion 
            # about the content in the same turn or next turn via ChatBot.
            # But for now, let's treat it as handled.
            return True

    # Handle image generation
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = queries.replace("generate", "").strip()
            ImageExecution = True

    # Handle email commands
    if EmailClient:
        for queries in Decision:
            if not EmailExecution:
                if queries.startswith("email"):
                    EmailExecution = True
                    email_client = EmailClient()
                    
                    if queries.startswith("email check"):
                        SetAssistantStatus("Checking emails...")
                        result = email_client.check_emails(limit=5)
                        Answer = result if isinstance(result, str) else "I've checked your emails."
                        ShowTextToScreen(f"{Assistantname} : {Answer}")
                        SetAssistantStatus("Answering ...")
                        TextToSpeech(Answer)
                    # Add other email handlers here if needed
                    return True

    # Handle general automation tasks and new Omni-Controls
    for queries in Decision:
        if not TaskExecution:
            if "system stats" in queries:
                response = GetSystemStats()
                ShowTextToScreen(f"{Assistantname} : {response}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(response)
                TaskExecution = True
                return True
            elif "battery status" in queries:
                response = GetBatteryStatus()
                ShowTextToScreen(f"{Assistantname} : {response}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(response)
                TaskExecution = True
                return True
            elif "media" in queries: # "media play", "media next", etc.
                response = MediaControl(queries)
                ShowTextToScreen(f"{Assistantname} : {response}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(response)
                TaskExecution = True
                return True
            elif "file manipulation" in queries: # e.g., "file manipulation write file foo.txt content hello"
                # Decision Model needs to be precise for this.
                # For now, it's a direct pass-through.
                response = FileManipulation(queries.split("file manipulation")[1].strip().split(" ")[0], 
                                            queries.split("file manipulation")[1].strip().split(" ")[1],
                                            " ".join(queries.split("file manipulation")[1].strip().split(" ")[2:]))
                ShowTextToScreen(f"{Assistantname} : {response}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(response)
                TaskExecution = True
                return True
            elif "deep web research" in queries:
                topic = queries.split("deep web research")[1].strip()
                response = DeepWebResearch(topic)
                ShowTextToScreen(f"{Assistantname} : {response}")
                SetAssistantStatus("Answering ...")
                TextToSpeech(response)
                TaskExecution = True
                return True
            # Existing automation logic
            elif any(queries.startswith(func) for func in ["open", "close", "play", "system", "content", "google search", "youtube search"]):
                run(Automation(list(Decision)))
                TaskExecution = True

    if ImageExecution:

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_data_path = os.path.join(current_dir, "Frontend", "Files", "ImageGeneration.data")
        image_gen_script = os.path.join(current_dir, "Backend", "ImageGeneration.py")
        
        with open(image_data_path, "w") as file:
            file.write(f"{ImageGenerationQuery},True")

        try:
            subprocess.Popen(['python3', image_gen_script],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE, shell=False)
        except Exception as e:
            print(f"Error running ImageGeneration.py: {e}")

    # Handle responses
    try:
        if G and R:
            SetAssistantStatus("Searching ...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(Answer)
            return True
        elif R:
            SetAssistantStatus("Searching ...")
            Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
            ShowTextToScreen(f"{Assistantname} : {Answer}")
            SetAssistantStatus("Answering ...")
            TextToSpeech(Answer)
            return True
        else:
            for Queries in Decision:
                if "general" in Queries:
                    SetAssistantStatus("Thinking ...")
                    QueryFinal = Queries.replace("general", "")
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    SetAssistantStatus("Answering ...")
                    TextToSpeech(Answer)
                    return True
                
                elif "exit" in Queries:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryModifier(QueryFinal))
                    ShowTextToScreen(f"{Assistantname} : {Answer}")
                    SetAssistantStatus("Answering ...")
                    TextToSpeech(Answer)
                    os._exit(1)
    except Exception as e:
        print(f"Error in response handling: {e}")
        return False

    return False

def FirstThread():
    processing_states = ["Thinking", "Listening", "Searching", "Answering"]
    
    while True:
        try:
            CurrentStatus = GetMicroPhoneStatus()
            AIStatus = GetAssistantStatus()
            
            if CurrentStatus == "True":
                if not any(state in AIStatus for state in processing_states):
                    # Passive listening for Wake Word
                    SetAssistantStatus("Waiting...")
                    Query = SpeechRecognition()
                    
                    if Assistantname.lower() in Query.lower():
                        print(f"Wake word '{Assistantname}' detected!")
                        SetAssistantStatus("Listening...")
                        TextToSpeech("Yes?") # Quick response to wake word
                        MainExecution()
            else:
                if (AIStatus != "Available..." and 
                    not any(state in AIStatus for state in processing_states)):
                    SetAssistantStatus("Available...")
            
            time.sleep(0.5) # Reduced delay for better responsiveness
            
        except Exception as e:
            print(f"Error in FirstThread: {e}")
            time.sleep(1.0)

def SecondThread():
    # Start the global shortcut listener in a background thread
    threading.Thread(target=StartShortcutListener, daemon=True).start()
    
    GraphicalUserInterface(on_start=InitialExecution)

if __name__ == "__main__":
    # Start the GUI on the main thread
    # InitialExecution will be called as a callback to start the background thread
    SecondThread()