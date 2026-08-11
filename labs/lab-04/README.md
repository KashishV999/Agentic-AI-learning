# Lab 04: Flashcard Generator API

## Why This Lab Exists

This lab is for turning the flashcard prompt from Lab 02 into an actual API. The focus is not just generating text anymore. It is about exposing the workflow through FastAPI, validating the request, and returning structured flashcard data instead of loose text.

## What I Learned On The First Pass

- How to move an LLM workflow from a CLI into a web API.
- Why structured outputs are easier to use than raw text when another program needs the result.
- How Pydantic schemas help validate both the input and the output shape.
- How to connect prompt-based generation to FastAPI routes.
- Why API design matters when wrapping an LLM feature for reuse.

## Core AI And Tech Topics

- Structured outputs
- FastAPI
- Pydantic validation
- JSON response design
- API integration for LLM workflows
- Prompt reuse from an earlier lab

## Folder Structure

```text
lab-04/
├── README.md
├── SYSTEM_PROMPT.md
├── flashcard_generator.py
├── notes.txt
├── requirements.txt
├── schemas.py
├── server.py
└── test_client.py
```

## Files

- `server.py` starts the FastAPI app and exposes `POST /api/generate`.
- `flashcard_generator.py` calls the model and parses the response into a schema.
- `schemas.py` defines the Pydantic response models.
- `test_client.py` sends a sample request to the local API.
- `SYSTEM_PROMPT.md` contains the flashcard instructions.
- `notes.txt` is sample content for testing.

## Setup

```bash
cd labs/lab-04
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with:

```env
OPENROUTER_API_KEY=your_key_here
```

## Run

Start the API:

```bash
python3 server.py
```

In another terminal, run the sample client:

```bash
python3 test_client.py
```

## API Contract

- Endpoint: `POST /api/generate`
- Request body:

```json
{
  "notes": "Your notes here",
  "cards": 3
}
```

## Notes

- The server listens on `http://localhost:3000`.
- Middleware adds an `X-Process-Time` header to responses.
