"""
Unit tests for Vision Service (Claude Vision API Integration)
Tests image analysis and screenshot processing
"""

import pytest
import sys
from pathlib import Path
import base64

# Adjust path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kappa.services.vision import VisionService


@pytest.fixture
def vision_service(monkeypatch):
    """Create vision service without API key for testing"""
    monkeypatch.setenv("KAPPA_ANTHROPIC_API_KEY", "")
    service = VisionService()
    return service


class TestVisionService:
    """Vision Service tests"""

    def test_service_initialization_without_api_key(self, vision_service):
        """Test service initializes gracefully without API key"""
        assert vision_service is not None
        assert not vision_service.available, "Service should not be available without API key"

    def test_analyze_image_without_api_key(self, vision_service):
        """Test analyze_image returns stub response without API key"""
        import asyncio

        async def run_test():
            # Create fake base64 image data
            fake_image = base64.b64encode(b"fake_image_data").decode()
            prompt = "Analysiere dieses Bild"
            analysis, confidence = await vision_service.analyze_image(fake_image, prompt)
            assert "[STUB]" in analysis or "[ERROR]" in analysis
            assert confidence == 0.0

        asyncio.run(run_test())

    def test_analyze_dashboard_without_api_key(self, vision_service):
        """Test analyze_dashboard returns stub response without API key"""
        import asyncio

        async def run_test():
            fake_image = base64.b64encode(b"fake_dashboard_image").decode()
            analysis, confidence = await vision_service.analyze_dashboard(fake_image)
            assert "[STUB]" in analysis or "[ERROR]" in analysis
            assert confidence == 0.0

        asyncio.run(run_test())

    def test_analyze_screenshot_for_context_without_api_key(self, vision_service):
        """Test analyze_screenshot_for_context returns stub response without API key"""
        import asyncio

        async def run_test():
            fake_image = base64.b64encode(b"fake_screenshot").decode()
            context, confidence = await vision_service.analyze_screenshot_for_context(fake_image)
            assert "[STUB]" in context or "[ERROR]" in context
            assert confidence == 0.0

        asyncio.run(run_test())

    def test_verify_technical_feasibility_without_api_key(self, vision_service):
        """Test verify_technical_feasibility returns stub response without API key"""
        import asyncio

        async def run_test():
            fake_image = base64.b64encode(b"fake_technical_system").decode()
            claim = "ORC efficiency > 15%"
            verified, reasoning, confidence = await vision_service.verify_technical_feasibility(
                fake_image, claim
            )
            assert isinstance(verified, bool)
            assert reasoning is not None
            assert confidence == 0.0

        asyncio.run(run_test())

    def test_analyze_with_different_media_types(self, vision_service):
        """Test analyze_image accepts different media types"""
        import asyncio

        async def run_test():
            fake_image = base64.b64encode(b"fake_image").decode()
            media_types = ["image/png", "image/jpeg", "image/webp"]

            for media_type in media_types:
                analysis, confidence = await vision_service.analyze_image(
                    fake_image, "Test prompt", media_type
                )
                assert analysis is not None

        asyncio.run(run_test())

    def test_analyze_with_context(self, vision_service):
        """Test analyze_dashboard accepts optional context"""
        import asyncio

        async def run_test():
            fake_image = base64.b64encode(b"fake_dashboard").decode()
            context = "Fokus auf CO₂-Metriken"
            analysis, confidence = await vision_service.analyze_dashboard(fake_image, context)
            assert analysis is not None

        asyncio.run(run_test())

    def test_service_structure(self, vision_service):
        """Test service has proper methods and structure"""
        assert hasattr(vision_service, "analyze_image")
        assert hasattr(vision_service, "analyze_dashboard")
        assert hasattr(vision_service, "analyze_screenshot_for_context")
        assert hasattr(vision_service, "verify_technical_feasibility")
        assert hasattr(vision_service, "available")
        assert hasattr(vision_service, "api_key")

    def test_confidence_score_format(self, vision_service):
        """Test confidence scores are valid floats"""
        import asyncio

        async def run_test():
            fake_image = base64.b64encode(b"fake_image").decode()

            # Test analyze_image
            analysis, confidence = await vision_service.analyze_image(fake_image, "Test")
            assert isinstance(confidence, float)
            assert 0.0 <= confidence <= 1.0

            # Test verify_technical_feasibility
            verified, reasoning, confidence = await vision_service.verify_technical_feasibility(
                fake_image, "Test claim"
            )
            assert isinstance(confidence, float)
            assert 0.0 <= confidence <= 1.0

        asyncio.run(run_test())

    def test_empty_image_handling(self, vision_service):
        """Test service handles empty image data gracefully"""
        import asyncio

        async def run_test():
            empty_image = ""
            analysis, confidence = await vision_service.analyze_image(empty_image, "Test")
            # Should return error or stub, not crash
            assert analysis is not None
            assert isinstance(confidence, float)

        asyncio.run(run_test())

    def test_invalid_base64_handling(self, vision_service):
        """Test service handles invalid base64 data"""
        import asyncio

        async def run_test():
            invalid_base64 = "not_valid_base64!!!"
            # Should return error or stub, not crash
            analysis, confidence = await vision_service.analyze_image(invalid_base64, "Test")
            assert analysis is not None

        asyncio.run(run_test())
