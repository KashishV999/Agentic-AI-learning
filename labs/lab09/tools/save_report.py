## This tool takes a filename and Markdown content string, and writes the file to disk.
from agents import function_tool

@function_tool
def save_report(filename: str, content: str):
    """Write a Markdown report to disk."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Report saved to {filename}")
    except Exception as e:
        print(f"Error saving report to {filename}: {e}")
        
        
    