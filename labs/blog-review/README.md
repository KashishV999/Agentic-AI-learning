# Blog Review Prototype

## Why This Lab Exists

This lab is for experimenting with prompt-based editorial review. Instead of generating new content, the model acts like a reviewer for a draft blog post and checks it against Kubernetes blog expectations and writing quality rules.

## What I Learned On The First Pass

- How a system prompt can turn the model into a specialized reviewer instead of a generic chatbot.
- Why review tasks need clear criteria, not just "give feedback."
- How local markdown files can act as the full context for an evaluation workflow.
- How AI can help with editorial quality, structure, and policy alignment.
- Why evaluation prompts are different from generation prompts.

## Core AI And Tech Topics

- Review prompting
- System prompt design
- Editorial evaluation
- Prompt-driven quality checks
- Markdown-based context loading

## Folder Structure

```text
blog-review/
├── BLOG.md
├── MAJOR_ISSUES.md
├── README.md
├── SYSTEM_PROMPT.md
├── main.py
└── requirements.txt
```

## Files

- `main.py` loads the prompt and blog content, then sends both to OpenRouter.
- `SYSTEM_PROMPT.md` defines the Kubernetes blog review rules.
- `BLOG.md` is the draft article being reviewed.
- `MAJOR_ISSUES.md` contains extra review notes and examples.
- `requirements.txt` lists the Python dependencies.

## Setup

```bash
cd labs/blog-review
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Run

```bash
python3 main.py
```

## Notes

- `main.py` currently reads `SYSTEM_PROMPT.md` and `BLOG.md`.
- The script uses relative paths, so run it from inside `labs/blog-review`.
