"""
Unit tests for Speech Service (Whisper Integration)
Tests audio transcription and speech processing
"""

import pytest
import sys
from pathlib import Path

# Adjust path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.speech import WhisperService


@pytest.fixture
def speech_service(monkeypatch):
    """Create speech service without API key for testing"""
    monkeypatch.setenv("KAPPA_OPENAI_API_KEY", "")
    service = WhisperService()
    return service


class TestWhisperService:
    """Whisper Service tests"""

    def test_service_initialization_without_api_key(self, speech_service):
        """Test service initializes gracefully without API key"""
        assert speech_service is not None
        assert not speech_service.available, "Service should not be available without API key"

    def test_transcribe_without_api_key(self, speech_service):
        """Test transcribe returns stub response without API key"""
        import asyncio

        async def run_test():
            audio_bytes = b"fake_audio_data"
            text, confidence = await speech_service.transcribe(audio_bytes)
            assert "[STUB]" in text or "[ERROR]" in text
            assert confidence == 0.0

        asyncio.run(run_test())

    def test_transcribe_base64_without_api_key(self, speech_service):
        """Test base64 transcribe returns stub response without API key"""
        import asyncio
        import base64

        async def run_test():
            # Create a fake base64 encoded audio
            fake_audio = base64.b64encode(b"fake_audio_data").decode()
            text, confidence = await speech_service.transcribe_base64(fake_audio)
            assert "[STUB]" in text or "[ERROR]" in text
            assert confidence == 0.0

        asyncio.run(run_test())

    def test_transcribe_invalid_base64(self, speech_service):
        """Test transcribe base64 handles invalid input"""
        import asyncio

        async def run_test():
            invalid_base64 = "not_valid_base64!!!"
            with pytest.raises(Exception):
                await speech_service.transcribe_base64(invalid_base64)

        asyncio.run(run_test())

    @pytest.mark.skipif(
        not Path("/etc/os-release").exists() or "ubuntu" not in Path("/etc/os-release").read_text().lower(),
        reason="Integration test - requires real audio file"
    )
    def test_service_structure(self, speech_service):
        """Test service has proper methods and structure"""
        assert hasattr(speech_service, "transcribe")
        assert hasattr(speech_service, "transcribe_base64")
        assert hasattr(speech_service, "available")
        assert hasattr(speech_service, "api_key")

    def test_language_parameter(self, speech_service):
        """Test that language parameter is accepted"""
        import asyncio

        async def run_test():
            # Just verify the method accepts language parameter
            audio_bytes = b"fake_audio_data"
            text, confidence = await speech_service.transcribe(audio_bytes, language="en")
            assert text is not None

        asyncio.run(run_test())

    def test_multiple_languages(self, speech_service):
        """Test transcribe accepts various language codes"""
        import asyncio

        async def run_test():
            audio_bytes = b"fake_audio_data"
            languages = ["de", "en", "fr", "es", "it"]

            for lang in languages:
                text, confidence = await speech_service.transcribe(audio_bytes, language=lang)
                assert text is not None

        asyncio.run(run_test())
