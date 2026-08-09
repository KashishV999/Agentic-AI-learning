from pydantic import BaseModel, Field
from typing import List


class SkillFrequency(BaseModel):
    """A skill/technology and how often it appeared across analyzed postings."""
    skill: str = Field(..., description="Name of the skill or technology (e.g. 'Python', 'AWS', 'React').")
    posting_count: int = Field(..., description="Number of postings (out of the total analyzed) that required or mentioned this skill.")


class SalaryInsight(BaseModel):
    """Salary observations aggregated across postings that disclosed compensation."""
    typical_range: str = Field(
        ...,
        description="The typical or most common salary range observed across postings that disclosed one (e.g. '$90,000 - $120,000 USD'). If fewer than 2 postings disclosed salary, write 'Insufficient data'."
    )
    observations: List[str] = Field(
        ...,
        description="Notable patterns in compensation, e.g. differences by seniority, location, or role type. Each observation should be a separate item. If none observed, return an empty list."
    )


class ExperienceEducationInsight(BaseModel):
    """Aggregated view of seniority and education requirements across postings."""
    typical_experience_level: str = Field(
        ...,
        description="The most common seniority level or years-of-experience range across postings (e.g. 'Mostly Mid-level, 3-5 years'). If postings vary too widely to identify a pattern, write 'Highly varied' and briefly describe the spread."
    )
    typical_education_requirement: str = Field(
        ...,
        description="The most common minimum education requirement across postings (e.g. 'Bachelor's degree in Computer Science or related field'). If not consistently specified, write 'Not consistently specified'."
    )


class RolePatternInsight(BaseModel):
    """Common responsibilities and structural patterns across the analyzed roles."""
    common_responsibilities: List[str] = Field(
        ...,
        description="Responsibilities that recur across multiple postings, each as a separate item. If none recur, return an empty list."
    )
    role_pattern_notes: List[str] = Field(
        ...,
        description="Observations about how roles are structured or framed across postings, e.g. 'most postings combine backend and DevOps duties'. Each should be a separate item. If none observed, return an empty list."
    )


class IndustryCultureInsight(BaseModel):
    """Aggregated industry and company culture expectations across postings."""
    common_industries: List[str] = Field(
        ...,
        description="Industries or sectors represented across the analyzed companies, each as a separate item. If none identified, return an empty list."
    )
    culture_expectations: List[str] = Field(
        ...,
        description="Recurring culture-related expectations or signals across postings/companies, e.g. 'remote-first is common', 'fast-paced startup environment expected'. Each should be a separate item. If none observed, return an empty list."
    )


class MarketSchema(BaseModel):
    """Structured representation of a market analysis aggregated across job postings."""

    total_postings_analyzed: int = Field(
        ...,
        description="The total number of job postings included in this analysis."
    )

    most_common_skills: List[SkillFrequency] = Field(
        ...,
        description="The most commonly required skills and technologies across all analyzed postings, ranked by frequency. If none found, return an empty list."
    )

    experience_and_education: ExperienceEducationInsight = Field(
        ...,
        description="Aggregated patterns in typical experience level and education requirements across postings."
    )

    salary_insights: SalaryInsight = Field(
        ...,
        description="Aggregated salary/compensation patterns across postings that disclosed a range."
    )

    role_patterns: RolePatternInsight = Field(
        ...,
        description="Common responsibilities and structural patterns observed across the analyzed roles."
    )

    industry_and_culture: IndustryCultureInsight = Field(
        ...,
        description="Aggregated industry representation and company culture expectations across postings."
    )

    notable_trends: List[str] = Field(
        ...,
        description="Any other notable trends or observations that don't fit the categories above — e.g. emerging technologies appearing across postings, shifts in remote-work expectations, unusual hiring patterns. Each should be a separate item. If none observed, return an empty list."
    )

    summary: str = Field(
        ...,
        description="A short (3-5 sentence) narrative summary of the overall market analysis, written for a job applicant audience."
    )