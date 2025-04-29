"""
Tests for the MCP implementation.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from mcp import ContextRequest, ContextRequestMetadata

from mcp_rule.mcp import handle_rule_mcp


class TestMCPImplementation(unittest.TestCase):
    """Test case for MCP implementation."""
    
    @patch("mcp_rule.mcp.RuleClient")
    async def test_get_subscribers(self, mock_rule_client_cls):
        """Test GET /subscribers endpoint."""
        # Set up mock client
        mock_client = MagicMock()
        mock_rule_client_cls.return_value = mock_client
        
        # Mock the client method
        mock_client.get_subscribers.return_value = [
            MagicMock(
                model_dump=lambda: {
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
            )
        ]
        
        # Create request
        request = ContextRequest(
            method="GET",
            path="/subscribers",
            query_params={"page": "1", "limit": "10"},
            metadata=ContextRequestMetadata(api_key="test_key"),
        )
        
        # Call handler
        response = await handle_rule_mcp(request)
        
        # Check response
        self.assertEqual(response.status, 200)
        
        body_dict = json.loads(response.body)
        self.assertIn("subscribers", body_dict)
        self.assertEqual(len(body_dict["subscribers"]), 1)
        self.assertEqual(body_dict["subscribers"][0]["id"], "123")
        self.assertEqual(body_dict["subscribers"][0]["email"], "test@example.com")
    
    @patch("mcp_rule.mcp.RuleClient")
    async def test_create_subscriber(self, mock_rule_client_cls):
        """Test POST /subscribers endpoint."""
        # Set up mock client
        mock_client = MagicMock()
        mock_rule_client_cls.return_value = mock_client
        
        # Mock the client method
        mock_client.create_subscriber.return_value = MagicMock(
            model_dump=lambda: {
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
        )
        
        # Create request
        request = ContextRequest(
            method="POST",
            path="/subscribers",
            body=json.dumps({
                "email": "new@example.com",
                "tags": ["tag1"],
            }),
            metadata=ContextRequestMetadata(api_key="test_key"),
        )
        
        # Call handler
        response = await handle_rule_mcp(request)
        
        # Check response
        self.assertEqual(response.status, 200)
        
        body_dict = json.loads(response.body)
        self.assertEqual(body_dict["id"], "123")
        self.assertEqual(body_dict["email"], "new@example.com")
        self.assertEqual(body_dict["tags"], ["tag1"])
        
        # Check that the client method was called correctly
        mock_client.create_subscriber.assert_called_once_with(
            email="new@example.com",
            tags=["tag1"],
            fields=None,
        )


if __name__ == "__main__":
    unittest.main()
