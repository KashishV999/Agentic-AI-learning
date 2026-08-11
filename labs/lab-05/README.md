# Lab 05: PR Advice Tool With Function Calling

## Why This Lab Exists

This lab is for learning tool calling. In Lab 03 the model only worked with the diff and comments that the program provided up front. In this version, the model can ask for extra repository files when it needs more context, which makes the review flow more agent-like and less static.

## What I Learned On The First Pass

- How to define a tool schema the model can call instead of guessing file contents.
- Why tool calling is useful when the initial prompt does not include enough context.
- How to run a multi-step loop where the model asks for a file, receives it, and continues reasoning.
- How Pydantic helps make tool inputs explicit and safer.
- Why guardrails like iteration limits matter in a tool-calling workflow.

## Core AI And Tech Topics

- Tool calling
- Function schemas
- Multi-turn LLM workflows
- Pydantic models for tools
- Context expansion on demand
- GitHub raw file retrieval

## Folder Structure

```text
lab-05/
├── README.md
├── SYSTEM_PROMPT.md
├── github_file_object.py
├── notes.txt
├── pr_advice.py
├── requirements.txt
├── test_tool.py
└── tools.py
```

## Files

- `pr_advice.py` runs the tool-calling review loop.
- `tools.py` fetches raw file content from GitHub.
- `github_file_object.py` defines the schema for requested files.
- `test_tool.py` is a local test/helper script for the GitHub file tool.
- `SYSTEM_PROMPT.md` contains the reviewer instructions.
- `notes.txt` is a local notes file kept with the lab.

## Setup

```bash
cd labs/lab-05
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Usage

```bash
python3 pr_advice.py
```

The script prompts for a public GitHub pull request URL and then lets the model call `ReadGithubFiles` if it needs more context.

## Notes

- Tool calls are limited to 5 iterations.
- Files are fetched from `raw.githubusercontent.com`.
- Long files are truncated based on the request schema.
