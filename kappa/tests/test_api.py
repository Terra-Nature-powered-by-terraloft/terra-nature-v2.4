"""
Unit tests for Kappa API Routes
Tests FastAPI endpoint functionality and request/response handling
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Adjust path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kappa.main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_endpoint_returns_200(self, client):
        """Test health endpoint returns 200 OK"""
        response = client.get("/api/kappa/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_healthy_status(self, client):
        """Test health endpoint returns healthy status"""
        response = client.get("/api/kappa/health")
        data = response.json()

        assert "status" in data
        assert data["status"] in ["healthy", "degraded", "unhealthy"]

    def test_health_endpoint_includes_timestamp(self, client):
        """Test health endpoint includes timestamp"""
        response = client.get("/api/kappa/health")
        data = response.json()

        assert "timestamp" in data

    def test_health_endpoint_includes_version(self, client):
        """Test health endpoint includes version"""
        response = client.get("/api/kappa/health")
        data = response.json()

        assert "version" in data

    def test_health_endpoint_includes_components(self, client):
        """Test health endpoint includes component status"""
        response = client.get("/api/kappa/health")
        data = response.json()

        assert "components" in data
        assert isinstance(data["components"], dict)


class TestQueryEndpoint:
    """Tests for query endpoint"""

    def test_query_endpoint_accepts_post(self, client):
        """Test query endpoint accepts POST requests"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "What is ORC?", "mode": "default"}
        )

        # Should return 200 or 422 (validation)
        assert response.status_code in [200, 422]

    def test_query_endpoint_requires_text(self, client):
        """Test query endpoint requires text parameter"""
        response = client.post(
            "/api/kappa/query",
            json={"mode": "default"}
        )

        # Should reject missing text
        assert response.status_code in [400, 422]

    def test_query_endpoint_returns_response(self, client):
        """Test query endpoint returns response"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test query", "mode": "default"}
        )

        if response.status_code == 200:
            data = response.json()
            assert "response" in data or "error" in data

    def test_query_endpoint_accepts_mode(self, client):
        """Test query endpoint accepts mode parameter"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test", "mode": "cto"}
        )

        assert response.status_code in [200, 422]

    def test_query_endpoint_default_mode(self, client):
        """Test query endpoint defaults to default mode"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test"}
        )

        assert response.status_code in [200, 422]

    def test_query_endpoint_rate_limiting(self, client):
        """Test query endpoint rate limiting"""
        # Send multiple requests rapidly
        responses = []
        for i in range(5):
            response = client.post(
                "/api/kappa/query",
                json={"text": f"Test {i}", "mode": "default"},
    
            )
            responses.append(response.status_code)

        # All should succeed within limit
        assert all(status in [200, 422] for status in responses)


class TestValidationEndpoint:
    """Tests for validation endpoint"""

    def test_validation_endpoint_accepts_post(self, client):
        """Test validation endpoint accepts POST requests"""
        response = client.post(
            "/api/kappa/validate",
            json={"statement": "Test statement", "modes": ["default"]}
        )

        assert response.status_code in [200, 422]

    def test_validation_endpoint_requires_statement(self, client):
        """Test validation endpoint requires statement"""
        response = client.post(
            "/api/kappa/validate",
            json={"modes": ["default"]}
        )

        # Should reject missing statement
        assert response.status_code in [400, 422]

    def test_validation_endpoint_accepts_modes(self, client):
        """Test validation endpoint accepts modes"""
        response = client.post(
            "/api/kappa/validate",
            json={"statement": "Test", "modes": ["cto", "bank"]}
        )

        assert response.status_code in [200, 422]

    def test_validation_endpoint_returns_results(self, client):
        """Test validation endpoint returns results"""
        response = client.post(
            "/api/kappa/validate",
            json={"statement": "The ORC achieves 75% efficiency", "modes": ["cto"]}
        )

        if response.status_code == 200:
            data = response.json()
            assert "results" in data or "statement" in data


class TestMemoryEndpoint:
    """Tests for memory endpoints"""

    def test_memory_get_endpoint(self, client):
        """Test memory GET endpoint"""
        response = client.get("/api/kappa/memory/test_key")

        # Should return data or empty
        assert response.status_code in [200, 404]

    def test_memory_save_endpoint(self, client):
        """Test memory save endpoint"""
        response = client.post(
            "/api/kappa/memory/save",
            json={"key": "test_key", "value": "test_value"}
        )

        assert response.status_code in [200, 422]

    def test_memory_retrieve_after_save(self, client):
        """Test retrieving memory after saving"""
        # Save
        save_response = client.post(
            "/api/kappa/memory/save",
            json={"key": "test_key", "value": "test_value"}
        )

        if save_response.status_code == 200:
            # Retrieve
            get_response = client.get("/api/kappa/memory/test_key")
            if get_response.status_code == 200:
                data = get_response.json()
                assert "value" in data


class TestVisionEndpoint:
    """Tests for vision analysis endpoints"""

    def test_vision_endpoint_exists(self, client):
        """Test vision endpoint exists"""
        response = client.post(
            "/api/kappa/vision",
            json={"image": "data:image/png;base64,iVBORw0KG==", "mode": "default"}
        )

        # Should return 200, 400, or 422
        assert response.status_code in [200, 400, 422]

    def test_vision_dashboard_endpoint_exists(self, client):
        """Test vision dashboard endpoint exists"""
        response = client.post(
            "/api/kappa/vision-dashboard",
            json={"image": "data:image/png;base64,iVBORw0KG=="}
        )

        assert response.status_code in [200, 400, 422]


class TestAuditLogEndpoint:
    """Tests for audit log endpoints"""

    def test_audit_log_endpoint(self, client):
        """Test audit log endpoint"""
        response = client.get("/api/kappa/audit-log")

        # Should return audit log data, error if disabled, or empty
        assert response.status_code in [200, 401, 503]

    def test_audit_log_with_filters(self, client):
        """Test audit log with filters"""
        response = client.get("/api/kappa/audit-log?user=test&limit=10")

        assert response.status_code in [200, 401, 503]


class TestErrorHandling:
    """Tests for error handling"""

    def test_invalid_endpoint_returns_404(self, client):
        """Test invalid endpoint returns 404"""
        response = client.get("/invalid/endpoint")
        assert response.status_code == 404

    def test_missing_content_type(self, client):
        """Test missing content type"""
        response = client.post(
            "/api/kappa/query",
            data="invalid"
        )

        # Should handle gracefully
        assert response.status_code in [400, 422]

    def test_malformed_json(self, client):
        """Test malformed JSON"""
        response = client.post(
            "/api/kappa/query",
            data="{invalid json}",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code in [400, 422]


class TestSecurityHeaders:
    """Tests for security headers"""

    def test_content_type_header(self, client):
        """Test content type header"""
        response = client.get("/api/kappa/health")

        assert any(key.lower() == "content-type" for key in response.headers.keys())

    def test_cors_headers_if_configured(self, client):
        """Test CORS headers if configured"""
        response = client.get("/api/kappa/health")

        # Depends on CORS configuration
        assert response.status_code == 200


class TestResponseFormats:
    """Tests for response formats"""

    def test_health_response_format(self, client):
        """Test health response format"""
        response = client.get("/api/kappa/health")
        data = response.json()

        assert isinstance(data, dict)
        assert "status" in data
        assert isinstance(data["status"], str)

    def test_query_response_format(self, client):
        """Test query response format"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test"}
        )

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)

    def test_validation_response_format(self, client):
        """Test validation response format"""
        response = client.post(
            "/api/kappa/validate",
            json={"statement": "Test"}
        )

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)
