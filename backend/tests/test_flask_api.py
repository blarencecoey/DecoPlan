#!/usr/bin/env python3
"""
Integration tests for Flask API endpoints
"""

import sys
from pathlib import Path
import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Import app after path is set
from api.app import app, DB_PATH


@pytest.fixture
def client():
    """Create test client for Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test /health endpoint."""
    response = client.get('/health')
    assert response.status_code in [200, 503], f"Unexpected status code: {response.status_code}"

    data = response.get_json()
    assert 'status' in data
    assert 'ready' in data
    assert 'database_path' in data

    print(f"✓ Health check: status={data['status']}, ready={data['ready']}")
    print(f"  Database path: {data['database_path']}")


def test_database_path_is_absolute():
    """Test that DB_PATH is an absolute path."""
    assert Path(DB_PATH).is_absolute(), f"DB_PATH is not absolute: {DB_PATH}"
    print(f"✓ DB_PATH is absolute: {DB_PATH}")


def test_api_search_endpoint_structure(client):
    """Test /api/search endpoint structure (may fail if RAG not initialized)."""
    response = client.post(
        '/api/search',
        json={"query": "modern sofa", "n_results": 3}
    )

    # Should return either 200 (success) or 503 (RAG not initialized)
    assert response.status_code in [200, 503], f"Unexpected status code: {response.status_code}"

    data = response.get_json()

    if response.status_code == 503:
        assert 'error' in data
        print(f"⚠ RAG system not initialized (expected in some environments)")
    else:
        assert 'success' in data
        assert 'results' in data
        print(f"✓ Search endpoint working, found {data.get('n_results', 0)} results")


def test_api_recommendations_endpoint_structure(client):
    """Test /api/recommendations endpoint structure."""
    response = client.post(
        '/api/recommendations',
        json={"prompt": "modern living room", "n_results": 5}
    )

    # Should return either 200 (success) or 503 (RAG not initialized)
    assert response.status_code in [200, 503], f"Unexpected status code: {response.status_code}"

    data = response.get_json()

    if response.status_code == 503:
        assert 'error' in data
        print(f"⚠ RAG system not initialized (expected in some environments)")
    else:
        assert 'recommendations' in data
        assert 'totalResults' in data
        print(f"✓ Recommendations endpoint working, found {data.get('totalResults', 0)} items")


def test_404_handler(client):
    """Test 404 error handler."""
    response = client.get('/nonexistent/endpoint')
    assert response.status_code == 404

    data = response.get_json()
    assert 'error' in data
    print(f"✓ 404 handler working")


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "-s"])
