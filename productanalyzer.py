import requests
from collections import Counter
import json

def fetch_products():
  try:
    response = requests.get("https://fakestoreapi.com/products", timeout=5)
    response.raise_for_status()
    products = response.json()
    # product_list = pd.json_normalize(products)
    return products

  except requests.exceptions.RequestException as e:
    print("Error:", e)
    return None

def filter_products(products, keyword, max_price=None):
  matches = []
  for product in products:
    title = product["title"].lower()
    desc = product["description"].lower()
    category = product["category"].lower()
    price = product["price"]

    if keyword in title or keyword in desc or keyword in category:
      if max_price is None or price <= max_price:
        matches.append(product)
  return matches

def summarize_products(matches):
  if not matches:
    print("No products found matching the keyword.")
    return
    
  total = len(matches)
  avg_price = sum(p["price"] for p in matches) / total
  avg_rating = sum(p["rating"]["rate"] for p in matches) / total
  categories = [p["category"] for p in matches]
  most_common = Counter(categories).most_common(1)[0][0]
  
  #print summary
  print("\n--- Product Summary ---")
  print(f"Total products found: {total}")
  print(f"Average price: ${avg_price:.2f}")
  print(f"Average rating: {avg_rating:.1f}")
  print(f"Most common category: {most_common}")

def export_matches(matches, filename="matches.json"):
  if not matches:
    print("No matches to export.")
    return

  with open(filename, "w") as file:
    json.dump(matches, file, indent=2)
  print(f"Matches exported to {filename}")

print("Product Search Tool")
#1. Fetch product data
products = fetch_products()
if not products:
  print("Failed to fetch products.")
  exit()
#2. Filter products by keyword
keyword = input("Enter a keyword: ").strip().lower()

#Max Price
max_price = None
user_max = input("Do you want to filter by max price? (y/n): ").strip().lower()
if user_max == "y":
  try:
    max_price = float(input("Enter max price: "))
  except ValueError:
    print("Invalid price. Using no max price.")
else:
  max_price = None
#3. Filter products by keyword
matches = filter_products(products, keyword, max_price)
summarize_products(matches)
#5. Ask to export
export = input("Export matches to file? (y/n): ").strip().lower()
if export == "y":
  export_matches(matches)
#4. Show summary

  


  