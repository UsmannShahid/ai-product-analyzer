import requests
import json

def fetch_products():
  response = requests.get("https://fakestoreapi.com/products")
  response.raise_for_status()
  return response.json()

def filter_products(products, keyword):
  #Fetch product data from FakeStoreAPI and returns JSON list
  matches = [
    p for p in products
    if keyword in p["title"].lower()
    or keyword in p["description"].lower()
    or keyword in p["category"].lower()
  ]
  if not matches:
    print("No products found matching the keyword.")
  else:
    print(f"Found {len(matches)} product(s) matching '{keyword}':")
          
    return matches

def prepare_summary(product):
  product_summary = ""
  product_summary += f"\nTitle: {product['title']}\n"
  product_summary += f"Description: {product['description']}\n"
  product_summary += f"Category: {product['category']}\n"
  product_summary += f"Price: ${product['price']:.2f}\n"
  product_summary += f"Rating: {product['rating']['rate']} ({product['rating']['count']} reviews)\n"
  product_summary += "-" * 40 + "\n"
  return product_summary

def build_prompt(matches, keyword):
  prompt = f"Analyze the following products matching the keyword '{keyword}':\n\n"
  for product in matches:
    prompt += f"- {product['title']} (${product['price']}) - {product['category']}\n"
    prompt += f"  {product['description'][:100]}...\n\n"
  prompt += "\nWhich one would you recommend and why?"
  return prompt

def mock_ai_recommendations(matches, keyword):
  prompt = build_prompt(matches, keyword)
  recommended = matches[0]['title'] if matches else "No product"
  ai_reply = f"🤖 AI (mock): Based on this prompt...\n{prompt}\n\nRecommendation: Try '{recommended}'."
  return ai_reply

def export_to_file(matches, filename="matches.json"):
  with open(filename, "w") as file:
    json.dump(matches, file, indent=2)
    print(f"Matches exported to {filename}")

#Helper function to clean product data
def clean_product_data(product):
  title = product.get("title", "")
  price = product.get("price", 0.0)
  category = product.get("category", "")
  description = product.get("description", "")
  rating = product.get("rating", {"rate": 0, "count": 0})

  clean_product_dict = {
    "title": title,
    "price": price,
    "category": category,
    "description": description,
    "rating": rating
  }

  return clean_product_dict
#Helper function to display product list
def display_product_list(products):
  for p in products:
    print(prepare_summary(p))
    
#Helper function to search for products by category 
def search_by_category(products):
  categories = set(p["category"] for p in products)
  category_list = list(categories)
  category_list_sorted = sorted(category_list)

  for i, category in enumerate(category_list_sorted):
    print(f"{i+1}. {category}")

  while True:
    try:
      choice = int(input("Enter the number of the category you want to search: "))
      if 1 <= choice <= len(category_list_sorted):
        category = category_list_sorted[choice - 1]
        #filter products by selected category
        filtered_products = [p for p in products if p["category"] == category]
        return filtered_products
      else:
        print("Invalid choice. Please try again.")
    except ValueError:
      print("Invalid input. Please enter a number.")

# Helper function to filter products by max price
def filter_by_max_price(products, max_price):
  filtered_products = [p for p in products if p["price"] <= max_price]
  return filtered_products
  

#---------------Main menu function----------------------
def main_menu():
  # Step 1: Load and clean data
  products = fetch_products()
  cleaned_products = [clean_product_data(p) for p in products]
  
  matches = [] # Holds latest search results
  keyword = ""
  
  # Step 2: Main loop
  while True:
    print("\n--- Main Menu ---")
    print("1. Search for products")
    print("2. Export results")
    print("3. Get Ai recommendation")
    print("4. Search by category")
    print("5. Search by max price")
    print("6. Exit")

    choice = input("Enter your choice: ").strip()
    # --- Option 1: Search ---
    if choice == "1":
      while True:
        keyword = input("Enter a product keyword (e.g. shirt, bag, etc):\n ").strip().lower()
        if keyword:
          break
        print("Keyword cannot be empty. Please try again.")
        
      matches = filter_products(cleaned_products, keyword)
      
      if matches:
        display_product_list(matches)
      else:
        print("No products found matching the keyword.")
        
        #Fallback Logic If No Keyword Matches
        fallback = input("Would you like to search by (c)ategory or (p)rice? (c/p): ").strip().lower()

        if fallback == "c":
          matches = search_by_category(cleaned_products)
          if matches:
            display_product_list(matches)
            
        elif fallback == "p":
          try:
            max_price = float(input("Enter max price: "))
            matches = filter_by_max_price(cleaned_products, max_price)
            if matches:
              display_product_list(matches)
            else:
              print("No products found within the specified price range.")
          except ValueError:
            print("Invalid price. Please enter a valid number.")
        
    # --- Option 2: Export ---
    elif choice == "2":
      if matches:
        export_to_file(matches)
      else:
        print("No matches to export.")
    # --- Option 3: AI Recommendations ---
    elif choice == "3":
      if matches:
        ai_reply = mock_ai_recommendations(matches, keyword)
        print(ai_reply)
      else:
        print("Search for products first.")
    # --- Option 4: Search by category ---
    elif choice == "4":
      matches = search_by_category(cleaned_products)
      if matches:
        display_product_list(matches)
    # --- Option 5: Search by max price ---
    elif choice == "5":
      try:
        max_price = float(input("Enter max price: "))
        matches = filter_by_max_price(cleaned_products, max_price)
        if matches:
          display_product_list(matches)
        else:
          print("No products found within the specified price range.")
      except ValueError:
        print("Invalid price. Please enter a valid number.")
    # --- Option 6: Exit ---
    elif choice == "6":
      print("Exiting...")
      break
      
    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main_menu()
