# Lab 01: AI Commit Message Generator

## Why This Lab Exists

This lab is for learning the basic shape of an LLM-powered developer tool. The script reads the staged git diff, sends that diff to a model, and asks for a commit message in Conventional Commits format. It is the first lab where the model is doing useful work inside a normal CLI workflow instead of only in chat.

## What I Learned On The First Pass

- How to turn real developer context (`git diff --staged`) into model input.
- Why prompt wording matters when I need one short output instead of a long explanation.
- How a system prompt can force a response format like Conventional Commits.
- How CLI flags like `--creative`, `--verbose`, and `-y` change model behavior or the final workflow.
- How to "dogfood" the tool by using the AI-generated message to commit the tool itself.

## Core AI And Tech Topics

- Prompting from code diffs
- Conventional Commit formatting
- LLM parameter tuning with temperature
- CLI automation
- Git subprocess usage
- OpenRouter via the `openai` SDK

## Folder Structure

```text
lab-01/
├── README.md
├── git_cm.py
├── git_diff_subprocess.py
└── requirements.txt
```

## Files

- `git_cm.py` is the main CLI script.
- `git_diff_subprocess.py` reads the staged diff using `git diff --staged`.
- `requirements.txt` lists the Python dependencies.

## Setup

```bash
cd labs/lab-01
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Usage

Stage your changes first, then run:

```bash
python3 git_cm.py
```

Useful flags:

- `--creative` uses a higher-temperature prompt.
- `--verbose` asks for a subject plus a short body paragraph.
- `-y` skips the confirmation prompt and runs `git commit -m`.

Example:

```bash
python3 git_cm.py --creative --verbose
```

## Notes

- The script only analyzes staged changes.
- `-y` creates the commit immediately after generation.
