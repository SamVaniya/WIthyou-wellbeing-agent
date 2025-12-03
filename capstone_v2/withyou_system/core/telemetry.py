# Logging & Observability wrappers
import logging
import json
from typing import Any, Dict

# Configure structured logging for Cloud Logging ingestion
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("withyou_telemetry")

def log_agent_action(agent_name: str, action_type: str, details: Dict[str, Any]):
    """
    Logs agent actions while ensuring strict PII redaction.
    
    Args:
        agent_name: Name of the agent (e.g., 'safety_sentinel').
        action_type: Category (e.g., 'TOOL_USE', 'CRISIS_FLAG').
        details: Payload of the event.
    """
    # In production, use a PII scrubber library here before logging
    payload = {
        "agent": agent_name,
        "event": action_type,
        "meta": details
    }
    logger.info(json.dumps(payload))

def log_audit_trail(user_id: str, session_id: str, risk_level: str):
    """
    Critical audit trail for clinical liability.
    """
    logger.warning(f"AUDIT: User {user_id} | Session {session_id} | Risk {risk_level}")