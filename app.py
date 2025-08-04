import streamlit as st
import json
from aiapimodV2 import (
    fetch_products, filter_products, prepare_summary,
    real_ai_recommendations, build_prompt, export_to_file,
    load_from_file, clean_product_data, get_all_categories,
    display_product_list, search_by_category, display_product_card
)

# ----------------- 🧠 Title & Description -----------------
st.title("🧠 AI Product Analyzer")
st.markdown("Easily search, analyze, and export products using AI.")
st.markdown("---")

# ----------------- 🔍 Session State Init -----------------
if "matches" not in st.session_state:
    st.session_state.matches = []

if "search_history" not in st.session_state:
    st.session_state.search_history = []

# ----------------- 🧹 Data Loading (with caching) -----------------
@st.cache_data
def load_cleaned_products():
    products = fetch_products()
    return [clean_product_data(p) for p in products]

cleaned_products = load_cleaned_products()
category_options = get_all_categories(cleaned_products)

# ----------------- 📜 Recent Searches & Repeat Last Search -----------------
selected = None

if st.session_state.search_history:
    st.subheader("📜 Recent Searches")

    # Dropdown to select from recent searches
    options = [
        f"{entry['keyword']} | {entry['category']} | ${entry['max_price']}"
        for entry in st.session_state.search_history
    ]
    selected_index = st.selectbox("Select a previous search:", options, index=None)

    if selected_index is not None:
        # Find the index of the selected option in the options list
        option_index = options.index(selected_index)
        selected = st.session_state.search_history[option_index]

    # Repeat Last Search Button
    if st.button("🔁 Repeat Last Search"):
        if st.session_state.search_history:
            last = st.session_state.search_history[-1]
            # Optional: assign these to prefill inputs on rerun
            st.session_state.keyword = last["keyword"]
            st.session_state.selected_category = last["category"]
            st.session_state.max_price = last["max_price"]
            st.rerun()

    # ----------------- 🔍 Search Input -----------------
keyword = st.text_input(
        "Enter a product keyword (e.g. shirt, bag, etc):",
        value=selected["keyword"] if selected else st.session_state.get("keyword", "")
    ).strip().lower()

with st.expander("🔍 Advanced Search Options"):
        selected_category = st.selectbox(
            "📂 Filter by Category",
            category_options,
            index=category_options.index(
                selected["category"] if selected else st.session_state.get("selected_category", "All")
            )
        )
        max_price = st.number_input(
            "💲 Max Price",
            min_value=0.0,
            step=1.0,
            value=float(selected["max_price"]) if selected else st.session_state.get("max_price", 0.0)
        )


# ----------------- 🔍 Search Logic -----------------
if keyword:
    matches = filter_products(cleaned_products, keyword)

    if selected_category != "All":
        matches = [p for p in matches if p["category"] == selected_category]

    if max_price > 0:
        matches = [p for p in matches if p["price"] <= max_price]

    st.session_state.matches = matches

    # Log search
    st.session_state.search_history.append({
        "keyword": keyword,
        "category": selected_category,
        "max_price": max_price
    })
    st.session_state.search_history = st.session_state.search_history[-5:]

    # ✅ Show filter summary
    st.markdown("### 🔍 Filter Summary")
    st.write(f"Keyword: `{keyword}`")
    st.write(f"Category: `{selected_category}`")
    st.write(f"Max Price: ${max_price if max_price else 'No limit'}")

    if not matches:
        st.warning("⚠️ No products found matching your criteria.")

    else:
        st.markdown("---")
        st.markdown("### 📦 Matching Products")
        for product in matches:
            display_product_card(product)

        # -------- 🤖 AI Recommendation + 📁 Export Buttons --------
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 Get AI Recommendation"):
                with st.spinner("Thinking..."):
                    prompt = build_prompt(matches, keyword)
                    reply = real_ai_recommendations(matches, keyword)
                st.markdown("### 🤖 AI Suggestion")
                st.success(reply)
        with col2:
            json_data = json.dumps(matches, indent=2)
            st.download_button("📁 Download Results", json_data, "matches.json", "application/json")

# ----------------- 🦶 Footer -----------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit and OpenAI")