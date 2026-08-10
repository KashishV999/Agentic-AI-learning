# Repository Guidelines

## Project Structure & Module Organization
Core code lives under `src/`. Use `src/phases/phase_1.py` for job extraction and market analysis, and `src/phases/phase_2.py` for resume extraction and gap analysis. Shared helpers are in `src/helper/`, tool integrations are in `src/tools/`, schemas are in `src/schema/`, and prompt templates are in `src/prompts/`.

Project inputs and generated artifacts are separated in `data/`: raw PDFs live in `data/raw_jobs_pdf/` and `data/raw_resume_pdf/`, extracted JSON outputs in `data/jobs/`, `data/resume/`, and `data/analysis/`. Human-readable reports belong in `reports/`. Evaluation notes and manual checks are stored in `eval/` and `docs/`.

## Build, Test, and Development Commands
Create and activate a virtual environment first, then install the package in editable mode:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the pipelines from the repository root:

```bash
python3 src/phases/phase_1.py   # extract job PDFs and write market analysis
python3 src/phases/phase_2.py   # extract resume PDF and write gap analysis
```

If dependencies are not resolved by editable install, use `pip install -r requirements.txt`.

## Coding Style & Naming Conventions
Follow existing Python style: 4-space indentation, `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for module constants, and short docstrings on non-trivial functions. Keep new modules inside `src/` and prefer descriptive filenames such as `assess_market_tool.py` or `resume_schema.py`.

There is no configured formatter or linter in the repository today, so keep imports tidy, avoid unused code, and match the surrounding style before submitting changes.

## Testing Guidelines
There is no automated test suite yet. Validate changes by running the relevant phase script against the sample files in `data/` and reviewing generated JSON and Markdown outputs in `data/analysis/` and `reports/`. When adding tests, place them in a new `tests/` package and name files `test_<module>.py`.

## Commit & Pull Request Guidelines
Recent commits use short, capitalized summaries such as `Added Phase-1 job extraction` and `Restructured folders`. Keep commit messages brief, imperative, and scoped to one change. Pull requests should describe the pipeline impact, list changed data or report outputs, and include sample output or screenshots when report formatting changes.

## Security & Configuration Tips
Do not commit secrets. `phase_1.py` and `phase_2.py` expect `OPENROUTER_API_KEY`, and optionally `OPENAI_TRACING_KEY`, via environment variables or a local `.env` file.


## Phase 3 Context
See `steering/phase-3-spec.md` for the full Phase 3 requirements. Key constraint:
reuse existing extraction/search tools; do not reimplement them.