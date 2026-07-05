from utils import load_database, search_products
import json


def main():
    products_with_embeddings = load_database()
    
    
    while True:
        
        user_input  = input("Enter your search query (or type 0 to quit): ")
        
        if user_input  == "0":
            break # Exit the loop immediately
        
        results = search_products(user_input , products_with_embeddings, min_score=0.2)
        if  len(results) == 0:
            print(f"I'm sorry, we don't have anything like that in stock.")
            continue
        
        else:
            print(f"Top {len(results)} results for '{user_input }':")
            i=0
            for result in results:
                print(f"{i}.[ Rerank: {result['rerank_score']:.4f} | Vector: {result['similarity_score']:.4f} ] Title: {result['title']} - {result['price']}")
                i += 1
            
        



if __name__ == "__main__":
    main()