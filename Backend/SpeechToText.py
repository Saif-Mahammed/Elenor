import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from dotenv import dotenv_values
import torch

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")

# Whisper expects ISO 639-1 language codes (2 letters). 
# If 'en-US' is provided, we use 'en'.
if len(InputLanguage) > 2:
    InputLanguage = InputLanguage[:2]

# Initialize Whisper Model
# 'base' is a good balance between speed and accuracy. 
# Use 'tiny' for maximum speed or 'small'/'medium' for better accuracy.
model_size = "base"
device = "cuda" if torch.cuda.is_available() else "cpu"
# On macOS with Apple Silicon, 'cpu' is often fine, but we can also use 'mps' if supported by faster-whisper/ctranslate2
# For now, let's stick to 'cpu' for stability across all systems.
model = WhisperModel(model_size, device=device, compute_type="int8")

def SetAssistantStatus(status):
    current_dir = os.getcwd()
    status_file_path = os.path.join(current_dir, "Frontend", "Files", 'Status.data')
    os.makedirs(os.path.dirname(status_file_path), exist_ok=True)
    with open(status_file_path, "w", encoding='utf-8') as file:
        file.write(status)

def QueryModifier(Query):
    if not Query: return ""
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()

def InitializeDriver():
    """Legacy function kept for compatibility with Main.py, but no longer needed for Whisper."""
    pass

def SpeechRecognition():
    """
    Captures audio from the microphone and transcribes it using Faster Whisper.
    """
    try:
        SetAssistantStatus("Listening...")
        
        fs = 16000  # Sample rate
        seconds = 5  # Duration of recording
        
        print(f"Listening for {seconds} seconds...")
        
        # Record audio
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
        sd.wait()  # Wait until recording is finished
        
        print("Processing...")
        SetAssistantStatus("Processing...")
        
        # Transcribe audio from the numpy array
        # We flatten the recording since sd.rec returns a 2D array
        segments, info = model.transcribe(recording.flatten(), beam_size=5, language=InputLanguage)
        
        text = ""
        for segment in segments:
            text += segment.text + " "
        
        text = text.strip()
        
        if text:
            print(f"Recognized text: {text}")
            return QueryModifier(text)
        else:
            print("No speech detected.")
            return ""
            
    except Exception as e:
        print(f"Error in Whisper Speech Recognition: {e}")
        return ""

if __name__ == "__main__":
    while True:
        recognized_text = SpeechRecognition()
        if recognized_text:
            print(f"Final Query: {recognized_text}")
