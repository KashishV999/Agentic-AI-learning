import asyncio
import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from chat_completion import  chatCompletion, ChatCompletionArgs
from read_file_tool import read_file
from openai import OpenAI
from debug_utils import debug_log, set_debug
from git_diff_subprocess import get_staged_diff
# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



# Command line argument parsing

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, help='Output filename')
parser.add_argument('--file', type=str, help='Path to a specific file to review (defaults to staged git diff)')
parser.add_argument('--debug', action='store_true', help='Print detailed debug logs to stderr')
args = parser.parse_args()


# HTML store filename -- output
if args.output is None:
    args.output = "review-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".html"

filename= args.output

# debug flag
is_debug= args.debug
set_debug(is_debug)

file_to_review = args.file

if file_to_review:
    debug_log(f"[Main] --file provided: {file_to_review}. Reading file...")
    content = read_file(file_to_review)
    debug_log(f"[Main] {file_to_review} read successfully ({len(content)} chars).")
else:
    debug_log("[Main] No --file provided. Falling back to staged git diff...")
    content = get_staged_diff()
    debug_log(f"[Main] Staged diff retrieved ({len(content)} chars).")

if not content or not content.strip():
    debug_log("[Main] ERROR: content is empty. Nothing to review.")
    print("Error: No content to review.")
    sys.exit(1)



debug_log(f"[Main] Debug mode enabled: {is_debug}")
debug_log(f"[Main] Output filename: {filename}")








# Prompts
debug_log("[Main] Loading system prompts...")
security_system_prompt= read_file("SECURITY_AUDITOR_PROMPT.md")
architect_system_prompt= read_file("SENIOR_ARCHITECT_PROMPT.md")
judge_system_prompt= read_file("JUDGE_PROMPT.md")

# arguments for child assistants to call chat_completion 
args_security = ChatCompletionArgs(
        name="Security Auditor",
        model="google/gemini-3.5-flash",
        user_prompt=f"""<file> {content}</file>""",
        system_prompt=security_system_prompt,
        temperature=0.1,
        openrouter_key=OPENROUTER_API_KEY,
        tool_names=["ReadFileTool", "RipGrepTool"]
    )

args_architect = ChatCompletionArgs(
        name="Senior Architect",
        model="google/gemini-3.5-flash",
        user_prompt=f"""<file> {content}</file>""",
        system_prompt=architect_system_prompt,
        temperature=0.4,
        openrouter_key=OPENROUTER_API_KEY,
        tool_names=["ReadFileTool", "RipGrepTool"]
    )




def JudgeCompletion(output_security, output_architect, system_prompt):
    debug_log("[Lead Developer] Starting synthesis of security + architecture findings...")
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )
    
    debug_log("[Lead Developer] Calling LLM ")
    completion = client.chat.completions.create(
        model="anthropic/claude-sonnet-4.6",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },

            { 
                "role": "user",
                "content": f"<security_findings>{output_security}</security_findings><architectural_findings>{output_architect}</architectural_findings>"            
            },
        ]
    )
    html_content= completion.choices[0].message.content
    debug_log(f"[Lead Developer] Received HTML report")
    
    debug_log(f"[Lead Developer] Writing report to {filename}...")
    with open(filename, "w") as f:
        f.write(html_content)
    debug_log(f"[Lead Developer] Report written successfully to {filename}.")
    
    
    

async def main():
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")
        
       
       
    debug_log("[Main] Launching Security Auditor and Senior Architect reviews in parallel...")

    result_security, result_architect = await asyncio.gather(
        chatCompletion(args_security),
        chatCompletion(args_architect)
    )

    debug_log("[Main] Security Auditor review complete.")
    debug_log("[Main] Senior Architect review complete.")
    
    debug_log("[Main] Sending both reviews to Lead Developer (Judge) for synthesis...")
    html_file= JudgeCompletion(result_security, result_architect, judge_system_prompt )
    debug_log("[Main] Pipeline complete.")
    
    
    


if __name__ == "__main__":
    asyncio.run(main())
