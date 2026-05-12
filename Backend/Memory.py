import json
import os

# Get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
memory_path = os.path.join(current_dir, "Data", "Memory.json")

def LoadMemory():
    try:
        if os.path.exists(memory_path):
            with open(memory_path, "r", encoding='utf-8') as f:
                return json.load(f)
        else:
            os.makedirs(os.path.dirname(memory_path), exist_ok=True)
            default_mem = {
                "facts": [], 
                "user_preferences": {}, 
                "relationship": {"level": 1, "sentiment": "Neutral", "interactions": 0},
                "last_session": ""
            }
            with open(memory_path, "w", encoding='utf-8') as f:
                json.dump(default_mem, f, indent=4)
            return default_mem
    except Exception as e:
        print(f"Error loading memory: {e}")
        return {"facts": [], "user_preferences": {}, "relationship": {"level": 1}, "last_session": ""}

def IncrementRelationship():
    memory = LoadMemory()
    memory["relationship"]["interactions"] += 1
    # Level up every 10 interactions
    memory["relationship"]["level"] = (memory["relationship"]["interactions"] // 10) + 1
    SaveMemory(memory)

def GetRelationshipSummary():
    memory = LoadMemory()
    rel = memory["relationship"]
    return f"Relationship Level: {rel['level']} ({rel['interactions']} interactions)"

def SaveMemory(memory_data):
    try:
        with open(memory_path, "w", encoding='utf-8') as f:
            json.dump(memory_data, f, indent=4)
    except Exception as e:
        print(f"Error saving memory: {e}")

def AddFact(fact):
    memory = LoadMemory()
    if fact not in memory["facts"]:
        memory["facts"].append(fact)
        SaveMemory(memory)

def UpdatePreference(key, value):
    memory = LoadMemory()
    memory["user_preferences"][key] = value
    SaveMemory(memory)

def GetMemoryContext():
    memory = LoadMemory()
    context = "### User Memory & Facts ###\n"
    if memory["facts"]:
        context += "- " + "\n- ".join(memory["facts"]) + "\n"
    if memory["user_preferences"]:
        context += "### User Preferences ###\n"
        for k, v in memory["user_preferences"].items():
            context += f"- {k}: {v}\n"
    
    # Add relationship context
    rel = memory.get("relationship", {"level": 1, "interactions": 0})
    context += f"\n### Assistant Relationship ###\n"
    context += f"- Current Bond Level: {rel['level']}\n"
    context += f"- Total Meaningful Interactions: {rel['interactions']}\n"
    context += "The user's trust in you grows with each interaction. Use this to be more warm and personal."
    
    return context
