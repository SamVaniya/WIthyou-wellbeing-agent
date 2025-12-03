# Memory Bank & Session Management
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

# Initialize persistent layers
# In production, this would connect to Vertex AI Memory Bank for long-term vector storage
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

def get_session_services():
    return session_service, memory_service