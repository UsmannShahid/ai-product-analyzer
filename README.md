# 🧠 AI Product Analyzer

An interactive Streamlit app that helps users search, filter, and analyze products with AI-powered recommendations.

## 🔍 Features

- Search products by **keyword**
- Filter by **category** and **price**
- View detailed product info
- Get **OpenAI GPT-3.5 recommendations**
- Export matched products to JSON
- Track and repeat recent searches

## 🛠️ Tech Stack

- **Streamlit** for frontend and interactivity
- **OpenAI GPT-3.5** for AI suggestions
- **Python** for backend logic
- **FakeStoreAPI** for product data

## 🚀 How to Use

1. Type a keyword (e.g. `shirt`, `laptop`, `bag`)
2. Optionally filter by category or max price
3. View results and get an AI recommendation
4. Download results or repeat past searches

## Requirements
streamlit
openai
python-dotenv
requests

## 📦 Setup (Optional for Local Use)

```bash
git clone https://github.com/your-username/ai-product-analyzer.git
cd ai-product-analyzer
pip install -r requirements.txt
streamlit run app.py


