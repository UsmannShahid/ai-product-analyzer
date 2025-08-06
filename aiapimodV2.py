import requests
import json
import openai
import os
from datetime import datetime

#AI API Key
api_key = os.getenv("Oz_API_Key")


def real_ai_recommendations(matches, keyword):
  api_key = os.getenv("Oz_API_Key")
  client = openai.OpenAI(api_key=api_key)

  prompt = build_prompt(matches, keyword)

  try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "You are a helpful assistant."
        }, {
            "role": "user",
            "content": prompt
        }],
        temperature=0.7,
        max_tokens=256)

    ai_reply = response.choices[0].message.content
    return f"🤖 AI: \n\n{ai_reply}"

  except Exception as e:
    print(f"Error: {e}")


#API Key for Fetching Products
def fetch_products():
  response = requests.get("https://fakestoreapi.com/products")
  response.raise_for_status()
  return response.json()


def filter_products(products, keyword):
  #Fetch product data from FakeStoreAPI and returns JSON list
  matches = [
      p for p in products
      if keyword in p["title"].lower() or keyword in p["description"].lower()
      or keyword in p["category"].lower()
  ]

  if matches:
    return matches
  else:
    return []
  # if not matches:
  #   print("No products found matching the keyword.")
  # else:
  #   print(f"Found {len(matches)} product(s) matching '{keyword}':")

  #   return matches


def prepare_summary(product):
  product_summary = ""
  product_summary += f"\nTitle: {product['title']}\n"
  product_summary += f"Description: {product['description']}\n"
  product_summary += f"Category: {product['category']}\n"
  product_summary += f"Price: ${product['price']:.2f}\n"
  product_summary += f"Rating: {product['rating']['rate']} ({product['rating']['count']} reviews)\n"
  product_summary += "-" * 40 + "\n"
  return product_summary


# def build_prompt(matches, keyword):
#   prompt = f"Analyze the following products matching the keyword '{keyword}':\n\n"
#   for product in matches:
#     prompt += f"- {product['title']} (${product['price']}) - {product['category']}\n"
#     prompt += f"  {product['description'][:100]}...\n\n"
#   prompt += "\nWhich one would you recommend and why?"
#   return prompt

# def mock_ai_recommendations(matches, keyword):
#   prompt = build_prompt(matches, keyword)
#   recommended = matches[0]['title'] if matches else "No product"
#   ai_reply = f"🤖 AI (mock): Based on this prompt...\n{prompt}\n\nRecommendation: Try '{recommended}'."
#   return ai_reply


#AI Prompt Builder
def build_intro(keyword):
  return f"Analyze the following products matching the keyword '{keyword}':\n\n"


def build_product_list(matches):
  product_lines = ""
  for product in matches:
    product_lines += f"- {product['title']} (${product['price']}) - {product['category']}\n"
    product_lines += f"  {product['description'][:100]}...\n\n"

  return product_lines


def build_question():
  return "\nSummarize the key features of each product in 1-2 lines."


def build_prompt(matches, keyword):
  return (build_intro(keyword) + build_product_list(matches) +
          build_question()).strip()


#Export to JSON
def export_to_file(matches, filename="matches.json"):
  with open(filename, "w") as file:
    json.dump(matches, file, indent=2)
    print(f"📁 Results saved to '{filename}' successfully.")


#Helper function to load_from_file
def load_from_file(filename="matches.json"):
  try:
    with open(filename, "r") as file:
      matches = json.load(file)
      return matches
  except FileNotFoundError:
    print(f"File {filename} not found.")
    return []


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
      choice = int(
          input("Enter the number of the category you want to search: "))
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


#Mini Analytics Helper Function
#Helper function to log search history
def log_search_history(keyword, match_count, filename="search_history.json"):
  log_entry = {
      "keyword": keyword,
      "results": match_count,
      "timestamp": datetime.now().isoformat()
  }
  try:
    with open(filename, "r") as file:
      history = json.load(file)
  except FileNotFoundError:  #empty list
    history = []

  history.append(log_entry)
  with open(filename, "w") as file:
    json.dump(history, file, indent=2)


