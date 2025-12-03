import os
from pathlib import Path

def create_file(path, content=""):
    """Creates a file with the given content."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Created file: {path}")

def create_directory(path):
    """Creates a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    print(f"fvD82 Created directory: {path}")

def build_structure():
    base_dir = Path("withyou")
    
    # 1. Define the structure and content
    # The structure is defined as: { "path/to/file": "File Content" }
    
    structure = {
        # --- Config ---
        base_dir / "config" / "__init__.py": "",
        base_dir / "config" / "settings.py": 
'''"""
Centralized configuration (Models, Safety Thresholds).
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SAFETY_THRESHOLD = 0.8
    MODEL_NAME = "gemini-1.5-pro"

settings = Settings()
''',

        # --- Core ---
        base_dir / "core" / "__init__.py": "",
        base_dir / "core" / "telemetry.py": 
'''"""
Structured logging for clinical audit.
Handles tracing of conversation flows and risk detection events.
"""
import logging

def setup_logger():
    # TODO: Configure structured JSON logging
    pass
''',
        base_dir / "core" / "exceptions.py": 
'''"""
Custom exceptions for the application.
"""

class WithYouException(Exception):
    """Base exception for the app."""
    pass

class CrisisDetectedException(WithYouException):
    """Raised when immediate risk is detected."""
    pass
''',

        # --- Domain: Agents ---
        base_dir / "domain" / "__init__.py": "",
        base_dir / "domain" / "agents" / "__init__.py": "",
        
        base_dir / "domain" / "agents" / "safety_agent.py": 
'''"""
Layer 0: The Shield.
Responsible for detecting Immediate Harm/Crisis before any other processing.
"""

class SafetyAgent:
    def check_safety(self, user_input: str) -> bool:
        # TODO: Implement safety check logic
        return True
''',
        
        base_dir / "domain" / "agents" / "triage_agent.py": 
'''"""
Layer 1: The Orchestrator.
Analyzes intent and routes the conversation to the appropriate specialist (Coach vs Planner).
"""
''',

        base_dir / "domain" / "agents" / "coach_agent.py": 
'''"""
Layer 2: CBT Specialist.
Handles cognitive reframing and empathetic dialogue.
"""
''',

        base_dir / "domain" / "agents" / "planner_agent.py": 
'''"""
Layer 2: Behavioral Activation.
Helps the user plan small, actionable steps.
"""
''',

        # --- Domain: Tools ---
        base_dir / "domain" / "tools" / "__init__.py": "",
        base_dir / "domain" / "tools" / "crisis_tools.py": 
'''"""
Deterministic safety lookups.
Contains helplines, emergency resources, and static safety protocols.
"""
''',
        
        base_dir / "domain" / "tools" / "mood_tools.py": 
'''"""
Mood logging & pattern recognition.
Tools to save and retrieve user mood data.
"""
''',

        # --- Root Files ---
        base_dir / "main.py": 
'''"""
The Application Entry Point (Runner).
"""
from config.settings import settings
import sys

def main():
    print("Starting 'WithYou' application...")
    if not settings.GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in .env")
        sys.exit(1)
        
    # TODO: Initialize agents and start conversation loop

if __name__ == "__main__":
    main()
''',
        
        base_dir / ".env": 
'''GOOGLE_API_KEY=your_api_key_here
ENVIRONMENT=development
''',
        
        base_dir / "requirements.txt": 
'''python-dotenv
google-generativeai
pydantic
'''
    }

    # 2. Execution Loop
    print(f"🚀 Initializing project structure for: {base_dir}\n")
    
    for path, content in structure.items():
        # Ensure the parent directory exists
        create_directory(path.parent)
        # Create the file with content
        create_file(path, content)

    print(f"\n✅ Project 'withyou' created successfully!")

if __name__ == "__main__":
    build_structure()