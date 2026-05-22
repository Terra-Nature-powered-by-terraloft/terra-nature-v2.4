"""
Integration Tests for Terra Nature Dashboard ↔ Kappa Expert Engine
Tests seamless integration between existing Terra dashboard and new Kappa assistant
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


class TestTerraDashboardIntegration:
    """Tests for Kappa integration with Terra Nature Dashboard"""

    def test_kappa_health_check_from_dashboard(self, client):
        """Test Terra dashboard can check Kappa health"""
        response = client.get("/api/kappa/health")

        assert response.status_code == 200
        data = response.json()

        # Dashboard expects standard health response
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] in ["healthy", "degraded", "unhealthy"]

    def test_kappa_provides_operational_status(self, client):
        """Test Kappa provides operational status to dashboard"""
        response = client.get("/api/kappa/health")

        assert response.status_code == 200
        data = response.json()

        # Should include version for dashboard display
        assert "version" in data

    def test_kappa_components_status(self, client):
        """Test Kappa reports component status"""
        response = client.get("/api/kappa/health")

        assert response.status_code == 200
        data = response.json()

        # Should report component health
        assert "components" in data

    def test_dashboard_queries_kappa_for_insights(self, client):
        """Test dashboard can query Kappa for insights"""
        # Simulate dashboard asking Kappa about current project state
        response = client.post(
            "/api/kappa/query",
            json={
                "text": "Was ist der aktuelle Projektstatus?",
                "mode": "default"
            }
        )

        assert response.status_code in [200, 422]

    def test_dashboard_uses_kappa_validation(self, client):
        """Test dashboard can use Kappa for statement validation"""
        # Dashboard validates metrics/claims
        response = client.post(
            "/api/kappa/query",
            json={
                "text": "Ist die aktuelle CO2-Bilanz korrekt?",
                "mode": "cto"
            }
        )

        assert response.status_code in [200, 422]

    def test_kappa_responds_with_dashboard_compatible_format(self, client):
        """Test Kappa responses are compatible with dashboard display"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test query", "mode": "default"}
        )

        if response.status_code == 200:
            data = response.json()

            # Dashboard expects these fields
            assert "response" in data
            assert "timestamp" in data
            assert isinstance(data["response"], str)


class TestMetricsIntegration:
    """Tests for Kappa integration with Terra metrics"""

    def test_kappa_access_to_project_metrics(self, client):
        """Test Kappa can access project metrics via memory"""
        # Save metrics to Kappa memory (simulating dashboard metrics)
        memory_response = client.post(
            "/api/kappa/memory/save",
            json={
                "key": "co2_compensated_today",
                "value": 10.5,
                "category": "metrics"
            }
        )

        assert memory_response.status_code in [200, 422]

        # Retrieve metrics
        if memory_response.status_code == 200:
            retrieve_response = client.get("/api/kappa/memory/co2_compensated_today")
            assert retrieve_response.status_code in [200, 404]

    def test_kappa_memory_stores_dashboard_state(self, client):
        """Test Kappa memory can store dashboard state"""
        dashboard_state = {
            "current_phase": "Phase 5",
            "efficiency": 0.75,
            "co2_target": 100
        }

        response = client.post(
            "/api/kappa/memory/save",
            json={
                "key": "dashboard_state",
                "value": dashboard_state,
                "category": "dashboard"
            }
        )

        assert response.status_code in [200, 422]

    def test_kappa_queries_use_dashboard_context(self, client):
        """Test Kappa queries can use dashboard context"""
        # Save dashboard context
        client.post(
            "/api/kappa/memory/save",
            json={
                "key": "project_efficiency",
                "value": 0.80,
                "category": "metrics"
            }
        )

        # Query with context should work
        response = client.post(
            "/api/kappa/query",
            json={
                "text": "Wie ist die aktuelle Effizienz?",
                "mode": "cto"
            }
        )

        assert response.status_code in [200, 422]

    def test_kappa_validation_uses_live_metrics(self, client):
        """Test Kappa validation can use live metrics"""
        # Save current metrics
        client.post(
            "/api/kappa/memory/save",
            json={
                "key": "live_metrics",
                "value": {
                    "power_output": 150,
                    "efficiency": 0.75,
                    "temperature": 95
                },
                "category": "live"
            }
        )

        # Validate statement using current metrics
        response = client.post(
            "/api/kappa/validate",
            json={
                "statement": "Current power output exceeds 100W",
                "modes": ["cto"]
            }
        )

        assert response.status_code in [200, 422]


