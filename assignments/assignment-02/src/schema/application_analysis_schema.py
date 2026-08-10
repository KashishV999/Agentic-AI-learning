from typing import List, Literal

from pydantic import BaseModel, Field


class RequirementAssessment(BaseModel):
    requirement: str = Field(..., description="A concrete requirement or expectation from the posting.")
    status: Literal["Met", "Partially Met", "Gap"] = Field(
        ...,
        description="How well the candidate matches this requirement.",
    )
    evidence: str = Field(
        ...,
        description="Evidence from the resume and/or job posting supporting the status.",
    )
    positioning_advice: str = Field(
        ...,
        description="How the candidate should present this requirement in the application or interview.",
    )


class FitAssessment(BaseModel):
    fit_score: int = Field(..., ge=0, le=100, description="Overall fit score from 0-100.")
    recommendation_band: Literal["Strong fit", "Good fit", "Stretch", "Growth target"] = Field(
        ...,
        description="Encouraging fit band for the candidate.",
    )
    recommendation_text: str = Field(
        ...,
        description="Encouraging recommendation text aligned with the fit band.",
    )
    overall_narrative: str = Field(
        ...,
        description="A concise narrative assessment of why this role is or is not a strong near-term target.",
    )
    requirement_breakdown: List[RequirementAssessment] = Field(
        ...,
        description="Requirement-by-requirement comparison between the posting and the candidate.",
    )


class ResumeAdaptationItem(BaseModel):
    target_section: str = Field(
        ...,
        description="Resume section to change, such as Summary, Skills, Experience, or Projects.",
    )
    priority: Literal["High", "Medium", "Low"] = Field(..., description="How urgently the candidate should make this change.")
    current_signal: str = Field(
        ...,
        description="What the resume currently shows or misses related to this change.",
    )
    suggested_change: str = Field(
        ...,
        description="Specific wording or structural change to make for this exact posting.",
    )
    reason: str = Field(
        ...,
        description="Why this change matters for this role.",
    )


class CoverLetterPoint(BaseModel):
    theme: str = Field(..., description="Short label for the talking point.")
    talking_point: str = Field(
        ...,
        description="Specific content to include in the cover letter.",
    )
    reason: str = Field(
        ...,
        description="Why this point is persuasive for this company and role.",
    )


class InterviewQuestion(BaseModel):
    question: str = Field(..., description="Likely interview question.")
    why_this_is_likely: str = Field(..., description="Why the interviewer is likely to ask this question.")
    prep_guidance: str = Field(..., description="How the candidate should prepare or answer.")


class SkillReviewItem(BaseModel):
    skill: str = Field(..., description="Skill or topic the candidate should review.")
    why_it_matters: str = Field(..., description="Why this topic matters for the role.")
    review_plan: str = Field(..., description="Concrete guidance on what to review or practice.")


class CompanyResearchPoint(BaseModel):
    topic: str = Field(..., description="Company or team topic to research.")
    why_it_matters: str = Field(..., description="Why this topic will help during the application process.")
    suggested_angle: str = Field(..., description="How the candidate can use this topic in the interview or cover letter.")


class ExperienceTalkingPoint(BaseModel):
    theme: str = Field(..., description="Short label connecting the candidate's experience to the role.")
    supporting_evidence: str = Field(..., description="Resume evidence the candidate should mention.")
    why_it_resonates: str = Field(..., description="Why this talking point is relevant to the posting.")


class InterviewPrep(BaseModel):
    likely_questions: List[InterviewQuestion] = Field(
        ...,
        description="Likely interview questions based on this posting.",
    )
    skills_to_review: List[SkillReviewItem] = Field(
        ...,
        description="Skills or topics the candidate should refresh before interviewing.",
    )
    company_research_points: List[CompanyResearchPoint] = Field(
        ...,
        description="Company-specific research topics to review before applying or interviewing.",
    )
    experience_talking_points: List[ExperienceTalkingPoint] = Field(
        ...,
        description="Ways to connect the candidate's experience directly to this posting.",
    )


class ApplicationAnalysisSchema(BaseModel):
    fit_assessment: FitAssessment = Field(
        ...,
        description="Overall fit evaluation for the candidate against this posting.",
    )
    resume_adaptation: List[ResumeAdaptationItem] = Field(
        ...,
        description="Specific resume tailoring suggestions for this exact posting.",
    )
    cover_letter_guidance: List[CoverLetterPoint] = Field(
        ...,
        description="Specific cover letter talking points for this role and company.",
    )
    interview_prep: InterviewPrep = Field(
        ...,
        description="Interview preparation guidance grounded in the posting and the candidate's background.",
    )
