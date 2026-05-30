
import os
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from urllib.parse import urljoin
import requests
from typing import List, Dict
import re

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


# function to validate the PR URL and extract owner, repo, and pr_number
def isValidPrUrl(url: str, pr_details: dict[str, str | None]) -> bool:
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


# function to construct the diff URL and fetch the diff content
def constructDiffUrl(baseUrl: str) -> str:
    diff_url = baseUrl+".diff"
    response= requests.get(diff_url)
    data= response.text
    # if data greated that 95000 charatcer truncate it and warn the user 
    if len(data) > 95000:
        print("Warning: Diff is too large, truncating to 95000 characters")
        data = data[:95000] + "... [Diff truncated]..."
    return data


# function to fetch comments from the PR thread using GitHub API
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



# Function to read file contents with error handling
def get_file_contents(path: str, description: str) -> str:
    """Read a file and return its contents, or exit on error."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: {description} not found: {path}")
        sys.exit(1)
    except Exception as err:
        print(f"❌ Error reading {description}: {path}")
        print(f"   {err}")
        sys.exit(1)



# Function to get the commit message from the LLM
def chatCompletion(url: str) -> str:
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )

    # PR Details dictionary to store owner, repo, and pr_number
    details: dict[str, str | None] = {
        "owner": None,
        "repo": None,
        "pr_number": None
    }

    isValidUrl = isValidPrUrl(url, details)
    if not isValidUrl:
        print("Error: Invalid PR URL")
        sys.exit(1)

    else:
        diff= constructDiffUrl(url)
        comments= fetchComments(details["owner"], details["repo"], details["pr_number"])

        # DEBUGGING PRINTS
        # print("Owner: ", details["owner"])
        # print("Repo: ", details["repo"])
        # print("PR Number: ", details["pr_number"])
        # print("Valid PR URL")
        # print("---------------------------------------------------")

        # for comment in comments:
        #     print("Username: ", comment["username"])
        #     print("Comment: ", comment["body"])
        #     print("Date: ", comment["date"])
        #     print("---------------------------------------------------")

        # print("Diff: ", diff)

    system_prompt = get_file_contents('SYSTEM_PROMPT.md', 'System prompt file')
    user_prompt = f"""
        <pr_diff>
        ```diff
        {diff}
        ```
        </pr_diff>
        <thread>
        {comments}
        </thread>
    """


    completion = client.chat.completions.create(
        model="anthropic/claude-3-haiku",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },

            { 
                "role": "user",
                "content": user_prompt
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

    url : str = input("Please enter the PR URL: ")
    commit_message = chatCompletion(url)
    print("Generated Commit Message:")
    print(commit_message)


if __name__ == "__main__":
    main()
    