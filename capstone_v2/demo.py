import os
from pathlib import Path

def create_project_structure():
    # Define the root directory name
    root_dir = Path("withyou_system")

    # Define the structure
    # Key = directory path (relative to root), Value = dictionary of {filename: content/comment}
    structure = {
        "config": {
            "__init__.py": "",
            "settings.py": "# API Keys, Model Configs, Thresholds"
        },
        "core": {
            "__init__.py": "",
            "memory.py": "# Memory Bank & Session Management",
            "telemetry.py": "# Logging & Observability wrappers",
            "safety_guard.py": "# Deterministic regex/keyword filters"
        },
        "tools": {
            "__init__.py": "",
            "clinical_tools.py": "# Symptom checkers, Mood analysis",
            "crisis_tools.py": "# Hotline lookups, Emergency protocols",
            "scheduling_tools.py": "# Calendar/Routine management"
        },
        "agents": {
            "__init__.py": "",
            "safety_agent.py": "# The Sentinel",
            "triage_agent.py": "# The Router",
            "coach_agent.py": "# CBT/Empathy specialist",
            "planner_agent.py": "# Behavioral activation specialist",
            "clinician_agent.py": "# Summarization specialist"
        },
        "": { # Files directly in the root directory
            "main.py": "# Application Entry Point (Orchestrator)",
            "requirements.txt": "# Dependencies",
            ".env": "# Secrets (API Keys, DB URLs)"
        }
    }

    print(f"🚀 Initializing '{root_dir}' project structure...\n")

    # Create the root directory
    if not root_dir.exists():
        root_dir.mkdir()
        print(f"Created root directory: {root_dir}")

    # Iterate through the structure dictionary
    for folder, files in structure.items():
        # Create the full path for the subdirectory
        current_dir = root_dir / folder
        
        # Create directory if it doesn't exist
        if not current_dir.exists():
            current_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {current_dir}")

        # Create files within the directory
        for filename, content in files.items():
            file_path = current_dir / filename
            
            # Write the file (will overwrite if it exists, to ensure content matches)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            
            print(f"  └── Created file: {filename}")

    print("\n✅ Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()