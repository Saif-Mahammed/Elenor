from notion_client import Client
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
NOTION_TOKEN = env_vars.get("NOTION_TOKEN")
NOTION_DATABASE_ID = env_vars.get("NOTION_DATABASE_ID")

if NOTION_TOKEN:
    notion = Client(auth=NOTION_TOKEN)
else:
    print("Warning: NOTION_TOKEN not found. NotionAssistant will be limited.")

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["notion", "create page", "add task", "list tasks"])

def execute(command):
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        return "I cannot access Notion without NOTION_TOKEN and NOTION_DATABASE_ID configured in your .env file."

    try:
        if "create notion page" in command.lower():
            title = command.lower().split("create notion page")[1].strip()
            new_page = notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={"Name": {"title": [{"text": {"content": title}}]}}
            )
            return f"Created Notion page: {title} (ID: {new_page['id']})"
        elif "add task to notion" in command.lower():
            task_name = command.lower().split("add task to notion")[1].strip()
            # Assuming a simple database with a 'Task Name' property
            notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties={
                    "Name": {"title": [{"text": {"content": task_name}}]},
                    "Status": {"select": {"name": "Not started"}} # Adjust to your database properties
                }
            )
            return f"Added task '{task_name}' to Notion."
        else:
            return "Notion command not understood. Try 'create notion page [title]' or 'add task to notion [task_name]'."
    except Exception as e:
        return f"Error interacting with Notion: {e}. Make sure your token has permissions and the database ID is correct."

