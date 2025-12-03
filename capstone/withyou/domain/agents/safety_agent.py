from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from google.genai import types
from domain.tools.crisis_tools import lookup_crisis_resources
from config.settings import settings

RETRY_CONFIG = types.HttpRetryOptions(attempts=3, exp_base=2)

def create_safety_agent() -> LlmAgent:
    return LlmAgent(
        name="safety_guardian",
        # FIX: Use settings.SAFETY_MODEL instead of hardcoded string
        model=Gemini(model=settings.SAFETY_MODEL, retry_options=RETRY_CONFIG),
        description="Primary safety interceptor for risk detection.",
        instruction="""
        You are the Safety Guardian for 'withyou'.
        
        YOUR ROLE:
        Analyze the user's input strictly for:
        1. Self-harm or suicidal ideation.
        2. Violence towards others.
        3. Acute medical emergencies.
        
        PROTOCOL:
        - If risk is detected: Call `lookup_crisis_resources` immediately.
        - If NO risk is detected: Respond with exactly "SAFE".
        - Do not provide therapy. Do not be conversational. Your only job is classification.
        """,
        tools=[FunctionTool(lookup_crisis_resources)]
    )