from pathlib import Path

from agents import RunContextWrapper, function_tool

from helper.debug_logging import debug_extraction_summary, debug_tool_call, debug_tool_result
from helper.save_disk import save_disk
from schema.application_analysis_schema import ApplicationAnalysisSchema


@function_tool
def assess_application_tool(ctx: RunContextWrapper, applicationAnalysis: ApplicationAnalysisSchema) -> dict:
    """
    Record a structured application analysis and persist it to disk as JSON.
    """
    output_path: Path = ctx.context.output_path_json
    payload = applicationAnalysis.model_dump()
    debug_tool_call("assess_application_tool", output_path=str(output_path))
    debug_extraction_summary("Application analysis summary", payload)

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=applicationAnalysis.model_dump_json(indent=2),
    )
    debug_tool_result("assess_application_tool", status=result.get("status"), saved_to=result.get("path"))

    return {
        "status": "evaluation_recorded",
        "saved_to": result.get("path"),
        "application_analysis": applicationAnalysis.model_dump(),
    }
