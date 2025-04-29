"""
MCP implementation for Rule.io API.
"""

from mcp_rule.client import RuleClient
from mcp_rule.models import (
    Campaign, 
    CustomField, 
    Subscriber, 
    Tag, 
    Transaction
)
from mcp_rule.errors import RuleAPIError

__version__ = "0.1.0"
