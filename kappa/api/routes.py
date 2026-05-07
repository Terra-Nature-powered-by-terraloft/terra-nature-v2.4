from fastapi import APIRouter, Query, HTTPException, UploadFile, File
from datetime import datetime
import json

from .models import (
    QueryRequest, QueryResponse, HealthResponse,
    ValidationRequest, ValidationResponse, ValidationResult,
    MemorySaveRequest, MemoryResponse,
    ErrorResponse, AuditLogEntry
)
from ..utils.logging import logger, audit_logger
from ..config import config
from ..core.knowledge_base import kb
from ..core.memory import memory
from ..services.speech import whisper_service

router = APIRouter(prefix="/api/kappa", tags=["kappa"])

# === HEALTH CHECK ===

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - verifies Kappa system status
    """
    kb_stats = kb.get_stats()
    memory_stats = memory.get_memory_stats()

    components = {
        "fastapi": "operational",
        "config": "loaded",
        "logging": "operational",
        "audit": "operational" if config.enable_audit else "disabled",
        "mock_mode": "enabled" if config.mock_mode else "disabled",
        "knowledge_base": "operational",
        "project_memory": "operational",
    }

    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        components=components,
        stats={
            "knowledge_base": kb_stats,
            "project_memory": memory_stats
        }
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

    sources = []
    confidence = 0.5
    response_text = None

    # Search knowledge base for relevant concepts
    search_results = kb.search_concepts(request.text)
    if search_results:
        sources.append("knowledge_base")
        confidence = max(confidence, 0.7)
        concept_info = []
        for concept in search_results[:3]:  # Limit to top 3
            concept_info.append(f"{concept['name']} ({concept['category']}): {concept['definition']}")
        response_text = "Wissensbank-Treffer:\n" + "\n".join(concept_info)

    # Check project memory for context
    memory_summary = memory.get_memory_summary()
    if memory_summary and memory_summary.get("project_status"):
        sources.append("project_memory")
        if response_text:
            response_text += "\n\nProjekt-Status: " + str(memory_summary["project_status"].get("current_phase", "Unbekannt"))

    # Fallback if no knowledge found
    if not response_text:
        if config.mock_mode:
            if "CO₂" in request.text or "Energie" in request.text or "Wärme" in request.text:
                response_text = "[MOCK] Kappa verarbeitet MRV-relevante Daten. Detaillierte Antwort kommt mit Phase 5 Expert Engine."
            else:
                response_text = "[MOCK] Eingabe erkannt. Volle Intelligenz wird in Phase 5 verfügbar."
        else:
            response_text = f"Keine direkten Treffer für '{request.text}'. Knowledge Base wird kontinuierlich erweitert."
        sources.append("fallback")
        confidence = 0.3

    result = QueryResponse(
        response=response_text,
        mode=request.mode,
        confidence=confidence,
        sources=sources,
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

# === MEMORY ENDPOINTS ===

@router.post("/memory/save", response_model=MemoryResponse)
async def save_memory(request: MemorySaveRequest):
    """Save data to project memory"""

    logger.info(
        "memory_save",
        key=request.key,
        category=request.category,
        user=request.user
    )

    try:
        # Route to appropriate memory manager based on category
        if request.category == "task":
            memory.add_task(
                request.value,
                priority=request.metadata.get("priority", "medium") if request.metadata else "medium",
                assigned_to=request.metadata.get("assigned_to") if request.metadata else None
            )
        elif request.category == "decision":
            memory.add_decision(
                request.value,
                reason=request.metadata.get("reason", "") if request.metadata else "",
                decided_by=request.user
            )
        elif request.category == "project_status":
            memory.update_project_status({request.key: request.value})
        elif request.category == "technical_module":
            memory.update_technical_module(
                request.key,
                request.value,
                details=request.metadata
            )
        elif request.category == "financial":
            memory.update_financial_data(**request.metadata) if request.metadata else None
        elif request.category == "stakeholder":
            memory.add_stakeholder(
                request.value,
                role=request.metadata.get("role", "") if request.metadata else ""
            )
        elif request.category == "milestone":
            memory.add_milestone(
                request.value,
                target_date=request.metadata.get("target_date", "") if request.metadata else "",
                description=request.metadata.get("description", "") if request.metadata else ""
            )
        else:
            # Generic audit event
            memory.record_audit_event(f"memory_save_{request.category}", {
                "key": request.key,
                "value": request.value,
                "metadata": request.metadata
            })

        return MemoryResponse(
            key=request.key,
            value=request.value,
            category=request.category,
            timestamp=datetime.utcnow().isoformat() + "Z",
            user=request.user
        )
    except Exception as e:
        logger.error("memory_save_failed", error=str(e), key=request.key)
        raise HTTPException(status_code=500, detail=f"Failed to save to memory: {str(e)}")

@router.get("/memory/{key}", response_model=MemoryResponse)
async def get_memory(key: str = Query(..., min_length=1)):
    """Retrieve data from project memory"""

    logger.info("memory_retrieve", key=key)

    try:
        # Try to find in project status
        status = memory.get_project_status()
        if key in status:
            return MemoryResponse(
                key=key,
                value=status[key],
                category="project_status",
                timestamp=datetime.utcnow().isoformat() + "Z",
                user="system"
            )

        # Try technical modules
        tech_modules = memory.get_technical_modules()
        if key in tech_modules:
            return MemoryResponse(
                key=key,
                value=tech_modules[key],
                category="technical_module",
                timestamp=datetime.utcnow().isoformat() + "Z",
                user="system"
            )

        # Key not found
        return MemoryResponse(
            key=key,
            value=None,
            category=None,
            timestamp=datetime.utcnow().isoformat() + "Z",
            user="system"
        )
    except Exception as e:
        logger.error("memory_retrieve_failed", error=str(e), key=key)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve from memory: {str(e)}")

@router.get("/memory-summary")
async def get_memory_summary():
    """Get complete project memory summary"""

    logger.info("memory_summary_requested")

    try:
        summary = memory.get_memory_summary()
        return {
            "summary": summary,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error("memory_summary_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get memory summary: {str(e)}")

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

# === LISTEN ENDPOINT (Whisper Integration) ===

@router.post("/listen")
async def listen(audio: UploadFile = File(...), language: str = Query("de", min_length=2, max_length=5)):
    """
    Audio input endpoint - transcribes audio to text using Whisper

    Args:
        audio: Audio file (WAV, MP3, M4A, etc.)
        language: Language code (de, en, fr, etc.)

    Returns:
        Transcribed text with confidence score
    """
    logger.info("listen_request", filename=audio.filename, content_type=audio.content_type)

    try:
        # Read audio file
        audio_bytes = await audio.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Audio file is empty")

        # Transcribe using Whisper
        transcribed_text, confidence = await whisper_service.transcribe(audio_bytes, language=language)

        logger.info(
            "listen_transcription_complete",
            text_length=len(transcribed_text),
            confidence=confidence
        )

        return {
            "text": transcribed_text,
            "confidence": confidence,
            "language": language,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("listen_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.post("/listen-and-query")
async def listen_and_query(
    audio: UploadFile = File(...),
    mode: str = Query("default"),
    language: str = Query("de"),
    user: str = Query("system")
):
    """
    Combined endpoint - transcribes audio and returns expert response in one call

    Args:
        audio: Audio file to transcribe
        mode: Expert mode for response
        language: Language of audio
        user: User identifier

    Returns:
        Both transcribed text and Kappa's response
    """
    logger.info("listen_and_query_request", filename=audio.filename, mode=mode)

    try:
        # Read and transcribe audio
        audio_bytes = await audio.read()
        transcribed_text, transcription_confidence = await whisper_service.transcribe(
            audio_bytes,
            language=language
        )

        # Now run query with transcribed text
        search_results = kb.search_concepts(transcribed_text)
        sources = []
        response_text = None
        confidence = 0.5

        if search_results:
            sources.append("knowledge_base")
            confidence = max(confidence, 0.7)
            concept_info = []
            for concept in search_results[:3]:
                concept_info.append(f"{concept['name']} ({concept['category']}): {concept['definition']}")
            response_text = "Wissensbank-Treffer:\n" + "\n".join(concept_info)

        memory_summary = memory.get_memory_summary()
        if memory_summary and memory_summary.get("project_status"):
            sources.append("project_memory")
            if response_text:
                response_text += "\n\nProjekt-Status: " + str(memory_summary["project_status"].get("current_phase", "Unbekannt"))

        if not response_text:
            response_text = f"Keine Treffer für: {transcribed_text}"
            sources.append("fallback")
            confidence = 0.3

        # Log the combined operation
        audit_logger.log_query(
            text=transcribed_text,
            mode=mode,
            user=user,
            response=response_text,
            status="success"
        )

        return {
            "transcribed_text": transcribed_text,
            "transcription_confidence": transcription_confidence,
            "response": response_text,
            "response_confidence": confidence,
            "sources": sources,
            "mode": mode,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        logger.error("listen_and_query_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

# === SPEAK ENDPOINT (STUB for TTS) ===

@router.post("/speak")
async def speak(text: str = Query(..., min_length=1)):
    """Text-to-speech endpoint (stub)"""
    return {
        "status": "stub",
        "message": "TTS available in Phase 3 or via external API"
    }
