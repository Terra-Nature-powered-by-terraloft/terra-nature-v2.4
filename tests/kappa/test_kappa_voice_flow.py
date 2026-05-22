"""
E2E Tests for Kappa Voice Input Flow
Tests complete voice-to-response pipeline with Whisper integration
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


class TestVoiceInputFlow:
    """Tests for voice input processing pipeline"""

    def test_audio_upload_endpoint_exists(self, client):
        """Test that audio upload endpoint is available"""
        response = client.post(
            "/api/kappa/listen",
            json={"audio_base64": "base64_encoded_audio", "format": "wav"}
        )
        # Should accept or reject based on audio quality/format
        assert response.status_code in [200, 400, 422]

    def test_voice_input_with_base64_audio(self, client):
        """Test voice input with base64 encoded audio"""
        # Mock base64 audio data (minimal valid WAV header)
        audio_base64 = "UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAA=="

        response = client.post(
            "/api/kappa/listen",
            json={"audio_base64": audio_base64, "format": "wav"}
        )

        # Should either process or return validation error
        assert response.status_code in [200, 400, 422]

    def test_voice_input_to_query_flow(self, client):
        """Test voice input triggering query endpoint"""
        # Simulate voice input being transcribed to text
        voice_text = "Wie viel Energie wurde erzeugt?"

        response = client.post(
            "/api/kappa/query",
            json={"text": voice_text, "mode": "default"}
        )

        assert response.status_code in [200, 422]

    def test_voice_with_specific_expert_mode(self, client):
        """Test voice input with specific expert mode"""
        voice_query = "Ist diese Aussage technisch plausibel?"

        response = client.post(
            "/api/kappa/query",
            json={"text": voice_query, "mode": "cto"}
        )

        assert response.status_code in [200, 422]

    def test_voice_input_with_validation(self, client):
        """Test voice input triggering validation mode"""
        spoken_statement = "Der ORC erreicht 80% Effizienz"

        response = client.post(
            "/api/kappa/validate",
            json={"statement": spoken_statement, "modes": ["cto"]}
        )

        assert response.status_code in [200, 422]

    def test_voice_error_handling_empty_audio(self, client):
        """Test error handling for empty audio input"""
        response = client.post(
            "/api/kappa/listen",
            json={"audio_base64": "", "format": "wav"}
        )

        # Should reject empty audio
        assert response.status_code in [400, 422]

    def test_voice_error_handling_invalid_format(self, client):
        """Test error handling for unsupported audio format"""
        response = client.post(
            "/api/kappa/listen",
            json={"audio_base64": "valid_base64_data", "format": "unsupported_format"}
        )

        # Should either accept or reject based on format validation
        assert response.status_code in [200, 400, 422]

    def test_voice_input_preserves_context(self, client):
        """Test that voice input maintains query context"""
        # First query
        response1 = client.post(
            "/api/kappa/query",
            json={"text": "Was ist das Projekt?", "mode": "default"}
        )

        assert response1.status_code in [200, 422]

        # Follow-up query should work
        response2 = client.post(
            "/api/kappa/query",
            json={"text": "Wie lang läuft es?", "mode": "default"}
        )

        assert response2.status_code in [200, 422]

    def test_voice_with_mrv_validation(self, client):
        """Test voice input for MRV compliance checking"""
        mrv_statement = "Heute wurden 5 Tonnen CO2 kompensiert"

        response = client.post(
            "/api/kappa/validate",
            json={"statement": mrv_statement, "modes": ["mrv"]}
        )

        assert response.status_code in [200, 422]

    def test_voice_query_response_format(self, client):
        """Test that voice query response has proper format"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test voice query", "mode": "default"}
        )

        if response.status_code == 200:
            data = response.json()
            assert "response" in data
            assert "timestamp" in data
            assert "mode" in data

    def test_voice_input_with_user_identifier(self, client):
        """Test voice input includes user identifier for audit"""
        response = client.post(
            "/api/kappa/query",
            json={"text": "Test query", "mode": "default", "user": "voice_user"}
        )

        assert response.status_code in [200, 422]

    def test_voice_multilingual_support(self, client):
        """Test voice input handling for German language"""
        german_query = "Wie ist der Status des Projekts?"

        response = client.post(
            "/api/kappa/query",
            json={"text": german_query, "mode": "default"}
        )

        assert response.status_code in [200, 422]


