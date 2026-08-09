def save_disk(filename: str, folder: str, content: str):
    """Write a file to disk."""
    try:
        path = f"{folder}/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Report saved to {path}")
        return {"status": "saved", "path": path}
    except Exception as e:
        print(f"Error saving report to {folder}/{filename}: {e}")
        return {"status": "error", "message": str(e)}