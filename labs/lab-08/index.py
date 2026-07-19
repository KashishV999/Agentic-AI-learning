import os
import sys
import json
from tool import lookup_error
from openai import OpenAI
import openai
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv
from process_image import process_image

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

IMAGES_DIR = "images"


class LookupError(BaseModel):
    """Searches the web for technical documentation, coding errors, and other details to help with debugging the error"""
    query: str = Field(..., description="The search query to use based on the screenshot")


function_map = {
    "LookupError": lookup_error
}


# to get the content inside the system prompt file
def get_file_contents(path: str, description: str) -> str:
    """Read a TEXT file and return its contents, or exit on error. Not for images."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {description} not found: {path}")
        sys.exit(1)
    except Exception as err:
        print(f"Error reading {description}: {path}")
        print(f"   {err}")
        sys.exit(1)


def run_conversation(img_base64_url: str) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    system_prompt = get_file_contents('SYSTEM_PROMPT.md', 'System prompt file')

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Here's a screenshot of the error:"},
                {"type": "image_url", "image_url": {"url": img_base64_url}}
            ]
        }
    ]

    tools = [openai.pydantic_function_tool(LookupError)]

    max_iterations = 5
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        response = client.chat.completions.create(
            model="google/gemini-3-flash-preview",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name

            try:
                args_json = json.loads(tool_call.function.arguments)
                if fn_name == "LookupError":
                    validated_args = LookupError(**args_json)

                    print(f"Tool call: lookup_error(query=\"{validated_args.query}\")")
                    print(f"   Searching Tavily for: '{validated_args.query}'...")

                    fn = function_map[fn_name]
                    result = fn(validated_args.query)

                    print(f" Got {len(result)} result(s) from Tavily.")
                else:
                    result = {"error": "Unknown tool"}
            except Exception as e:
                result = {"error": str(e)}
                print(f"Tool call failed: {e}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Max Iterations reached"


def main():
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")

    filename = input(f"Enter the image filename (with extension) in '{IMAGES_DIR}/': ").strip()
    image_path = os.path.join(IMAGES_DIR, filename)

    if not os.path.isfile(image_path):
        print(f"❌ '{filename}' was not found in '{IMAGES_DIR}/'. Exiting.")
        sys.exit(1)

    b64 = process_image(image_path)
    img_url = f"data:image/jpeg;base64,{b64}"

    print(f"\n=== Running: {filename} ===")
    response = run_conversation(img_url)

    print(f"\n--- Result ---")
    print(response)


if __name__ == "__main__":
    main()