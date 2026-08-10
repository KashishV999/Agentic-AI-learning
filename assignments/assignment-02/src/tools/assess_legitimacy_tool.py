from pathlib import Path

from agents import RunContextWrapper, function_tool

from helper.debug_logging import debug_extraction_summary, debug_tool_call, debug_tool_result
from helper.save_disk import save_disk
from schema.legitimacy_schema import LegitimacySchema


@function_tool
def assess_legitimacy_tool(ctx: RunContextWrapper, legitimacyData: LegitimacySchema) -> dict:
    """
    Record a structured legitimacy assessment and persist it to disk as JSON.
    """
    output_path: Path = ctx.context.output_path_json
    payload = legitimacyData.model_dump()
    debug_tool_call("assess_legitimacy_tool", output_path=str(output_path))
    debug_extraction_summary("Legitimacy analysis summary", payload)

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=legitimacyData.model_dump_json(indent=2),
    )
    debug_tool_result("assess_legitimacy_tool", status=result.get("status"), saved_to=result.get("path"))

    return {
        "status": "evaluation_recorded",
        "saved_to": result.get("path"),
        "legitimacy_assessment": legitimacyData.model_dump(),
    }
