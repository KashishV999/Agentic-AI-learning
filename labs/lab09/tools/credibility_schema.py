## The tool's schema is the credibility rubric. 

from enum import Enum
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    PEER_REVIEWED_JOURNAL = "peer_reviewed_journal"
    NEWS_ORGANIZATION = "news_organization"
    GOVERNMENT_AGENCY = "government_agency"
    NONPROFIT_ORGANIZATION = "nonprofit_organization"
    CORPORATE_BLOG = "corporate_blog"
    PERSONAL_BLOG = "personal_blog"
    SOCIAL_MEDIA = "social_media"
    WIKI = "wiki"
    UNKNOWN = "unknown"


class PublicationEditorialProcess(str, Enum):
    PEER_REVIEWED = "peer_reviewed"
    EDITOR_REVIEW = "editor_review"
    SELF_PUBLISHED = "self_published"
    UNKNOWN = "unknown"


class ContentSourceType(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    

class OverallCredibility(str, Enum):
    HIGH ="high"
    MEDIUM = "medium"
    LOW = "low"
    VERY_LOW = "very_low"

class Author(BaseModel):
    name: str = Field(..., description="Check the Author name. If unknown after investigation, write Unknown and explain what you checked")
    credentials: str = Field(..., description="What qualifications does the author have? If you couldn't find them, describe what you searched for")
    credibility_assessment: str = Field(..., description="Your assessment of author credibility. If unknown, explain how this affects your overall assessment")


class Publication(BaseModel):
    name: str = Field(..., description="Publication or website name. If not a recognized outlet, use the domain name")
    reputation: str = Field(..., description="What did your research reveal about this publication? If unknown, describe what you searched for")
    editorial_process: PublicationEditorialProcess = Field(..., description="The editorial process of the publication")


class ContentAnalysis(BaseModel):
    claims_supported_by_evidence: bool = Field(..., description="Are the main claims backed by data, citations, or primary sources?")
    sources_cited: bool = Field(..., description="Does the article cite its sources?")
    corroborated_by_other_sources: bool = Field(..., description="Did you find other credible sources reporting the same claims?")
    contradicted_by_other_sources: bool = Field(..., description="Did you find credible sources that contradict the claims?")
    primary_vs_secondary_sources: ContentSourceType = Field(..., description="Are the sources primary, secondary, or tertiary")
    funding_or_sponsorship: str = Field(..., description="Did you find evidence of who funds the publication or research?")
    date_published: str = Field(..., description="When was the content published? If unknown, explain what you searched for")

# Final Schema

class CredibilitySchema(BaseModel):
    source_url: str = Field(..., description="The URL of the source being evaluated")
    source_type: SourceType = Field(..., description="The type of source being evaluated")
    author: Author = Field(..., description="Information about the author of the source")
    publication: Publication = Field(..., description="Information about the publication or website of the source")
    content_analysis: ContentAnalysis = Field(..., description="Analysis of the content's accuracy, bias, and evidence")
    transparency_score: int = Field(..., description="1 to 5 rating of how transparent the source is about authorship, methods, and funding")
    overall_credibility: OverallCredibility = Field(..., description="Your overall assessment of the source's credibility")
    reasoning: str = Field(..., description="Explain your overall credibility rating, citing specific evidence from your research")