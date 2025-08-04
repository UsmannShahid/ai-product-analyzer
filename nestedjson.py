from collections import Counter
import requests
import pandas as pd


response = requests.get("https://fakestoreapi.com/products")
products = response.json()

# categories = ["Electronics", "Books", "Electronics", "Books", "Books", "Electronics", "Electronics", "Books"]
# counts = Counter(categories)
# categories = [product["category"] for product in products]
# category_counts = Counter(categories)
# for category, count in category_counts.items():
#   print(f"{category}: {count}")

flat_data = pd.json_normalize(products)
print(flat_data.head())