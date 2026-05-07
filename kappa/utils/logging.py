import logging
import structlog
import sys
from pathlib import Path
from datetime import datetime
import json

from config import config

def setup_logging():
    """Initialize structured logging for Kappa"""

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure Python logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, config.log_level),
    )

    return structlog.get_logger()

logger = setup_logging()

class AuditLogger:
    """Append-only audit trail for compliance"""

    def __init__(self, audit_path: str):
        self.audit_path = Path(audit_path)
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, user: str = "system",
                  data: dict = None, status: str = "success"):
        """Log audit event to append-only file"""

        if not config.enable_audit:
            return

        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": event_type,
            "user": user,
            "status": status,
            "data": data or {},
        }

        try:
            with open(self.audit_path, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            logger.error("audit_write_failed", error=str(e), event_type=event_type)

    def log_query(self, text: str, mode: str, user: str = "system",
                  response: str = None, status: str = "success"):
        """Log a query/interaction"""
        self.log_event(
            event_type="query",
            user=user,
            data={
                "input": text,
                "mode": mode,
                "response_length": len(response) if response else 0,
            },
            status=status,
        )

    def log_validation(self, statement: str, mode: str, result: dict, user: str = "system"):
        """Log expert validation result"""
        self.log_event(
            event_type="validation",
            user=user,
            data={
                "statement": statement,
                "mode": mode,
                "approved": result.get("approved", False),
                "result": result,
            },
            status="success",
        )

# Initialize audit logger
audit_logger = AuditLogger(config.audit_path)
