import json
import os
import datetime
from datetime import datetime, timedelta

REMINDERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "reminders.json")

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w", encoding='utf-8') as f:
        json.dump(reminders, f, indent=4)

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["set reminder", "list reminders", "clear reminders"])

def execute(command):
    reminders = load_reminders()

    if "set reminder" in command.lower():
        # Example: "set reminder for 5 PM to call mom"
        parts = command.lower().split("set reminder for ")[1].split(" to ")
        time_str = parts[0].strip()
        message = parts[1].strip()

        # Simple parsing for now, can be improved with dateutil
        try:
            # Assuming "today" for simplicity. Can expand to parse dates like "tomorrow", "on 5th aug"
            current_date = datetime.now().date()
            if "am" in time_str or "pm" in time_str:
                dt_obj = datetime.strptime(f"{current_date} {time_str}", "%Y-%m-%d %I %p")
            else:
                dt_obj = datetime.strptime(f"{current_date} {time_str}", "%Y-%m-%d %H:%M")
            
            new_reminder = {"time": dt_obj.isoformat(), "message": message, "set_at": datetime.now().isoformat()}
            reminders.append(new_reminder)
            save_reminders(reminders)
            return f"Reminder set for {time_str}: {message}."
        except ValueError:
            return "Could not understand the time format. Please try 'set reminder for 5 PM to call mom'."
    
    elif "list reminders" in command.lower():
        if not reminders:
            return "You have no active reminders."
        
        response = "Your reminders:
"
        for r in reminders:
            try:
                dt = datetime.fromisoformat(r["time"])
                response += f"- {r['message']} at {dt.strftime('%I:%M %p on %Y-%m-%d')}
"
            except:
                response += f"- {r['message']} (time unknown)
"
        return response

    elif "clear reminders" in command.lower():
        save_reminders([])
        return "All reminders cleared."
    
    return "Reminder command not understood."

