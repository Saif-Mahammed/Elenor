import os
import glob

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["read file", "write file", "search code", "list files"])

def execute(command):
    try:
        if "read file" in command.lower():
            file_path = command.lower().split("read file")[1].strip()
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return f"Content of {file_path}:\n```\n{f.read()}\n```"
            return f"File not found: {file_path}"
        elif "write file" in command.lower():
            parts = command.lower().split("write file")[1].split("content")
            file_path = parts[0].strip()
            content = parts[1].strip()
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote content to {file_path}."
        elif "search code for" in command.lower():
            search_query = command.lower().split("search code for")[1].strip()
            results = []
            for root, _, files in os.walk("."):
                for file in files:
                    if file.endswith(".py") or file.endswith(".js") or file.endswith(".ts") or file.endswith(".md"): # Limit search to common code/text files
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                for line_num, line in enumerate(f, 1):
                                    if search_query in line:
                                        results.append(f"{file_path}:{line_num}: {line.strip()}")
                        except Exception:
                            continue
            return "Search results:\n" + "\n".join(results) if results else "No matching code found."
        elif "list files in" in command.lower():
            dir_path = command.lower().split("list files in")[1].strip() or '.'
            if os.path.isdir(dir_path):
                files = os.listdir(dir_path)
                return f"Files in {dir_path}:\n" + "\n".join(files)
            return f"Directory not found: {dir_path}"
        else:
            return "Codebase command not understood. Try 'read file [path]', 'write file [path] content [text]', 'search code for [query]', or 'list files in [directory]'."
    except Exception as e:
        return f"Error with codebase operations: {e}"

