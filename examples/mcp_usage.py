"""
Example of using Rule.io through the MCP interface.
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Optional

from mcp import (
    ContextRequest, 
    ContextRequestMetadata, 
    ContextResponseBody,
    get_provider
)


async def fetch_subscribers(api_key: str) -> Dict:
    """
    Fetch subscribers using the MCP interface.
    """
    # Get the Rule MCP provider
    provider = get_provider("rule")
    
    # Create request metadata with API key
    metadata = ContextRequestMetadata(api_key=api_key)
    
    # Create request to get subscribers
    request = ContextRequest(
        method="GET",
        path="/subscribers",
        query_params={"page": "1", "limit": "5"},
        metadata=metadata,
    )
    
    # Send request and get response
    response = await provider.handle_request(request)
    
    # Parse and return the response
    return json.loads(response.body)


async def create_subscriber(api_key: str, email: str) -> Dict:
    """
    Create a subscriber using the MCP interface.
    """
    # Get the Rule MCP provider
    provider = get_provider("rule")
    
    # Create request metadata with API key
    metadata = ContextRequestMetadata(api_key=api_key)
    
    # Create request to create a subscriber
    request = ContextRequest(
        method="POST",
        path="/subscribers",
        body=json.dumps({"email": email}),
        metadata=metadata,
    )
    
    # Send request and get response
    response = await provider.handle_request(request)
    
    # Parse and return the response
    return json.loads(response.body)


async def main():
    """
    Demonstrate MCP usage with Rule.io.
    """
    # Get API key from environment or command line
    api_key = os.environ.get("RULE_API_KEY")
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("Error: API key is required. Set RULE_API_KEY environment variable or pass as argument.")
        return 1
    
    # Fetch subscribers
    print("Fetching subscribers via MCP...")
    try:
        result = await fetch_subscribers(api_key)
        subscribers = result.get("subscribers", [])
        print(f"Found {len(subscribers)} subscribers:")
        for sub in subscribers:
            print(f"  - {sub['email']} (ID: {sub['id']})")
    except Exception as e:
        print(f"Error fetching subscribers via MCP: {str(e)}")
    
    # Create a new subscriber
    if len(sys.argv) > 2:
        new_email = sys.argv[2]
        print(f"\nCreating subscriber with email {new_email}...")
        try:
            result = await create_subscriber(api_key, new_email)
            print(f"Subscriber created with ID: {result.get('id')}")
        except Exception as e:
            print(f"Error creating subscriber via MCP: {str(e)}")
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
