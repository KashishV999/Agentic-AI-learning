from pydantic import BaseModel, Field
from typing import List


class WorkExperience(BaseModel):
    role: str = Field(..., description="Job title/role held. If not present, write 'Unknown'.")
    company: str = Field(..., description="Name of the employer/company. If not present, write 'Unknown'.")
    duration: str = Field(..., description="Duration or date range of employment. If not present, write 'Unknown'.")
    key_responsibilities: List[str] = Field(..., description="Main duties or responsibilities held in this role. Each responsibility should be a separate item in the list. If none are found, return an empty list.")
    achievements: List[str] = Field(..., description="Notable achievements or measurable outcomes from this role. Each achievement should be a separate item in the list. If none are found, return an empty list.")


class Education(BaseModel):
    degree_name: str = Field(..., description="Name of the degree or qualification (e.g., 'B.Sc. Computer Science'). If not present, write 'Unknown'.")
    institution: str = Field(..., description="Name of the school/university/institution. If not present, write 'Unknown'.")
    relevant_coursework: List[str] = Field(..., description="Relevant courses taken as part of this degree. Each course should be a separate item in the list. If none are found, return an empty list.")


class Projects(BaseModel):
    name: str = Field(..., description="Name/title of the project. If not present, write 'Unknown'.")
    technology_used: List[str] = Field(..., description="Technologies, tools, frameworks, or languages used in the project. Each should be a separate item in the list. If none are found, return an empty list.")
    achievement: str = Field(..., description="Key outcome or result of the project. If not present, write 'Unknown'.")
    awards: str = Field(..., description="Any award or recognition received for this project. If not present, write 'Unknown'.")


class ResumeSchema(BaseModel):
    hard_skills_technologies: List[str] = Field(
        ...,
        description="Programming skills, tools, frameworks, platforms or technologies (e.g., Python, React, AWS, Docker). Each skill or technology should be a separate item in the list. If none are found, return an empty list."
    )
    soft_skills: List[str] = Field(
        ...,
        description="Soft skills such as communication, leadership, collaboration, problem-solving, etc. Each skill should be a separate item in the list. If none are found, return an empty list."
    )
    work_experience: List[WorkExperience] = Field(
        ...,
        description="List of all work experience entries found in the resume. If none are found, return an empty list."
    )
    education: List[Education] = Field(
        ...,
        description="List of all education entries found in the resume. If none are found, return an empty list."
    )
    certifications_and_training: List[str] = Field(
        ...,
        description="Certifications, licenses, or training programs completed. Each should be a separate item in the list. If none are found, return an empty list."
    )
    keywords_and_domain_expertise: List[str] = Field(
        ...,
        description="Domain-specific keywords or areas of expertise (e.g., 'Machine Learning', 'FinTech', 'Cloud Security'). Each should be a separate item in the list. If none are found, return an empty list."
    )
    projects: List[Projects] = Field(
        ...,
        description="List of all projects mentioned in the resume. If none are found, return an empty list."
    )
    accomplishments: List[str] = Field(
        ...,
        description="Notable accomplishments not already captured under work experience or projects (e.g., publications, competitions won). Each should be a separate item in the list. If none are found, return an empty list."
    )