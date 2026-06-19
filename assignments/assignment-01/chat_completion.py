## Generic Chat completion function (customize by passing the args)
## test- security auditor
import json
import openai
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from output_schema import Report # Output structured Response
from read_file_tool import read_file
from ripgrep_tool import ripgrep


# Arguments
class ChatCompletionArgs(BaseModel):
    model: str
    user_prompt: str
    system_prompt: str
    temperature: float
    openrouter_key: str
    tool_names: list[str]
    




# Pydantic model gives the LLM (or your code) a structured schema for the tool's inputs.
class ReadFileTool(BaseModel):
    """
    Read the contents of a file.
    Optionally reads only a specific line range. Large outputs
    are truncated to 1000 lines.
    """

    file_path: str = Field(..., description="Path to the file to read.")

    start_line: int | None = Field( None, description="Starting line number to read (inclusive).")

    end_line: int | None = Field(None, description="Ending line number to read (exclusive).")


class RipGrepTool(BaseModel):
    """
    Search for a pattern in all Python files under the current directory.
    Returns up to 30 matching results as a list of dictionaries.
    The text field of each result is truncated to 1000 lines if needed.
    """

    search_pattern: str = Field(..., description="Pattern to search for in Python files.")



# mapping of model to actual function
function_map= {
    "ReadFileTool": read_file,
    "RipGrepTool": ripgrep
}

# Maps a string name to a Pydantic class:
tool_schema_map = {
    "ReadFileTool": ReadFileTool,
    "RipGrepTool": RipGrepTool,
}


def chatCompletion(args: ChatCompletionArgs) -> Report:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key= args.openrouter_key
    )


    # Define tools list that are available to use using the Pydantic helper
    tools = [
        openai.pydantic_function_tool(
            tool_schema_map[name]
        )
        for name in args.tool_names
    ]


    # Variables
    max_iterations=10
    iteration=0

    messages= [
        { 
            "role": 'system', 
            "content": args.system_prompt
        },
        {
            "role": 'user',
            "content": args.user_prompt,
        },
    ]



    # Note: so now tool/s calling will happen so need to implement loop manually : there is nothing like 
    # openai.chat.completions.runTools in python its in nodejs sdk


    # As long as there are tool calls, keep processing until done
    while iteration < max_iterations:
        iteration+=1

        # Call LLM
        response = client.responses.parse(
                model=args.model,
                input= messages,
                temperature=args.temperature,
                text_format=Report,
                tools=tools
        )


        # If the model successfully returned a Report,
        # we're done.
        if response.output_parsed is not None:
            return response.output_parsed

        # Collect function calls from the response output
        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:
            raise RuntimeError(
                "Model returned neither a Report nor a tool call."
            )

        for tool_call in tool_calls:
            try:
                fn_name = tool_call.name
                args_json = json.loads(tool_call.arguments)

                if fn_name == "ReadFileTool":
                    validated_args = ReadFileTool(**args_json)

                    result = function_map["ReadFileTool"](
                        validated_args.file_path,
                        validated_args.start_line,
                        validated_args.end_line,
                    )

                elif fn_name == "RipGrepTool":
                    validated_args = RipGrepTool(**args_json)

                    result = function_map["RipGrepTool"](
                        validated_args.search_pattern
                    )

                else:
                    result = {
                        "error": f"Unknown tool: {fn_name}"
                    }

            except Exception as e:
                result = {
                    "error": str(e)
                }

            # Feed tool output back into the Responses API
            messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": json.dumps(result),
            })

    raise RuntimeError("Max iterations reached")





# Note about client.chat.completions.create vs client.responses.parse

# response = client.chat.completions.create
# response.choices        # list[Choice]
# choice = response.choices[0]
# message = response.choices[0].message     # the actual ChatCompletionMessage
# - message.tool_calls  -> list of tool calls
# tool_call -> id, name, arguments  
# -

# // client.chat.completions.create
# {
#   "choices": [
#     {
#       "message": {
#         "tool_calls": [
#           { "id": "...", "name": "...", "arguments": "..." }
#         ]
#       }
#     }
#   ]
# }

# client.responses.parse

## response.output          # list[...] 
## response.output_parsed   # text_format
# for item in response.output:   -> list iterate
#     if item.type == "function_call":
#         item.name           # e.g. "ReadFileTool"
#         item.arguments       # JSON string — json.loads() it
#         item.call_id          # use to match the result back
#         item.id    

        
# // client.responses.parse
# {
#   "output": [
#     {
#       "type": "function_call",
#       "name": "...",
#       "arguments": "...",
#       "call_id": "...",
#       "id": "..."
#     }
#   ],
#   "output_parsed": { }
# }
        
             
        
        
        













