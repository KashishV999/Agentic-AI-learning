# - serialize_product : convert to a single string format
# - dot_product : compute the dot product of two vectors
# - load_database : load products.json and vectors.tsv and combine them into a list of products with embeddings
# - search_products : search for products based on a query and return the top 20 results with a minimum similarity score
# - rerank_results : rerank the top N results using the OpenRouter API and return the reranked results with their relevance scores

import os
import requests
import json
from typing import List, Dict, Any
from indexer import create_embedding
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# This function takes a product dictionary and serializes it into a single string format. 
# Eg: "Title: Dolce Shine Eau de | Category: fragrances | Description: Dolce Shine by Dolce & Gabbana is a vibrant and fruity fragrance, featuring notes of mango, jasmine, and blonde woods. It's a joyful and youthful scent. | Tags: fragrances, perfumes | Brand: Dolce & Gabbana";
# check if the key exists before accessing it to avoid keyError. If the key does not exist, it will return an not include that key
def serialize_product(product):
    parts = []
    
    if product.get('title'):
        parts.append(f"Title: {product['title']}")
    if product.get('category'):
        parts.append(f"Category: {product['category']}")
    if product.get('description'):
        parts.append(f"Description: {product['description']}")
    if product.get('tags'):
        parts.append(f"Tags: {', '.join(product['tags'])}")
    if product.get('brand'):
        parts.append(f"Brand: {product['brand']}")
    
    return " | ".join(parts)


# This function takes two vectors (lists of floats) and computes their dot product.
def dot_product(vec_a: list[float], vec_b: list[float]) -> float:
    return sum(a * b for a, b in zip(vec_a, vec_b))



# This function takes 2 lists -> one of products and one of vectors and then use the
# zip() function to combine them into a single list of dictionaries, 
# where each dictionary contains a product and its corresponding vector.
def load_database() -> list[dict]:
    # 1. Read the JSON file
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f) # list[dict]

    # 2. Read the TSV file
    with open('vectors.tsv', 'r', encoding='utf-8') as f:
        vectors_data = f.read()
        lines = vectors_data.strip().split('\n') # list[string], each string is a line in the file

    # 3. Attach vectors to products
    # Python's zip() function pairs the two lists automatically
    products_with_embeddings = []

    for product, line in zip(products, lines):
        # Convert tab-separated values to a list of floats
        vector = [float(x) for x in line.split('\t')]

        # Add the embedding to the product dictionary
        product['embedding'] = vector
        products_with_embeddings.append(product)

    return products_with_embeddings


# Test
# def main():
#     # Example product dictionary
#     product = {
#         "title": "Dolce Shine Eau de",
#         "category": "fragrances",
#         "description": "Dolce Shine by Dolce & Gabbana is a vibrant and fruity fragrance, featuring notes of mango, jasmine, and blonde woods. It's a joyful and youthful scent.",
#         "tags": ["fragrances", "perfumes"],
#         "brand": "Dolce & Gabbana"
#     }

#     serialized_product = serialize_product(product)
#     print(serialized_product)
    
    
# if __name__ == "__main__":
#     main()



def rerank_results(
    query: str,
    candidates: list[dict],
    top_n: int = 5
) -> list[dict]:
    documents = [
        serialize_product(p) for p in candidates
    ]

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

    return [
        {**candidates[r['index']],
         'rerank_score': r['relevance_score']}
        for r in data['results']
    ]

# Flow of the search_products function:        
#   // 1. Embed the query
#   // 2. Calculate dot product against all products
#   // 3. Sort by score (descending)
#   // 4. Filter out anything below minScore
#   // 5. Attach the vector score to each candidate
#   // 6. Take top 20 candidates (wider net)
#   // 7. If no candidates, return []
#   // 8. Rerank the candidates and return top 5

def search_products(
    query: str,
    products: List[Dict[str, Any]],
    min_score: float = 0.2
) -> List[Dict[str, Any]]:
    # 1. Embed the query
    query_embedding= create_embedding([query])
    # 2. Calculate dot product of query embedding and all product embeddings
    products_with_embeddings = load_database()
    
    
    for product in products_with_embeddings:
        product_embedding = product['embedding']
        similarity_score = dot_product(query_embedding[0].embedding, product_embedding)
        product['similarity_score'] = similarity_score
        
    # 3. Sort by score (descending)
    products_with_embeddings.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    
    # # Take the wide net 
    # top_20_candidates = products_with_embeddings[:20]

    # #  Filter out anything below minScore
    # top_20_candidates = [p for p in top_20_candidates if p['similarity_score'] >= min_score]
    
    # 4. Filter out anything below minScore
    filtered_products = [product for product in products_with_embeddings if product['similarity_score'] >= min_score]
    # 5. Return top 20 results
    top_20_candidates = filtered_products[:20]

    if not top_20_candidates:
        return []

    return rerank_results(query, top_20_candidates, top_n=5)


    
    

        
        
        