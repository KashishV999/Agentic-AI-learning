
import os
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from urllib.parse import urljoin
import requests
from typing import List, Dict

# LLM chat completion import
from openai import OpenAI

# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



# Function to print the header information
def printHeader():
    now = datetime.now()
    print ("--------------------------------------------------------------")
    print("pr-advice: Developed by Kashish Verma - 151579232")
    print("Run Date: ", now.strftime("%Y-%m-%d %H:%M:%S"))
    print ("--------------------------------------------------------------")











def main():
    # Print the header information
    printHeader()

    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")




if __name__ == "__main__":
    main()
    