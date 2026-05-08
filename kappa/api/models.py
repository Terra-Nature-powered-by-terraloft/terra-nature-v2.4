from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, List, Any, Literal
from datetime import datetime

# === INPUT MODELS ===

class QueryRequest(BaseModel):
    """User query input to Kappa"""
    text: str = Field(..., min_length=1, max_length=5000, description="User input text")
    mode: Literal[
        "default", "cto", "mrv", "bank", "funding", "industrial", "ip", "communication", "professorale", "business"
    ] = Field(default="default", description="Expert mode for validation")
    user: str = Field(default="system", description="User identifier")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Wie viel MRV-relevante Energie wurde heute erfasst?",
                "mode": "default",
                "user": "founder"
            }
        }
    )

class ValidationRequest(BaseModel):
    """Request to validate statement against expert rules"""
    statement: str = Field(..., min_length=1, max_length=5000)
    modes: List[str] = Field(default=["all"], description="Which expert perspectives to check")
    user: str = Field(default="system")

class ListenRequest(BaseModel):
    """Audio input (stub for future Whisper integration)"""
    audio_base64: Optional[str] = Field(default=None, description="Base64 encoded audio")
    format: str = Field(default="wav", description="Audio format")

class MemorySaveRequest(BaseModel):
    """Save to project memory"""
    key: str = Field(..., min_length=1, max_length=100)
    value: Any = Field(...)
    category: Optional[str] = Field(default=None)
    user: str = Field(default="system")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

# === OUTPUT MODELS ===

class HealthResponse(BaseModel):
    """Health check response"""
    status: Literal["healthy", "degraded", "unhealthy"]
    timestamp: str
    version: str = "1.0.0"
    components: Dict[str, str] = Field(default_factory=dict)
    stats: Optional[Dict[str, Any]] = Field(default=None, description="System statistics")

class QueryResponse(BaseModel):
    """Response to user query"""
    response: str
    mode: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list, description="Where response came from")
    timestamp: str
    requires_approval: bool = False
    approval_level: Literal["approved", "conditional", "requires_review"] = "approved"

class ValidationResult(BaseModel):
    """Single expert validation result"""
    expert: str
    approved: bool
    confidence: float
    feedback: str
    suggestions: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list, description="Conditional requirements")

class ValidationResponse(BaseModel):
    """Response to validation request"""
    statement: str
    timestamp: str
    results: Dict[str, ValidationResult]
    overall_approved: bool
    approval_level: Literal["approved", "conditional", "requires_review"]
    user: str

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    code: str
    timestamp: str
    details: Optional[Dict[str, Any]] = None

class MemoryResponse(BaseModel):
    """Project memory data"""
    key: str
    value: Any
    category: Optional[str]
    timestamp: str
    user: str

class AuditLogEntry(BaseModel):
    """Single audit log entry - flexible schema for append-only audit trail"""
    timestamp: str
    event_type: str
    action: str
    user: str
    version: str = "1.0"
    status: Optional[str] = None
    # Additional fields that vary by event type
    data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="allow")
