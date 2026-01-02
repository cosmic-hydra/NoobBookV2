"""Tests for Projects API."""

import pytest
import json
from unittest.mock import patch


@pytest.mark.unit
class TestProjectsAPI:
    """Test suite for projects API endpoints."""

    def test_get_projects_empty(self, client, mock_env_vars):
        """Test getting projects when none exist."""
        with patch('app.services.data_services.project_service.get_all_projects') as mock_get:
            mock_get.return_value = []
            
            response = client.get('/api/v1/projects')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 0

    def test_get_projects_with_data(self, client, sample_project_data, mock_env_vars):
        """Test getting projects when some exist."""
        with patch('app.services.data_services.project_service.get_all_projects') as mock_get:
            mock_get.return_value = [sample_project_data]
            
            response = client.get('/api/v1/projects')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert isinstance(data, list)
            assert len(data) == 1
