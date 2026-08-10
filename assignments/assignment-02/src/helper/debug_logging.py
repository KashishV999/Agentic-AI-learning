from __future__ import annotations

import os
import sys
from collections.abc import Mapping, Sequence
from typing import Any


def is_debug_enabled() -> bool:
    return os.getenv("LOG_LEVEL", "").strip().lower() == "debug"


def debug_log(message: str) -> None:
    if is_debug_enabled():
        print(f"[DEBUG] {message}", file=sys.stderr)


def _truncate(value: str, limit: int = 140) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3]}..."


def _safe_repr(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return f'"{_truncate(value)}"'
    if isinstance(value, Mapping):
        return f"<dict keys={list(value.keys())[:6]}>"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return f"<list len={len(value)}>"
    return f"<{type(value).__name__}>"


def debug_tool_call(tool_name: str, **kwargs: Any) -> None:
    args = ", ".join(f"{key}={_safe_repr(value)}" for key, value in kwargs.items())
    debug_log(f"Tool call: {tool_name}({args})")


def debug_tool_result(tool_name: str, **kwargs: Any) -> None:
    details = ", ".join(f"{key}={_safe_repr(value)}" for key, value in kwargs.items())
    debug_log(f"Tool result: {tool_name} -> {details}")


def debug_agent_start(agent_name: str, *, max_turns: int, output_path: str | None = None) -> None:
    parts = [f'Agent start: "{agent_name}"', f"max_turns={max_turns}"]
    if output_path:
        parts.append(f'output="{output_path}"')
    debug_log(", ".join(parts))


def debug_agent_end(agent_name: str, *, status: str) -> None:
    debug_log(f'Agent end: "{agent_name}", status={status}')


def debug_extraction_summary(kind: str, payload: Mapping[str, Any]) -> None:
    extracted_fields: list[str] = []
    for key, value in payload.items():
        if value in (None, "", [], {}, "Unknown"):
            continue
        extracted_fields.append(key)

    debug_log(
        f"{kind}: extracted_fields={_safe_repr(extracted_fields)}, "
        f"missing_or_unknown={max(0, len(payload) - len(extracted_fields))}"
    )
