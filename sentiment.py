# sentiment.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_sentiment(user_query):
    prompt = f"""
You are a sentiment analysis expert.

Classify the following user message as one of:
- Positive
- Neutral
- Negative

User message: "{user_query}"

Respond only with the sentiment label (one word).
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        result = response.json()

        # Debug: print Groq sentiment output
        print("Sentiment raw response:", result)

        if "choices" in result:
            sentiment = result["choices"][0]["message"]["content"].strip().capitalize()
            return sentiment if sentiment in ["Positive", "Neutral", "Negative"] else "Neutral"
        else:
            return "Neutral"

    except Exception as e:
        return f"Error detecting sentiment: {str(e)}"
