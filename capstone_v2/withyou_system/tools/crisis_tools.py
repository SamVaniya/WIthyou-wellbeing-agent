# Hotline lookups, Emergency protocols
from typing import Dict, List

def resource_lookup(location: str, urgency: str) -> Dict[str, str]:
    """
    Retrieves vetted mental health resources based on location and urgency.
    
    Args:
        location: The user's region (e.g., "India", "USA").
        urgency: Level of crisis ("immediate", "informational").
        
    Returns:
        Dictionary containing helpline numbers and website links.
    """
    # In production, this queries a verified database via API
    resources = {
        "India": {
            "immediate": "Vandrevala Foundation: 1860-266-2345 | AASRA: 9820466726",
            "informational": "https://nimhans.ac.in/"
        },
        "Global": {
            "immediate": "International Suicide Prevention: findahelpline.com",
            "informational": "WHO Mental Health Resources"
        }
    }
    
    # Default to Global if location unknown
    return resources.get(location, resources["Global"])