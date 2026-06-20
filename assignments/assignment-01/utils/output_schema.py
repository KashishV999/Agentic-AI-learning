
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
 
 
 
 
 
#  findings=[
# 	Finding(
# 		path='vulnerable_app.py',
# 		line=5, 
# 		severity=<Severity.CRITICAL: 'critical'>, 
# 		category='Hardcoded Secret', 
# 		description="A hardcoded API key (starting with 'sk_live_') is defined directly in the source code. This can lead to credential exposure if the code is committed to a repository. Use environment variables or a secrets manager to load credentials securely."), 
# 	Finding(
# 		path='vulnerable_app.py', 
# 		line=11, 
# 		severity=<Severity.CRITICAL: 'critical'>, category='SQL Injection', 
# 		description='User-controlled inputs \'username\' and \'password\' are directly interpolated into a SQL query string, leading to SQL injection. Use parameterized queries instead, e.g., `cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))`.'), 
# 	]