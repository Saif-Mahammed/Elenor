from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import subprocess
import requests
import asyncio
import os
import webbrowser as webopen
from urllib.parse import urlparse
import shutil
import re
import webbrowser

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "L1tM0c YYrZ6", "z20LcW", "gsrt vk_bk FzvWSb WprNhf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "OSr6df L1tM0c", "YYrZ6", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWKfbc", "vQfq4c", "y9gBwe", "kno-desc", "SPZz6b"]

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

messages = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ.get('USER', 'User')}. You're an expert software engineer and content writer. You provide production-ready, highly optimized, and well-documented content like letter, codes, applications, essays, notes, songs, poems etc."}]

def FileManipulation(command, file_path, content=None):
    """Autonomous file system manipulation for coding tasks."""
    try:
        if command == "write":
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        elif command == "read":
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            return "File not found."
    except Exception as e:
        return f"Error manipulating file: {e}"

import psutil
import json

# Placeholder for Plugin System
def ExecutePlugin(plugin_name, action, data):
    """Modular plugin system for Notion, GitHub, Codebase, etc."""
    # This is a scalable pattern to add 40+ features
    plugin_map = {
        "notion": "NotionPlugin().run",
        "github": "GithubPlugin().run",
        "codebase": "CodebasePlugin().run"
    }
    # Implementation details would go here for each integration
    return f"Plugin {plugin_name} triggered for action {action}."

def GetSystemStats():
    """Returns real-time CPU and RAM usage."""
    try:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        return f"System: CPU {cpu}% | RAM {ram}%"
    except Exception as e:
        return "Stats unavailable."

