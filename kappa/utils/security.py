"""
Security Utilities für Kappa
JWT-Validierung, Rate-Limiting, Input-Validierung
"""

import jwt
import time
from typing import Dict, Optional, Tuple
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict

from ..config import config
from ..utils.logging import logger


class JWTManager:
    """JWT Token-Management"""

    def __init__(self, secret: str = None):
        """Initialisiere JWT Manager"""
        self.secret = secret or config.jwt_secret
        self.algorithm = "HS256"
        logger.info("jwt_manager_init", algorithm=self.algorithm)

    def create_token(self, user_id: str, expires_in_hours: int = 24) -> str:
        """
        Erstelle JWT Token

        Args:
            user_id: Benutzer-Identifier
            expires_in_hours: Gültigkeitsdauer in Stunden

        Returns:
            JWT Token als String
        """
        try:
            payload = {
                "user_id": user_id,
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
                "type": "access"
            }

            token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
            logger.info("jwt_token_created", user_id=user_id)
            return token

        except Exception as e:
            logger.error("jwt_token_creation_failed", error=str(e))
            raise

    def verify_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """
        Verifiziere JWT Token

        Args:
            token: JWT Token zum Prüfen

        Returns:
            (valid: bool, user_id: Optional[str])
        """
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            user_id = payload.get("user_id")
            logger.info("jwt_token_verified", user_id=user_id)
            return True, user_id

        except jwt.ExpiredSignatureError:
            logger.warning("jwt_token_expired")
            return False, None
        except jwt.InvalidTokenError as e:
            logger.warning("jwt_token_invalid", error=str(e))
            return False, None
        except Exception as e:
            logger.error("jwt_verification_failed", error=str(e))
            return False, None


class RateLimiter:
    """Rate-Limiting pro Benutzer und Endpoint"""

    def __init__(self, requests_per_minute: int = 60):
        """
        Initialisiere Rate Limiter

        Args:
            requests_per_minute: Anfragen pro Minute pro Benutzer
        """
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.requests = defaultdict(list)
        logger.info("rate_limiter_init", rpm=requests_per_minute)

    def is_allowed(self, user_id: str, endpoint: str = "default") -> Tuple[bool, Dict]:
        """
        Prüfe ob Anfrage erlaubt ist

        Args:
            user_id: Benutzer-Identifier
            endpoint: Endpoint-Bezeichnung

        Returns:
            (allowed: bool, info: Dict mit Limit-Info)
        """
        key = f"{user_id}:{endpoint}"
        now = time.time()
        cutoff = now - self.window_seconds

        # Entferne alte Einträge
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > cutoff
        ]

        request_count = len(self.requests[key])
        remaining = self.requests_per_minute - request_count

        if request_count >= self.requests_per_minute:
            logger.warning(
                "rate_limit_exceeded",
                user_id=user_id,
                endpoint=endpoint,
                count=request_count
            )
            return False, {
                "limit": self.requests_per_minute,
                "remaining": 0,
                "reset_in_seconds": self.window_seconds
            }

        # Registriere diese Anfrage
        self.requests[key].append(now)

        return True, {
            "limit": self.requests_per_minute,
            "remaining": remaining - 1,
            "reset_in_seconds": self.window_seconds
        }

    def get_status(self, user_id: str, endpoint: str = "default") -> Dict:
        """Hole Rate-Limit Status"""
        key = f"{user_id}:{endpoint}"
        now = time.time()
        cutoff = now - self.window_seconds

        request_count = len([
            t for t in self.requests[key]
            if t > cutoff
        ])

        return {
            "limit": self.requests_per_minute,
            "used": request_count,
            "remaining": max(0, self.requests_per_minute - request_count)
        }


class InputValidator:
    """Input-Validierung und Sanitization"""

    @staticmethod
    def validate_statement(statement: str, max_length: int = 5000) -> Tuple[bool, Optional[str]]:
        """
        Validiere Statement-Input

        Args:
            statement: Zu validierende Aussage
            max_length: Maximale Länge

        Returns:
            (valid: bool, error_message: Optional[str])
        """
        if not statement:
            return False, "Statement darf nicht leer sein"

        if len(statement) > max_length:
            return False, f"Statement überschreitet maximale Länge von {max_length} Zeichen"

        # Prüfe auf gefährliche Patterns
        dangerous_patterns = [
            r"<script",
            r"javascript:",
            r"onerror=",
            r"onload=",
            r"eval\(",
        ]

        import re
        for pattern in dangerous_patterns:
            if re.search(pattern, statement, re.IGNORECASE):
                logger.warning("dangerous_input_detected", pattern=pattern)
                return False, "Input enthält potentiell gefährliche Zeichen"

        return True, None

    @staticmethod
    def validate_user_id(user_id: str) -> Tuple[bool, Optional[str]]:
        """Validiere User-ID"""
        if not user_id or len(user_id) < 1 or len(user_id) > 255:
            return False, "Ungültige User-ID"

        # Nur alphanumerisch, Bindestriche und Unterstriche
        import re
        if not re.match(r"^[a-zA-Z0-9_-]+$", user_id):
            return False, "User-ID enthält ungültige Zeichen"

        return True, None

    @staticmethod
    def validate_mode(mode: str, allowed_modes: list) -> Tuple[bool, Optional[str]]:
        """Validiere Expert-Mode"""
        if mode not in allowed_modes:
            return False, f"Ungültiger Mode: {mode}"
        return True, None


class SecurityManager:
    """Zentrale Security-Verwaltung"""

    def __init__(self):
        """Initialisiere Security Manager"""
        self.jwt_manager = JWTManager()
        self.rate_limiter = RateLimiter(requests_per_minute=60)
        self.input_validator = InputValidator()
        logger.info("security_manager_init")

    def validate_request(
        self,
        token: Optional[str],
        user_id: str,
        endpoint: str,
        statement: str = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Validiere komplette Anfrage

        Args:
            token: JWT Token
            user_id: Benutzer-ID
            endpoint: Endpoint-Name
            statement: Optional Statement zum Validieren

        Returns:
            (valid: bool, error_message: Optional[str])
        """
        # 1. User-ID validieren
        valid, error = self.input_validator.validate_user_id(user_id)
        if not valid:
            return False, error

        # 2. Rate-Limit prüfen
        allowed, _ = self.rate_limiter.is_allowed(user_id, endpoint)
        if not allowed:
            return False, "Rate-Limit überschritten"

        # 3. Statement validieren falls vorhanden
        if statement:
            valid, error = self.input_validator.validate_statement(statement)
            if not valid:
                return False, error

        # 4. Token validieren falls vorhanden
        if token:
            valid, _ = self.jwt_manager.verify_token(token)
            if not valid:
                return False, "Ungültiger Token"

        return True, None


# Globale Instanz
security_manager = SecurityManager()
