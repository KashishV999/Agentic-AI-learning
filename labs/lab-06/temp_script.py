# Similarity Threshold: to define a cut-off point where values should be considered usable
# anything below the threshold should be ignored, anything above should be considered usable.

# This is a temporary script to determine the threshold for similarity scores between a query and the product embeddings.
from utils import load_database, dot_product
from indexer import create_embedding

def main():
    products_with_embeddings = load_database()
    
    query_exist="My dog need to eat he is hungry"
    query_not_exist="instructions for repairing a car engine"
    
    query_exist_embedding = create_embedding([query_exist])
    query_not_exist_embedding = create_embedding([query_not_exist])
    
    query_exist_similarity_array = []
    query_not_exist_similarity_array = []
    
    for products in products_with_embeddings:
        product_embedding = products['embedding']
        
        # Calculate similarity for existing query
        similarity_exist = dot_product(query_exist_embedding[0].embedding, product_embedding)
        query_exist_similarity_array.append((products['title'], similarity_exist))
        # print(f"Similarity for existing query '{query_exist}' with product '{products['title']}': {similarity_exist}")
        
        # Calculate similarity for non-existing query
        similarity_not_exist = dot_product(query_not_exist_embedding[0].embedding, product_embedding)
        query_not_exist_similarity_array.append((products['title'], similarity_not_exist))
        # print(f"Similarity for non-existing query '{query_not_exist}' with product '{products['title']}': {similarity_not_exist}")
        
    # Sort the similarity arrays in descending order based on similarity scores
    query_exist_similarity_array.sort(key=lambda x: x[1], reverse=True)
    query_not_exist_similarity_array.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Top 3 matches for '{query_exist}':")
    for title, score in query_exist_similarity_array[:3]:
        print(f"  {title}: {score}")
    
    print(f"Top 3 matches for '{query_not_exist}':")
    for title, score in query_not_exist_similarity_array[:3]:
        print(f"  {title}: {score}")


if __name__ == "__main__":
    main()




# What was the similarity score for a "Good Match" (e.g., "Fruit" -> "Apple")?
# It was ~0.4
# Top 3 matches for 'Nice smelling scent':
#   Gucci Bloom Eau de: 0.41121359565840976
#   Dior J'adore: 0.40080544559558007
#   Dolce Shine Eau de: 0.3883764025846972

# What was the similarity score for a "Bad Match" (e.g., "Quantum Physics" -> "Mascara")?
# It was ~0 .13
# Top 3 matches for “Quantum mechanics”:
#   Calvin Klein CK One: 0.1358192451045852
#   Powder Canister: 0.12253618038397462
#   Dior J'adore: 0.11039135967615721

# What value did you choose for your MIN_SIMILARITY_SCORE?
# I chose 0.2 for min similarity score
