# Lab 8: A Visual Debugger

## Overview
This lab builds a simple CLI tool that takes a screenshot of an error from a terminal, IDE, or browser, optimizes it for the web, sends it to a vision-capable LLM, and uses web search to find current documentation and a likely fix.

## Setup
1. `cd lab-08`
2. Create and activate a virtual environment:
   `python3 -m venv .venv`
   `source .venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Create a `.env` file with your API keys:
   `OPENROUTER_API_KEY=your_key`
   `TAVILY_API_KEY=your_key`
5. Make sure the image files are present in the `images` folder.

## Files
- `tool.py`: uses the Tavily API to search for recent documentation and error-related results.
- `process_image.py`: opens an image, resizes and compresses it, and converts it to a base64 JPEG string.
- `index.py`: connects everything together, sends the image to the model, and uses the search tool when needed.

## Usage

Run the tool from the project root:

```bash
python main.py
```

You'll be prompted for a filename:

Type the exact filename (including extension) of an image sitting inside `images/`, and press Enter.

Example:
```
Enter the image filename (with extension) in 'images/': next_js_error.png
```
