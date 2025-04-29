"""
Model Context Protocol implementation for Rule.io API.
"""

import json
from typing import Any, Dict, List, Optional, Union

from mcp import (
    Context,
    ContextRequest,
    ContextResponse,
    create_handler,
    create_router,
    register_handler,
)
from mcp.errors import MCPError, NotFoundError, ValidationError
from pydantic import BaseModel, Field

from mcp_rule.client import RuleClient
from mcp_rule.models import (
    Campaign,
    CustomField,
    Subscriber,
    Tag,
    Transaction,
)


# MCP Request/Response models

class SubscriberData(BaseModel):
    """Subscriber data model for MCP requests/responses."""
    
    email: str
    tags: Optional[List[str]] = None
    fields: Optional[Dict[str, Any]] = None


class SearchParams(BaseModel):
    """Search parameters for list operations."""
    
    page: Optional[int] = 1
    limit: Optional[int] = 100
    filters: Optional[Dict[str, str]] = None


class TagData(BaseModel):
    """Tag data model for MCP requests/responses."""
    
    name: str


class CampaignData(BaseModel):
    """Campaign data model for MCP requests/responses."""
    
    name: str
    subject: Optional[str] = None
    sender_name: Optional[str] = None
    sender_email: Optional[str] = None


class CustomFieldData(BaseModel):
    """Custom field data model for MCP requests/responses."""
    
    name: str
    field_type: str
    default_value: Optional[Any] = None


# MCP Router

router = create_router()


@router.get("/subscribers")
async def get_subscribers(context: Context, params: SearchParams) -> Dict[str, Any]:
    """
    Get a list of subscribers.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    filters = params.filters or {}
    subscribers = client.get_subscribers(
        page=params.page,
        limit=params.limit,
        **filters,
    )
    
    return {
        "subscribers": [sub.model_dump() for sub in subscribers],
        "page": params.page,
        "limit": params.limit,
        "total": len(subscribers),
    }


@router.get("/subscribers/{subscriber_id}")
async def get_subscriber(context: Context, subscriber_id: str) -> Dict[str, Any]:
    """
    Get a subscriber by ID.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    try:
        subscriber = client.get_subscriber(subscriber_id)
        return subscriber.model_dump()
    except Exception as e:
        raise NotFoundError(f"Subscriber not found: {str(e)}")


@router.post("/subscribers")
async def create_subscriber(context: Context, data: SubscriberData) -> Dict[str, Any]:
    """
    Create a new subscriber.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    subscriber = client.create_subscriber(
        email=data.email,
        tags=data.tags,
        fields=data.fields,
    )
    
    return subscriber.model_dump()


@router.put("/subscribers/{subscriber_id}")
async def update_subscriber(
    context: Context,
    subscriber_id: str,
    data: SubscriberData,
) -> Dict[str, Any]:
    """
    Update a subscriber.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    subscriber = client.update_subscriber(
        subscriber_id=subscriber_id,
        email=data.email,
        tags=data.tags,
        fields=data.fields,
    )
    
    return subscriber.model_dump()


@router.delete("/subscribers/{subscriber_id}")
async def delete_subscriber(context: Context, subscriber_id: str) -> Dict[str, Any]:
    """
    Delete a subscriber.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    client.delete_subscriber(subscriber_id)
    return {"success": True}


@router.get("/tags")
async def get_tags(context: Context, params: SearchParams) -> Dict[str, Any]:
    """
    Get a list of tags.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    tags = client.get_tags(
        page=params.page,
        limit=params.limit,
    )
    
    return {
        "tags": [tag.model_dump() for tag in tags],
        "page": params.page,
        "limit": params.limit,
        "total": len(tags),
    }


@router.post("/tags")
async def create_tag(context: Context, data: TagData) -> Dict[str, Any]:
    """
    Create a new tag.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    tag = client.create_tag(name=data.name)
    return tag.model_dump()


@router.get("/campaigns")
async def get_campaigns(context: Context, params: SearchParams) -> Dict[str, Any]:
    """
    Get a list of campaigns.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    campaigns = client.get_campaigns(
        page=params.page,
        limit=params.limit,
    )
    
    return {
        "campaigns": [campaign.model_dump() for campaign in campaigns],
        "page": params.page,
        "limit": params.limit,
        "total": len(campaigns),
    }


@router.get("/fields")
async def get_custom_fields(context: Context, params: SearchParams) -> Dict[str, Any]:
    """
    Get a list of custom fields.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    fields = client.get_custom_fields(
        page=params.page,
        limit=params.limit,
    )
    
    return {
        "fields": [field.model_dump() for field in fields],
        "page": params.page,
        "limit": params.limit,
        "total": len(fields),
    }


@router.post("/fields")
async def create_custom_field(context: Context, data: CustomFieldData) -> Dict[str, Any]:
    """
    Create a new custom field.
    """
    client = context.get("client")
    if not client:
        raise MCPError("Rule client not initialized")
    
    field = client.create_custom_field(
        name=data.name,
        field_type=data.field_type,
        default_value=data.default_value,
    )
    
    return field.model_dump()


# MCP Handler


async def handle_rule_mcp(request: ContextRequest) -> ContextResponse:
    """
    Main MCP handler for Rule.io API integration.
    """
    # Extract API key from request
    metadata = request.metadata or {}
    api_key = metadata.get("api_key")
    
    if not api_key:
        raise ValidationError("API key is required")
    
    # Initialize Rule client
    client = RuleClient(api_key=api_key)
    
    # Create context with client
    context = Context({"client": client})
    
    # Process the request
    return await router.handle_request(request, context)


# Register MCP handler
handler = create_handler(handle_rule_mcp)
register_handler("rule", handler)
