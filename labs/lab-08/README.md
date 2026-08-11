# Lab 08: Visual Debugger

## Why This Lab Exists

This lab is for learning multimodal AI plus tool calling. The tool takes a screenshot of an error, prepares the image for model input, asks a vision-capable model to inspect the problem, and lets that model search the web for up-to-date fixes.

## What I Learned On The First Pass

- How to preprocess screenshots before sending them to an API so they are cheaper and easier to handle.
- How to prompt a vision model to describe, analyze, and fix an error systematically.
- Why tool calling matters when the screenshot mentions a framework or version that needs outside research.
- How to combine image understanding with web search in one workflow.
- Why debugging prompts need both technical accuracy and clear action steps.

## Core AI And Tech Topics

- Multimodal prompting
- Vision input
- Tool calling
- Web-assisted debugging
- Image preprocessing
- Tavily search integration

## Folder Structure

```text
lab-08/
├── README.md
├── SYSTEM_PROMPT.md
├── images/
│   ├── edge_case.png
│   ├── next_js_error.png
│   └── stack_trace.png
├── index.py
├── process_image.py
├── requirements.txt
└── tool.py
```

## Files

- `index.py` is the main CLI and tool-calling loop.
- `process_image.py` resizes and compresses an image, then returns base64 output.
- `tool.py` searches Tavily for technical references related to the error.
- `SYSTEM_PROMPT.md` contains the debugging instructions.
- `images/` contains example screenshots for testing.

## Setup

```bash
cd labs/lab-08
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

## Run

```bash
python3 index.py
```

When prompted, enter an image filename from `images/`, for example:

```text
next_js_error.png
```

## Notes

- The entrypoint is `index.py`.
- Tavily search in `tool.py` currently filters results using a `start_date` of `2026-01-01`.
