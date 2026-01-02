"""Tests for Web Agent Service."""

import pytest
from unittest.mock import patch
from app.services.ai_agents.web_agent_service import web_agent_service


@pytest.mark.unit
class TestWebAgentService:
    """Test suite for web agent."""

    def test_web_agent_initialization(self):
        """Test that web agent initializes correctly."""
        assert web_agent_service is not None
        assert web_agent_service.AGENT_NAME == "web_agent"
        assert web_agent_service.MAX_ITERATIONS == 8

    @patch('app.services.integrations.claude.claude_service.send_message')
    def test_web_agent_extraction(self, mock_send):
        """Test successful web content extraction."""
        mock_send.return_value = {
            "content": [{
                "type": "tool_use",
                "id": "tool_123",
                "name": "return_search_result",
                "input": {
                    "extracted_text": "Content extracted",
                    "success": True
                }
            }],
            "stop_reason": "tool_use",
            "usage": {"input_tokens": 100, "output_tokens": 50},
            "model": "claude-sonnet-4-5-20250929",
        }

        result = web_agent_service.run(
            url="https://example.com",
            project_id="test-123"
        )

        assert result["success"] is True
        assert "extracted_text" in result