#Helper function to display search history
def view_search_history(filename="search_history.json"):
  try:
    with open(filename, "r") as file:
      history = json.load(file)
      history.sort(key=lambda x: x["timestamp"], reverse=True)
      print("📖 Search History:\n")
      for entry in history:
        dt = datetime.fromisoformat(entry["timestamp"])
        formatted = dt.strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"Keyword: {entry['keyword']}, Results: {entry['results']}, Times: {formatted}"
        )
        print("-" * 40)
  except FileNotFoundError:
    print(f"File {filename} not found.")


#Helper function to get all categories
def get_all_categories(products):
  categories = set(p["category"] for p in products)
  category_list = sorted(categories)
  category_list.insert(0, "All")

  return category_list

# Helper function Streamlit app.py
# Display Product Card Function
def display_product_card(product):
  import streamlit as st
  with st.expander(product["title"]):
      st.markdown(f"💰 **${product['price']}**  |  🏷️ *{product['category']}*")
      st.markdown(f"**Rating:** {product['rating']['rate']} ⭐ ({product['rating']['count']} reviews)")
      st.markdown(product["description"])


  #---------------Main menu function----------------------
def main_menu():
  products = fetch_products()
  cleaned_products = [clean_product_data(p) for p in products]
  matches = []
  keyword = ""

  while True:
    print("\n📦 Product Analyzer Menu")
    print("1️⃣  Search Products")
    print("2️⃣  Export Results")
    print("3️⃣  Get AI Recommendation")
    print("4️⃣  Load Saved Results")
    print("5️⃣  View Search History")
    print("6️⃣  Exit")
    print("-" * 40)

    choice = input("Enter your choice (1-6): ").strip()

    # --- Option 1: Search ---
    if choice == "1":
      while True:
        keyword = input("Enter a product keyword (e.g. shirt, bag, etc):\n "
                        ).strip().lower()
        if keyword:
          print("\n🔍 Searching for products...")
          print("-" * 40)
          break
        print("❗ Keyword cannot be empty. Please try again.")

      matches = filter_products(cleaned_products, keyword)

      if matches:
        print(f"✅ Found {len(matches)} matching products for '{keyword}'")
        print("-" * 40)
        display_product_list(matches)
        log_search_history(keyword, len(matches))
      else:
        print("❌ No products found for that keyword.")

        print("⚠️  No products found matching your keyword.")
        print("🔁 Would you like to try searching by:")

      print("   c️⃣  Category")
      print("   p️⃣  Price range")
      print("   n️⃣  No, go back to main menu")

      fallback = input("Choose an option (c/p/n): ").strip().lower()

      if fallback == "c":
        matches = search_by_category(cleaned_products)
        if matches:
          display_product_list(matches)
        else:
          print("❌ No products found in that category.")
      elif fallback == "p":
        try:
          max_price = float(input("Enter a maximum price: $").strip())
          matches = filter_by_max_price(cleaned_products, max_price)
          if matches:
            display_product_list(matches)
          else:
            print("❌ No products found under that price.")
        except ValueError:
          print("⚠️  Invalid input. Please enter a number.")
      elif fallback == "n":
        print("🔙 Returning to main menu.")
      else:
        print("❓ Invalid option. Returning to main menu.")

    # --- Option 2: Export ---
    elif choice == "2":
      if matches:
        export_to_file(matches)
      else:
        print("📂 No matches to export.")

    # --- Option 3: AI Recommendations ---
    elif choice == "3":
      if matches:
        ask_user = input(
            "Would you like to view the AI prompt before sending? (y/n): "
        ).strip().lower()

        print("\n🤖 Generating AI recommendation...")
        print("-" * 40)

        if ask_user == "y":
          print("📝 Prompt Preview:")
          print(build_prompt(matches, keyword))
          print("-" * 40)

        ai_reply = real_ai_recommendations(matches, keyword)
        print(ai_reply)
      else:
        print("❗ Please search for products first.")

    # --- Option 4: Load from file ---
    elif choice == "4":
      matches = load_from_file()
      if matches:
        display_product_list(matches)
      else:
        print("📂 No matches loaded from file.")

    # --- Option 5: View Search History ---
    elif choice == "5":
      view_search_history()

    # --- Option 6: Exit ---
    elif choice == "6":
      print("👋 Exiting... Goodbye!")
      break

    else:
      print("❓ Invalid choice. Please select a valid option.")


if __name__ == "__main__":
  main_menu()
