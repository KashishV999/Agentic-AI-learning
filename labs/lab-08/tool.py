# define the functionality of this tool : Use the Tavily SDK to do a search and fetch results 

import os
import sys
from tavily import TavilyClient
from dotenv import load_dotenv, find_dotenv


# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def lookup_error(query: str):
    if not TAVILY_API_KEY:
        print("Error: TAVILY_API_KEY not found")
        sys.exit(1)
    else:
        print("TAVILY__API_KEY found successfully!")
        
    tavily_client = TavilyClient(TAVILY_API_KEY)
    
    response = tavily_client.search(
    query=query,
    start_date="2026-01-01",         # Returns results strictly AFTER this date
    max_results=3
    )


    return [
    {"title": r["title"], "url": r["url"], "content": r["content"]}
    for r in response["results"]
    ]


