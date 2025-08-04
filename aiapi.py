import requests
import json

# Step 1: Get user input
keyword = input("Enter a product keyword (e.g. shirt, bag, etc): ").strip().lower()

# Step 2: Fetch product data from FakeStoreAPI
response = requests.get("https://fakestoreapi.com/products")
response.raise_for_status()
products = response.json()

# Step 3: Filter products by keyword
matches = [
    p for p in products
    if keyword in p["title"].lower()
    or keyword in p["description"].lower()
    or keyword in p["category"].lower()
]

# Step 4: If no matches, show a message
if not matches:
    print("No products found matching the keyword.")
else:
    print(f"Found {len(matches)} product(s) matching '{keyword}':")

# Step 5: Prepare product summary for AI (or mock)
product_summary = ""
for product in matches:
    product_summary += f"Title: {product['title']}\n"
    product_summary += f"Description: {product['description']}\n"
    product_summary += f"Category: {product['category']}\n"
    product_summary += f"Price: ${product['price']:.2f}\n"
    product_summary += f"Rating: {product['rating']['rate']} ({product['rating']['count']} reviews)\n"
    product_summary += "-" * 40 + "\n"

# Step 6: Mock AI logic (instead of real API)
recommended = matches[0]['title'] if matches else "No product"
ai_reply = f"🤖 Based on the products listed, I recommend trying: '{recommended}' as it appears first in the filtered results."

# Step 7: Show AI response
print("\n 🤖 AI Recommendation:")
print(ai_reply)
