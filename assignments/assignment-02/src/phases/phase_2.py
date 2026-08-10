"""
Phase 2: Resume Extraction + Gap Analysis Pipeline.

This script runs two sequential stages:
1. Resume extraction — converts the candidate's resume PDF into structured JSON
   (skips extraction if the output JSON already exists).
2. Gap analysis — compares the extracted resume against the market analysis
   produced by phase_1, and produces an aggregated gap analysis (strengths,
   gaps, unique value, and a triaged action plan), saved as both structured
   JSON and a Markdown report.

Requires phase_1.py to have been run first, since this reads its market
analysis output as input.

Reference on context passing:
https://openai.github.io/openai-agents-python/context/#what-runcontextwrapper-exposes
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from datetime import datetime
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
from config import PROMPTS_FOLDER, RAW_RESUME_FOLDER, RESUME_JSON_FOLDER, ANALYSIS_FOLDER,  REPORTS_FOLDER
from tools import web_search_tool, assess_resume_tool , save_disk_tool, assess_gap_analysis_tool


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


system_prompt_resume = get_file_contents(
    PROMPTS_FOLDER / "RESUME-ANALYSIS-PROMPT.md", "System prompt file for analysing resume"
)

system_prompt_gap_analysis = get_file_contents(
    PROMPTS_FOLDER / "RESUME-GAP-ANALYSIS-PROMPT.md", "System prompt file for gap analyses between resume and market"
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
    output_path_json: Path            # where assess_* tools save JSON using save_disk_tool in data/ path
    output_path_md: Path = None       # where save_disk_tool saves the Markdown report in analysis/ path



# (Part 1) - Extraction : converts resume PDF into a structured JSON file
   

async def extract_resume(pdf_path: Path, agent: Agent) -> None:
    """Extract one job posting PDF into structured JSON.
    Skips the PDF if its output JSON already exists.
    """
    output_path_json = RESUME_JSON_FOLDER / f"{pdf_path.stem}.json"

    if output_path_json.exists():
        debug_log(f'Skip resume extraction: "{pdf_path}" already processed -> "{output_path_json}"')
        print(f"Skipping {pdf_path.name} — already processed")
        return

    resume_text = pdf_extraction(str(pdf_path))
    ctx = PathContext(output_path_json=output_path_json)
    debug_agent_start(agent.name, max_turns=10, output_path=str(output_path_json))

    await Runner.run(
        agent,
        f"Analyze the resume: {resume_text}",
        max_turns=10,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    print(f"{pdf_path.name} -> {output_path_json.name}")



# (Part 2): GAP resume-market analysis : reads the resume.json and market_analysis.json to do gap analysis


async def run_gap_analysis_phase(agent: Agent, resume_file: Path, market_analysis_file: Path) -> None:
    """
    Analysis of resume against the market and product the gap analysis report (.json and md) with the actionable steps
    """
    # .read_text(encoding="utf-8")

    resume_text = resume_file.read_text(encoding="utf-8")
    market_text = market_analysis_file.read_text(encoding="utf-8")
    user_prompt = f"<resume>\n{resume_text}\n</resume>\n\n<market_analysis>\n{market_text}\n</market_analysis>"
        
    output_path_json= ANALYSIS_FOLDER / "gap-analysis.json"
    output_path_md= REPORTS_FOLDER / "gap-analysis.md"

    ctx = PathContext(output_path_json=output_path_json, output_path_md=output_path_md)
    debug_log(
        f'Gap analysis input files: resume="{resume_file}", market="{market_analysis_file}"'
    )
    debug_agent_start(agent.name, max_turns=10, output_path=str(output_path_json))

    result = await Runner.run(
        agent,
        f"Do the gap analysis of the resume with the market: {user_prompt}",
        max_turns=10,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    print(f"Gap analysis saved. Report: {output_path_md.name}")
    print(result.final_output)


async def main():
    debug_log("Phase 2 start")
    agent_resume = Agent(
        name="Assistant", instructions=system_prompt_resume, tools=[assess_resume_tool]
    )

    resume_path= RAW_RESUME_FOLDER/ "resume.pdf"
    if not resume_path.exists():
        debug_log(f'Resume PDF missing: "{resume_path}"')
        print("No file found!")
        return
    await extract_resume(resume_path, agent_resume)

    # --------------------
    print("Starting Gap Analysis")
    
    agent_analysis = Agent(
        name="Assistant", instructions=system_prompt_gap_analysis, tools=[web_search_tool, assess_gap_analysis_tool, save_disk_tool]
    )
        
    market_analysis_file= ANALYSIS_FOLDER / "market-analysis.json"
    resume_analysis_file= RESUME_JSON_FOLDER/ "resume.json"
    
    if not market_analysis_file.exists():
        debug_log(f'Required market analysis missing: "{market_analysis_file}"')
        print(f"No market analysis found at {market_analysis_file} — run phase_1 first.")
        return
    if not resume_analysis_file.exists():
        debug_log(f'Required resume analysis missing: "{resume_analysis_file}"')
        print(f"No resume analysis found at {resume_analysis_file}")
        return
    
    await run_gap_analysis_phase(agent_analysis, resume_file=resume_analysis_file, market_analysis_file=market_analysis_file)
    debug_log("Phase 2 complete")


if __name__ == "__main__":
    asyncio.run(main())
