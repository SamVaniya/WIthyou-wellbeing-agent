# from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
# from google.adk.models.google_llm import Gemini
# from google.adk.runners import InMemoryRunner
# from google.adk.tools import AgentTool, FunctionTool, google_search
# from google.genai import types

# print("✅ ADK components imported successfully.")

# retry_config=types.HttpRetryOptions(
#     attempts=5,  # Maximum retry attempts
#     exp_base=7,  # Delay multiplier
#     initial_delay=1,
#     http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
# )


# # Research Agent: Its job is to use the google_search tool and present findings.
# research_agent = Agent(
#     name="ResearchAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""You are a specialized research agent. Your only job is to use the
#     google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
#     tools=[google_search],
#     output_key="research_findings",  # The result of this agent will be stored in the session state with this key.
# )

# print("✅ research_agent created.")

# # Summarizer Agent: Its job is to summarize the text it receives.
# summarizer_agent = Agent(
#     name="SummarizerAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # The instruction is modified to request a bulleted list for a clear output format.
#     instruction="""Read the provided research findings: {research_findings}
# Create a concise summary as a bulleted list with 3-5 key points.""",
#     output_key="final_summary",
# )

# print("✅ summarizer_agent created.")


# # Root Coordinator: Orchestrates the workflow by calling the sub-agents as tools.
# root_agent = Agent(
#     name="ResearchCoordinator",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # This instruction tells the root agent HOW to use its tools (which are the other agents).
#     instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
# 1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
# 2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
# 3. Finally, present the final summary clearly to the user as your response.""",
#     # We wrap the sub-agents in `AgentTool` to make them callable tools for the root agent.
#     tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
# )

# print("✅ root_agent created.")

# # runner = InMemoryRunner(agent=root_agent)
# # import asyncio

# # async def main():
# #     response = await runner.run_debug(
# #         "What are the latest advancements in quantum computing and what do they mean for AI?"
# #     )
# #     print(response)

# # asyncio.run(main())



# withyou_minimal_agents.py
"""
Minimal multi-agent withyou demo using ADK-style primitives and Gemini.
This is a lightweight, demo-only example with mocked tools (no API keys).
"""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool
from google.genai import types

import asyncio
import re
import json

print("✅ ADK components imported successfully.")

# ---------- Retry config for robust LLM calls ----------
retry_config = types.HttpRetryOptions(
    attempts=3,      # fewer attempts for demo
    exp_base=2,
    initial_delay=0.5,
    http_status_codes=[429, 500, 503, 504],
)

# ---------- Mocked tools implemented as simple Python functions ----------
def symptom_checker_tool_fn(payload: str) -> dict:
    """
    A minimal symptom checker that looks for basic keywords and returns a severity.
    This is NOT a clinical tool — it's a mocked helper for the demo.
    """
    text = payload.lower()
    flags = {
        "suicidal": bool(re.search(r"\b(suicid|kill myself|end my life)\b", text)),
        "self_harm": bool(re.search(r"\b(cut myself|hurt myself)\b", text)),
        "anxiety": bool(re.search(r"\b(anxious|anxiety|panic)\b", text)),
        "sleep": bool(re.search(r"\b(sleep|insomnia|can't sleep)\b", text)),
    }
    if flags["suicidal"] or flags["self_harm"]:
        severity = "high"
    elif flags["anxiety"] or flags["sleep"]:
        severity = "moderate"
    else:
        severity = "low"
    return {"severity": severity, "flags": flags, "summary": "Mocked symptom check result."}

def scheduler_tool_fn(payload: dict) -> dict:
    """Mock scheduler: returns a fake scheduled item."""
    # payload expected to include: {"title": str, "time": str}
    title = payload.get("title", "self-care activity")
    time = payload.get("time", "tomorrow 9:00 AM")
    return {"scheduled": True, "title": title, "time": time, "id": "mock-event-123"}

def resource_lookup_tool_fn(query: str) -> dict:
    """Mock resource lookup returning a couple of curated links."""
    # In a real system, you'd call a vetted resource database.
    return {
        "resources": [
            {"title": "National Crisis Hotline", "url": "tel:+18002738255"},
            {"title": "Mental Health Organization - Self Help", "url": "https://example.org/selfhelp"}
        ],
        "query": query
    }

# Wrap Python functions as FunctionTool so agents can call them
symptom_checker_tool = FunctionTool(name="symptom_checker", func=symptom_checker_tool_fn, description="Check symptom keywords and return severity.")
scheduler_tool = FunctionTool(name="scheduler_tool", func=scheduler_tool_fn, description="Schedule a small self-care activity (mock).")
resource_lookup_tool = FunctionTool(name="resource_lookup", func=resource_lookup_tool_fn, description="Return curated resources for a query.")

print("✅ Mock tools created (symptom_checker, scheduler_tool, resource_lookup).")

# ---------- Define Agents ----------
# Note: model choice uses Gemini but the demo will run even without contacting cloud if ADK mocks responses.
base_model_cfg = {
    "model": "gemini-2.5-flash-lite",
    "retry_options": retry_config,
}

# Safety Agent: always run to check for crisis language. High priority.
safety_agent = Agent(
    name="SafetyAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are the Safety Agent for withyou. "
        "Your job is to determine whether the user's message indicates self-harm, suicidal ideation, or immediate risk. "
        "First, call the `symptom_checker` tool with the user's message. "
        "If the tool reports high severity or flags suicidal/self-harm keywords, respond with a JSON object containing "
        "`{'action': 'escalate', 'message': <text to send to user>, 'resources': <resource list>}`. "
        "If no immediate risk, respond with `{'action': 'continue'}`."
    ),
    tools=[symptom_checker_tool, resource_lookup_tool],
    output_key="safety_result",
)

