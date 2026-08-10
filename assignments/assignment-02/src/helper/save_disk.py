from helper.debug_logging import debug_log


def save_disk(filename: str, folder: str, content: str):
    """Write a file to disk."""
    try:
        path = f"{folder}/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        debug_log(f'File saved: "{path}", chars={len(content)}')
        print(f"Report saved to {path}")
        return {"status": "saved", "path": path}
    except Exception as e:
        debug_log(f'File save failed: "{folder}/{filename}", error="{e}"')
        print(f"Error saving report to {folder}/{filename}: {e}")
        return {"status": "error", "message": str(e)}
