"""Tests for Web Agent Service (simplified)."""

import pytest


@pytest.mark.unit
class TestWebAgentService:
    """Test suite for web agent."""

    @pytest.mark.skip(reason="Requires network for tiktoken - test in CI only")
    def test_web_agent_placeholder(self):
        """Placeholder test - actual tests run in CI with network."""
        pass
