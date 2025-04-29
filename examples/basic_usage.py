"""
Basic usage example for the Rule.io MCP client.
"""

import os
import sys
from typing import List

from mcp_rule import RuleClient


def main():
    """
    Demonstrate basic usage of the Rule.io client.
    """
    # Get API key from environment or command line
    api_key = os.environ.get("RULE_API_KEY")
    if not api_key and len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    if not api_key:
        print("Error: API key is required. Set RULE_API_KEY environment variable or pass as argument.")
        return 1
    
    # Initialize client
    client = RuleClient(api_key=api_key)
    
    # List subscribers
    print("Fetching subscribers...")
    try:
        subscribers = client.get_subscribers(limit=5)
        print(f"Found {len(subscribers)} subscribers:")
        for sub in subscribers:
            print(f"  - {sub.email} (ID: {sub.id})")
    except Exception as e:
        print(f"Error fetching subscribers: {str(e)}")
    
    # List tags
    print("\nFetching tags...")
    try:
        tags = client.get_tags(limit=5)
        print(f"Found {len(tags)} tags:")
        for tag in tags:
            print(f"  - {tag.name} (ID: {tag.id}, Subscribers: {tag.subscriber_count})")
    except Exception as e:
        print(f"Error fetching tags: {str(e)}")
    
    # List campaigns
    print("\nFetching campaigns...")
    try:
        campaigns = client.get_campaigns(limit=5)
        print(f"Found {len(campaigns)} campaigns:")
        for campaign in campaigns:
            print(f"  - {campaign.name} (ID: {campaign.id}, Status: {campaign.status})")
    except Exception as e:
        print(f"Error fetching campaigns: {str(e)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
