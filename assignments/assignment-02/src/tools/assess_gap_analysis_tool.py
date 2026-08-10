#  This tool doesn't do anything! Instead, we'll use it to force the agent to stop and
# organize its thinking into a structured evaluation before it produces its job json file
from pathlib import Path

from agents import function_tool, RunContextWrapper
from helper.debug_logging import debug_extraction_summary, debug_tool_call, debug_tool_result
from helper.save_disk import save_disk
from schema.gap_analysis_schema import GapAnalysisSchema

@function_tool
def assess_gap_analysis_tool(ctx: RunContextWrapper, gapAnalysis: GapAnalysisSchema) -> dict:
    """
    Record a structured gap analysis Data and persist it to disk as JSON.
    """
    output_path: Path = ctx.context.output_path_json
    payload = gapAnalysis.model_dump()
    debug_tool_call("assess_gap_analysis_tool", output_path=str(output_path))
    debug_extraction_summary("Gap analysis summary", payload)

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=gapAnalysis.model_dump_json(indent=2)
    )
    debug_tool_result("assess_gap_analysis_tool", status=result.get("status"), saved_to=result.get("path"))

    return {
        "status": "evaluation_recorded",
        "saved_to": result.get("path"), 
        "market_analysis": gapAnalysis.model_dump()
    }
    
