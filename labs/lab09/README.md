# Resource Credibility Analyzer Agent

An AI agent that investigates a given URL and produces a structured, evidence-based credibility report ,  checking the author, publication, and claims before writing a verdict.

Built with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), routed through **OpenRouter** (not the OpenAI API) via a custom `ModelProvider`.

## How it works

1. `read_url` — fetches the source (and related pages, e.g. author/about) via the Jina Reader API
2. `web_search` — researches the author, publication, and claims via the Tavily API
3. `assess_credibility` — forces the agent to record a complete, structured evaluation (Pydantic schema) before writing its report — this is a "think" tool: it does no computation, but prevents the agent from skipping steps or hand-waving its assessment
4. `save_report` — writes the final Markdown report to disk

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=sk-or-v1-...
TAVILY_API_KEY=tvly-...
```

## Run

```bash
python3 index.py
```

## Project structure

```
.
├── index.py                  # entry point — builds the agent, runs it
├── SYSTEM_PROMPT.md           # agent instructions, tool docs, error handling
├── requirements.txt
├── .env                        # API keys (not committed)
└── tools/
    ├── __init__.py            # re-exports all tools
    ├── read_url.py
    ├── web_search.py
    ├── assess_credibility.py
    ├── save_report.py
    └── credibility_schema.py  # Pydantic rubric used by assess_credibility
```

## Notes

- **Tracing:** OpenAI's built-in trace upload is disabled (`set_tracing_disabled(disabled=True)`) since no OpenAI key is used. Debug visibility comes from `enable_verbose_stdout_logging()` instead — logs print to the terminal as the agent runs.
- **Model:** defaults to `anthropic/claude-haiku-4.5` via OpenRouter; change `MODEL_NAME` in `index.py` to swap models.
- **Turn limit:** `max_turns` is set in `Runner.run()` to prevent runaway tool-calling loops.