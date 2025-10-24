# groq_llm.py

import os
import requests

# Hugging Face Secrets: GROQ_API_KEY must be set in Hugging Face Space Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_groq_response(user_query, category, sentiment, matched_faq=None, language="English"):
    if not GROQ_API_KEY:
        return "❌ Missing Groq API key. Please set GROQ_API_KEY in Hugging Face Secrets."

    # Optional FAQ section for RAG
    faq_instruction = f"\nRelevant FAQ:\n{matched_faq}\n" if matched_faq else ""

    # Translation instruction
    translate_instruction = ""
    if language and language != "English":
        translate_instruction = f"\nPlease translate the final response to {language}."

    # Prompt
    prompt = f"""
You are an AI customer support assistant. Always sign your responses as [AI Customer Care].

User Query: "{user_query}"

Issue Category: {category}
Sentiment: {sentiment}
{faq_instruction}
{translate_instruction}

Generate a professional, helpful, and empathetic response for the user. Sign off as [AI Customer Care].
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return "⚠️ Groq API returned no response."

    except requests.Timeout:
        return "Groq error: Request timed out."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error from Groq: {http_err}"
    except Exception as e:
        return f"Groq error: {str(e)}"
