"""
Vision Processing Service
Claude Vision API integration for screenshot analysis
"""

import base64
import io
from typing import Optional, Tuple

from ..config import config
from ..utils.logging import logger


class VisionService:
    """Handle image analysis using Claude Vision API"""

    def __init__(self):
        """Initialize Vision service"""
        self.api_key = config.anthropic_api_key
        self.available = bool(self.api_key)
        logger.info("vision_service_init", available=self.available, api_key_set=bool(config.anthropic_api_key))

    async def analyze_image(
        self,
        image_base64: str,
        prompt: str = "Analysiere dieses Dashboard und beschreibe die wichtigsten Metriken und Trends.",
        image_media_type: str = "image/png"
    ) -> Tuple[str, float]:
        """
        Analyze image using Claude Vision API

        Args:
            image_base64: Base64-encoded image data
            prompt: Analysis prompt/question
            image_media_type: Image MIME type (image/png, image/jpeg, etc.)

        Returns:
            Tuple of (analysis_text, confidence)
        """
        if not self.available:
            logger.warning("vision_analysis_attempted_without_api_key")
            return "[STUB] Vision analysis not available - API key not configured", 0.0

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            logger.info("vision_analysis_started", image_type=image_media_type, prompt_length=len(prompt))

            # Call Claude Vision API
            message = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": image_media_type,
                                    "data": image_base64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            analysis = message.content[0].text
            confidence = 0.9  # Claude vision is highly reliable

            logger.info(
                "vision_analysis_success",
                response_length=len(analysis),
                confidence=confidence
            )

            return analysis, confidence

        except ImportError:
            logger.warning("anthropic_library_not_installed")
            return "[ERROR] Anthropic library not installed", 0.0
        except Exception as e:
            logger.error("vision_analysis_failed", error=str(e))
            raise

    async def analyze_dashboard(
        self,
        image_base64: str,
        context: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        Analyze Terra Nature dashboard screenshot

        Args:
            image_base64: Base64-encoded dashboard screenshot
            context: Optional context about what to look for

        Returns:
            Tuple of (analysis_text, confidence)
        """
        prompt = """Analysiere dieses Terra Nature Dashboard und beschreibe:
1. Aktuelle CO₂-Kompensations-Metriken
2. Energieproduktion und -verbrauch Trends
3. MRV-relevante Daten-Status
4. Technische Modulstatus (ORC, TEG, etc.)
5. Wichtige Anomalien oder Alerts

Fokus auf MRV-Konformität und technische Realität."""

        if context:
            prompt += f"\n\nZusätzlicher Kontext: {context}"

        return await self.analyze_image(image_base64, prompt, image_media_type="image/png")

    async def analyze_screenshot_for_context(
        self,
        image_base64: str
    ) -> Tuple[str, float]:
        """
        Analyze screenshot to extract context for Kappa responses

        Args:
            image_base64: Base64-encoded screenshot

        Returns:
            Tuple of (context_description, confidence)
        """
        prompt = """Extrahiere aus diesem Screenshot:
1. Sichtbare Datenmetriken und deren Werte
2. Projektstatus und aktive Module
3. Fehler oder Warnungen
4. Zeitstempel und Kontextinformationen

Gib ein JSON-ähnliches Format aus für strukturierte Verarbeitung."""

        return await self.analyze_image(image_base64, prompt, image_media_type="image/png")

    async def verify_technical_feasibility(
        self,
        image_base64: str,
        technical_claim: str
    ) -> Tuple[bool, str, float]:
        """
        Verify technical claims against visual evidence

        Args:
            image_base64: Screenshot showing technical system
            technical_claim: Claim to verify (e.g., "ORC efficiency > 15%")

        Returns:
            Tuple of (verified, reasoning, confidence)
        """
        prompt = f"""Überprüfe diese technische Aussage basierend auf dem Screenshot:
"{technical_claim}"

Antworte mit:
1. VERIFIED oder UNVERIFIED
2. Begründung basierend auf visuellen Daten
3. Vertrauensscore (0-100)"""

        analysis, confidence = await self.analyze_image(image_base64, prompt)

        # Parse response to extract verification status
        verified = "VERIFIED" in analysis.upper()
        reasoning = analysis

        return verified, reasoning, confidence


# Global Vision service instance
vision_service = VisionService()
