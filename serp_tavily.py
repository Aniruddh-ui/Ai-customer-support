# serp_tavily.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def fetch_web_summary(query):
    try:
        # 1. Try SERP API
        serp_url = "https://serpapi.com/search.json"
        params = {"q": query, "num": 3, "api_key": SERP_API_KEY}
        serp_res = requests.get(serp_url, params=params).json()
        snippet = serp_res.get("organic_results", [{}])[0].get("snippet", "")
        return snippet if snippet else "No relevant result from SERP."

    except Exception as e1:
        print("SERP error:", e1)

    try:
        # 2. Fallback to Tavily
        tavily_url = "https://api.tavily.com/search"
        headers = {"Authorization": f"Bearer {TAVILY_API_KEY}", "Content-Type": "application/json"}
        data = {"query": query, "num_results": 1}
        tavily_res = requests.post(tavily_url, headers=headers, json=data).json()
        summary = tavily_res.get("results", [{}])[0].get("content", "")
        return summary if summary else "No result from Tavily."
    except Exception as e2:
        print("Tavily error:", e2)
        return "Failed to fetch from web."
