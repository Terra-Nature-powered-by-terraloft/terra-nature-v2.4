"""
Audit-Logging System für Kappa
Append-only JSON-L Format für Compliance und Nachvollziehbarkeit
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from ..config import config
from ..utils.logging import logger


class AuditLogger:
    """Structured Audit-Trail Logging"""

    def __init__(self, audit_path: Optional[str] = None):
        """
        Initialisiere Audit Logger

        Args:
            audit_path: Pfad zur Audit-Log Datei
        """
        self.audit_path = audit_path or config.audit_path
        self.enabled = config.enable_audit

        if self.enabled:
            self._ensure_audit_file()
            logger.info("audit_logger_init", path=self.audit_path)
        else:
            logger.info("audit_logger_disabled")

    def _ensure_audit_file(self):
        """Stelle sicher, dass Audit-Datei existiert"""
        try:
            path = Path(self.audit_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.touch()
                logger.info("audit_file_created", path=self.audit_path)
        except Exception as e:
            logger.error("audit_file_creation_failed", error=str(e))

    def _write_event(self, event: Dict[str, Any]) -> None:
        """
        Schreibe Event in Audit-Log (append-only)

        Args:
            event: Event-Daten als Dict
        """
        if not self.enabled:
            return

        try:
            # Füge Standard-Felder hinzu
            event.setdefault("timestamp", datetime.utcnow().isoformat() + "Z")
            event.setdefault("version", "1.0")

            # Schreibe als JSON-Line
            with open(self.audit_path, "a") as f:
                f.write(json.dumps(event) + "\n")

        except Exception as e:
            logger.error("audit_write_failed", error=str(e))

    def log_query(
        self,
        text: str,
        mode: str,
        user: str,
        response: str = "",
        status: str = "success"
    ) -> None:
        """Protokolliere Query-Anfrage"""
        self._write_event({
            "event_type": "query",
            "action": "query_processed",
            "user": user,
            "mode": mode,
            "query_length": len(text),
            "response_length": len(response),
            "status": status,
        })

    def log_validation(
        self,
        statement: str,
        modes: list,
        result: Dict,
        user: str
    ) -> None:
        """Protokolliere Validierungs-Anfrage"""
        self._write_event({
            "event_type": "validation",
            "action": "statement_validated",
            "user": user,
            "modes": modes,
            "statement_length": len(statement),
            "approval_level": result.get("level", "unknown"),
            "approved": result.get("approved", False),
        })

    def log_memory_access(
        self,
        action: str,
        key: str,
        category: str,
        user: str,
        value_length: int = 0
    ) -> None:
        """Protokolliere Memory-Zugriff"""
        self._write_event({
            "event_type": "memory",
            "action": action,
            "key": key,
            "category": category,
            "user": user,
            "value_length": value_length,
        })

    def log_vision_analysis(
        self,
        analysis_type: str,
        image_size: int,
        result_length: int,
        user: str,
        status: str = "success"
    ) -> None:
        """Protokolliere Vision-Analyse"""
        self._write_event({
            "event_type": "vision",
            "action": "image_analyzed",
            "analysis_type": analysis_type,
            "image_size": image_size,
            "result_length": result_length,
            "user": user,
            "status": status,
        })

    def log_speech_transcription(
        self,
        language: str,
        audio_duration: float,
        text_length: int,
        user: str,
        confidence: float = 0.0
    ) -> None:
        """Protokolliere Speech-Transkription"""
        self._write_event({
            "event_type": "speech",
            "action": "audio_transcribed",
            "language": language,
            "audio_duration_seconds": audio_duration,
            "text_length": text_length,
            "confidence": confidence,
            "user": user,
        })

    def log_rate_limit_exceeded(
        self,
        user: str,
        endpoint: str,
        limit: int
    ) -> None:
        """Protokolliere Rate-Limit Überschreitung"""
        self._write_event({
            "event_type": "security",
            "action": "rate_limit_exceeded",
            "severity": "warning",
            "user": user,
            "endpoint": endpoint,
            "limit": limit,
        })

    def log_invalid_input(
        self,
        input_type: str,
        reason: str,
        user: str
    ) -> None:
        """Protokolliere ungültige Input"""
        self._write_event({
            "event_type": "security",
            "action": "invalid_input_rejected",
            "severity": "warning",
            "input_type": input_type,
            "reason": reason,
            "user": user,
        })

    def log_auth_failure(
        self,
        user: str,
        reason: str,
        endpoint: str
    ) -> None:
        """Protokolliere Authentifizierungsfehler"""
        self._write_event({
            "event_type": "security",
            "action": "auth_failure",
            "severity": "warning",
            "user": user,
            "reason": reason,
            "endpoint": endpoint,
        })

    def log_decision(
        self,
        decision: str,
        reason: str,
        decided_by: str
    ) -> None:
        """Protokolliere wichtige Entscheidung"""
        self._write_event({
            "event_type": "decision",
            "action": "decision_made",
            "decision": decision,
            "reason": reason,
            "decided_by": decided_by,
        })

    def get_recent_events(self, limit: int = 100) -> list:
        """
        Hole letzte Events aus Audit-Log

        Args:
            limit: Anzahl der Events

        Returns:
            Liste von Event-Dicts
        """
        if not self.enabled:
            return []

        try:
            events = []
            with open(self.audit_path, "r") as f:
                for line in f.readlines()[-limit:]:
                    if line.strip():
                        try:
                            events.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
            return events
        except Exception as e:
            logger.error("audit_read_failed", error=str(e))
            return []

    def get_events_by_user(self, user: str, limit: int = 50) -> list:
        """Hole Events eines bestimmten Benutzers"""
        all_events = self.get_recent_events(limit * 2)
        return [e for e in all_events if e.get("user") == user][:limit]

    def get_events_by_type(self, event_type: str, limit: int = 50) -> list:
        """Hole Events eines bestimmten Typs"""
        all_events = self.get_recent_events(limit * 2)
        return [e for e in all_events if e.get("event_type") == event_type][:limit]


# Globale Instanz
audit_logger = AuditLogger()
