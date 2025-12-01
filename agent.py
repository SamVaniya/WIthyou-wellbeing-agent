# withyou_real_agents.py
"""
withyou - production-oriented minimal multi-agent demo.

Features replaced mocks with:
 - PHQ-9 based symptom checker (structured intake)
 - explicit suicidal ideation handling
 - Google Calendar scheduler integration (real calls)
 - Curated resource lookup (expandable)
 - Optional Google Cloud Natural Language journaling sentiment
 - Safety-first orchestration

THIS IS NOT MEDICAL ADVICE. Requires clinical review before any production use.
"""

import os
import re
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

# ADK imports (assumes ADK is installed and configured)
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool
from google.genai import types

# Google API imports (Calendar + Cloud Natural Language)
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.cloud import language_v1

# Basic logging
import logging
logging.basicConfig(level=logging.INFO)


# ---------------------- Configuration & Retry ----------------------
retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=0.5,
    http_status_codes=[429, 500, 503, 504],
)

base_model_cfg = {
    "model": "gemini-2.5-flash-lite",
    "retry_options": retry_config,
}

# ---------------------- Utilities & Consent ----------------------
def requires_consent(user: Dict[str, Any]) -> bool:
    """Check that user explicitly consented to store long-term data."""
    return bool(user.get("consent", False))

# ---------------------- PHQ-9 Symptom Checker (real, structured) ----------------------
PHQ9_QUESTIONS = [
    "Little interest or pleasure in doing things",
    "Feeling down, depressed, or hopeless",
    "Trouble falling or staying asleep, or sleeping too much",
    "Feeling tired or having little energy",
    "Poor appetite or overeating",
    "Feeling bad about yourself — or that you are a failure",
    "Trouble concentrating on things",
    "Moving or speaking so slowly… or being fidgety/restless",
    "Thoughts that you would be better off dead or of hurting yourself"  # Q9
]

def score_phq9(answers: Dict[int,int]) -> Dict[str,Any]:
    """
    answers: {1:0..3, 2:0..3, ..., 9:0..3}
    Returns severity and flags.
    """
    total = sum(int(answers.get(i,0)) for i in range(1,10))
    q9 = int(answers.get(9,0))
    severity = "minimal"
    if total >= 20:
        severity = "severe"
    elif total >= 15:
        severity = "moderately severe"
    elif total >= 10:
        severity = "moderate"
    elif total >= 5:
        severity = "mild"
    flags = {"q9_nonzero": q9 > 0}
    return {"total": total, "severity": severity, "flags": flags, "phq9_answers": answers}


# ---------------------- Google Calendar scheduler (real) ----------------------
def build_calendar_service_from_service_account(service_account_file: str, subject_email: str = None):
    """
    Build a calendar service using a service account (domain-wide delegation or user impersonation).
    Alternatively, use OAuth2 web flow for user calendar access.
    """
    if not os.path.exists(service_account_file):
        raise FileNotFoundError("Service account file not found: " + service_account_file)

    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)

    # If impersonation is desired: credentials = credentials.with_subject(subject_email)
    if subject_email:
        credentials = credentials.with_subject(subject_email)

    service = build('calendar', 'v3', credentials=credentials, cache_discovery=False)
    return service

def create_calendar_event(service, calendar_id='primary', title='Self-care', start_dt=None, duration_minutes=20):
    if start_dt is None:
        start_dt = datetime.utcnow() + timedelta(hours=24)  # default tomorrow
    end_dt = start_dt + timedelta(minutes=duration_minutes)
    event = {
        'summary': title,
        'start': {'dateTime': start_dt.isoformat() + 'Z'},
        'end': {'dateTime': end_dt.isoformat() + 'Z'},
        'description': 'Scheduled by withyou (self-care activity).'
    }
    created = service.events().insert(calendarId=calendar_id, body=event).execute()
    return {"created": True, "event_id": created.get("id"), "htmlLink": created.get("htmlLink")}


# ---------------------- Curated resource lookup (expandable) ----------------------
CURATED_RESOURCES = {
    "US": [
        {"title": "988 Suicide & Crisis Lifeline (US)", "url": "tel:988"},
        {"title": "SAMHSA National Helpline", "url": "https://www.samhsa.gov/find-help/national-helpline"}
    ],
    "IN": [
        {"title": "AASRA (India)", "url": "tel:+912266555555"},
        {"title": "Sneha (India)", "url": "https://www.snehamumbai.org/"}
    ]
}

