#  This tool doesn't do anything! Instead, we'll use it to force the agent to stop and
# organize its thinking into a structured evaluation before it produces its job json file
from pathlib import Path

from agents import function_tool, RunContextWrapper
from helper.save_disk import save_disk
from helper.debug_logging import debug_extraction_summary, debug_tool_call, debug_tool_result
from schema.job_schema import JobSchema

@function_tool
def assess_job_tool(ctx: RunContextWrapper, jobData: JobSchema) -> dict:
    """
    Record a structured Job Data and persist it to disk as JSON.
    """
    output_path: Path = ctx.context.output_path_json
    payload = jobData.model_dump()
    debug_tool_call("assess_job_tool", output_path=str(output_path))
    debug_extraction_summary("Job extraction summary", payload)

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=jobData.model_dump_json(indent=2)
    )
    debug_tool_result("assess_job_tool", status=result.get("status"), saved_to=result.get("path"))

    return {
        "status": "evaluation_recorded",
        "saved_to": result.get("path")
    }
    
