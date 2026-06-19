import asyncio
import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from chat_completion import  chatCompletion, ChatCompletionArgs
from read_file_tool import read_file
from openai import OpenAI
# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



# Command line argument parsing

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, help='Output filename')
args = parser.parse_args()


if args.output is None:
    args.output = "review-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".html"

filename= args.output


print("-----")
# print(args.output)
print(filename)
print("-------")



test_file= read_file("test_file.py")
# print(test_file)


# Prompts
security_system_prompt= read_file("SECURITY_AUDITOR_PROMPT.md")
architect_system_prompt= read_file("SENIOR_ARCHITECT_PROMPT.md")
judge_system_prompt= read_file("JUDGE_PROMPT.md")

# arguments for child assistants to call chat_completion 
args_security = ChatCompletionArgs(
        model="google/gemini-3.5-flash",
        user_prompt=f"""<file> {test_file}</file>""",
        system_prompt=security_system_prompt,
        temperature=0.1,
        openrouter_key=OPENROUTER_API_KEY,
        tool_names=["ReadFileTool", "RipGrepTool"]
    )

args_architect = ChatCompletionArgs(
        model="google/gemini-3.5-flash",
        user_prompt=f"""<file> {test_file}</file>""",
        system_prompt=architect_system_prompt,
        temperature=0.4,
        openrouter_key=OPENROUTER_API_KEY,
        tool_names=["ReadFileTool", "RipGrepTool"]
    )




def JudgeCompletion(output_security, output_architect, system_prompt):
   
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )
    
    
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
    with open(filename, "w") as f:
        f.write(html_content)
    
    
    
    



async def main():
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")
        
       
       
        
    # Structured outputs    
    result_security = await chatCompletion(args_security)
    result_architect= await chatCompletion(args_architect)
    
    
    html_file= JudgeCompletion(result_security, result_architect, judge_system_prompt )
    
    print(html_file)
    
    
    
    
    
    print("Generated Review:---------")
    print(result_security)
    
    print("-----------------")
    print(result_architect)



if __name__ == "__main__":
    asyncio.run(main())
