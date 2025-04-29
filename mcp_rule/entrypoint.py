"""
Entry point for uvx mcp-rule installation.
"""

import asyncio
import os
import sys
from typing import Dict, List, Optional, Union

from mcp import create_context_provider
from mcp.errors import MCPError

from mcp_rule.mcp import handler


def install():
    """
    Install the mcp-rule provider.
    """
    provider = create_context_provider("rule", handler)
    
    try:
        provider.register()
        print("mcp-rule has been successfully installed!")
        return 0
    except Exception as e:
        print(f"Error installing mcp-rule: {str(e)}")
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for uvx mcp-rule command.
    """
    if args is None:
        args = sys.argv[1:]
    
    # For now, we only support installation
    return install()


if __name__ == "__main__":
    sys.exit(main())
