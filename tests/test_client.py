"""
Tests for the Rule.io API client.
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from mcp_rule import RuleClient
from mcp_rule.errors import RuleAPIError


class TestRuleClient(unittest.TestCase):
    """Test case for RuleClient."""
    
    def setUp(self):
        """Set up test client."""
        self.api_key = "test_api_key"
        
        # Create a client with mocked HTTP client
        with patch("httpx.Client"):
            self.client = RuleClient(api_key=self.api_key)
            self.client._client = MagicMock()
    
    def test_get_subscribers(self):
        """Test getting subscribers."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "123",
                    "email": "test@example.com",
                    "created": "2023-01-01T00:00:00Z",
                    "updated": "2023-01-01T00:00:00Z",
                    "fields": {},
                    "tags": [],
                    "unsubscribed": False,
                    "bounced": False,
                    "status": "active",
                }
            ],
            "pagination": {
                "total": 1,
                "count": 1,
                "per_page": 10,
                "current_page": 1,
                "total_pages": 1,
            }
        }
        
        # Set up mock client
        self.client._client.get.return_value = mock_response
        
        # Call the method
        subscribers = self.client.get_subscribers()
        
        # Check that the client was called correctly
        self.client._client.get.assert_called_once_with("/subscribers", params={"page": 1, "limit": 100})
        
        # Check that the response was parsed correctly
        self.assertEqual(len(subscribers), 1)
        self.assertEqual(subscribers[0].id, "123")
        self.assertEqual(subscribers[0].email, "test@example.com")
    
    def test_create_subscriber(self):
        """Test creating a subscriber."""
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": "123",
                "email": "new@example.com",
                "created": "2023-01-01T00:00:00Z",
                "updated": "2023-01-01T00:00:00Z",
                "fields": {},
                "tags": ["tag1"],
                "unsubscribed": False,
                "bounced": False,
                "status": "active",
            }
        }
        
        # Set up mock client
        self.client._client.post.return_value = mock_response
        
        # Call the method
        subscriber = self.client.create_subscriber(
            email="new@example.com",
            tags=["tag1"],
        )
        
        # Check that the client was called correctly
        self.client._client.post.assert_called_once()
        
        # Check that the response was parsed correctly
        self.assertEqual(subscriber.id, "123")
        self.assertEqual(subscriber.email, "new@example.com")
        self.assertEqual(subscriber.tags, ["tag1"])
    
    def test_api_error(self):
        """Test handling of API errors."""
        # Set up mock error response
        from httpx import HTTPStatusError, Response
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not found"}
        mock_response.text = "Not found"
        
        mock_error = HTTPStatusError("Not found", request=MagicMock(), response=mock_response)
        
        # Set up mock client to raise the error
        self.client._client.get.side_effect = mock_error
        
        # Call the method and check that it raises the expected error
        with self.assertRaises(RuleAPIError) as context:
            self.client.get_subscribers()
        
        # Check error properties
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.message, "Not found")


if __name__ == "__main__":
    unittest.main()