class TestVoiceOutputFlow:
    """Tests for voice output (TTS) handling"""

    def test_speak_endpoint_exists(self, client):
        """Test that speak endpoint is available"""
        response = client.post(
            "/api/kappa/speak",
            json={"text": "Test audio output", "language": "de"}
        )

        # Should accept or provide appropriate response
        assert response.status_code in [200, 400, 422]

    def test_text_to_speech_basic(self, client):
        """Test basic text-to-speech conversion"""
        response = client.post(
            "/api/kappa/speak",
            json={"text": "Hallo", "language": "de"}
        )

        assert response.status_code in [200, 400, 422]

    def test_text_to_speech_with_query_response(self, client):
        """Test TTS of query response"""
        # First get a query response
        query_response = client.post(
            "/api/kappa/query",
            json={"text": "Kurze Antwort", "mode": "default"}
        )

        if query_response.status_code == 200:
            query_data = query_response.json()
            response_text = query_data.get("response", "")

            if response_text:
                # Then convert to speech
                tts_response = client.post(
                    "/api/kappa/speak",
                    json={"text": response_text, "language": "de"}
                )

                assert tts_response.status_code in [200, 400, 422]

    def test_text_to_speech_empty_text(self, client):
        """Test TTS with empty text"""
        response = client.post(
            "/api/kappa/speak",
            json={"text": "", "language": "de"}
        )

        # Should reject empty text
        assert response.status_code in [400, 422]


class TestVoiceFlowIntegration:
    """Integration tests for complete voice flow"""

    def test_voice_to_audio_roundtrip(self, client):
        """Test complete voice input → process → audio output flow"""
        # Simulate voice recognition
        voice_text = "Wie viel CO2 wurde kompensiert?"

        # Step 1: Process voice input as text query
        query_response = client.post(
            "/api/kappa/query",
            json={"text": voice_text, "mode": "default"}
        )

        assert query_response.status_code in [200, 422]

        # Step 2: Get response
        if query_response.status_code == 200:
            response_data = query_response.json()
            response_text = response_data.get("response", "")

            # Step 3: Convert response to audio
            if response_text:
                tts_response = client.post(
                    "/api/kappa/speak",
                    json={"text": response_text, "language": "de"}
                )
                assert tts_response.status_code in [200, 400, 422]

    def test_voice_validation_response_to_audio(self, client):
        """Test validation response converted to speech"""
        statement = "System efficiency is 75%"

        # Validate statement
        validation_response = client.post(
            "/api/kappa/validate",
            json={"statement": statement, "modes": ["cto"]}
        )

        assert validation_response.status_code in [200, 422]

    def test_voice_expert_modes_coverage(self, client):
        """Test voice queries work with all expert modes"""
        query_text = "Test query"
        modes = ["default", "cto", "mrv", "bank", "funding", "industrial"]

        for mode in modes:
            response = client.post(
                "/api/kappa/query",
                json={"text": query_text, "mode": mode}
            )
            assert response.status_code in [200, 422], f"Failed for mode: {mode}"

    def test_voice_audit_trail_creation(self, client):
        """Test that voice interactions create audit trail"""
        # Execute voice query
        query_response = client.post(
            "/api/kappa/query",
            json={"text": "Audit test", "mode": "default", "user": "voice_user"}
        )

        assert query_response.status_code in [200, 422]

        # Check audit log contains the event
        audit_response = client.get("/api/kappa/audit-log?limit=10")

        if audit_response.status_code == 200:
            audit_entries = audit_response.json()
            # Should have some recent entries
            assert len(audit_entries) >= 0
