# Lab 03: PR Advice Tool

## Why This Lab Exists

This lab is for learning how to prompt with real software engineering context. Instead of prompting with only plain text, this tool combines a GitHub PR diff and the PR discussion, then asks the model to explain what is happening like a senior engineer reviewing the change.

## What I Learned On The First Pass

- How to parse a GitHub PR URL into owner, repo, and pull request number.
- How to fetch both the code diff and human discussion because each one gives different context.
- Why mixed inputs like code and comments need clear delimiters in the prompt.
- How role-based prompting changes the quality of the explanation.
- Why context gathering matters before asking the model for advice.

## Core AI And Tech Topics

- PR review prompting
- Code-as-text prompting
- Context assembly
- GitHub API integration
- URL parsing
- Delimiter-based prompt design

## Folder Structure

```text
lab-03/
├── README.md
├── SYSTEM_PROMPT.md
└── pr_advice.py
```

## Files

- `pr_advice.py` is the interactive CLI.
- `SYSTEM_PROMPT.md` contains the review instructions for the model.

## Setup

```bash
cd labs/lab-03
python3 -m venv .venv
source .venv/bin/activate
pip install requests openai python-dotenv
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Usage

```bash
python3 pr_advice.py
```

The script prompts for a GitHub PR URL in this format:

```text
https://github.com/OWNER/REPO/pull/123
```

## Notes

- The tool reads the public `.diff` representation of the pull request.
- It also fetches PR comments from the GitHub API.
- Large diffs are truncated before being sent to the model.
