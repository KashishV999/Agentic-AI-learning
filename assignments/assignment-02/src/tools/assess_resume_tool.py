#  This tool doesn't do anything! Instead, we'll use it to force the agent to stop and
# organize its thinking into a structured evaluation before it produces its job json file
from pathlib import Path

from schema.resume_schema import ResumeSchema
from agents import function_tool, RunContextWrapper
from helper.save_disk import save_disk

@function_tool
def assess_resume_tool(ctx: RunContextWrapper, resumeData: ResumeSchema) -> dict:
    """
    Record a structured Resume analysis Data and persist it to disk as JSON.
    """
    output_path: Path = ctx.context.output_path_json

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=resumeData.model_dump_json(indent=2)
    )

    return {
        "status": "evaluation_recorded",
        "saved_to": result.get("path"), 
        "resume_analysis": resumeData.model_dump()
    }
    