import sys

# Read a text file and return its contents.
# Can return a specific line range.
# Large outputs are truncated to 1000 lines.
# Exits with an error if the file cannot be read.

def read_file(
    file_path: str,
    start_line: int | None = None,
    end_line: int | None = None
) -> str:
    truncate_value = 1000
    if start_line is not None and start_line < 0:
        raise ValueError("start_line must be non-negative")
    if end_line is not None and end_line < 0:
        raise ValueError("end_line must be non-negative")
    if (
        start_line is not None
        and end_line is not None
        and start_line > end_line
    ):
        raise ValueError("start_line cannot be greater than end_line")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} not found")
    except Exception as err:
        raise RuntimeError(f"Error reading {file_path}: {err}")

    if start_line is None and end_line is None:
        final_lines = lines
    else:
        if start_line is None:
            start_line = 0
        if end_line is None:
            end_line = len(lines)
        final_lines = lines[start_line:end_line]

    if len(final_lines) > truncate_value:
        return (
            "\n".join(final_lines[:truncate_value])
            + f"\n... [File truncated: showing {truncate_value} "
            f"of {len(final_lines)} lines]"
        )
    return "\n".join(final_lines)