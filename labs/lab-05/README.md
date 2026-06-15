# Lab 03: PR Advice Tool

## Purpose
- Provide automated advice and information for GitHub Pull Requests (PRs)

## Features
- Validates GitHub PR URLs
- Fetches PR details and comments from GitHub
- Integrates with OpenAI/OpenRouter LLM to generate advice based on PR content and discussion

## Usage
1. Ensure you have Python 3 and required packages installed (`requests`, `openai`, `python-dotenv`).
2. Set your `OPENROUTER_API_KEY` in a `.env` file in the project root.
3. Run the script:
   ```bash
   python pr_advice.py
   ```
4. The script will print header info, validate a sample PR URL, and fetch advice/comments using the LLM.

---
Developed by Kashish Verma - 151579232
