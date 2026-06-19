
from ripgrepy import Ripgrepy

    # Search for a pattern in all Python files under the current directory.
    # Returns up to 20 matching results as a list of dictionaries.
    # The text field of each result is truncated to 1000 lines if needed.

def ripgrep(search_pattern : str) -> list[dict]:
    
    max_results=30
    truncated_value=1000

    # Each line is a JSON string
    rg = Ripgrepy(search_pattern, ".")   # 

    # results is a list of dicts, eg:  [{"path": "src/main.py","line_number": 23,"text": "def read_file():"}, {...}]
    results = rg.as_dict()[:max_results]    # slicing to max_results

    for result in results:
        lines= result["text"].splitlines()
        if len(lines) > truncated_value:
            result["text"]= "\n".join(lines[:1000])
        else:
            result["text"]="\n".join(lines)

    return results
        




