"""
Custom exceptions for the application.
"""

class ClinicalSystemException(Exception):
    """Base exception for the clinical agent system."""
    pass

class CrisisDetectedException(ClinicalSystemException):
    """Raised when the Safety Shield intercepts a dangerous prompt."""
    def __init__(self, message="Crisis risk detected. Protocol initiated."):
        self.message = message
        super().__init__(self.message)

class ToolExecutionError(ClinicalSystemException):
    """Raised when an MCP tool fails to execute safely."""
    pass