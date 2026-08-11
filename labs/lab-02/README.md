# Lab 02: Flashcard Generator CLI

## Why This Lab Exists

This lab is for learning prompt engineering, not complicated backend code. The goal is to take raw notes and reliably turn them into ACE-style flashcards, which means the real challenge is teaching the model a custom format, a specific tone, and strict content rules.

## What I Learned On The First Pass

- How to separate a long system prompt into `SYSTEM_PROMPT.md` so it is easier to iterate on.
- Why custom output formats need stronger instructions than just "make flashcards."
- How few-shot examples help the model follow the ACE structure.
- Why delimiters matter when I pass large note files into a prompt.
- How to validate the result with regex parsing and estimate API cost from token usage.

## Core AI And Tech Topics

- Prompt engineering
- Few-shot prompting
- Delimiters for prompt safety
- Structured prompting workflow
- Output parsing
- Token cost tracking

## Folder Structure

```text
lab-02/
├── README.md
├── SYSTEM_PROMPT.md
├── cost.py
├── file.txt
├── first_prompt.md
├── flashcards.py
└── notes.txt
```

## Files

- `flashcards.py` reads notes, calls the model, and prints generated flashcards.
- `cost.py` computes estimated API cost from usage metadata.
- `SYSTEM_PROMPT.md` contains the flashcard-generation instructions.
- `notes.txt` and `file.txt` are sample note inputs.
- `first_prompt.md` is an earlier prompt draft/reference.

## Setup

```bash
cd labs/lab-02
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Usage

```bash
python3 flashcards.py notes.txt --cards 3
```

Arguments:

- `notes_path` is required.
- `--cards` accepts a value from `1` to `5` and defaults to `3`.

## Notes

- The implemented flag is `--cards`, not `--count`.
- The current script calls the model twice in `main()`, once for cost reporting and again for the printed output.
