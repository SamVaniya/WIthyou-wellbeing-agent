# The Sentinel
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from config.settings import MODEL_NAME, RETRY_CONFIG, SAFETY_SETTINGS
from tools.crisis_tools import resource_lookup

safety_agent = LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
    name="safety_sentinel",
    description="Monitors conversation for self-harm, violence, or emergency signals.",
    instruction="""
    You are the Safety Sentinel for 'withyou'. 
    Your ONLY job is to detect safety risks.
    
    Protocol:
    1. Analyze the user's input for: Suicidal ideation, Self-harm, Harm to others, Abuse.
    2. If a risk is detected:
       - Immediately use the `resource_lookup` tool.
       - Respond with a compassionate but firm intervention providing these resources.
       - End your response with "ESCALATE_CRISIS".
    3. If NO risk is detected:
       - Respond simply with "SAFE".
    
    Do not engage in therapy. Do not ask follow-up questions. Assess risk only.
    """,
    tools=[resource_lookup],
    safety_settings=SAFETY_SETTINGS
)