"""
Phase 1: Job Posting Extraction + Market Analysis Pipeline.

This script runs two sequential stages:
1. Extraction : converts each raw job posting PDF into a structured JSON file
   (skips PDFs that have already been processed).
2. Market analysis : reads all extracted job JSONs and produces an aggregated
   market analysis, saved as both structured JSON and a Markdown report.
   
Reference Context pass: https://openai.github.io/openai-agents-python/context/#what-runcontextwrapper-exposes
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from pathlib import Path

from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
from agents import (
    Agent,
    Model,
    ModelProvider,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    set_tracing_export_api_key,
)

from helper import get_file_contents, pdf_extraction
from helper.debug_logging import debug_agent_end, debug_agent_start, debug_log
from config import PROMPTS_FOLDER, RAW_PDF_JOB_FOLDER, JOBS_JSON_FOLDER, ANALYSIS_FOLDER, REPORTS_FOLDER
from tools import web_search_tool, assess_job_tool, assess_market_tool, save_disk_tool


# --- Environment & model provider setup ---

load_dotenv(find_dotenv())  # locate .env by searching up the directory tree
API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "anthropic/claude-haiku-4.5"

if not API_KEY:
    raise ValueError("Please set OPENROUTER_API_KEY via env var or code.")

# This uses a custom provider (OpenRouter) for calls to Runner.run().
# Tracing is a separate system from inference — it uploads run logs to
# platform.openai.com, so it needs a real OpenAI key even though model
# calls themselves are routed through OpenRouter, not OpenAI.
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_export_api_key(os.getenv("OPENAI_TRACING_KEY"))


class CustomModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)


CUSTOM_MODEL_PROVIDER = CustomModelProvider()


# --- System prompts ---

system_prompt_job = get_file_contents(
    PROMPTS_FOLDER / "JOB-ANALYSIS-PROMPT.md", "System prompt file"
)
system_prompt_analysis = get_file_contents(
    PROMPTS_FOLDER / "JOB-MARKET-ANALYSIS-PROMPT.md", "System prompt file for market analysis"
)



# RunContextWrapper
# Contexts are not passed to the LLM. 
# They're a way to pass dependencies and data to code you implement, like tool functions, callbacks, hooks, etc.
# This is just the name of class holding the data, it can be named anything
@dataclass
class PathContext:
    """Carries output file locations into a run, so tools never have to
    guess or be told a path by the LLM — they read it straight from here.
    """
    output_path_json: Path            # where assess_job_tool / assess_market_tool save JSON
    output_path_md: Path = None       # where save_disk_tool saves the Markdown report



# (Part 1) - Extraction : converts each raw job posting PDF into a structured JSON file
   

async def extract_job_posting(pdf_path: Path, agent: Agent) -> None:
    """Extract one job posting PDF into structured JSON.
    Skips the PDF if its output JSON already exists.
    """
    output_path_json = JOBS_JSON_FOLDER / f"{pdf_path.stem}.json"

    if output_path_json.exists():
        debug_log(f'Skip extraction: "{pdf_path}" already processed -> "{output_path_json}"')
        print(f"Skipping {pdf_path.name} — already processed")
        return

    job_text = pdf_extraction(str(pdf_path))
    ctx = PathContext(output_path_json=output_path_json)
    debug_agent_start(agent.name, max_turns=10, output_path=str(output_path_json))

    await Runner.run(
        agent,
        f"Analyze the job description: {job_text}",
        max_turns=10,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    print(f"{pdf_path.name} -> {output_path_json.name}")


async def run_extraction_phase(agent: Agent) -> None:
    """Extract every raw job posting PDF into JSON (reruns
    only process PDFs that haven't been extracted yet).
    """
    pdf_files = sorted(RAW_PDF_JOB_FOLDER.glob("*.pdf"))
    if not pdf_files:
        debug_log(f'No PDFs found for extraction in "{RAW_PDF_JOB_FOLDER}"')
        print(f"No PDFs found in {RAW_PDF_JOB_FOLDER}")
        return
    debug_log(f'Phase 1 extraction start: pdf_count={len(pdf_files)}')

    # Launch all extractions at once; they run concurrently instead of one-by-one
    await asyncio.gather(*(extract_job_posting(pdf_path, agent) for pdf_path in pdf_files))
    debug_log("Phase 1 extraction complete")



# (Part 2): Market analysis : reads all extracted job JSONs and produces an aggregated json and md

def load_all_job_postings() -> str:
    """Read every extracted job JSON and combine them into one text block, to provide as a context to agent
    separated so the model can clearly tell postings apart.
    """
    json_job_files = sorted(JOBS_JSON_FOLDER.glob("*.json"))
    job_texts = [f.read_text(encoding="utf-8") for f in json_job_files]
    return "\n\n---\n\n".join(job_texts)


async def run_market_analysis_phase(agent: Agent) -> None:
    """Aggregate all extracted job postings into one market analysis.
    Always re-analyzes the full current set of postings (not idempotent by
    design — adding new postings should change the result on the next run).
    """
    json_job_files = sorted(JOBS_JSON_FOLDER.glob("*.json"))
    if not json_job_files:
        debug_log(f'No extracted job JSONs found in "{JOBS_JSON_FOLDER}"')
        print(f"No JSONs found in {JOBS_JSON_FOLDER}")
        return

    combined_jobs_text = load_all_job_postings()


    output_path_json = ANALYSIS_FOLDER / f"market-analysis.json"
    output_path_md = REPORTS_FOLDER / f"market-analysis.md"

    ctx = PathContext(output_path_json=output_path_json, output_path_md=output_path_md)
    debug_agent_start(agent.name, max_turns=10, output_path=str(output_path_json))

    result = await Runner.run(
        agent,
        f"Do the market analysis of the jobs:\n\n{combined_jobs_text}",
        max_turns=10,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    print(f"Market analysis saved. Report: {output_path_md.name}")
    print(result.final_output)


async def main():
    debug_log("Phase 1 start")
    agent_job = Agent(
        name="Assistant", instructions=system_prompt_job, tools=[web_search_tool, assess_job_tool]
    )
    agent_analysis = Agent(
        name="Assistant", instructions=system_prompt_analysis, tools=[assess_market_tool, save_disk_tool]
    )

    await run_extraction_phase(agent_job)

    print("Starting Market Analysis")
    await run_market_analysis_phase(agent_analysis)
    debug_log("Phase 1 complete")


if __name__ == "__main__":
    asyncio.run(main())
