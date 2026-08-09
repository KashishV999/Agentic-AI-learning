from pydantic import BaseModel, Field
from typing import List, Literal


class Strength(BaseModel):
    skill_or_qualification: str = Field(..., description="A specific skill, technology, or qualification the candidate has that is also commonly requested across the analyzed postings.")
    evidence: str = Field(..., description="Where this appears in the resume (e.g. 'Listed in hard_skills_technologies', 'Demonstrated in the Acme Corp role').")


class Gap(BaseModel):
    skill_or_qualification: str = Field(..., description="A specific skill, technology, or qualification that appears frequently in postings but is missing or underrepresented in the resume.")
    severity: Literal["Missing entirely", "Underrepresented"] = Field(
        ...,
        description="'Missing entirely' if there is no evidence of this in the resume at all. 'Underrepresented' if the resume shows related experience but doesn't clearly state this specific skill/qualification."
    )


class UniqueValue(BaseModel):
    skill_or_qualification: str = Field(..., description="A specific skill, experience, or qualification the candidate has that is NOT commonly requested across the postings, but could differentiate them as a candidate.")
    why_it_differentiates: str = Field(..., description="A brief, specific explanation of why this could be a differentiator (e.g. 'Few postings mention accessibility experience, but it is increasingly valued in frontend roles').")


class ActionItem(BaseModel):
    title: str = Field(..., description="A short, specific, actionable title for this recommendation. Must name the exact skill, certification, or action — never a vague action like 'Learn AWS'.")
    description: str = Field(
        ...,
        description=(
            "A specific, actionable description of what to do, including concrete details where relevant "
            "(e.g. exact path, estimated time/cost, specific project idea). "
            "Must be specific enough to act on  — e.g. 'Get the AWS Cloud Practitioner certification or make this project "
            ", not 'Learn  just say AWS'."
        )
    )
    related_gap_or_skill: str = Field(..., description="The specific skill or gap (from the gaps list) this action item addresses.")
    estimated_effort: str = Field(..., description="A concrete estimate of time/effort required (e.g. '~20 hours', '2-3 weeks').")
    sources: List[str] = Field(
        default_factory=list,
        description="URLs used to inform this recommendation (e.g. a certification page, tutorial, or course found via web search). If no web search was needed for this item, return an empty list."
    )


class TriageLevel(BaseModel):
    quick_wins: List[ActionItem] = Field(
        ...,
        description="Wording or framing changes to the resume — e.g. the candidate has the skill but didn't list it, or used different terminology than the postings use. No new skill acquisition required. If none identified, return an empty list."
    )
    short_term: List[ActionItem] = Field(
        ...,
        description="Actions addressable in days to weeks — e.g. completing a tutorial, building a small project, getting a free certification. If none identified, return an empty list."
    )
    medium_term: List[ActionItem] = Field(
        ...,
        description="Actions requiring weeks to months of effort — e.g. learning a new framework, contributing to open source, building a portfolio project. If none identified, return an empty list."
    )
    long_term: List[ActionItem] = Field(
        ...,
        description="Actions requiring significant time or structural change — e.g. getting a degree, accumulating years of experience in a new area. If none identified, return an empty list."
    )


class GapAnalysisSchema(BaseModel):
    """Structured gap analysis comparing a candidate's resume against a set of analyzed job postings."""

    strengths: List[Strength] = Field(
        ...,
        description="Skills and qualifications the candidate has that are commonly requested across the analyzed postings. If none found, return an empty list."
    )
    gaps: List[Gap] = Field(
        ...,
        description="Skills and qualifications that appear frequently in postings but are missing or underrepresented in the resume. If none found, return an empty list."
    )
    unique_value: List[UniqueValue] = Field(
        ...,
        description="Things the candidate brings that aren't commonly listed across postings but could differentiate them as a candidate. If none found, return an empty list."
    )
    action_plan: TriageLevel = Field(
        ...,
        description="Specific, actionable recommendations to close identified gaps, triaged into quick win / short-term / medium-term / long-term based on effort required."
    )
    summary: str = Field(
        ...,
        description="A short (3-5 sentence) narrative summary of the candidate's overall competitiveness against this job market, written directly to the candidate."
    )