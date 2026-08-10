"""
Phase 3: Application Advisor pipeline.

This script accepts a new job-posting PDF, extracts a structured posting using
the existing Phase 1 extraction components, runs a legitimacy analysis, runs a
fit/application analysis against the saved resume + market data, and renders a
single schema-grounded HTML report.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
from dataclasses import dataclass
from pathlib import Path

from agents import (
    Agent,
    Model,
    ModelProvider,
    OpenAIChatCompletionsModel,
    RunConfig,
    Runner,
    set_tracing_export_api_key,
)
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI

from config import ANALYSIS_FOLDER, JOBS_JSON_FOLDER, PROMPTS_FOLDER, REPORTS_FOLDER, RESUME_JSON_FOLDER
from helper import get_file_contents, pdf_extraction
from helper.debug_logging import debug_agent_end, debug_agent_start, debug_log
from helper.save_disk import save_disk
from schema.application_analysis_schema import ApplicationAnalysisSchema
from schema.legitimacy_schema import LegitimacySchema
from tools import (
    assess_application_tool,
    assess_job_tool,
    assess_legitimacy_tool,
    web_search_tool,
    whois_lookup_tool,
)

load_dotenv(find_dotenv())
API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "anthropic/claude-haiku-4.5"

if not API_KEY:
    raise ValueError("Please set OPENROUTER_API_KEY via env var or code.")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_export_api_key(os.getenv("OPENAI_TRACING_KEY"))


class CustomModelProvider(ModelProvider):
    def get_model(self, model_name: str | None) -> Model:
        return OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)


CUSTOM_MODEL_PROVIDER = CustomModelProvider()

SYSTEM_PROMPT_JOB = get_file_contents(
    PROMPTS_FOLDER / "JOB-ANALYSIS-PROMPT.md", "System prompt file for job extraction"
)
SYSTEM_PROMPT_LEGITIMACY = get_file_contents(
    PROMPTS_FOLDER / "LEGITIMACY-PROMPT.md", "System prompt file for legitimacy analysis"
)
SYSTEM_PROMPT_APPLICATION = get_file_contents(
    PROMPTS_FOLDER / "APPLICATION-ANALYSIS-PROMPT.md", "System prompt file for application analysis"
)
SYSTEM_PROMPT_REPORT = get_file_contents(
    PROMPTS_FOLDER / "APPLICATION-REPORT-PROMPT.md", "System prompt file for application report rendering"
)

REQUIRED_REPORT_SECTION_IDS = [
    "legitimacy-assessment",
    "fit-assessment",
    "resume-adaptation",
    "cover-letter-guidance",
    "interview-prep",
]


@dataclass
class PathContext:
    output_path_json: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a new job posting PDF and generate an application report."
    )
    parser.add_argument("job_pdf", help="Path to the new job posting PDF")
    return parser.parse_args()


def ensure_prerequisites(pdf_path: Path) -> tuple[Path, Path]:
    if not pdf_path.exists() or not pdf_path.is_file():
        debug_log(f'Job posting PDF missing: "{pdf_path}"')
        raise FileNotFoundError(f"Job posting PDF not found: {pdf_path}")

    market_analysis_path = ANALYSIS_FOLDER / "market-analysis.json"
    resume_path = RESUME_JSON_FOLDER / "resume.json"

    if not market_analysis_path.exists():
        debug_log(f'Required market analysis missing: "{market_analysis_path}"')
        raise FileNotFoundError(
            f"Required market analysis not found: {market_analysis_path}. Run Phase 1 first."
        )
    if not resume_path.exists():
        debug_log(f'Required resume analysis missing: "{resume_path}"')
        raise FileNotFoundError(
            f"Required resume analysis not found: {resume_path}. Run Phase 2 first."
        )

    return market_analysis_path, resume_path




async def extract_job_posting(pdf_path: Path) -> Path:
    output_path_json = JOBS_JSON_FOLDER / f"{pdf_path.stem}.json"
    job_text = pdf_extraction(str(pdf_path))
    if not job_text or job_text.strip() == "Unable to parse the pdf":
        debug_log(f'Job extraction failed: unreadable PDF "{pdf_path}"')
        raise RuntimeError(f"Failed to extract readable text from PDF: {pdf_path}")

    agent = Agent(
        name="Job Extraction Assistant",
        instructions=SYSTEM_PROMPT_JOB,
        tools=[web_search_tool, assess_job_tool],
    )
    ctx = PathContext(output_path_json=output_path_json)
    debug_log(f'Phase 3 extraction input: "{pdf_path}"')
    debug_agent_start(agent.name, max_turns=10, output_path=str(output_path_json))

    await Runner.run(
        agent,
        f"Analyze the job description: {job_text}",
        max_turns=10,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    if not output_path_json.exists():
        debug_log(f'Job extraction did not produce output JSON: "{output_path_json}"')
        raise RuntimeError(f"Job extraction did not produce output JSON: {output_path_json}")

    print(f"Structured job posting saved to {output_path_json}")
    return output_path_json


async def run_legitimacy_analysis(
    job_json_path: Path,
    market_analysis_path: Path,
) -> Path:
    output_path_json = ANALYSIS_FOLDER / "legitimacy-analysis.json"
    job_json_text = get_file_contents(job_json_path, "Structured job posting JSON")
    market_text = get_file_contents(market_analysis_path, "Market analysis JSON")

    agent = Agent(
        name="Legitimacy Assistant",
        instructions=SYSTEM_PROMPT_LEGITIMACY,
        tools=[web_search_tool, whois_lookup_tool, assess_legitimacy_tool],
    )
    ctx = PathContext(output_path_json=output_path_json)
    debug_log(
        f'Legitimacy analysis input files: job="{job_json_path}", market="{market_analysis_path}"'
    )
    debug_agent_start(agent.name, max_turns=12, output_path=str(output_path_json))
    user_prompt = (
        "<structured_job_posting>\n"
        f"{job_json_text}\n"
        "</structured_job_posting>\n\n"
        "<market_analysis>\n"
        f"{market_text}\n"
        "</market_analysis>"
    )

    await Runner.run(
        agent,
        f"Investigate the legitimacy of this job posting:\n\n{user_prompt}",
        max_turns=12,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    if not output_path_json.exists():
        debug_log(f'Legitimacy analysis did not produce output JSON: "{output_path_json}"')
        raise RuntimeError(f"Legitimacy analysis did not produce output JSON: {output_path_json}")

    print(f"Legitimacy analysis saved to {output_path_json}")
    return output_path_json


async def run_application_analysis(
    job_json_path: Path,
    market_analysis_path: Path,
    resume_path: Path,
) -> Path:
    output_path_json = ANALYSIS_FOLDER / "application-analysis.json"
    job_json_text = get_file_contents(job_json_path, "Structured job posting JSON")
    market_text = get_file_contents(market_analysis_path, "Market analysis JSON")
    resume_text = get_file_contents(resume_path, "Resume JSON")

    agent = Agent(
        name="Application Advisor Assistant",
        instructions=SYSTEM_PROMPT_APPLICATION,
        tools=[web_search_tool, assess_application_tool],
    )
    ctx = PathContext(output_path_json=output_path_json)
    debug_log(
        f'Application analysis input files: job="{job_json_path}", resume="{resume_path}", market="{market_analysis_path}"'
    )
    debug_agent_start(agent.name, max_turns=12, output_path=str(output_path_json))
    user_prompt = (
        "<structured_job_posting>\n"
        f"{job_json_text}\n"
        "</structured_job_posting>\n\n"
        "<resume>\n"
        f"{resume_text}\n"
        "</resume>\n\n"
        "<market_analysis>\n"
        f"{market_text}\n"
        "</market_analysis>"
    )

    await Runner.run(
        agent,
        f"Create a posting-specific application analysis:\n\n{user_prompt}",
        max_turns=12,
        context=ctx,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    if not output_path_json.exists():
        debug_log(f'Application analysis did not produce output JSON: "{output_path_json}"')
        raise RuntimeError(f"Application analysis did not produce output JSON: {output_path_json}")

    print(f"Application analysis saved to {output_path_json}")
    return output_path_json


async def generate_html_report(legitimacy_path: Path, application_path: Path) -> Path:
    output_path = REPORTS_FOLDER / "application-report.html"
    debug_log(
        f'Report generation input files: legitimacy="{legitimacy_path}", application="{application_path}"'
    )
    legitimacy = LegitimacySchema.model_validate_json(
        get_file_contents(legitimacy_path, "Legitimacy analysis JSON")
    )
    application = ApplicationAnalysisSchema.model_validate_json(
        get_file_contents(application_path, "Application analysis JSON")
    )

    agent = Agent(
        name="Application Report Renderer",
        instructions=SYSTEM_PROMPT_REPORT,
    )
    debug_agent_start(agent.name, max_turns=2, output_path=str(output_path))
    user_prompt = (
        "Render the final application report as one complete HTML document using only these two validated JSON "
        "objects.\n\n"
        "<legitimacy_analysis>\n"
        f"{legitimacy.model_dump_json(indent=2)}\n"
        "</legitimacy_analysis>\n\n"
        "<application_analysis>\n"
        f"{application.model_dump_json(indent=2)}\n"
        "</application_analysis>"
    )

    result = await Runner.run(
        agent,
        user_prompt,
        max_turns=2,
        run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER),
    )
    debug_agent_end(agent.name, status="completed")

    html = result.final_output
    if not isinstance(html, str):
        html = str(html)

    debug_log(f'Report render complete: output="{output_path}", chars={len(html)}')

    result = save_disk(output_path.name, str(output_path.parent), html)
    if result.get("status") != "saved":
        debug_log(f'HTML report save failed: output="{output_path}", result="{result}"')
        raise RuntimeError(f"Failed to save HTML report: {result}")
    print(f"Application report saved to {output_path}")
    return output_path


async def main() -> None:
    debug_log("Phase 3 start")
    args = parse_args()
    pdf_path = Path(args.job_pdf).expanduser().resolve()
    market_analysis_path, resume_path = ensure_prerequisites(pdf_path)

    job_json_path = await extract_job_posting(pdf_path)
    legitimacy_path = await run_legitimacy_analysis(job_json_path, market_analysis_path)
    application_path = await run_application_analysis(
        job_json_path,
        market_analysis_path,
        resume_path,
    )
    await generate_html_report(legitimacy_path, application_path)
    debug_log("Phase 3 complete")


if __name__ == "__main__":
    asyncio.run(main())
