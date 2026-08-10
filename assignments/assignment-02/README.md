# Assignment 02

This project is a 3-phase agent pipeline for:

- Phase 1: extracting job postings and generating a market analysis
- Phase 2: extracting a resume and generating a resume gap analysis
- Phase 3: analyzing a new target posting and generating an application advisor report

See the detailed phase docs:

- [Phase 1](/Users/kashish/Desktop/Seneca/sem6/AIP/aip444/assignments/assignment-02/docs/phase-1.md)
- [Phase 2](/Users/kashish/Desktop/Seneca/sem6/AIP/aip444/assignments/assignment-02/docs/phase-2.md)
- [Phase 3](/Users/kashish/Desktop/Seneca/sem6/AIP/aip444/assignments/assignment-02/docs/phase-3.md)

## Project Structure

```text
assignment-02/
├── data/
│   ├── analysis/          # Generated JSON analysis outputs
│   ├── jobs/              # Extracted job posting JSON files
│   ├── raw_jobs_pdf/      # Source job posting PDFs
│   ├── raw_resume_pdf/    # Source resume PDF
│   └── resume/            # Extracted resume JSON output
├── docs/                  # Phase documentation and reflection notes
├── eval/                  # Manual validation and evaluation notes
├── reports/               # Generated Markdown/HTML reports
├── steering/              # Phase 3 spec, plan, and supporting notes
├── src/
│   ├── helper/            # Shared helpers for PDF extraction, file IO, logging
│   ├── phases/
│   │   ├── phase_1.py     # Job extraction and market analysis pipeline
│   │   ├── phase_2.py     # Resume extraction and gap analysis pipeline
│   │   └── phase_3.py     # Target job application advisor pipeline
│   ├── prompts/           # Prompt templates used by tools/phases
│   ├── schema/            # Structured output schemas
│   ├── tools/             # Reusable agent tools and integrations
│   └── config.py          # Shared configuration
├── AGENTS.md              # Repository-specific agent instructions
├── pyproject.toml         # Project packaging metadata
├── requirements.txt       # Dependency fallback install list
└── README.md
```

## Setup

Create and activate a virtual environment, then install the project:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

If editable install does not resolve everything, run:

```bash
pip install -r requirements.txt
```

Environment variables:

- `OPENROUTER_API_KEY` required for model calls
- `TAVILY_API_KEY` required for web search tool usage
- `OPENAI_TRACING_KEY` optional for tracing
- `LOG_LEVEL=debug` optional for debug logs

Input folders:

- Job PDFs: `data/raw_jobs_pdf/`
- Resume PDF: `data/raw_resume_pdf/resume.pdf`

## Run

Phase 1, job market analysis:

```bash
python3 src/phases/phase_1.py
```

Outputs:

- `data/jobs/*.json`
- `data/analysis/market-analysis.json`
- `reports/market-analysis.md`

Phase 2, resume gap analysis:

```bash
python3 src/phases/phase_2.py
```

Outputs:

- `data/resume/resume.json`
- `data/analysis/gap-analysis.json`
- `reports/gap-analysis.md`

Phase 3, application advisor:

```bash
python3 src/phases/phase_3.py path/to/new-job-posting.pdf
```

Outputs:

- `data/jobs/<job-name>.json`
- `data/analysis/legitimacy-analysis.json`
- `data/analysis/application-analysis.json`
- `reports/application-report.html`

## Order

Run phases in this order:

1. `phase_1.py`
2. `phase_2.py`
3. `phase_3.py <job-pdf>`

Phase 2 depends on Phase 1 outputs. Phase 3 depends on both Phase 1 and Phase 2 outputs.
