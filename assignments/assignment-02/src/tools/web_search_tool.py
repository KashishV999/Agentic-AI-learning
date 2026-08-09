# Uses TavilyAPI : it accepts a query string and returns the search results.
# define the functionality of this tool : Use the Tavily SDK to do a search and fetch results 

import os
import sys
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv
from agents import function_tool




# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@function_tool
def web_search_tool(query: str):
    """Search the web using Tavily and return the top 3 relevant results."""
    if not TAVILY_API_KEY:
        print("Error: TAVILY_API_KEY not found")
        sys.exit(1)
    else:
        print("TAVILY__API_KEY found successfully!")
        
    tavily_client = TavilyClient(TAVILY_API_KEY)
    
    response = tavily_client.search(
    query=query,
    # start_date="2026-01-01",         # Returns results strictly AFTER this date
    max_results=3
    )

    return [
    {"title": r["title"], "url": r["url"], "content": r["content"]}
    for r in response["results"]
    ]


