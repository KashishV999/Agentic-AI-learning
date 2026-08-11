# Lab 09: Resource Credibility Analyzer Agent

## Why This Lab Exists

This lab is for learning what makes an agent different from a normal prompt-response app. Instead of hard-coding every step, the agent reads a source, searches for supporting information, records a structured credibility assessment, and saves a report. It is a full tool-using workflow with a clear goal.

## What I Learned On The First Pass

- How an agent loop works when the model decides which tool to call next.
- Why tool design matters as much as prompt design in agent systems.
- How a "think tool" can force better reasoning before the final answer.
- Why a structured credibility schema makes the assessment more complete and less hand-wavy.
- How to connect reading, searching, evaluating, and saving into one agent workflow.

## Core AI And Tech Topics

- Agents
- Tool calling
- OpenAI Agents SDK
- Think-tool pattern
- Structured evaluation schemas
- Report generation

## Folder Structure

```text
lab09/
├── README.md
├── SYSTEM_PROMPT.md
├── index.py
├── reports/
├── requirements.txt
└── tools/
    ├── __init__.py
    ├── assess_credibility.py
    ├── credibility_schema.py
    ├── read_url.py
    ├── save_report.py
    └── web_search.py
```

## Files

- `index.py` builds the agent and runs it with a custom OpenRouter-backed model provider.
- `SYSTEM_PROMPT.md` contains the agent instructions.
- `tools/read_url.py` fetches page content through the Jina Reader API.
- `tools/web_search.py` searches Tavily for supporting evidence.
- `tools/assess_credibility.py` forces a structured evaluation step.
- `tools/credibility_schema.py` defines the report schema.
- `tools/save_report.py` writes the final markdown report.
- `reports/` contains saved example outputs.

## Setup

```bash
cd labs/lab09
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
OPENAI_TRACING_KEY=your_openai_key_here
```

`OPENAI_TRACING_KEY` is optional and only affects tracing.

## Run

```bash
python3 index.py
```

## Notes

- `index.py` currently evaluates one hard-coded test URL.
- Reports are saved into the local `reports/` directory.
