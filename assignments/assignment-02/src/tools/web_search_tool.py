# Uses TavilyAPI : it accepts a query string and returns the search results.
# define the functionality of this tool : Use the Tavily SDK to do a search and fetch results 

import os
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv
from agents import function_tool
from helper.debug_logging import debug_tool_call, debug_tool_result, debug_log




# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@function_tool
def web_search_tool(query: str):
    """Search the web using Tavily and return the top 3 relevant results."""
    debug_tool_call("web_search_tool", query=query)
    if not TAVILY_API_KEY:
        debug_log("web_search_tool failed: TAVILY_API_KEY not found")
        raise RuntimeError("TAVILY_API_KEY not found")
        
    tavily_client = TavilyClient(TAVILY_API_KEY)
    
    response = tavily_client.search(
    query=query,
    # start_date="2026-01-01",         # Returns results strictly AFTER this date
    max_results=3
    )

    results = [
    {"title": r["title"], "url": r["url"], "content": r["content"]}
    for r in response["results"]
    ]
    debug_tool_result("web_search_tool", result_count=len(results))
    return results
