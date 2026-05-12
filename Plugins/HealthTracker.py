import json
import os
import datetime

# Local storage for health data
HEALTH_DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "health_data.json")

def load_health_data():
    if os.path.exists(HEALTH_DATA_FILE):
        with open(HEALTH_DATA_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    return {"water_intake_ml": 0, "steps": 0, "goals": {}}

def save_health_data(data):
    with open(HEALTH_DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["log water", "log steps", "set health goal", "my health status"])

def execute(command):
    data = load_health_data()
    today = str(datetime.date.today())

    if "log water" in command.lower():
        amount_ml = int("".join(filter(str.isdigit, command)) or "250")
        data["water_intake_ml"] = data.get("water_intake_ml", 0) + amount_ml
        save_health_data(data)
        return f"Logged {amount_ml}ml of water. Total for today: {data['water_intake_ml']}ml."
    elif "log steps" in command.lower():
        steps = int("".join(filter(str.isdigit, command)) or "1000")
        data["steps"] = data.get("steps", 0) + steps
        save_health_data(data)
        return f"Logged {steps} steps. Total for today: {data['steps']} steps."
    elif "set health goal" in command.lower():
        parts = command.lower().split("set health goal")[1].strip().split(" for ")
        goal_name = parts[0].strip()
        goal_value = parts[1].strip() if len(parts) > 1 else "unspecified"
        data["goals"][goal_name] = goal_value
        save_health_data(data)
        return f"Set new health goal: {goal_name} to {goal_value}."
    elif "my health status" in command.lower():
        water = data.get("water_intake_ml", 0)
        steps = data.get("steps", 0)
        goals = ", ".join([f"{k}: {v}" for k, v in data["goals"].items()]) if data["goals"] else "None set."
        return f"Today's Health Status: Water Intake: {water}ml, Steps: {steps}. Goals: {goals}."
    return "Health tracking command not understood."
