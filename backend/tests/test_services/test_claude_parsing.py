"""Tests for Claude parsing utilities."""

import pytest
from app.utils import claude_parsing_utils


@pytest.mark.unit
class TestClaudeParsingUtils:
    """Test suite for Claude response parsing."""

    def test_is_tool_use_true(self):
        """Test detection of tool_use stop reason."""
        response = {"stop_reason": "tool_use", "content": []}
        assert claude_parsing_utils.is_tool_use(response) is True

    def test_is_tool_use_false(self):
        """Test detection when not tool_use."""
        response = {"stop_reason": "end_turn", "content": []}
        assert claude_parsing_utils.is_tool_use(response) is False

    def test_extract_text_simple(self):
        """Test extracting text from response."""
        response = {
            "content": [{"type": "text", "text": "Hello"}]
        }
        text = claude_parsing_utils.extract_text(response)
        assert text == "Hello"

    def test_extract_text_empty(self):
        """Test extracting text from empty content."""
        response = {"content": []}
        text = claude_parsing_utils.extract_text(response)
        assert text == ""
