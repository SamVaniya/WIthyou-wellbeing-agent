"""
The Application Entry Point (Runner).
"""
import asyncio
import os
from dotenv import load_dotenv 
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from config.settings import settings
from core.telemetry import setup_telemetry

from domain.agents.safety_agent import create_safety_agent
from domain.agents.triage_agent import create_triage_agent

# Load environment variables
load_dotenv()

async def main():
    setup_telemetry()
    
    print(f"--- 'withyou' Clinical Agent System Initializing [Env: {settings.ENV}] ---")
    
    # 1. Initialize Services
    session_service = InMemorySessionService()
    
    # 2. Initialize Agents
    safety_guardian = create_safety_agent()
    triage_brain = create_triage_agent()
    
    # 3. Create Runners
    safety_runner = Runner(
        agent=safety_guardian,
        app_name=settings.APP_NAME, 
        session_service=session_service
    )
    triage_runner = Runner(
        agent=triage_brain,
        app_name=settings.APP_NAME, 
        session_service=session_service
    )
    
    # --- SESSION CONTEXT SETUP ---
    session_id = "session_user_001"
    safety_session_id = f"{session_id}_safety"
    user_id = "patient_001"
    
    # [FIX]: Explicitly create the sessions before using them
    print("[System]: initializing secure sessions...")
    await session_service.create_session(
        app_name=settings.APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    await session_service.create_session(
        app_name=settings.APP_NAME,
        user_id=user_id,
        session_id=safety_session_id
    )
    
    print("Ready. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # --- LAYER 0: SAFETY INTERCEPTION ---
        is_safe = False
        safety_content = types.Content(role="user", parts=[types.Part(text=user_input)])
        
        print(f"\n[System]: Running Safety Scan...")
        
        async for event in safety_runner.run_async(
            user_id=user_id,
            session_id=safety_session_id, 
            new_message=safety_content
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text.strip()
                if "SAFE" in response_text:
                    is_safe = True
                else:
                    print(f"\n[withyou 🛡️]: {response_text}")
        
        if not is_safe:
            continue

        # --- LAYER 1: CLINICAL TRIAGE ---
        print(f"[System]: Safety Pass. Routing to Triage...")
        triage_content = types.Content(role="user", parts=[types.Part(text=user_input)])
        
        async for event in triage_runner.run_async(
            user_id=user_id,
            session_id=session_id, 
            new_message=triage_content
        ):
            if event.is_final_response():
                print(f"\n[withyou]: {event.content.parts[0].text}\n")

if __name__ == "__main__":
    asyncio.run(main())