"""
Structured logging for clinical audit.
Handles tracing of conversation flows and risk detection events.
"""
import logging
import sys

def setup_telemetry():
    """
    Configures structured logging for Clinical Auditing.
    Format: [TIMESTAMP] [LEVEL] [LOGGER] - MESSAGE
    """
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
    
    # Specific clinical logger
    audit_logger = logging.getLogger("clinical_audit")
    audit_logger.setLevel(logging.INFO)
    
    return audit_logger