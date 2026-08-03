# Resource Credibility Analyzer Agent

An AI agent that investigates a given URL and produces a structured, evidence-based credibility report — checking the author, publication, and claims before writing a verdict.

Built with the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), routed through **OpenRouter** (not the OpenAI API) via a custom `ModelProvider`.
- [Agents SDK Documentation](https://developers.openai.com/api/docs/guides/agents/define-agents)

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
OPENAI_TRACING_KEY=sk-...          # optional — see Tracing note below
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

- **Tracing:** model calls are routed through OpenRouter, but the SDK's tracing dashboard lives at `platform.openai.com/traces` — a separate system from inference, so it needs its own real OpenAI key. Set `OPENAI_TRACING_KEY` in `.env` and the app calls `set_tracing_export_api_key(os.getenv("OPENAI_TRACING_KEY"))` to enable it. If left unset, tracing is skipped with no error — debug visibility still comes from `enable_verbose_stdout_logging()`, which prints every step to the terminal regardless of whether tracing is enabled.
- **Model:** defaults to `anthropic/claude-haiku-4.5` via OpenRouter; change `MODEL_NAME` in `index.py` to swap models.
- **Turn limit:** `max_turns` is set in `Runner.run()` to prevent runaway tool-calling loops.

Example URLS to test:
1. High credibility — Government or institutional source:  https://our-languages.canada.ca/en/blogue-blog/navigateur-linguistique-language-navigator-eng

2. High credibility — Major news organization: https://www.bbc.com/news/uk-62821117

3. Medium credibility — Organizational or corporate blog: https://blog.cloudflare.com/how-cloudflare-advocates-for-a-better-internet/

4. Researcher : https://doi.org/10.48550/arXiv.2404.04475

5. Personal Blog: https://www.kashishverma.com/blog/whiskerBot/firstBlog

6. LOW Credibility: https://www.hilarispublisher.com/open-access/nurses-advance-pharmacological-management-critical-roles-and-outcomes-117816.html
