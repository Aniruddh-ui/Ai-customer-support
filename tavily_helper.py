# tavily_helper.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def tavily_search(query):
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {TAVILY_API_KEY}"}
    data = {
        "query": query,
        "search_depth": "basic",  # or "advanced" if needed
        "include_answer": True
    }

    try:
        res = requests.post(url, headers=headers, json=data, timeout=15)
        res.raise_for_status()
        response = res.json()
        return response.get("answer", "No answer found via Tavily.")
    except requests.Timeout:
        return "Tavily Error: Request timed out."
    except Exception as e:
        return f"Tavily Error: {e}"
