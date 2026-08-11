# Research Judge Runner

## Why This Lab Exists

This folder is for evaluating model outputs instead of generating an end-user feature. It compares answer sets from different models, asks a judge model to score them, and writes the results into CSV and markdown tables for analysis.

## What I Learned On The First Pass

- How "LLM as judge" works in a repeatable evaluation workflow.
- Why evaluation prompts need a clear rubric before scoring can mean anything.
- How to parse structured scores out of model responses.
- How to aggregate results into files that are easier to compare.
- Why benchmarking is a separate skill from building assistants or agents.

## Core AI And Tech Topics

- LLM as judge
- Evaluation pipelines
- Rubric-based prompting
- Output parsing
- Benchmark reporting
- Result aggregation

## Folder Structure

```text
research/
├── README.md
├── Question.md
├── SYSTEM_PROMPT.md
├── answers_gpt4omini.md
├── answers_llama.md
├── answers_mistral.md
├── judge_scores.csv
├── judge_scores_table.md
├── judge_scores_table_5.md
└── main.py
```

## Files

- `main.py` runs the judging pipeline and writes output files.
- `SYSTEM_PROMPT.md` contains the grading rubric for the judge model.
- `Question.md` contains the questions being scored.
- `answers_llama.md`, `answers_mistral.md`, and `answers_gpt4omini.md` are the answer sets being compared.
- `judge_scores.csv`, `judge_scores_table.md`, and `judge_scores_table_5.md` are generated outputs.

## Setup

```bash
cd labs/research
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
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

- The judge model is currently set to `openai/gpt-4o`.
- Answer files must preserve IDs like `R1`, `C2`, or `F5` so parsing works correctly.
