import os
import sys
import argparse
from cost import calculate_cost
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import re

# LLM chat completion import
from openai import OpenAI

# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate ACE flashcards from course notes'
    )
    parser.add_argument(
        'notes_path',
        help='Path to the notes file (Markdown, HTML, or text)'
    )
    parser.add_argument(
        '--cards',
        type=int,
        default=3,
        help='Number of flashcards to generate (1-5, default: 3)'
    )

    args = parser.parse_args()

    # Validate cards range
    if args.cards < 1 or args.cards > 5:
        parser.error('--cards must be between 1 and 5')

    return args



# Function to print the header information
def printHeader():
    now = datetime.now()
    print ("--------------------------------------------------------------")
    print("flashcards: Developed by Kashish Verma - 151579232")
    print("Run Date: ", now.strftime("%Y-%m-%d %H:%M:%S"))
    print ("--------------------------------------------------------------")



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




def chatCompletion():

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )

    # Usage
    args = parse_arguments()
    notes_path = args.notes_path
    cards = args.cards

    # Usage
    system_prompt = get_file_contents('SYSTEM_PROMPT.md', 'System prompt file')
    notes_content = get_file_contents(notes_path, 'Notes file')

    completion = client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },

            { 
                "role": "user",
                "content": f"Here are the notes:\n<notes>\n{notes_content}\n</notes>\n\nPlease create {cards} flashcards based on these notes."
            }
        ]
    )

    return completion




def main():

    printHeader()
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")

    completion_dict = chatCompletion().model_dump()
    cost = calculate_cost(completion_dict)
    print(f"Total cost: ${cost['total']:.6f}")
    print(f"Tokens used: {cost['tokens']['total']}")

    print("-------------------------------------------------")




    completion_choice= chatCompletion().choices[0].message.content
    print("Generated Flashcards:")
    print(completion_choice)


        # Extract all cards using regex
    cards = re.findall(
        r'(=== CARD \d+ ===.*?===)',
        completion_choice,
        re.DOTALL
    )

    if not cards:
        print("❌ No cards found in output.")
        sys.exit(1)

    print(f"\n✅ Generated {len(cards)} flashcard(s):\n")
    for card in cards:
        print(card)
        print()  # blank line between cards






if __name__ == "__main__":
    main()