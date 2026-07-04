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


        
    
    
    

        
        
        