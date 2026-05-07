from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
import json

from api.models import (
    QueryRequest, QueryResponse, HealthResponse,
    ValidationRequest, ValidationResponse, ValidationResult,
    MemorySaveRequest, MemoryResponse,
    ErrorResponse, AuditLogEntry
)
from utils.logging import logger, audit_logger
from config import config

router = APIRouter(prefix="/api/kappa", tags=["kappa"])

# === HEALTH CHECK ===

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - verifies Kappa system status
    """
    components = {
        "fastapi": "operational",
        "config": "loaded",
        "logging": "operational",
        "audit": "operational" if config.enable_audit else "disabled",
        "mock_mode": "enabled" if config.mock_mode else "disabled",
    }

    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        components=components
    )

# === QUERY ENDPOINT (STUB) ===

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Main query endpoint - receives text input and returns expert response

    Modes:
    - default: No expert validation
    - cto: CTO / Climate Deep Tech validation
    - mrv: MRV / Compliance validation
    - bank: Bankfähigkeit validation
    - funding: Fördermittel validation
    - industrial: Industrial customer validation
    - ip: IP / Governance validation
    - communication: Communication validation
    - professorale: Academic validation
    - business: Business Development validation
    """

    logger.info(
        "query_received",
        text=request.text[:100],
        mode=request.mode,
        user=request.user
    )

    # STUB RESPONSE - in Phase 2, this will call the expert engine
    response_text = f"[STUB] Received in mode '{request.mode}': {request.text}"

    if config.mock_mode:
        # Mock response for testing without API keys
        if "CO₂" in request.text or "Energie" in request.text or "Wärme" in request.text:
            response_text = "[MOCK] Kappa verarbeitet MRV-relevante Daten. Spezifische Antwort kommt in Phase 2."
        else:
            response_text = "[MOCK] Stub-Antwort. Volle Intelligenz kommt in Phase 2."

    result = QueryResponse(
        response=response_text,
        mode=request.mode,
        confidence=0.5 if config.mock_mode else 0.0,
        sources=["stub"],
        timestamp=datetime.utcnow().isoformat() + "Z",
        requires_approval=False,
        approval_level="approved"
    )

    # Log the query
    audit_logger.log_query(
        text=request.text,
        mode=request.mode,
        user=request.user,
        response=response_text,
        status="success"
    )

    return result

# === VALIDATION ENDPOINT (STUB) ===

@router.post("/validate", response_model=ValidationResponse)
async def validate(request: ValidationRequest):
    """
    Expert validation endpoint - checks statement against expert rules

    Validates against multiple expert perspectives:
    - CTO: Technical reality & feasibility
    - MRV: Compliance & monitoring capability
    - Bank: Financial & creditworthiness
    - Funding: Innovation & grant eligibility
    - Industrial: Practical utility for operators
    - IP: Intellectual property & legal
    - Communication: Message appropriateness
    - Professorale: Academic rigor
    - Business: Market & growth potential
    """

    logger.info(
        "validation_requested",
        statement=request.statement[:100],
        modes=request.modes,
        user=request.user
    )

    # STUB: Return approved for now
    stub_result = ValidationResult(
        expert="stub",
        approved=True,
        confidence=0.0,
        feedback="[STUB] Validation framework ready. Actual rules load in Phase 5.",
        suggestions=["Load expert rules from YAML"],
        conditions=[]
    )

    result = ValidationResponse(
        statement=request.statement,
        timestamp=datetime.utcnow().isoformat() + "Z",
        results={"stub": stub_result},
        overall_approved=True,
        approval_level="conditional",
        user=request.user
    )

    audit_logger.log_validation(
        statement=request.statement,
        mode="stub",
        result={"approved": True},
        user=request.user
    )

    return result

# === MEMORY ENDPOINTS (STUB) ===

@router.post("/memory/save", response_model=MemoryResponse)
async def save_memory(request: MemorySaveRequest):
    """Save data to project memory (stub)"""

    logger.info(
        "memory_save",
        key=request.key,
        category=request.category,
        user=request.user
    )

    # STUB: Just acknowledge for now
    return MemoryResponse(
        key=request.key,
        value=request.value,
        category=request.category,
        timestamp=datetime.utcnow().isoformat() + "Z",
        user=request.user
    )

@router.get("/memory/{key}", response_model=MemoryResponse)
async def get_memory(key: str = Query(..., min_length=1)):
    """Retrieve data from project memory (stub)"""

    logger.info("memory_retrieve", key=key)

    # STUB: Return empty for now
    return MemoryResponse(
        key=key,
        value=None,
        category=None,
        timestamp=datetime.utcnow().isoformat() + "Z",
        user="system"
    )

# === AUDIT LOG ENDPOINT ===

@router.get("/audit-log", response_model=list[AuditLogEntry])
async def get_audit_log(limit: int = Query(100, ge=1, le=1000)):
    """Retrieve recent audit log entries"""

    if not config.enable_audit:
        raise HTTPException(status_code=503, detail="Audit logging disabled")

    entries = []
    try:
        with open(config.audit_path, "r") as f:
            for line in f.readlines()[-limit:]:
                if line.strip():
                    entries.append(AuditLogEntry(**json.loads(line)))
    except FileNotFoundError:
        logger.info("audit_log_not_yet_created")

    return entries

# === LISTEN ENDPOINT (STUB for Audio) ===

@router.post("/listen")
async def listen():
    """Audio input endpoint (stub for Whisper integration)"""
    return {
        "status": "stub",
        "message": "Audio transcription available in Phase 3 (Whisper integration)"
    }

# === SPEAK ENDPOINT (STUB for TTS) ===

@router.post("/speak")
async def speak(text: str = Query(..., min_length=1)):
    """Text-to-speech endpoint (stub)"""
    return {
        "status": "stub",
        "message": "TTS available in Phase 3 or via external API"
    }
