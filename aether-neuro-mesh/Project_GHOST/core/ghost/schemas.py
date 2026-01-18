from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ShadowToken(BaseModel):
    """Structured representation of a token and its governance metadata."""

    token_id: str = Field(..., description="Shadow token (e.g., SSN_A31C88F9D2E1)")
    category: str = Field(..., description="PII Type (e.g., PERSON, EMAIL_ADDRESS, SSN)")
    original_value: Optional[str] = None

    # Deterministic tokenization metadata
    tenant_id: str = Field(default="TENANT_DEFAULT")
    epoch_id: int = Field(default=1)
    key_id: Optional[str] = None  # e.g., TENANT_DEFAULT:SSN:E123

    # Governance flags
    is_authorized: bool = True
    is_restricted: bool = False

    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class GhostContext(BaseModel):
    """Optional session container (not wired into the demo yet)."""
    session_id: str
    tokens: Dict[str, ShadowToken] = {}


class SentinelIncident(BaseModel):
    """Metadata for Jira tickets created or escalated by Project Sentinel."""

    token_id: str
    jira_key: Optional[str] = None
    jira_url: Optional[str] = None
    incident_type: str = "REHYDRATION_FAILURE"

    severity: str = "MEDIUM"
    occurrence_count: int = 1

    detected_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_escalated_at: Optional[str] = None

    resolved: bool = False
    resolution_type: Optional[str] = None

    metadata: Dict[str, Any] = {}
