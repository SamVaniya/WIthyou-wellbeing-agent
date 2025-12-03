# The Router
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from config.settings import ROUTING_MODEL, RETRY_CONFIG
from agents.coach_agent import coach_agent
# Assuming planner_agent and clinician_agent are similarly defined and imported

triage_agent = LlmAgent(
    model=Gemini(model=ROUTING_MODEL, retry_options=RETRY_CONFIG),
    name="clinical_triage",
    description="Analyzes user intent and routes to the specific specialist.",
    instruction="""
    You are the Clinical Triage Router. You do not talk to the user directly.
    Your job is to analyze the user's input and specific signals to activate the right agent.
    
    Routing Logic:
    1. Emotional Distress / Need to Talk -> Delegate to `cbt_coach`.
    2. Routine / Sleep / Habits / Scheduling -> Delegate to `planner_agent`.
    3. Request for Medical Summary / History -> Delegate to `clinician_agent`.
    
    Analyze the input carefully. If the user mentions "feeling overwhelmed by schedule", that is likely a Planner task, not just a Coach task.
    """,
    # We wrap the specialists as tools for the router
    tools=[AgentTool(coach_agent)] # Add Planner/Clinician here in full implementation
)