# Application Entry Point (Orchestrator)
import asyncio
from google.adk.runners import Runner
from google.adk.apps.app import App
from google.genai import types

from agents.safety_agent import safety_agent
from agents.triage_agent import triage_agent
from core.memory import get_session_services

# Initialize Services
session_service, memory_service = get_session_services()

# Define the App - The Triage Agent is the entry point for the standard flow
withyou_app = App(
    name="withyou_wellness_system",
    root_agent=triage_agent,
    session_service=session_service,
    memory_service=memory_service
)

# Initialize Runner
runner = Runner(app=withyou_app)

async def process_user_interaction(user_input: str, user_id: str, session_id: str):
    print(f"\n--- Processing for User: {user_id} ---")
    
    # --- STEP 1: SAFETY GATE (The Sentinel) ---
    # We create a temporary runner for the safety check to keep it isolated
    safety_runner = Runner(agent=safety_agent, session_service=session_service)
    
    print("🛡️ Running Safety Protocol...")
    safety_response_text = ""
    
    # Process Safety Check
    async for event in safety_runner.run_async(
        user_id=user_id, 
        session_id=f"{session_id}_safety", 
        new_message=types.Content(parts=[types.Part(text=user_input)])
    ):
        if event.is_final_response() and event.content:
             safety_response_text = event.content.parts[0].text

    # --- STEP 2: CRISIS INTERVENTION LOGIC ---
    if "ESCALATE_CRISIS" in safety_response_text:
        print("🚨 CRISIS DETECTED. INTERRUPTING WORKFLOW.")
        # Strip the system flag and show the compassionate resource message provided by the agent
        clean_response = safety_response_text.replace("ESCALATE_CRISIS", "").strip()
        print(f"System Response: {clean_response}")
        # In a real app, this would trigger an alert to human review
        return

    # --- STEP 3: CLINICAL TRIAGE & INTERVENTION ---
    print("✅ Safety Check Passed. Routing to Clinical Triage.")
    
    # The Triage agent will now take over and route to Coach/Planner via AgentTool
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(parts=[types.Part(text=user_input)])
    ):
        if event.is_final_response() and event.content:
            print(f"withyou > {event.content.parts[0].text}")

# --- Execution Simulation ---
if __name__ == "__main__":
    # Scenario 1: Anxiety (Standard Flow)
    asyncio.run(process_user_interaction(
        "I can't sleep because I'm worried about my job presentation tomorrow.", 
        "user_123", 
        "session_001"
    ))
    
    # Scenario 2: Safety Risk (Crisis Flow)
    asyncio.run(process_user_interaction(
        "I don't want to be here anymore. I'm thinking of hurting myself.", 
        "user_123", 
        "session_002"
    ))