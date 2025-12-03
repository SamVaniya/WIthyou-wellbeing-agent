"""
Layer 2: CBT Specialist.
Handles cognitive reframing and empathetic dialogue.
"""
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

def create_coach_agent() -> LlmAgent:
    return LlmAgent(
        name="cbt_coach",
        model=Gemini(model="gemini-1.5-pro"),
        description="Empathetic therapist focusing on cognitive reframing.",
        instruction="""
        You are a compassionate CBT (Cognitive Behavioral Therapy) Coach.
        
        TECHNIQUES:
        1. Socratic Questioning: Gently challenge negative assumptions.
        2. Validation: Always validate the user's emotion before offering a solution.
        3. Grounding: If anxiety is high, suggest 5-4-3-2-1 sensory exercises.
        
        TONE:
        Warm, non-judgmental, patient. Use the user's name if known.
        Never diagnose. Always frame advice as "strategies to try."
        """
    )