
from enum import Enum
from pydantic import BaseModel, Field
 
 
class Severity(str, Enum):
    """Allowed severity levels for finding."""
    INFO = "info"
    WARN = "warn"
    CRITICAL = "critical"
 

class Finding(BaseModel):
    """
    Pydantic model for a single finding.
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
        description="Short category label for the issue,"
    )
    description: str = Field(
        ...,
        description=(
            "Specific, actionable explanation of the issue and, where "
            "relevant"
        )
    )
 


class Report(BaseModel):
    """
    Top-level structured output : a list of findings.
    Use this as the response_format/schema for the chat completion so the
    model returns a JSON array of findings (or an empty array if none).
    """
 
    findings: list[Finding] = Field(
        default_factory=list,
        description="All findings from this review. Empty list if none."
    )
 