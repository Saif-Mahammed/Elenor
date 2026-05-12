# Contributing to ELENOR OMNI

Welcome! We are building the most advanced, autonomous, and visually stunning AI assistant. Here is how you can contribute:

## Repository Structure
- `Backend/`: Core logic, AI models, and memory systems.
- `Frontend/`: The OMNI UI (PyQt6).
- `Plugins/`: Modular features (40+ capability target). Drop a `.py` file here to add a feature.
- `Features/`: Low-level offline utilities (Vector memory, local compute, hardware control).

## How to add a Feature (Plugin)
1. Create a new file in `Plugins/` (e.g., `GitHubPlugin.py`).
2. Implement the standard interface:
   ```python
   def can_handle(command):
       return "github" in command
   
   def execute(command):
       # Your logic here
       return "GitHub task performed."
   ```
3. ELENOR will auto-discover it on the next launch.

## Best Practices
- **Dark Mode only:** Keep UI sleek, black/dark-grey, and minimalist.
- **Local Fallback:** Always ensure new features have an offline/local-first path.
- **Async First:** Avoid blocking the GUI thread.
