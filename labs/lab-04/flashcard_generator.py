import os
import sys
from urllib import response
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Import your Pydantic model
from schemas import FlashcardResponse

# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_file_contents(path, description):
    """Read a file and return its contents, or exit on error."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: {description} not found: {path}")
        sys.exit(1)
    except Exception as err:
        print(f"❌ Error reading {description}: {path}")
        print(f"   {err}")
        sys.exit(1)




async def generate_flashcards(notes: str, cards: int) -> FlashcardResponse:
    """
    Generates flashcards from the provided notes using Structured Outputs.
    Args:
        notes: The raw text of the course notes
        cards: The number of cards to generate
    Returns:
        The validated Pydantic object containing the flashcards
    """
    
    system_prompt = get_file_contents('SYSTEM_PROMPT.md', 'System prompt file')

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )

    completion = client.responses.parse(
        model="gpt-4o-2024-08-06",
        input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },

                { 
                    "role": "user",
                    "content": f"Here are the notes:\n<notes>\n{notes}\n</notes>\n\nPlease create {cards} flashcards based on these notes."
                }
            ],
        text_format=FlashcardResponse,
    )
    return completion.output_parsed








