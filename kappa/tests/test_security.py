"""
Unit tests für Security Module
Tests JWT, Rate-Limiting, Input-Validierung, Audit-Logging
"""

import pytest
import sys
import tempfile
from pathlib import Path

# Adjust path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from kappa.utils.security import JWTManager, RateLimiter, InputValidator, SecurityManager
from kappa.utils.audit import AuditLogger


@pytest.fixture
def jwt_manager():
    """Create JWT Manager"""
    return JWTManager(secret="test-secret-key")


@pytest.fixture
def rate_limiter():
    """Create Rate Limiter"""
    return RateLimiter(requests_per_minute=10)


@pytest.fixture
def security_manager():
    """Create Security Manager"""
    return SecurityManager()


@pytest.fixture
def audit_logger_temp():
    """Create temporary Audit Logger"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        temp_path = f.name
    yield AuditLogger(audit_path=temp_path)
    # Cleanup
    try:
        Path(temp_path).unlink()
    except:
        pass


class TestJWTManager:
    """JWT Manager tests"""

    def test_create_token(self, jwt_manager):
        """Test token creation"""
        token = jwt_manager.create_token("test_user")
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_valid_token(self, jwt_manager):
        """Test token verification with valid token"""
        token = jwt_manager.create_token("test_user")
        valid, user_id = jwt_manager.verify_token(token)
        assert valid is True
        assert user_id == "test_user"

    def test_verify_invalid_token(self, jwt_manager):
        """Test token verification with invalid token"""
        valid, user_id = jwt_manager.verify_token("invalid_token_xyz")
        assert valid is False
        assert user_id is None

    def test_verify_empty_token(self, jwt_manager):
        """Test token verification with empty token"""
        valid, user_id = jwt_manager.verify_token("")
        assert valid is False
        assert user_id is None


class TestRateLimiter:
    """Rate Limiter tests"""

    def test_allow_within_limit(self, rate_limiter):
        """Test requests within limit are allowed"""
        for i in range(5):
            allowed, info = rate_limiter.is_allowed("user1", "endpoint1")
            assert allowed is True
            assert info["limit"] == 10

    def test_reject_over_limit(self, rate_limiter):
        """Test requests over limit are rejected"""
        # Fill up the limit
        for i in range(10):
            rate_limiter.is_allowed("user2", "endpoint2")

        # Next request should be rejected
        allowed, info = rate_limiter.is_allowed("user2", "endpoint2")
        assert allowed is False
        assert info["remaining"] == 0

    def test_different_users_separate_limits(self, rate_limiter):
        """Test different users have separate limits"""
        # User1 uses up their limit
        for i in range(10):
            rate_limiter.is_allowed("user1", "test")

        # User2 should still have requests available
        allowed, info = rate_limiter.is_allowed("user2", "test")
        assert allowed is True
        assert info["remaining"] == 9

    def test_get_status(self, rate_limiter):
        """Test rate limit status retrieval"""
        rate_limiter.is_allowed("user3", "endpoint")
        rate_limiter.is_allowed("user3", "endpoint")

        status = rate_limiter.get_status("user3", "endpoint")
        assert status["used"] == 2
        assert status["remaining"] == 8


class TestInputValidator:
    """Input Validator tests"""

    def test_validate_valid_statement(self):
        """Test validation of valid statement"""
        valid, error = InputValidator.validate_statement("Dies ist eine normale Aussage.")
        assert valid is True
        assert error is None

    def test_validate_empty_statement(self):
        """Test validation rejects empty statement"""
        valid, error = InputValidator.validate_statement("")
        assert valid is False
        assert error is not None

    def test_validate_oversized_statement(self):
        """Test validation rejects oversized statement"""
        long_statement = "a" * 6000
        valid, error = InputValidator.validate_statement(long_statement)
        assert valid is False
        assert "Länge" in error or "überschreitet" in error

    def test_validate_dangerous_script_tag(self):
        """Test validation rejects script tags"""
        valid, error = InputValidator.validate_statement("<script>alert('XSS')</script>")
        assert valid is False
        assert error is not None

    def test_validate_dangerous_javascript(self):
        """Test validation rejects javascript: protocol"""
        valid, error = InputValidator.validate_statement("javascript:alert('XSS')")
        assert valid is False

    def test_validate_valid_user_id(self):
        """Test validation of valid user ID"""
        valid, error = InputValidator.validate_user_id("user_123-test")
        assert valid is True

    def test_validate_invalid_user_id_empty(self):
        """Test validation rejects empty user ID"""
        valid, error = InputValidator.validate_user_id("")
        assert valid is False

    def test_validate_invalid_user_id_chars(self):
        """Test validation rejects invalid characters"""
        valid, error = InputValidator.validate_user_id("user@#$%")
        assert valid is False

    def test_validate_mode(self):
        """Test expert mode validation"""
        valid, error = InputValidator.validate_mode("cto", ["cto", "bank", "mrv"])
        assert valid is True

        valid, error = InputValidator.validate_mode("invalid", ["cto", "bank"])
        assert valid is False


class TestSecurityManager:
    """Security Manager tests"""

    def test_validate_request_valid(self, security_manager):
        """Test validation of valid request"""
        valid, error = security_manager.validate_request(
            token=None,
            user_id="test_user",
            endpoint="query",
            statement="Test statement"
        )
        assert valid is True
        assert error is None

    def test_validate_request_invalid_user_id(self, security_manager):
        """Test validation rejects invalid user ID"""
        valid, error = security_manager.validate_request(
            token=None,
            user_id="@#$%",
            endpoint="query"
        )
        assert valid is False

    def test_validate_request_invalid_statement(self, security_manager):
        """Test validation rejects invalid statement"""
        valid, error = security_manager.validate_request(
            token=None,
            user_id="test_user",
            endpoint="query",
            statement="<script>alert('XSS')</script>"
        )
        assert valid is False

    def test_validate_request_rate_limit(self, security_manager):
        """Test rate limiting in validate_request"""
        # Exhaust rate limit
        for i in range(60):
            security_manager.validate_request(
                token=None,
                user_id="limited_user",
                endpoint="query"
            )

        # Next request should be blocked
        valid, error = security_manager.validate_request(
            token=None,
            user_id="limited_user",
            endpoint="query"
        )
        assert valid is False
        assert "Rate-Limit" in error


class TestAuditLogger:
    """Audit Logger tests"""

    def test_audit_logger_initialization(self, audit_logger_temp):
        """Test audit logger initializes correctly"""
        assert audit_logger_temp is not None
        assert audit_logger_temp.enabled is True

    def test_log_query(self, audit_logger_temp):
        """Test query logging"""
        audit_logger_temp.log_query(
            text="Test query",
            mode="cto",
            user="test_user",
            response="Test response"
        )

        events = audit_logger_temp.get_recent_events(1)
        assert len(events) > 0
        event = events[-1]
        assert event["event_type"] == "query"
        assert event["user"] == "test_user"

    def test_log_validation(self, audit_logger_temp):
        """Test validation logging"""
        audit_logger_temp.log_validation(
            statement="Test statement",
            modes=["cto", "bank"],
            result={"approved": True, "level": "approved"},
            user="test_user"
        )

        events = audit_logger_temp.get_events_by_type("validation")
        assert len(events) > 0

    def test_log_security_event(self, audit_logger_temp):
        """Test security event logging"""
        audit_logger_temp.log_rate_limit_exceeded("user1", "/query", 60)

        events = audit_logger_temp.get_events_by_type("security")
        assert len(events) > 0
        assert events[-1]["action"] == "rate_limit_exceeded"

    def test_log_decision(self, audit_logger_temp):
        """Test decision logging"""
        audit_logger_temp.log_decision(
            decision="Proceed with Phase 6",
            reason="Security implementation complete",
            decided_by="founder"
        )

        events = audit_logger_temp.get_events_by_type("decision")
        assert len(events) > 0

    def test_get_events_by_user(self, audit_logger_temp):
        """Test filtering events by user"""
        audit_logger_temp.log_query("q1", "default", "user1", "r1")
        audit_logger_temp.log_query("q2", "default", "user2", "r2")

        user1_events = audit_logger_temp.get_events_by_user("user1")
        assert all(e.get("user") == "user1" for e in user1_events)

    def test_get_recent_events(self, audit_logger_temp):
        """Test retrieving recent events"""
        for i in range(5):
            audit_logger_temp.log_query(f"query{i}", "default", f"user{i}", f"response{i}")

        recent = audit_logger_temp.get_recent_events(3)
        assert len(recent) <= 3
        assert all("timestamp" in e for e in recent)
