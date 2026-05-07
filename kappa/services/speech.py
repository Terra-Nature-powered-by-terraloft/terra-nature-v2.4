"""
Speech Processing Service
Whisper integration for audio transcription
"""

import io
from typing import Optional, Tuple
import base64

from ..config import config
from ..utils.logging import logger


class WhisperService:
    """Handle speech-to-text conversion using OpenAI Whisper API"""

    def __init__(self):
        """Initialize Whisper service"""
        self.api_key = config.openai_api_key
        self.available = bool(self.api_key)
        logger.info("whisper_service_init", available=self.available, api_key_set=bool(config.openai_api_key))

    async def transcribe(self, audio_bytes: bytes, language: str = "de") -> Tuple[str, float]:
        """
        Transcribe audio to text using Whisper API

        Args:
            audio_bytes: Raw audio bytes (WAV, MP3, etc.)
            language: Language code (de, en, etc.)

        Returns:
            Tuple of (transcribed_text, confidence)
        """
        if not self.available:
            logger.warning("whisper_transcription_attempted_without_api_key")
            return "[STUB] Whisper not available - API key not configured", 0.0

        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)

            # Create file-like object from bytes
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.wav"

            logger.info("whisper_transcription_started", audio_size=len(audio_bytes))

            # Call Whisper API
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json"
            )

            text = transcript.text
            confidence = getattr(transcript, 'confidence', 0.9)

            logger.info(
                "whisper_transcription_success",
                text_length=len(text),
                confidence=confidence
            )

            return text, confidence

        except ImportError:
            logger.warning("openai_library_not_installed")
            return "[ERROR] OpenAI library not installed", 0.0
        except Exception as e:
            logger.error("whisper_transcription_failed", error=str(e))
            raise

    async def transcribe_base64(self, audio_base64: str, language: str = "de") -> Tuple[str, float]:
        """
        Transcribe base64-encoded audio

        Args:
            audio_base64: Base64-encoded audio data
            language: Language code

        Returns:
            Tuple of (transcribed_text, confidence)
        """
        try:
            # Decode base64 to bytes
            audio_bytes = base64.b64decode(audio_base64)
            return await self.transcribe(audio_bytes, language)
        except Exception as e:
            logger.error("base64_decode_failed", error=str(e))
            raise


# Global Whisper service instance
whisper_service = WhisperService()
