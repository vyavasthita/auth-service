"""
Functional tests for GET /health endpoint.

Test data is loaded from ./data/health.json.
Each test case is parameterized via @pytest.mark.test_section.
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from tests.api.common.file_helper import namespace_to_dict

TEST_DATA_FILE = "health.json"
BASE_API_URL = "/health"


@pytest.mark.test_section("health_check_validation")
@pytest.mark.asyncio
async def test_get_health(async_client: httpx.AsyncClient, test_case):
    """Should return 200 for health check."""
    with patch.object(
        __import__("src.api.dependencies.db_dependency", fromlist=["DatabaseDependency"]).DatabaseDependency,
        "check_connectivity",
        new_callable=AsyncMock,
    ):
        response = await async_client.get(
            BASE_API_URL,
            headers=namespace_to_dict(test_case.input.headers),
        )
    assert response.status_code == test_case.output.status_code
