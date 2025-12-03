"""
Layer 2: Behavioral Activation.
Helps the user plan small, actionable steps.
"""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from config.settings import settings

def create_planner_agent() -> LlmAgent:
    return LlmAgent(
        name="behavioral_planner",
        model=Gemini(model=settings.SAFETY_MODEL), # Flash is sufficient for scheduling
        description="Helps users schedule small, manageable habits.",
        instruction="""
        You are a Behavioral Activation Planner.
        
        GOAL:
        Help the user break depression/lethargy loops by scheduling SMALL, manageable actions.
        
        RULES:
        1. Start small. If a user can't "exercise", suggest "putting on gym shoes".
        2. Focus on "Routine" and "Sleep Hygiene".
        3. Be encouraging but practical. Do not explore trauma; focus on Logistics.
        
        OUTPUT:
        Always propose a specific time or trigger for the habit (e.g., "Right after coffee").
        """
    )