"""
Pytest configuration and shared fixtures for NoobBook tests.
"""

import os
import sys
import json
import uuid
import tempfile
from typing import Dict, Any, Generator
from pathlib import Path

import pytest
from flask import Flask
from unittest.mock import Mock, MagicMock, patch

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app import create_app


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Create a Flask app instance for testing."""
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,
        "ENV": "test",
    })
    yield test_app


@pytest.fixture
def client(app: Flask):
    """Create a test client for making API requests."""
    return app.test_client()


@pytest.fixture
def temp_data_dir() -> Generator[str, None, None]:
    """Create a temporary data directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_project_id() -> str:
    """Generate a mock project ID."""
    return str(uuid.uuid4())


@pytest.fixture
def mock_source_id() -> str:
    """Generate a mock source ID."""
    return str(uuid.uuid4())


@pytest.fixture
def mock_chat_id() -> str:
    """Generate a mock chat ID."""
    return str(uuid.uuid4())


@pytest.fixture
def sample_project_data() -> Dict[str, Any]:
    """Sample project data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "name": "Test Project",
        "description": "A test project",
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:00:00Z",
        "total_api_cost": 0.0,
        "api_calls": [],
    }


@pytest.fixture
def mock_claude_response() -> Dict[str, Any]:
    """Mock Claude API response."""
    return {
        "id": "msg_test123",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "This is a mock response."
            }
        ],
        "model": "claude-sonnet-4-5-20250929",
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
        },
    }


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("PINECONE_API_KEY", "test-key")
    monkeypatch.setenv("PINECONE_INDEX_NAME", "test-index")
    monkeypatch.setenv("ANTHROPIC_TIER", "1")
