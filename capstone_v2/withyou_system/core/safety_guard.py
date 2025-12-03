# Deterministic regex/keyword filters
import re

CRISIS_KEYWORDS = [
    r"\b(kill|hurt) myself\b",
    r"\bwant to die\b",
    r"\bsuicide\b",
    r"\boverdose\b",
    r"\bend it all\b"
]

def run_pre_computation_safety_check(user_input: str) -> bool:
    """
    Deterministic safety filter. Returns True if a hard crisis keyword is detected.
    This acts as a 'circuit breaker' before calling expensive or slow LLMs.
    """
    normalized_text = user_input.lower()
    for pattern in CRISIS_KEYWORDS:
        if re.search(pattern, normalized_text):
            return True
    return False