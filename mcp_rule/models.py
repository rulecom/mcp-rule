"""
Data models for Rule.io API entities.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    """Pagination information in API responses."""
    
    total: int
    count: int
    per_page: int
    current_page: int
    total_pages: int


class Subscriber(BaseModel):
    """Subscriber model representing a contact in Rule.io."""
    
    id: str
    email: str
    created: datetime
    updated: datetime
    fields: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    unsubscribed: bool = False
    bounced: bool = False
    status: str
    source: Optional[str] = None


class SubscriberCreate(BaseModel):
    """Model for creating a new subscriber."""
    
    email: str
    tags: List[str] = Field(default_factory=list)
    fields: Dict[str, Any] = Field(default_factory=dict)


class SubscriberResponse(BaseModel):
    """Response model for subscriber API endpoints."""
    
    data: Subscriber


class SubscribersResponse(BaseModel):
    """Response model for subscribers list API endpoint."""
    
    data: List[Subscriber]
    pagination: Pagination


class Tag(BaseModel):
    """Tag model representing a tag in Rule.io."""
    
    id: str
    name: str
    created: datetime
    updated: datetime
    subscriber_count: int


class TagResponse(BaseModel):
    """Response model for tag API endpoints."""
    
    data: Tag


class TagsResponse(BaseModel):
    """Response model for tags list API endpoint."""
    
    data: List[Tag]
    pagination: Pagination


class Campaign(BaseModel):
    """Campaign model representing a campaign in Rule.io."""
    
    id: str
    name: str
    created: datetime
    updated: datetime
    status: str
    type: str
    subject: Optional[str] = None
    sender_name: Optional[str] = None
    sender_email: Optional[str] = None


class CampaignResponse(BaseModel):
    """Response model for campaign API endpoints."""
    
    data: Campaign


class CampaignsResponse(BaseModel):
    """Response model for campaigns list API endpoint."""
    
    data: List[Campaign]
    pagination: Pagination


class CustomField(BaseModel):
    """Custom field model representing a custom field in Rule.io."""
    
    id: str
    name: str
    type: str
    created: datetime
    updated: datetime
    default_value: Optional[Any] = None


class CustomFieldResponse(BaseModel):
    """Response model for custom field API endpoints."""
    
    data: CustomField


class CustomFieldsResponse(BaseModel):
    """Response model for custom fields list API endpoint."""
    
    data: List[CustomField]
    pagination: Pagination


class Automation(BaseModel):
    """Automation model representing an automation in Rule.io."""
    
    id: str
    name: str
    created: datetime
    updated: datetime
    status: str
    trigger_type: str


class AutomationResponse(BaseModel):
    """Response model for automation API endpoints."""
    
    data: Automation


class AutomationsResponse(BaseModel):
    """Response model for automations list API endpoint."""
    
    data: List[Automation]
    pagination: Pagination


class Transaction(BaseModel):
    """Transaction model representing a transaction in Rule.io."""
    
    id: str
    subscriber_id: str
    created: datetime
    amount: float
    currency: str
    order_id: Optional[str] = None
    products: List[Dict[str, Any]] = Field(default_factory=list)


class TransactionResponse(BaseModel):
    """Response model for transaction API endpoints."""
    
    data: Transaction


class TransactionsResponse(BaseModel):
    """Response model for transactions list API endpoint."""
    
    data: List[Transaction]
    pagination: Pagination
