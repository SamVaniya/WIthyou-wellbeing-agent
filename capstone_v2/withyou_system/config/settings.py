# API Keys, Model Configs, Thresholds
import os
from google.genai import types

# Safety thresholds are strict for mental health
SAFETY_SETTINGS = [
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_LOW_AND_ABOVE"
    ),
    types.SafetySetting(
        category="HARM_CATEGORY_SELF_HARM",
        threshold="BLOCK_LOW_AND_ABOVE"
    ),
]

MODEL_NAME = "gemini-1.5-pro-002" # High reasoning for therapy
ROUTING_MODEL = "gemini-1.5-flash-002" # Fast for triage

RETRY_CONFIG = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    http_status_codes=[429, 500, 503]
)