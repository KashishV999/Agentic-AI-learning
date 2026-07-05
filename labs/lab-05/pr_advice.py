
import json
import os
import sys
from unittest import result
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from urllib.parse import urljoin
import openai
import requests
from typing import List, Dict
import re
from pydantic import BaseModel, Field
from github_file_object import GithubFile
from tools import read_github_files
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



# defines the schema for a tool the LLM can call:
class ReadGithubFiles(BaseModel):
    """Read files from GitHub repositories. Each file is specified by owner, repo, path, and ref (branch or commit). If the file is too long, it will be truncated to the first 1000 lines.
    Return the contents of the files as a list of strings, where each string is the content of one file, wrapped in <file name='filename'> tags."""
    files: List[GithubFile] = Field(..., description="List of files to read from GitHub.")




function_map= {
    "ReadGithubFiles": read_github_files
}

def run_conversation(url: str) -> str:
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

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
          "role": "user",
          "content": user_prompt
        }
    ]


    # Define tools list using the Pydantic helper
    tools = [
        openai.pydantic_function_tool(
            ReadGithubFiles)
    ]


    max_iterations = 5
    iteration = 0
    # As long as there are tool calls, keep processing until done
    while iteration < max_iterations:
        iteration+=1
        print("Loop")
        # Call LLM
        response = client.chat.completions.create(
            model="anthropic/claude-sonnet-4.6",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message
        
        if not message.tool_calls:
            print("No tool called")
            # No more tools needed, return final answer
            return message.content

        messages.append(message)

        # Process tool call(s) and continue
        for tool_call in message.tool_calls:
            print("Tool call !")
            # The function name matches the Pydantic Class Name
            fn_name = tool_call.function.name

            # Parse arguments using the Pydantic model to validate immediately
            try:
                args_json = json.loads(tool_call.function.arguments)
                if fn_name == "ReadGithubFiles":
                    validated_args = ReadGithubFiles(**args_json)
                    # print("Type of validated args")
                    # print(type(validated_args.files[0]))
                    # print("---------")

                    # we are uing githib file obejct to pass the arguments to the function

                    # result = function_map[fn_name](validated_args.files)
                    result = read_github_files(validated_args.files)
                else:
                    result = {"error": "Unknown tool"}
            except Exception as e:
                result = {"error": str(e)}

            # Feed result back to LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Max Iterations reached"






def main():
    # Print the header information
    printHeader()

    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")

    url : str = input("Please enter the PR URL: ")
    result = run_conversation(url)
    print("Generated Review:")
    print(result)


if __name__ == "__main__":
    main()
    