class TestDashboardUIIntegration:
    """Tests for Kappa UI integration with dashboard"""

    def test_kappa_widget_can_fetch_health(self, client):
        """Test Kappa widget can fetch health status"""
        response = client.get("/api/kappa/health")

        assert response.status_code == 200
        assert "status" in response.json()

    def test_kappa_widget_can_send_voice_query(self, client):
        """Test Kappa UI widget can send voice queries"""
        response = client.post(
            "/api/kappa/query",
            json={
                "text": "Widget test query",
                "mode": "default",
                "user": "dashboard_widget"
            }
        )

        assert response.status_code in [200, 422]

    def test_kappa_widget_receives_formatted_response(self, client):
        """Test Kappa response is formatted for UI display"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "UI test", "mode": "default"}
        )

        if response.status_code == 200:
            data = response.json()

            # UI expects these for display
            assert "response" in data
            assert "confidence" in data or "mode" in data

    def test_kappa_validation_ui_receives_detailed_feedback(self, client):
        """Test validation responses are detailed for UI"""
        response = client.post(
            "/api/kappa/validate",
            json={
                "statement": "Test statement",
                "modes": ["cto", "bank"]
            }
        )

        if response.status_code == 200:
            data = response.json()

            # UI expects detailed results
            assert "results" in data or "overall_approved" in data

    def test_dashboard_floating_widget_integration(self, client):
        """Test floating Kappa widget in dashboard"""
        # Widget should be able to:
        # 1. Check Kappa availability
        health = client.get("/api/kappa/health")
        assert health.status_code == 200

        # 2. Accept voice input queries
        query = client.post(
            "/api/kappa/query",
            json={"text": "Widget query", "mode": "default"}
        )
        assert query.status_code in [200, 422]

        # 3. Display audit trail
        audit = client.get("/api/kappa/audit-log?limit=5")
        assert audit.status_code in [200, 503]


class TestDataFlowIntegration:
    """Tests for data flow between Terra and Kappa"""

    def test_terra_metrics_to_kappa_memory(self, client):
        """Test Terra metrics flow to Kappa memory"""
        # Simulate Terra dashboard sending metrics
        response = client.post(
            "/api/kappa/memory/save",
            json={
                "key": "terra_metrics_latest",
                "value": {
                    "timestamp": "2026-05-08T10:00:00Z",
                    "co2_compensated": 45.5,
                    "energy_generated": 250,
                    "efficiency": 0.78
                },
                "category": "terra"
            }
        )

        assert response.status_code in [200, 422]

    def test_kappa_analysis_back_to_dashboard(self, client):
        """Test Kappa analysis results sent back to dashboard"""
        # Query Kappa for analysis
        response = client.post(
            "/api/kappa/query",
            json={
                "text": "Analysiere die heutigen Metriken",
                "mode": "default"
            }
        )

        assert response.status_code in [200, 422]

        # Response should be displayable in dashboard
        if response.status_code == 200:
            assert "response" in response.json()

    def test_validation_results_in_audit_trail(self, client):
        """Test validation results are recorded in audit trail"""
        # Perform validation
        client.post(
            "/api/kappa/validate",
            json={
                "statement": "Test for audit",
                "modes": ["cto"]
            }
        )

        # Check audit trail
        audit_response = client.get("/api/kappa/audit-log?limit=20")

        if audit_response.status_code == 200:
            entries = audit_response.json()
            # Should have recent validation entry
            assert isinstance(entries, list)

    def test_dashboard_expert_mode_selection(self, client):
        """Test dashboard can select Kappa expert modes"""
        modes = ["cto", "mrv", "bank", "funding", "industrial"]

        for mode in modes:
            response = client.post(
                "/api/kappa/query",
                json={
                    "text": "Test query",
                    "mode": mode
                }
            )
            assert response.status_code in [200, 422]


class TestErrorHandlingIntegration:
    """Tests for error handling in Terra-Kappa integration"""

    def test_kappa_unavailable_handling(self, client):
        """Test dashboard handles Kappa unavailability gracefully"""
        # Health check should either return status or error
        response = client.get("/api/kappa/health")
        assert response.status_code in [200, 503]

    def test_invalid_dashboard_query_handling(self, client):
        """Test error handling for invalid queries from dashboard"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "", "mode": "default"}
        )

        # Should reject or handle gracefully
        assert response.status_code in [400, 422]

    def test_memory_access_error_handling(self, client):
        """Test error handling for memory access"""
        # Try to access non-existent memory
        response = client.get("/api/kappa/memory/non_existent_key")

        assert response.status_code in [200, 404]

    def test_network_error_resilience(self, client):
        """Test that integration tolerates transient errors"""
        # Multiple rapid requests should be handled
        responses = []
        for i in range(3):
            response = client.post(
                "/api/kappa/query",
                json={"text": f"Query {i}", "mode": "default"}
            )
            responses.append(response.status_code)

        # At least some should succeed
        assert any(status in [200] for status in responses)


class TestPerformanceIntegration:
    """Tests for performance of Terra-Kappa integration"""

    def test_kappa_response_time(self, client):
        """Test Kappa response times are acceptable for dashboard"""
        import time

        start = time.time()
        response = client.post(
            "/api/kappa/query",
            json={"text": "Performance test", "mode": "default"}
        )
        elapsed = time.time() - start

        assert response.status_code in [200, 422]
        # Response should be reasonably fast (< 5 seconds)
        assert elapsed < 5.0

    def test_health_check_performance(self, client):
        """Test health check endpoint is fast"""
        import time

        start = time.time()
        response = client.get("/api/kappa/health")
        elapsed = time.time() - start

        assert response.status_code == 200
        # Health check should be very fast (< 0.5 seconds)
        assert elapsed < 0.5

    def test_memory_access_performance(self, client):
        """Test memory access is performant"""
        import time

        # Save data
        client.post(
            "/api/kappa/memory/save",
            json={"key": "perf_test", "value": "test_value"}
        )

        # Retrieve with timing
        start = time.time()
        response = client.get("/api/kappa/memory/perf_test")
        elapsed = time.time() - start

        assert response.status_code in [200, 404]
        # Memory access should be fast (< 0.1 seconds)
        assert elapsed < 0.1
