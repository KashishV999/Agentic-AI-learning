
import os
import random
import sys
import subprocess
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# LLM chat completion import
from openai import OpenAI

from git_diff_subprocess import get_staged_diff


is_creative = "--creative" in sys.argv
is_auto_yes = "-y" in sys.argv
is_verbose = "--verbose" in sys.argv

# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found")
    sys.exit(1)
else:
    print("OPENROUTER_API_KEY found successfully!")


# staged diff
diff = get_staged_diff()
# print("Staged Diff:")
# print(diff)

# Function to print the header information
def printHeader():
    now = datetime.now()
    print ("--------------------------------------------------------------")
    print("git-cm: Developed by Kashish Verma - 151579232")
    print("Run Date: ", now.strftime("%Y-%m-%d %H:%M:%S"))
    print ("--------------------------------------------------------------")



def chatCompletion():
    # gets API Key from environment variable OPENROUTER_API_KEY

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )


    if is_creative:
        system_prompt = (
            "You are an LLM running in a CLI tool that writes semantic git commit messages. "
            "Use Gitmoji and write a commit message like a dramatic movie trailer narrator "
            "but keep it concise, short, hardly over 50 characters. "
            "Rules: "
            "- Strictly keep the language English and be concise. "
            "- Follow Conventional Commits format: <type>: <description>. "
            "- Use one type only: feat, fix, docs, refactor, test, chore, ci, style, perf. "
            "- No quotes, markdown, explanations, or extra text. "
            "- Output only the commit message. "
            "- Keep description concise and imperative. "
            "- Infer type from the diff."
        )

    else:
        system_prompt = (
            "You are an LLM running in a CLI tool that writes semantic git commit messages. "
            "You will be given a git diff. Return ONLY a commit message using "
            "Conventional Commits format: <type>: <description>. "
            "Rules: "
            "- No emojis, be professional and concise. "
            "- Use one type only: feat, fix, docs, refactor, test, chore, ci, style, perf. "
            "- Keep description concise and imperative "
            "(e.g., add login validation, not added). "
            "- Infer type from the diff. "
            "- No quotes, markdown, explanations, or extra text. "
            "- Output only the commit message."
        )


    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },

            { 
                "role": "user",
                "content": diff
            },
        ],
        temperature = 0.1 if not is_creative else 1.5
    )
    return completion.choices[0].message.content



def main():
    # Print the header information
    printHeader()
    # Get the commit message from the LLM
    commit_message = chatCompletion()
    print("Generated Commit Message:")
    print(commit_message)

    # asks the user if they want to use the commit message
    if is_auto_yes:
        user_input = "y"
    else:
        user_input = input("Do you want to use this commit message? (y/n): ")
        if user_input.lower() == "y":
            # Stage the commit message using git commit -m "message"
            try:
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                print("Commit message staged successfully!")
            except subprocess.CalledProcessError as e:
                print("Error staging commit message:", e)
            
        else:
            print("Commit message rejected.")

if __name__ == "__main__":
    main()
    