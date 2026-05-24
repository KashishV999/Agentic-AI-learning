# Lab 2 

# Flashcards Generator

A Python CLI tool that generates **ACE flashcards** from course notes using an LLM through OpenRouter.


## Features

- Generate **1–5 flashcards** from notes
- Supports **Markdown, text, and HTML** files
- Uses **OpenRouter API** for LLM generation
- Calculates **token usage and API cost**
- Extracts flashcards using regex
- Validates structured flashcard formatting

## Usage
Run the flashcard generator:
   ```bash
   python flashcards.py notes.md --count 3
   ```
   min count is 1, max count is 5. If not specified, defaults to 3.
 