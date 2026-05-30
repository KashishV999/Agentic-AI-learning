
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


def isValidPrUrl(url, pr_details) -> bool:
    if not url.startswith("https://github.com/"):
        print("Error: URL must be a valid GitHub PR URL")
        return False

    parts = url[len("https://github.com/"):].split("/")

    if len(parts) != 4 or parts[2] != "pull":
        print("Error: URL must be in format https://github.com/OWNER/REPO/pull/PR_NUMBER")
        return False
    

    pr_details["owner"] = parts[0]
    pr_details["repo"] = parts[1]
    pr_details["pr_number"] = parts[3]

    return True



def fetchComments(owner: str, repo: str, issue_num: int) -> List[Dict[str, str]]:    
    baseUrl= "https://api.github.com/repos/"
    relative = f"{owner}/{repo}/issues/{issue_num}/comments"
    comments_url = urljoin(baseUrl, relative)

    response = requests.get(comments_url, headers={
        "User-Agent": "AIP444-Lab-03",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    })

    if response.status_code !=200:
        raise Exception(f"GitHub API Error: {response.status_code}")
    
    # Extract only the fields we need
    return [
        {
            "username": item["user"]["login"],
            "body": item["body"],
            "date": item["updated_at"]
        }
        for item in response.json()
    ]


def constructDiffUrl(baseUrl):
    diff_url = baseUrl+".diff"
    response= requests.get(diff_url)
    data= response.json()
    # if data greated that 95000 charatcer truncate it and warn the user 
    if len(data) > 95000:
        print("Warning: Diff is too large, truncating to 95000 characters")
        data = data[:95000] + "... [Diff truncated]..."
    return data




def chatCompletion():
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )



    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {
                "role": "system",
                "content": "be polite",
            },

            { 
                "role": "user",
                "content": "helllo how are you"
            },
        ]
    )
    return completion.choices[0].message.content



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
    