print("✅ safety_agent created.")

# Triage Agent: decides the next step based on symptoms + short conversation context
triage_agent = Agent(
    name="TriageAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are the Triage Agent for withyou. Use the available signals to pick the appropriate path: "
        "`coach` (self-help micro-intervention), `plan` (schedule an activity), or `refer` (show resources/clinician). "
        "Inputs available: user_message (string) and symptom_check (the output of symptom_checker). "
        "Return a JSON: {'path':'coach'|'plan'|'refer', 'reason': 'short explanation'}."
    ),
    tools=[symptom_checker_tool, resource_lookup_tool],
    output_key="triage_result",
)

print("✅ triage_agent created.")

# Coach Agent: provides a short, empathetic intervention
coach_agent = Agent(
    name="CoachAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are a gentle, non-judgmental Coach Agent for withyou. Given the user's message and short context, "
        "produce a brief supportive reply (1-3 short paragraphs) with one practical micro-action the user can take now. "
        "Do not provide diagnoses. If the triage signal suggests severe risk, instruct the caller to wait and let Safety Agent handle escalation."
    ),
    output_key="coach_reply",
)

print("✅ coach_agent created.")

# Planner Agent: schedule a small self-care activity using scheduler_tool
planner_agent = Agent(
    name="PlannerAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are the Planner Agent. When asked, propose a short self-care activity (title and suggested time). "
        "Then call the `scheduler_tool` to create the activity. Return the scheduler response as JSON."
    ),
    tools=[scheduler_tool],
    output_key="planner_result",
)

print("✅ planner_agent created.")

# Root Orchestrator: coordinates the flow.
# We'll create a SequentialAgent that first runs safety (in parallel check), then triage -> coach/plan/lookup depending on triage.
root_agent = Agent(
    name="WithYouCoordinator",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are the coordinator for the withyou demo. Workflow:\n"
        "1) Ensure SafetyAgent has run (safety_result) and if it returned escalate, present the safety message and resources immediately.\n"
        "2) Otherwise, run TriageAgent to pick a path.\n"
        "3) If triage -> 'coach', call CoachAgent and return the coach reply.\n"
        "4) If triage -> 'plan', call PlannerAgent and return scheduling confirmation.\n"
        "5) If triage -> 'refer', call resource_lookup and return resource suggestions.\n"
        "Return a final JSON summarizing: {'safety': ..., 'triage': ..., 'result': ...}."
    ),
    # We'll expose sub-agents and tools so the coordinator can call them as tools.
    tools=[
        AgentTool(safety_agent),
        AgentTool(triage_agent),
        AgentTool(coach_agent),
        AgentTool(planner_agent),
        resource_lookup_tool,  # direct tool for fallback resource lookup
    ],
    output_key="coordinator_result",
)

print("✅ root_agent (WithYouCoordinator) created.")

# ---------- Runner & Demo ----------
runner = InMemoryRunner(agent=root_agent)

async def demo_run(user_message: str):
    """
    Run a full demo: first ensure SafetyAgent runs (we call it directly),
    then call the coordinator which will invoke other sub-agents as tools.
    """
    print("\n--- Demo run starting ---")
    print(f"User message: {user_message}\n")

    # 1) Run safety agent directly (so it can short-circuit if needed)
    safety_resp = await runner.run_tool_debug(agent=safety_agent, input=user_message)
    # safety_resp will be the agent output structure; runner.run_tool_debug returns a rich structure depending on ADK
    # For demo simplicity, try to access the text or parsed output:
    print("Safety agent response (raw):")
    print(safety_resp)
    # If safety tool returned a structured output, check for escalation
    # We will attempt to read a parsed output or fallback to naive check using symptom_checker
    # Use symptom_checker directly for robust demo logic:
    symptom_info = symptom_checker_tool_fn(user_message)
    if symptom_info["severity"] == "high":
        resources = resource_lookup_tool_fn("crisis hotline")
        safety_message = (
            "I detect strong indicators of immediate risk. I’m sorry you’re feeling this way. "
            "Please consider contacting local emergency services or the crisis resources below."
        )
        print("\n*** SAFETY ESCALATION ***")
        print(json.dumps({"action":"escalate","message":safety_message,"resources":resources}, indent=2))
        return

    # 2) If not escalated, run the coordinator (it will orchestrate triage -> coach/plan)
    # Provide a structured input that coordinator can use
    coordinator_input = {
        "user_message": user_message,
        "symptom_check": symptom_info
    }
    # Convert input to a simple string payload for the coordinator-run (depends on ADK runner API)
    coordinator_payload = json.dumps(coordinator_input)
    coordinator_resp = await runner.run_debug(coordinator_payload)
    print("\nCoordinator response (raw):")
    print(coordinator_resp)

    # Depending on how the ADK returns the structure, display the essential parts
    print("\n--- Demo run completed ---\n")

# ---------- Example usage ----------
if __name__ == "__main__":
    # Replace this sample message to try different scenarios
    sample_messages = [
        "I'm really stressed about a presentation tomorrow and can't sleep.",
        "I've been feeling low for a week and keep thinking about giving up on everything.",
        "I can't stop worrying about my exams but it's manageable."
    ]

    async def main():
        for m in sample_messages:
            await demo_run(m)

    asyncio.run(main())
