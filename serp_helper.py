# serp_helper.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def search_google(query):
    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "num": 3  # Try fetching 3 results
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "organic_results" in data and data["organic_results"]:
            results = data["organic_results"]
            top_result = results[0]
            return f"{top_result['title']}\n{top_result['link']}"
        else:
            return "🔎 SERP: No relevant results found."
    except requests.Timeout:
        return "SERP error: Request timed out."
    except Exception as e:
        return f"SERP error: {e}"
