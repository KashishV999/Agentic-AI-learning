import sys

def get_file_contents(path: str, description: str) -> str:
    """Read a TEXT file and return its contents, or exit on error. Not for images."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {description} not found: {path}")
        sys.exit(1)
    except Exception as err:
        print(f"Error reading {description}: {path}")
        print(f"   {err}")
        sys.exit(1)
        