import requests
import json


keyword = input("Enter keyword: ").strip().lower()

try:
  response = requests.get("https://fakestoreapi.com/products", timeout=5)
  response.raise_for_status()
  data = response.json()

  matches = []
  for product in data:
    title = product["title"].lower()
    desc = product["description"].lower()
    if keyword in title or keyword in desc:
      matches.append(product)

  if matches:
    print(f"Found {len(matches)} product(s): ")
    for product in matches:
      print("Title:", product["title"])
      print("Price:", product["price"])
      print("-" * 40)

    export_file = input("Export to file? (y/n): ").strip().lower()
    if export_file.lower() == "y":
      with open("search_results.json", "w", newline="") as file:
        json.dump(matches, file, indent=2)

      print("Results exported to search_results.json")
        
  else:
    print("No products found matching the keyword.")

except requests.exceptions.RequestException as e:
  print("Error:", e)
  exit()
