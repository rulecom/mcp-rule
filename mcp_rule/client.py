"""
Rule.io API client implementation.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import httpx
from pydantic import BaseModel

from mcp_rule.models import (
    Campaign,
    CustomField,
    Subscriber,
    SubscriberCreate,
    SubscriberResponse,
    SubscribersResponse,
    Tag,
)
from mcp_rule.errors import RuleAPIError


class RuleClient:
    """
    Client for interacting with the Rule.io API.
    """

    BASE_URL = "https://app.rule.io/api/v3"
    
    def __init__(
        self, 
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize a new Rule API client.

        Args:
            api_key: Rule.io API key
            base_url: Optional custom base URL
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )
    
    def _request(
        self, 
        method: str, 
        path: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make a request to the Rule.io API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            params: Query parameters
            data: Request body data
        
        Returns:
            Parsed JSON response
        
        Raises:
            RuleAPIError: If the request fails
        """
        url = f"{path}"
        
        try:
            if method.upper() == "GET":
                response = self._client.get(url, params=params)
            elif method.upper() == "POST":
                response = self._client.post(url, json=data)
            elif method.upper() == "PUT":
                response = self._client.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self._client.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            if response.status_code == 204:
                return None
            
            return response.json()
        
        except httpx.HTTPStatusError as e:
            error_data = {}
            try:
                error_data = e.response.json()
            except Exception:
                error_data = {"detail": e.response.text}
            
            raise RuleAPIError(
                status_code=e.response.status_code,
                message=error_data.get("message", str(e)),
                details=error_data,
            )
        
        except httpx.RequestError as e:
            raise RuleAPIError(
                status_code=None,
                message=f"Request error: {str(e)}",
                details={},
            )
    
    # Subscribers
    
    def get_subscribers(
        self, 
        page: int = 1, 
        limit: int = 100,
        **filters,
    ) -> List[Subscriber]:
        """
        Get a list of subscribers.
        
        Args:
            page: Page number
            limit: Number of items per page
            **filters: Additional filters
        
        Returns:
            List of subscribers
        """
        params = {
            "page": page,
            "limit": limit,
            **{k: v for k, v in filters.items() if v is not None},
        }
        
        response = self._request("GET", "/subscribers", params=params)
        subscribers_response = SubscribersResponse(**response)
        return subscribers_response.data
    
    def get_subscriber(self, subscriber_id: str) -> Subscriber:
        """
        Get a subscriber by ID.
        
        Args:
            subscriber_id: Subscriber ID
        
        Returns:
            Subscriber details
        """
        response = self._request("GET", f"/subscribers/{subscriber_id}")
        subscriber_response = SubscriberResponse(**response)
        return subscriber_response.data
    
    def create_subscriber(
        self,
        email: str,
        tags: Optional[List[str]] = None,
        fields: Optional[Dict[str, Any]] = None,
    ) -> Subscriber:
        """
        Create a new subscriber.
        
        Args:
            email: Subscriber email
            tags: List of tag IDs to apply
            fields: Custom field values
        
        Returns:
            Created subscriber
        """
        data = SubscriberCreate(
            email=email,
            tags=tags or [],
            fields=fields or {},
        ).model_dump()
        
        response = self._request("POST", "/subscribers", data=data)
        subscriber_response = SubscriberResponse(**response)
        return subscriber_response.data
    
    def update_subscriber(
        self,
        subscriber_id: str,
        email: Optional[str] = None,
        tags: Optional[List[str]] = None,
        fields: Optional[Dict[str, Any]] = None,
    ) -> Subscriber:
        """
        Update a subscriber.
        
        Args:
            subscriber_id: Subscriber ID
            email: New email address
            tags: List of tag IDs to apply
            fields: Custom field values
        
        Returns:
            Updated subscriber
        """
        data = {
            k: v for k, v in {
                "email": email,
                "tags": tags,
                "fields": fields,
            }.items() if v is not None
        }
        
        response = self._request("PUT", f"/subscribers/{subscriber_id}", data=data)
        subscriber_response = SubscriberResponse(**response)
        return subscriber_response.data
    
    def delete_subscriber(self, subscriber_id: str) -> None:
        """
        Delete a subscriber.
        
        Args:
            subscriber_id: Subscriber ID
        """
        self._request("DELETE", f"/subscribers/{subscriber_id}")
    
    # Tags
    
    def get_tags(self, page: int = 1, limit: int = 100) -> List[Tag]:
        """
        Get a list of tags.
        
        Args:
            page: Page number
            limit: Number of items per page
        
        Returns:
            List of tags
        """
        params = {"page": page, "limit": limit}
        response = self._request("GET", "/tags", params=params)
        return [Tag(**tag) for tag in response.get("data", [])]
    
    def create_tag(self, name: str) -> Tag:
        """
        Create a new tag.
        
        Args:
            name: Tag name
        
        Returns:
            Created tag
        """
        data = {"name": name}
        response = self._request("POST", "/tags", data=data)
        return Tag(**response.get("data", {}))
    
    # Campaigns
    
    def get_campaigns(self, page: int = 1, limit: int = 100) -> List[Campaign]:
        """
        Get a list of campaigns.
        
        Args:
            page: Page number
            limit: Number of items per page
        
        Returns:
            List of campaigns
        """
        params = {"page": page, "limit": limit}
        response = self._request("GET", "/campaigns", params=params)
        return [Campaign(**campaign) for campaign in response.get("data", [])]
    
    # Custom Fields
    
    def get_custom_fields(self, page: int = 1, limit: int = 100) -> List[CustomField]:
        """
        Get a list of custom fields.
        
        Args:
            page: Page number
            limit: Number of items per page
        
        Returns:
            List of custom fields
        """
        params = {"page": page, "limit": limit}
        response = self._request("GET", "/fields", params=params)
        return [CustomField(**field) for field in response.get("data", [])]
    
    def create_custom_field(
        self,
        name: str,
        field_type: str,
        default_value: Optional[Any] = None,
    ) -> CustomField:
        """
        Create a new custom field.
        
        Args:
            name: Field name
            field_type: Field type (string, number, boolean, date)
            default_value: Default value
        
        Returns:
            Created custom field
        """
        data = {
            "name": name,
            "type": field_type,
        }
        
        if default_value is not None:
            data["default_value"] = default_value
        
        response = self._request("POST", "/fields", data=data)
        return CustomField(**response.get("data", {}))
