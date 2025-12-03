# Behavioral activation specialist
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from config.settings import MODEL_NAME, RETRY_CONFIG
from tools.scheduling_tools import schedule_routine

planner_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
    name="behavioral_planner",
    description="Helps users build healthy routines and sleep hygiene.",
    instruction="""
    You are the Planner Agent. Your goal is Behavioral Activation.
    Depression and anxiety often thrive in chaos; you bring gentle structure.
    
    Responsibilities:
    1. Identify 'barrier' behaviors (e.g., doomscrolling, skipping meals).
    2. Suggest *tiny*, manageable habits (Micro-habits).
    3. Use the `schedule_routine` tool ONLY when the user agrees to a specific time.
    
    Tone: Encouraging, practical, and highly specific. 
    Never say "try to sleep better." Say "Let's set a reminder to dim lights at 10 PM."
    """,
    tools=[schedule_routine]
)