import requests

response = requests.get("https://fakestoreapi.com/products")
data = response.json()
product_count = len(data)
print("Total products:", product_count)
print("-" * 40)

categories = set(product["category"] for product in data)
print("Categories:", categories)
for category in categories:
  print("-", category)


user_cat = input("Enter category: ").strip().lower()

matches = [p for p in data if p["category"].lower() == user_cat]

if matches:
  for product in matches:
    print("Title:", product["title"])
    print("Price:", product["price"])
    print("Category:", product["category"])
    print("-" * 40)
else:
  print("No products found in the specified category.")
# for product in data:
#   if product["category"] == user_cat:
#     print("Title:", product["title"])
#     print("Price:", product["price"])
#     print("Category:", product["category"])
#     print("-" * 40)