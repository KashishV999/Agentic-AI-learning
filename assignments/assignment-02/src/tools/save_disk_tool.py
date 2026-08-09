# tools/save_disk_tool.py
from pathlib import Path

from agents import function_tool, RunContextWrapper
from helper.save_disk import save_disk


@function_tool
def save_disk_tool(ctx: RunContextWrapper, content: str) -> dict:
    """
    Write a Markdown report to disk, using the report path provided for this run.
    """
    output_path: Path = ctx.context.output_path_md # md file path

    result = save_disk(
        filename=output_path.name,
        folder=str(output_path.parent),
        content=content
    )

    return {
        "status": "report_saved",
        "saved_to": result.get("path")
    }