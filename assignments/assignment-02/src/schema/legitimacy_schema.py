from typing import List, Literal

from pydantic import BaseModel, Field


class WhoisSummary(BaseModel):
    domain: str = Field(..., description="The official company domain investigated for this posting.")
    registrant_organization: str = Field(
        ...,
        description="Registrant organization from WHOIS if available; otherwise explain whether the value was redacted or unavailable.",
    )
    registration_date: str = Field(
        ...,
        description="Domain registration date in ISO format if available, otherwise a clear explanation of what was available.",
    )
    expiration_date: str = Field(
        ...,
        description="Domain expiration date in ISO format if available, otherwise a clear explanation of what was available.",
    )
    registrar: str = Field(..., description="Registrar name if available, otherwise explain that it could not be confirmed.")
    country: str = Field(..., description="Country listed in WHOIS if available, otherwise explain that it could not be confirmed.")
    notes: str = Field(
        ...,
        description="Short note about redaction, lookup reliability, or why certain WHOIS fields may be missing.",
    )


class LegitimacySignal(BaseModel):
    signal_type: Literal["green_flag", "yellow_flag", "red_flag"] = Field(
        ...,
        description="Whether the finding is a positive signal, caution, or clear red flag.",
    )
    title: str = Field(..., description="Short label for the signal.")
    evidence: str = Field(..., description="Specific evidence supporting this signal.")
    why_it_matters: str = Field(..., description="Plain-language explanation of how this affects legitimacy.")
    source_urls: List[str] = Field(
        default_factory=list,
        description="URLs used as evidence for this signal. Use an empty list if the evidence came from the posting or WHOIS without a URL.",
    )


class LegitimacySchema(BaseModel):
    company_name: str = Field(..., description="Company name associated with the posting.")
    official_domain: str = Field(
        ...,
        description="Best verified official domain for the company. If not confirmed, say 'Unknown' and explain in the summary.",
    )
    overall_verdict: Literal["green", "yellow", "red"] = Field(
        ...,
        description="Overall legitimacy verdict for the posting.",
    )
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence in the overall verdict on a 0-100 scale.",
    )
    summary: str = Field(
        ...,
        description="A concise summary of the legitimacy assessment, including the main reasons for the verdict.",
    )
    recommendation: str = Field(
        ...,
        description="Direct plain-language recommendation to the candidate, including any caution about sharing personal information.",
    )
    whois_summary: WhoisSummary = Field(
        ...,
        description="Normalized WHOIS details for the investigated company domain.",
    )
    signals: List[LegitimacySignal] = Field(
        ...,
        description="Evidence-backed green and red flags identified during the investigation.",
    )
    user_safety_actions: List[str] = Field(
        ...,
        description="Specific safety actions the user should take next, especially if the verdict is yellow or red.",
    )
