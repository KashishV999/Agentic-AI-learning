# Lab 04 Flashcard Generator

## What this server does
`server.py` starts a FastAPI server that accepts study notes via a POST request, calls `flashcard_generator.generate_flashcards(...)`, and returns structured JSON flashcards.

## Files

- `server.py`
  - Runs the FastAPI app.
  - Handles POST `/api/generate` with a Pydantic request model.
  - Uses CORS middleware and adds request processing time to responses.

- `flashcard_generator.py`
  - Loads the `.env` API key.
  - Reads `SYSTEM_PROMPT.md`.
  - Calls OpenAI / OpenRouter with `client.responses.parse(...)`.
  - Uses `text_format=FlashcardResponse` and returns `completion.output_parsed`.


- `schemas.py`
  - Defines data models with Pydantic.
  - `Flashcard`: single flashcard fields.
  - `FlashcardResponse`: wrapper with `flashcards` list and `message`.

- `test_client.py`
  - Reads `notes.txt`.
  - Sends a POST request to `http://localhost:3000/api/generate`.
  - Prints the returned JSON.

- `SYSTEM_PROMPT.md`
  - Contains the prompt and schema rules used by the flashcard generator. Uses pydantic Model

## How to run

1. Activate the virtual environment:
```bash
source .venv/bin/activate
```
2. Install dependencies if needed:
```bash
pip install -r requirements.txt
```
3. Start the server:
```bash
python server.py
```
4. Run the test client in another terminal:
```bash
python test_client.py
```

## Notes
- Make sure `.env` contains `OPENROUTER_API_KEY` if the generator needs the API key.
