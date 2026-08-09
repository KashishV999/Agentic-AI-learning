# TODO: Make the description of date better
from pydantic import BaseModel, Field
from typing import List


class CompanyInfo(BaseModel):
    """Structured company research to support a job applicant."""
    company_name: str = Field(..., description="The official name of the company")
    size: str = Field(..., description="Approximate company size, e.g. number of employees or a range. If not found, write Unknown and note what was checked")
    industry_info: str = Field(..., description="The industry or sector the company operates in, and a brief note on what the company does")
    recent_news: str = Field(..., description="Recent news or developments about the company, e.g. layoffs, expansions, funding rounds, leadership changes, product launches. If no recent news is found, write Unknown and note what was checked")
    company_culture: str = Field(..., description="Signals about company culture drawn from sources like employee reviews (e.g. Glassdoor), blog posts, or social media — e.g. work-life balance, management style, remote flexibility. If not found, write Unknown and note what was checked")
    any_related_information: str = Field(..., description="Any other context that would help a job applicant evaluate or prepare for this company, e.g. interview process insights, notable competitors, growth trajectory, or red flags. If nothing additional is found, write Unknown")



class JobSchema(BaseModel):
    """Structured representation of a job posting."""
    job_title: str = Field(..., description="The exact job title as listed in the posting, if not present then write Unknown and explain what you checked")
    company_info: CompanyInfo= Field(..., description="The information of the company")
    location: str = Field(..., description="Job location, e.g. city/remote/hybrid if not present then write Unknown and explain what you checked")
    posting_age: str = Field(
        ...,
    description=(
        "How long ago the job was posted, expressed in days (e.g. '4 days'). "
        "Calculate this using today's date provided in the system prompt. If the posting states an explicit date"
        "calculate the difference between that date and today's date. "
        "If the posting states a relative date (e.g. 'Posted 3 days ago'), treat that phrase "
        "as your best available estimate rather than recalculating it "
        "If no date information is present in the posting at all, set this to 'Unknown'."
        )
    )
    required_skills_technologies: List[str] = Field(
    ...,
    description="Must-have technical skills, tools, or technologies explicitly required. Each skill or technology should be a separate item in the list. If none are found, return an empty list."
    )
    nice_to_have_skills: List[str] = Field(
        ...,
        description="Preferred skills or qualifications. Each item should be a separate entry in the list. If none are mentioned, return an empty list."
    )
    experience_level: str = Field(..., description="Seniority level, e.g. Entry, Mid, Senior, Intern or how many years of experience required")
    education: str = Field(..., description="Minimum education requirement, if specified if not present then write Unknown and explain what you checked")
    key_responsibilities: str = Field(..., description="Main duties/responsibilities listed in the posting, listed as a comma-separated or semicolon-separated string")
    salary_range: str = Field(..., description="Salary or compensation range, if disclosed otherwise set to Unknown")