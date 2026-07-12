import argparse
import os
from openai import OpenAI
from query import search
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



def main():
    # Get the question from args
    parser = argparse.ArgumentParser(
        description="Search indexed documents",
        epilog='Example: python3 ask-node.py "How do I read a file?"',
    )
    parser.add_argument("query", help="Search query")

    args = parser.parse_args()
    question = args.query
    print(f"Query: {args.query}")
    
    # Search the chroma DB -> does embedding and rerank
    search_results = search(question)
    
    

    system_prompt = f"""You are ask-node, an expert node.js assistant that answers questions about Node.js.
    Here is some context from the official documentation:
    <context>
    {search_results}
    </context>
    Instructions:
    1. Answer the user's question based ONLY on the provided context.
    2. If the answer is not in the context, say "I don't have enough information to answer that."
    3. Cite the source file(s) (e.g., fs.md) for your information.
    """
    
    user_prompt = f"Question: {question}\nAnswer:"
    
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    )
        
    completion = client.chat.completions.create(
        model="google/gemini-3.1-flash-lite-preview",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },

            { 
                "role": "user",
                "content": user_prompt
            },
        ]
    )
    print("--------------------------------------------------------------")
    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
