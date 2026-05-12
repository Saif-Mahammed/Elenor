import cv2
import pyautogui
import os
import requests
import base64
from dotenv import dotenv_values

# Get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_vars = dotenv_values(os.path.join(current_dir, ".env"))

def CaptureScreen():
    try:
        screenshot_path = os.path.join(current_dir, "Data", "screen.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

def CaptureCamera():
    try:
        camera_path = os.path.join(current_dir, "Data", "camera.png")
        os.makedirs(os.path.dirname(camera_path), exist_ok=True)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(camera_path, frame)
            cap.release()
            return camera_path
        cap.release()
        return None
    except Exception as e:
        print(f"Error capturing camera: {e}")
        return None

def AnalyzeImage(image_path, prompt="Describe this image."):
    """
    Uses local Ollama (Moondream) to analyze images.
    Requires Ollama to be running with the moondream model.
    """
    try:
        with open(image_path, "rb") as image_file:
            img_str = base64.b64encode(image_file.read()).decode('utf-8')
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "moondream",
                "prompt": prompt,
                "images": [img_str],
                "stream": False
            }
        )
        
        if response.status_code == 200:
            return response.json().get("response", "I see something, but I can't quite describe it.")
        else:
            return "Vision error: Make sure Ollama is running with the 'moondream' model."
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "I encountered an error while trying to process the visual data."

if __name__ == "__main__":
    # Test screen capture
    path = CaptureScreen()
    if path:
        print(f"Screen captured to: {path}")
    
    # Test camera capture
    path = CaptureCamera()
    if path:
        print(f"Camera captured to: {path}")
