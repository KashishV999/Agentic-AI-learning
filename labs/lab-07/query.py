import os
import argparse
from dotenv import load_dotenv, find_dotenv
import chromadb
import requests
from openai import OpenAI

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def rerank_results(
    query: str,
    candidates: list[dict],
    top_n: int = 5,
    min_score: float = 0.3,
) -> list[dict]:
    documents = [c['content'] for c in candidates]
    response = requests.post(
        'https://openrouter.ai/api/v1/rerank',
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'model': 'cohere/rerank-v3.5',
            'query': query,
            'documents': documents,
            'top_n': top_n,
        },
    )

    data = response.json()
    # print(data)
    return [
        {**candidates[r['index']],
         'rerank_score': r['relevance_score']}
        for r in data['results']
        if r['relevance_score'] >= min_score
    ]


# This function takes an array of serialized product strings and creates embeddings for them using the OpenAI API.
def create_embedding(serialized_array):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    response = client.embeddings.create(
        model='openai/text-embedding-3-small',
        input=serialized_array
    )
    return response.data


client = chromadb.PersistentClient(path="./chroma_db")


def search(query: str):
    # Embed the query
    query_embedding = create_embedding([query])
    # 1. Initialize Chroma Collection, using our custom embedding function
    collection = client.get_collection(
        name="node-docs"
    )
    top_25_results = collection.query(
        query_embeddings=[query_embedding[0].embedding],
        n_results=25
    )
    # dict_keys(['ids', 'embeddings', 'documents', 'uris', 'included', 'data', 'metadatas', 'distances'])
    print(top_25_results.keys())
    candidates = [
        {
            'content': doc,
            'metadata': meta,
            'distance': dist,
        }
        for doc, meta, dist in zip(
            top_25_results['documents'][0],
            top_25_results['metadatas'][0],
            top_25_results['distances'][0],
        )
    ]
    # 4. Rerank to get top 5
    return rerank_results(query, candidates, top_n=5)


def main():
    parser = argparse.ArgumentParser(
        description="Search the node-docs Chroma collection and rerank results using Cohere rerank-v3.5.",
        epilog='Example: python3 query.py "How do I read a file asynchronously?"',
    )
    parser.add_argument(
        "query",
        type=str,
        help="The search query string, e.g. \"How do I read a file?\"",
    )
    args = parser.parse_args()

    results = search(args.query)

    if not results:
        print(f"\nNo sufficiently relevant results found for: \"{args.query}\"")
        return

    print("\nTop Reranked Results:")
    for i, r in enumerate(results):
        print(f"\n{i+1}. Metadata: {r['metadata']}")
        print(f"   Chroma distance: {r['distance']:.4f}") #  In Chroma, a smaller distance number means more similar.
        print(f"   Rerank relevance score: {r['rerank_score']:.4f}")
        print(f"   Content: {r['content']}...")


if __name__ == "__main__":
    main()
    
    
    
    
    
# NOTE:

# Why to use [0] ?

#     # dict_keys(['ids', 'embeddings', 'documents', 'uris', 'included', 'data', 'metadatas', 'distances'])
#     print(top_25_results.keys())
#     candidates = [
#         {
#             'content': doc,
#             'metadata': meta,
#             'distance': dist,
#         }
#         for doc, meta, dist in zip(
#             top_25_results['documents'][0],
#             top_25_results['metadatas'][0],
#             top_25_results['distances'][0],
#         )
#     ]
    
    
# Because Chroma always wraps .query() results in one extra outer list,
# since it supports sending multiple queries at once in a single call

# If you'd queried with two strings at once instead:
# collection.query(query_embeddings=[embedding1, embedding2], n_results=25)
# top_25_results['documents'] = [
#     ["doc1", "doc2", ..., "doc25"],   # 25 results for query #1
#     ["doc1", "doc2", ..., "doc25"],   # 25 results for query #2
# ] 
# --    