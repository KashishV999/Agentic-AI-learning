#  This tool doesn't do anything! Instead, we'll use it to force the agent to stop and
# organize its thinking into a structured evaluation before it produces its final report.

# By making this a tool with a detailed schema, we force the agent to fill out every field, 
# which prevents it from skipping steps or making up its assessment.

## By returning the analysis data back to be included in context as a tool result,
# the agent can reference its own structured evaluation when writing the final report.

from .credibility_schema import CredibilitySchema
from agents import function_tool


@function_tool
def assess_credibility(evaluation: CredibilitySchema) -> dict:
    """
    Record a structured credibility assessment for a source.

    Use this tool to organize your evaluation BEFORE writing your final report.
    You must fill out every field based on your research
    """
    return {
        "status": "evaluation_recorded",
        "evaluation": evaluation.model_dump()
    }