def resource_lookup(country_code: str = "US") -> Dict[str,Any]:
    return {"resources": CURATED_RESOURCES.get(country_code.upper(), CURATED_RESOURCES["US"]), "country": country_code.upper()}


# ---------------------- Google Cloud Natural Language journaling sentiment ----------------------
def analyze_journaling_sentiment(text: str) -> Dict[str,Any]:
    """
    Requires GOOGLE_APPLICATION_CREDENTIALS env var set to a service account with Cloud Natural Language access.
    """
    try:
        client = language_v1.LanguageServiceClient()
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})
        sentiment = response.document_sentiment
        return {"score": sentiment.score, "magnitude": sentiment.magnitude}
    except Exception as e:
        logging.exception("NL API error")
        return {"error": str(e)}


# ---------------------- Symptom checker tool function (real) ----------------------
def symptom_checker_tool_fn(payload: Any) -> Dict[str,Any]:
    """
    Accepts either:
     - a dict with 'phq9' key: {1:0..3, ..., 9:0..3} OR
     - a plain text user message (then we try to infer via regex + Q9 check)
    Returns structured severity and flags.
    """
    if isinstance(payload, dict) and "phq9" in payload:
        phq = payload["phq9"]
        return score_phq9(phq)
    else:
        # Fallback: text heuristics + Q9 check using regex
        text = str(payload).lower()
        # Very conservative: look for explicit self-harm phrases
        suicidal = bool(re.search(r"\b(kill myself|end my life|i want to die|suicid)\b", text))
        self_harm = bool(re.search(r"\b(cut myself|hurt myself)\b", text))
        anxiety = bool(re.search(r"\banxious|anxiety|panic\b", text))
        sleep = bool(re.search(r"\bsleep|insomnia|can't sleep\b", text))
        severity = "low"
        if suicidal or self_harm:
            severity = "high"
        elif anxiety or sleep:
            severity = "moderate"
        flags = {"suicidal": suicidal, "self_harm": self_harm, "anxiety": anxiety, "sleep": sleep}
        return {"severity": severity, "flags": flags, "summary": "Heuristic symptom check (no PHQ-9 provided)."}


# Wrap as FunctionTool for ADK
symptom_checker_tool = FunctionTool(name="symptom_checker", func=symptom_checker_tool_fn, description="PHQ-9 based symptom checker or heuristic check.")
resource_lookup_tool = FunctionTool(name="resource_lookup", func=lambda q: resource_lookup(q.get("country","US") if isinstance(q, dict) else "US"), description="Curated crisis resources (by country).")

# Scheduler tool uses Google Calendar: we wrap a small helper that expects service account path in env var
def scheduler_tool_fn(payload: Dict[str,Any]) -> Dict[str,Any]:
    """
    payload expected: {"title": str, "start_iso": "2025-12-03T09:00:00Z", "duration_minutes": 20, "calendar_impersonate": "<email>"}
    Requires: environment variable GCAL_SERVICE_ACCOUNT pointing to service account key file.
    """
    sa_file = os.environ.get("GCAL_SERVICE_ACCOUNT")
    if not sa_file:
        raise RuntimeError("Environment variable GCAL_SERVICE_ACCOUNT not set to service account JSON path.")
    subject = payload.get("calendar_impersonate")  # optional impersonation
    service = build_calendar_service_from_service_account(sa_file, subject_email=subject)
    start_iso = payload.get("start_iso")
    if start_iso:
        start_dt = datetime.fromisoformat(start_iso.replace("Z",""))
    else:
        start_dt = datetime.utcnow() + timedelta(hours=24)
    duration = int(payload.get("duration_minutes", 20))
    created = create_calendar_event(service, calendar_id='primary', title=payload.get("title","Self-care"), start_dt=start_dt, duration_minutes=duration)
    return created

scheduler_tool = FunctionTool(name="scheduler_tool", func=scheduler_tool_fn, description="Schedule an event on Google Calendar (service account).")

# journaling tool wrapper
journal_insights_tool = FunctionTool(name="journal_insights_tool", func=lambda txt: analyze_journaling_sentiment(txt), description="Analyze journaling sentiment using Cloud NL API (optional).")


# ---------------------- Agents ----------------------
safety_agent = Agent(
    name="SafetyAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are the Safety Agent for withyou. Your job is to examine the user's message and the symptom_check tool's output. "
        "If PHQ-9 Q9 is nonzero or tool reports 'high' severity, immediately instruct the system to escalate to human/crisis resources. "
        "Return structured JSON: {'action':'escalate'|'continue','message':..., 'resources': [...] }."
    ),
    tools=[symptom_checker_tool, resource_lookup_tool],
    output_key="safety_result"
)

