
import os
import random
import sys
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

# LLM chat completion import
from openai import OpenAI

from git_diff_subprocess import get_staged_diff


is_creative = "--creative" in sys.argv

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
        system_prompt= "You are an LLM running in a CLI tool that writes semantic git commit messages. " \
        "Use Gitmoji and write a commit message like a dramatic movie trailer narrator but keep it concise short hardly over 50 characters. " \
        "Rules:"
        " - Strictly keep the language English and be concise do not overexplain"
        " - Follow Conventional Commits format: <type>: <description>. " \
        "- Use one type only: feat, fix, docs, refactor, test, chore, ci, style, perf. " \
        "- No quotes, markdown, explanations, or extra text"
        " - Output only the commit message"
        "- Keep description concise and imperative . Infer type from the diff. Output only the commit message with appropriate Gitmoji." \

    else:
        system_prompt= "You are an LLM running in a CLI tool that writes semantic git commit messages."
        "You will be given a git diff. Return ONLY a commit message using Conventional Commits format:"
        "<type>: <description>"
        "Rules:"
        " - Use one type only: feat, fix, docs, refactor, test, chore, ci, style, perf"
        " - Keep description concise and imperative (e.g., add login validation, not added)"
        " - Infer type from the diff"
        " - No quotes, markdown, explanations, or extra text"
        " - Output only the commit message"


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




if __name__ == "__main__":
    main()
    