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
from debug_utils import debug_log


# Arguments
class ChatCompletionArgs(BaseModel):
    name: str
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


async def chatCompletion(args: ChatCompletionArgs) -> Report:
    client = AsyncOpenAI(
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

        debug_log(f"[{args.name}] --- Iteration {iteration} ---")
        debug_log(f"[{args.name}] Calling LLM (model={args.model}, temperature={args.temperature})...")
        # Call LLM
        response = await client.responses.parse(
                model=args.model,
                input= messages,
                temperature=args.temperature,
                text_format=Report,
                tools=tools
        )


        # If the model successfully returned a Report,
        # we're done.
        if response.output_parsed is not None:
            debug_log(f"[{args.name}] Model returned final Report. Successfully Done.")
            return response.output_parsed

        # Collect function calls from the response output
        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        debug_log(f"[{args.name}] Model returned {len(tool_calls)} tool call(s).")

        if not tool_calls:
            debug_log(f"[{args.name}] ERROR: Model returned neither a Report nor a tool call.")
            raise RuntimeError(
                "Model returned neither a Report nor a tool call."
            )

        for tool_call in tool_calls:
            try:
                fn_name = tool_call.name
                args_json = json.loads(tool_call.arguments)

                if fn_name == "ReadFileTool":
                    debug_log(f"[{args.name}] ReadFileTool called")
                    print("READFILE TOOL CALLL !!!!!!!!")
                    validated_args = ReadFileTool(**args_json)

                    result = await asyncio.to_thread(
                            function_map["ReadFileTool"],
                            validated_args.file_path,
                            validated_args.start_line,
                            validated_args.end_line,
                    )
                    debug_log(f"[{args.name}] ReadFileTool result: {result}")

                elif fn_name == "RipGrepTool":
                    debug_log(f"[{args.name}] RipGrepTool called")

                    validated_args = RipGrepTool(**args_json)

                    result = await asyncio.to_thread(function_map["RipGrepTool"],
                        validated_args.search_pattern
                    )
                    debug_log(f"[{args.name}] RipGrepTool result: {result}")

                else:
                    debug_log(f"[{args.name}] Unknown tool requested: {fn_name}")
                    result = {
                        "error": f"Unknown tool: {fn_name}"
                    }

            except Exception as e:
                debug_log(f"[{args.name}] Tool call raised exception: {e}")
                result = {
                    "error": str(e)
                }
                 
            # 1. Record that the model made this call
            messages.append(tool_call.model_dump(exclude_none=True))

                # 2. Record the result of executing it
            messages.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": json.dumps(result),
            })
            
    debug_log(f"[{args.name}] Max iterations reached.")         
    raise RuntimeError("Max iterations reached")





