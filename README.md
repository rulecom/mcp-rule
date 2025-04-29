# mcp-rule

A Model Context Protocol (MCP) implementation for the Rule.io marketing automation platform.

## Installation

You can install the `mcp-rule` package directly with the Universal Executor (uvx):

```bash
uvx mcp-rule
```

For development, you can install from the source code:

```bash
git clone https://github.com/swesam/mcp-rule.git
cd mcp-rule
pip install -e .
```


## Features

This MCP implementation provides a standardized interface to Rule.io's API, allowing you to:

- Manage subscribers (create, read, update, delete)
- Work with tags
- Access campaigns
- Create and use custom fields
- Track transactions
- Set up automations

## Direct API Usage

You can use the Rule.io client directly in your Python code:

```python
from mcp_rule import RuleClient

# Initialize the client with your API key
client = RuleClient(api_key="your_api_key_here")

# List subscribers
subscribers = client.get_subscribers(limit=10)
for subscriber in subscribers:
    print(f"{subscriber.email} - Created: {subscriber.created}")

# Create a new subscriber
new_subscriber = client.create_subscriber(
    email="new@example.com",
    tags=["new_user", "newsletter"],
    fields={"first_name": "John", "last_name": "Doe"}
)

# Get tags
tags = client.get_tags()
for tag in tags:
    print(f"{tag.name} - Subscribers: {tag.subscriber_count}")
```

## MCP Usage

The primary purpose of this package is to provide a Model Context Protocol implementation for Rule.io. Here's how to use it with MCP:

```python
import asyncio
import json
from mcp import ContextRequest, ContextRequestMetadata, get_provider

async def example():
    # Get the Rule MCP provider
    provider = get_provider("rule")
    
    # Set up metadata with your API key
    metadata = ContextRequestMetadata(api_key="your_api_key_here")
    
    # Create a request to list subscribers
    request = ContextRequest(
        method="GET",
        path="/subscribers",
        query_params={"limit": "10"},
        metadata=metadata,
    )
    
    # Send the request
    response = await provider.handle_request(request)
    
    # Parse and use the response
    result = json.loads(response.body)
    subscribers = result.get("subscribers", [])
    for subscriber in subscribers:
        print(f"{subscriber['email']}")

# Run the example
asyncio.run(example())
```

## API Endpoints

The following MCP endpoints are available:

### Subscribers

- `GET /subscribers` - List subscribers
- `GET /subscribers/{subscriber_id}` - Get a specific subscriber
- `POST /subscribers` - Create a new subscriber
- `PUT /subscribers/{subscriber_id}` - Update a subscriber
- `DELETE /subscribers/{subscriber_id}` - Delete a subscriber

### Tags

- `GET /tags` - List tags
- `POST /tags` - Create a new tag

### Campaigns

- `GET /campaigns` - List campaigns

### Custom Fields

- `GET /fields` - List custom fields
- `POST /fields` - Create a new custom field

## Examples

Check out the `examples` directory for complete usage examples:

- `basic_usage.py` - Direct API client usage
- `mcp_usage.py` - MCP interface usage

## Documentation

For more information about the Rule.io API, see:
- [Rule API v3 Documentation](https://app.rule.io/redoc/v3)
- [Additional API Documentation](https://apidoc.rule.se/)

For details on the Model Context Protocol (MCP), visit:
- [MCP Documentation](https://modelcontextprotocol.io/introduction)

## To-Do
[ ] Add more detailed error handling
[ ] Implement more MCP endpoints
[ ] Publish to a package registry (e.g., PyPI)
[ ] Add unit tests for existing functionality

## License
MIT
