"""
Custom exceptions for Rule.io API client.
"""

from typing import Any, Dict, Optional


class RuleAPIError(Exception):
    """Exception raised for Rule.io API errors."""
    
    def __init__(
        self,
        status_code: Optional[int],
        message: str,
        details: Dict[str, Any],
    ):
        """
        Initialize a new RuleAPIError.
        
        Args:
            status_code: HTTP status code
            message: Error message
            details: Additional error details
        """
        self.status_code = status_code
        self.message = message
        self.details = details
        
        super().__init__(self.message)
