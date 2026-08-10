# tools/save_disk_tool.py
from pathlib import Path

from agents import function_tool, RunContextWrapper
from helper.debug_logging import debug_tool_call, debug_tool_result
from helper.save_disk import save_disk


@function_tool
def save_disk_tool(ctx: RunContextWrapper, content: str) -> dict:
    """
    Write a Markdown report to disk, using the report path provided for this run.
    """
    output_path: Path = ctx.context.output_path_md # md file path
    debug_tool_call("save_disk_tool", output_path=str(output_path), content_chars=len(content))

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=content
    )
    debug_tool_result("save_disk_tool", status=result.get("status"), saved_to=result.get("path"))

    return {
        "status": "report_saved",
        "saved_to": result.get("path")
    }
