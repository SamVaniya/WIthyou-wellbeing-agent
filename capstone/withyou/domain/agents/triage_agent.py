"""
Layer 1: The Orchestrator.
Analyzes intent and routes the conversation to the appropriate specialist (Coach vs Planner).
"""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from .coach_agent import create_coach_agent
from config.settings import settings # <--- IMPORT SETTINGS

def create_triage_agent() -> LlmAgent:
    coach = create_coach_agent()
    
    return LlmAgent(
        name="triage_orchestrator",
        # FIX: Use settings.REASONING_MODEL
        model=Gemini(model=settings.REASONING_MODEL),
        description="Routes users to the correct mental health specialist.",
        instruction="""
        You are the Clinical Triage Router.
        
        DECISION MATRIX:
        1. Emotional Distress/Anxiety/Negative Thoughts -> Delegate to `cbt_coach`.
        2. Habit Forming/Sleep Issues/Routine Planning -> Delegate to `planner_agent` (if available).
        3. General Chit-Chat -> Handle politely but steer back to wellness.
        
        You do not provide therapy yourself. You connect the user to the right expert.
        """,
        tools=[AgentTool(coach)]
    )