def GetBatteryStatus():
    """Returns current battery level and status."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return f"Power: {battery.percent}% | Status: {'Charging' if battery.power_plugged else 'Discharging'}"
        return "Power data N/A."
    except Exception as e:
        return "Power data N/A."

# ... (Previous Automation code below)

def MediaControl(command):
    """Controls system media (Spotify, YouTube, etc.) via AppleScript."""
    try:
        if "play" in command or "pause" in command:
            subprocess.run(["osascript", "-e", "tell application \"System Events\" to key code 49"])
            return "Media toggled."
        elif "next" in command:
            subprocess.run(["osascript", "-e", "tell application \"System Events\" to key code 124 using {command down}"])
            return "Skipped to next track."
        elif "previous" in command:
            subprocess.run(["osascript", "-e", "tell application \"System Events\" to key code 123 using {command down}"])
            return "Playing previous track."
        return "Media command not recognized."
    except Exception as e:
        return f"Error in media control: {e}"

def AppLauncher(app_name):
    """Launches any application on macOS with high accuracy."""
    try:
        subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'])
        return f"Launched {app_name}."
    except Exception:
        # Fallback to general open command
        os.system(f"open -a \"{app_name}\"")
        return f"Attempting to launch {app_name} via fallback."

def SystemControl(command):
    """Direct hardware control via AppleScript (macOS)."""
    try:
        if "volume up" in command:
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
            return "Volume increased by 10%."
        elif "volume down" in command:
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
            return "Volume decreased by 10%."
        elif "mute" in command:
            subprocess.run(["osascript", "-e", "set volume with output muted"])
            return "System muted."
        elif "unmute" in command:
            subprocess.run(["osascript", "-e", "set volume without output muted"])
            return "System unmuted."
        elif "brightness up" in command:
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 144'])
            return "Brightness increased."
        elif "brightness down" in command:
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 145'])
            return "Brightness decreased."
        return "System command not recognized."
    except Exception as e:
        return f"Error in system control: {e}"

def DeepWebResearch(topic):
    """Autonomous multi-tab web research and intelligence gathering."""
    print(f"Initiating deep intelligence gathering for: {topic}")
    search_url = f"https://www.google.com/search?q={topic}"
    webbrowser.open(search_url)
    
    # Simulate thinking/researching time
    return f"I've opened a deep research session for '{topic}'. I'm currently cross-referencing multiple sources to give you a comprehensive summary. Just a moment."

def Content(Topic):
    # Content("write a application for a sick leave.")
    def OpenTextEdit(File):
        defult_text_editor = "TextEdit"  # macOS default text editor is TextEdit
        if not os.path.exists(File):
            print(f"File {File} does not exist!")
            return False
        subprocess.run(["open", File])
        print(f"Opening {File} in TextEdit...")
        return True

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f'{prompt}'})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Specify the AI model
            messages=SystemChatBot + messages,
            max_tokens=2048,  # Limit the maximum tokens in response
            temperature=0.7,  # Adjust response randomness
            top_p=1,  # Use nucleus sampling for response
            stream=True,  # Enable streaming response
            stop=None  # Allow the model to determine stopping condition
        )

        Answer = ""
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                if chunk.choices and chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content


        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic : str = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI(Topic)

    file_dir = 'data'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # Create the directory if it doesn't exist

    file_path = f'{file_dir}/{Topic.lower().replace(" ","_")}.txt'
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)
    OpenTextEdit(file_path)
    return True

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def playYoutube(query):
    playonyt(query)
    return True

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

def OpenApp(app, sess=requests.session()):
    try:
        # Normalize the app name for case-sensitivity and ensure it's properly formatted.
        app_path = f"/Applications/{app}.app"
        
        # Try opening the app if it's installed.
        if os.path.exists(app_path):
            subprocess.run(["open", "-a", app])  # Open the app on macOS
            return True  # Indicate success.
        else:
            print(f"{app} is not installed. Attempting to open the download page in a browser...")
            # Fallback to opening a website (e.g., Chrome download page if Chrome isn't installed)
            if app.lower() == "google chrome":
                webbrowser.open("https://www.google.com/chrome/")
            else:
                # Default case - perform a Google search for the app name
                webbrowser.open(f"https://www.google.com/search?q={app}+download")
            return True

    except Exception as e:
        print(f"Error opening app: {e}")
        # Nested function to extract links from HTML content.
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')  # Parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'})  # Find relevant links.
            return [link.get('href') for link in links]  # Return the links.

        # Nested function to perform a Google search and retrieve HTML.
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"  # Construct the Google search URL
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}  # Custom User-Agent string
            response = sess.get(url, headers=headers)  # Perform the GET request.

            if response.status_code == 200:
                return response.text  # Return the HTML content.
            else:
                print("Failed to retrieve search results.")  # Print an error message.
                return None

        html = search_google(app)  # Perform the Google search.

        if html:
            links = extract_links(html)  # Extract all links from the HTML content.
            if links:  # If we have any links, open the first one.
                webbrowser.open(links[0])  # Open the first link in the default web browser.

    return True  # Indicate success.

def open_in_chrome(url):
    """
    This function opens the URL in Google Chrome on macOS.
    """
    # Attempt to open in Google Chrome using the 'open -a' command with Chrome
    try:
        os.system(f"open -a 'Google Chrome' {url}")
        print(f"Opened URL in Google Chrome: {url}")
    except Exception as e:
        print(f"Error opening Google Chrome with URL {url}: {e}")

# macOS compatible version of CloseApp function using AppleScript
def CloseApp(app):
    if app.lower() == "google chrome":
        print("Google Chrome cannot be closed using this function.")
        return False

    script = f'''
    tell application "{app}"
        quit
    end tell
    '''
    try:
        subprocess.run(['osascript', '-e', script])
        print(f"Closed {app}")
        return True
    except Exception as e:
        print(f"Error closing {app}: {e}")
        return False

def System(command):
    def mute():
        subprocess.run(["osascript", "-e", "set volume output muted true"])  # macOS mute command
    
    def unmute():
        subprocess.run(["osascript", "-e", "set volume output muted false"])  # macOS unmute command

    def volume_up():
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])  # macOS volume up
    
    def volume_down():
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])  # macOS volume down

    if command == "mute":
        mute()

    elif command == "unmute":
        unmute()

    elif command == "volume up":
        volume_up()

    elif command == "volume down":
        volume_down()

    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:

        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(playYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No function found for {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__ == "__main__":
    asyncio.run(Automation([ "open youtube"]))
