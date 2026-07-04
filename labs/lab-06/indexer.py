# This script will fetch the product data, embed it, and save it to disk in three file formats:
    # API : https://dummyjson.com/products

    # products.json: The full "Database" (ID, Title, Description).
    # vectors.tsv: The "Index" (Row 1 corresponds to Product 1).
    # metadata.tsv: A helper file for the Visualization tool.

# Functions defined:
# - fetch_products : Fetches product data from the API and saves it to products.json.
# - create_embedding : Creates embeddings for an array of serialized product strings using the OpenAI API.



import os
import json
import os
import sys
import requests
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


# Locate the .env file by searching up the directory tree
load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Fetch the product data from API and save it to a  products.json file and return the array of products.
def fetch_products():
    api_url = "https://dummyjson.com/products"
    products_array = requests.get(api_url).json()["products"]
    with open("products.json", "w") as file:
        json.dump(products_array, file, indent=4)
    return products_array    
    
        
# This function takes an array of serialized product strings and creates embeddings for them using the OpenAI API.
def create_embedding(serialized_array):
    client= OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY, 
    )
    
    response = client.embeddings.create(
        model= 'openai/text-embedding-3-small',
        input= serialized_array
    )
            
    return response.data
        



        

def main():
    # Check if the OPENROUTER_API_KEY is set in the environment variables
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)
    else:
        print("OPENROUTER_API_KEY found successfully!")
        
    # Fetch the products    
    products_array = fetch_products()
    
    # array of serialized products strings
    from utils import serialize_product
    serialized_products = [] 
    for product in products_array:
        serialized_product = serialize_product(product)
        serialized_products.append(serialized_product)
        # print(serialized_product)
        
    # Create embeddings for the serialized products    
    data = create_embedding(serialized_products)
    
    # For each vector, join its numbers with a tab character (\t) 
    # and write it as a line in the file (i.e., join vector lines with \n).
    for item in data:
        vector = item.embedding
        vector_string = "\t".join(map(str, vector))
        
        # Save the vector string to a file
        with open("vectors.tsv", "a") as file:
            file.write(vector_string + "\n")
            
            
    # Create metatdata.tsv file with title, and category
    with open("metadata.tsv", "w") as file:
         file.write("Title\tCategory\n")  # Write header
         for product in products_array:
             # remove \n and \t from title and category to avoid breaking the tsv format
            title = product.get("title", "").replace("\n", " ").replace("\t", " ")
            category = product.get("category", "").replace("\n", " ").replace("\t", " ")
            file.write(f"{title}\t{category}\n")
         
        
    
    
if __name__ == "__main__":
    main()
     
     
     

## Note: 
# Display results. The response's `data` property will look like this:

# "data": [
#   {
#     "object": "embedding",
#     "index": 0,
#      "embedding": [
#      -0.006929283495992422,
#       -0.005336422007530928,
#      ...
#     ],
#.  },
#   ...
# ],
