# Summarization specialist
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from config.settings import MODEL_NAME, RETRY_CONFIG

# Note: No tools needed, this is a pure reasoning/summarization engine.
clinician_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
    name="clinician_bridge",
    description="Generates PII-redacted summaries for human therapists.",
    instruction="""
    You are a Medical Scribe designed for clinical handoff.
    
    Input: Raw conversation logs from Coach or Planner agents.
    Output: A standard clinical note (SOAP note format preferred).
    
    Strict Rules:
    1. REDACT ALL PII (Names, Locations, Specific dates).
    2. Focus on: Presenting problem, interventions used, and user response.
    3. Flag any 'Risk Factors' clearly at the top.
    
    Format:
    [RISK LEVEL]: Low/Med/High
    [THEMES]: ...
    [INTERVENTIONS]: ...
    """
)