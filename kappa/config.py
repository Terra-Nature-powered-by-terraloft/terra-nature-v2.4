import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Literal

class KappaConfig(BaseSettings):
    """Kappa Expert Engine Configuration"""

    # === Server ===
    port: int = int(os.getenv("KAPPA_PORT", "8000"))
    host: str = os.getenv("KAPPA_HOST", "127.0.0.1")
    debug: bool = os.getenv("KAPPA_DEBUG", "false").lower() == "true"
    environment: Literal["development", "production"] = os.getenv("KAPPA_ENV", "development")

    # === Security ===
    jwt_secret: str = os.getenv("KAPPA_JWT_SECRET", "dev-secret-change-in-production")

    # === API Keys (optional, Mock-Mode wenn leer) ===
    openai_api_key: str = os.getenv("KAPPA_OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("KAPPA_ANTHROPIC_API_KEY", "")

    # === Data Paths ===
    kb_path: str = os.getenv("KAPPA_KB_PATH", "./kappa/data/kb.db")
    memory_path: str = os.getenv("KAPPA_MEMORY_PATH", "./kappa/data/memory.jsonld")
    audit_path: str = os.getenv("KAPPA_AUDIT_PATH", "./kappa/data/audit.jsonl")
    rules_path: str = os.getenv("KAPPA_RULES_PATH", "./kappa/rules")

    # === Logging ===
    log_level: str = os.getenv("KAPPA_LOG_LEVEL", "DEBUG" if debug else "INFO")

    # === Feature Flags ===
    mock_mode: bool = os.getenv("KAPPA_MOCK_MODE", "false").lower() == "true"
    enable_audit: bool = os.getenv("KAPPA_ENABLE_AUDIT", "true").lower() == "true"

    model_config = ConfigDict(
        env_file=".env.local",
        case_sensitive=False
    )

# Global config instance
config = KappaConfig()

# Ensure data directories exist
os.makedirs(config.kb_path.rsplit("/", 1)[0], exist_ok=True)
os.makedirs(config.memory_path.rsplit("/", 1)[0], exist_ok=True)
os.makedirs(config.audit_path.rsplit("/", 1)[0], exist_ok=True)
os.makedirs(config.rules_path, exist_ok=True)
