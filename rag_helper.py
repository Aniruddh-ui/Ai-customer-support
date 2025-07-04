# rag_helper.py

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAQ data
faq_df = pd.read_csv("faqs.csv")
faq_questions = faq_df["question"].astype(str).tolist()
faq_answers = faq_df["answer"].astype(str).tolist()
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def retrieve_relevant_faq(user_query, threshold=0.45):
    # Embed the user query
    user_emb = model.encode(user_query, convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.cos_sim(user_emb, faq_embeddings)[0]

    # Get the best match
    best_idx = int(similarities.argmax())
    best_score = float(similarities[best_idx])

    print(f"[RAG Match] Score: {best_score:.2f} | Query: {user_query} | Matched: {faq_questions[best_idx]}")

    if best_score < threshold:
        return None, None  # Force fallback to Tavily/SERP

    return faq_questions[best_idx], faq_answers[best_idx]
