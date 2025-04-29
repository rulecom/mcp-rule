"""
Command-line interface for mcp-rule.
"""

import argparse
import sys
from typing import List, Optional

from mcp_rule.client import RuleClient


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description="MCP implementation for Rule.io API")
    parser.add_argument("--version", action="store_true", help="Show version information")
    parser.add_argument("--api-key", help="Rule.io API key")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Subscriber commands
    sub_parser = subparsers.add_parser("subscribers", help="Manage subscribers")
    sub_parser.add_argument("--list", action="store_true", help="List subscribers")
    sub_parser.add_argument("--get", help="Get subscriber by ID")
    sub_parser.add_argument("--create", action="store_true", help="Create a new subscriber")
    sub_parser.add_argument("--email", help="Email for subscriber operations")
    
    # Tag commands
    tag_parser = subparsers.add_parser("tags", help="Manage tags")
    tag_parser.add_argument("--list", action="store_true", help="List all tags")
    
    # Campaign commands
    campaign_parser = subparsers.add_parser("campaigns", help="Manage campaigns")
    campaign_parser.add_argument("--list", action="store_true", help="List all campaigns")
    
    parsed_args = parser.parse_args(args)
    
    if parsed_args.version:
        from mcp_rule import __version__
        print(f"mcp-rule version {__version__}")
        return 0
    
    if not parsed_args.api_key:
        print("Error: API key is required. Use --api-key option.")
        return 1
    
    client = RuleClient(api_key=parsed_args.api_key)
    
    if parsed_args.command == "subscribers":
        if parsed_args.list:
            subscribers = client.get_subscribers()
            for sub in subscribers:
                print(f"{sub.id}: {sub.email}")
        elif parsed_args.get:
            subscriber = client.get_subscriber(parsed_args.get)
            print(f"ID: {subscriber.id}")
            print(f"Email: {subscriber.email}")
            print(f"Created: {subscriber.created}")
        elif parsed_args.create and parsed_args.email:
            subscriber = client.create_subscriber(email=parsed_args.email)
            print(f"Created subscriber: {subscriber.id} ({subscriber.email})")
        else:
            print("Error: Invalid subscriber command. Use --list, --get, or --create.")
            return 1
    
    elif parsed_args.command == "tags":
        if parsed_args.list:
            tags = client.get_tags()
            for tag in tags:
                print(f"{tag.id}: {tag.name}")
        else:
            print("Error: Invalid tag command. Use --list.")
            return 1
    
    elif parsed_args.command == "campaigns":
        if parsed_args.list:
            campaigns = client.get_campaigns()
            for campaign in campaigns:
                print(f"{campaign.id}: {campaign.name}")
        else:
            print("Error: Invalid campaign command. Use --list.")
            return 1
    
    else:
        print("Error: No command specified. Use --help for usage information.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