triage_agent = Agent(
    name="TriageAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are the Triage Agent. Use user_message, symptom_check and journaling sentiment to decide path: 'coach','plan','refer'. "
        "Return JSON: {'path':'coach'|'plan'|'refer', 'reason': '...'}."
    ),
    tools=[symptom_checker_tool, journal_insights_tool, resource_lookup_tool],
    output_key="triage_result"
)

coach_agent = Agent(
    name="CoachAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are a supportive Coach Agent. Provide a concise, empathetic reply (2-4 short bullets/paragraphs) and one immediate micro-action. "
        "Always avoid diagnosis. If safety risk is flagged, say you cannot proceed and instruct contacting crisis resources."
    ),
    output_key="coach_reply"
)

planner_agent = Agent(
    name="PlannerAgent",
    model=Gemini(**base_model_cfg),
    instruction=(
        "You are a Planner Agent. Propose a single short self-care activity with a suggested ISO start time and duration. "
        "Return a small JSON payload that the scheduler_tool can use."
    ),
    tools=[scheduler_tool],
    output_key="planner_result"
)

# Coordinator exposes these agents as tools
root_agent = Agent(
    name="WithYouCoordinator",
    model=Gemini(**base_model_cfg),
    instruction=(
        "Coordinator: run SafetyAgent first. If safety->escalate, present resources and stop. Otherwise run TriageAgent. "
        "If triage.path == 'coach' call CoachAgent. If 'plan' call PlannerAgent then scheduler. If 'refer' call resource_lookup. "
        "Return final structured JSON {safety, triage, result}."
    ),
    tools=[
        AgentTool(safety_agent),
        AgentTool(triage_agent),
        AgentTool(coach_agent),
        AgentTool(planner_agent),
        resource_lookup_tool
    ],
    output_key="coordinator_result"
)

# ---------------------- Runner & orchestration ----------------------
runner = InMemoryRunner(agent=root_agent)

async def run_withyou_flow(user_message: str, user_meta: Dict[str,Any] = None):
    """
    user_meta may include:
      - phq9: dict of answers 1..9 -> 0..3
      - country: 'US' for resource lookup
      - consent: True/False
      - calendar_impersonate: email (optional, requires SA impersonation)
    """
    user_meta = user_meta or {}
    print("User message:", user_message)
    # 1) Compute symptom check (prefer structured PHQ-9)
    if "phq9" in user_meta:
        symptom_out = symptom_checker_tool_fn({"phq9": user_meta["phq9"]})
    else:
        symptom_out = symptom_checker_tool_fn(user_message)

    print("Symptom check:", symptom_out)

    # 2) Safety hard-stop: PHQ-9 Q9 positive or high severity
    if symptom_out.get("flags", {}).get("q9_nonzero") or symptom_out.get("severity") == "high":
        resources = resource_lookup(user_meta.get("country","US"))
        safety_msg = ("I detect signs of immediate risk. I can't handle this alone and we must escalate. "
                      "Please contact emergency services or the resources below. If you are in immediate danger, call local emergency services now.")
        print(json.dumps({"action":"escalate","message":safety_msg,"resources":resources}, indent=2))
        return {"safety":"escalate","message":safety_msg,"resources":resources}

    # 3) Optional journaling sentiment analysis (if journaling text provided)
    journal_sentiment = None
    if "journal_text" in user_meta:
        journal_sentiment = analyze_journaling_sentiment(user_meta["journal_text"])
        print("Journal sentiment:", journal_sentiment)

    # 4) Run coordinator (the ADK runner will call subagents as configured)
    # Provide a structured payload the coordinator can use
    coord_input = {
        "user_message": user_message,
        "symptom_check": symptom_out,
        "journal_sentiment": journal_sentiment,
        "meta": user_meta
    }
    # Many ADK runners expect a text payload; pass JSON string
    resp = await runner.run_debug(json.dumps(coord_input))
    print("Coordinator raw response:", resp)
    # NOTE: parse resp according to ADK runner shape; here we print and return the raw data
    return resp

# -------- Example usage --------
if __name__ == "__main__":
    async def main():
        # Example: user completed PHQ-9 (answers 1..9 each 0..3)
        phq9_example = {1:1,2:2,3:1,4:1,5:0,6:0,7:1,8:0,9:0}
        user_meta = {"phq9": phq9_example, "country":"US", "consent": True, "calendar_impersonate": None}
        result = await run_withyou_flow("I've been feeling down and can't sleep well.", user_meta)
        print("Flow result:", result)

    asyncio.run(main())
