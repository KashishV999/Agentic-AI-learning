## Use the Jina Reader API to fetch a URL and return its content as Markdown.

import requests
from agents import function_tool


@function_tool
def read_url(url: str) -> str:
    """Use the Jina Reader API to fetch a URL and return its content as Markdown."""
    try:
        response = requests.get(f"https://r.jina.ai/{url}", timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"
    # Truncate to avoid blowing up the context window
    return response.text[:60000]


def main():
    url = input("Enter a URL to read: ")
    content = read_url(url)
    print(content)
    
if __name__ == "__main__":
    main()


