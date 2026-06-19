
from enum import Enum
from pydantic import BaseModel, Field
 
 
class Severity(str, Enum):
    """Allowed severity levels for a Security Auditor finding."""
    INFO = "info"
    WARN = "warn"
    CRITICAL = "critical"
 

class SecurityAuditorFinding(BaseModel):
    """
    Pydantic model for a single Security Auditor finding.
    """
 
    path: str = Field(
        ...,
        description="Relative file path where the issue was found, e.g. 'api/users.py'."
    )
    line: int = Field(
        ...,
        description="1-indexed line number in the file where the issue occurs."
    )
    severity: Severity = Field(
        ...,
        description="Severity of the finding: 'info', 'warn', or 'critical'."
    )
    category: str = Field(
        ...,
        description="Short category label for the issue, e.g. 'security', 'secrets', 'injection'."
    )
    description: str = Field(
        ...,
        description=(
            "Specific, actionable explanation of the issue and, where "
            "relevant, what the fix should be."
        )
    )
 


class SecurityAuditorReport(BaseModel):
    """
    Top-level structured output for the Security Auditor: a list of findings.
    Use this as the response_format/schema for the chat completion so the
    model returns a JSON array of findings (or an empty array if none).
    """
 
    findings: list[SecurityAuditorFinding] = Field(
        default_factory=list,
        description="All security findings from this review. Empty list if none."
    )
 