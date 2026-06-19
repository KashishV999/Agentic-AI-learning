
from ripgrepy import Ripgrepy


    # Search for a pattern in all Python files under the current directory.
    # Returns up to 20 matching results as a list of dictionaries.
    # The text field of each result is truncated to 1000 lines if needed.



def ripgrep(search_pattern: str) -> list[dict]:
    max_results = 30
    truncated_value = 1000

    rg = Ripgrepy(search_pattern, ".")
    raw_results = rg.json().run().as_dict

    results = []
    for item in raw_results:
        if item.get("type") != "match":
            continue
        data = item["data"]
        results.append({
            "path": data["path"]["text"],
            "line_number": data["line_number"],
            "text": data["lines"]["text"],
        })
        if len(results) >= max_results:
            break

    for result in results:
        lines = result["text"].splitlines()
        result["text"] = "\n".join(lines[:truncated_value]) if len(lines) > truncated_value else "\n".join(lines)

    return results




