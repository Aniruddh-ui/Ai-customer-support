# rag_helper.py

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load and embed FAQs
faq_df = pd.read_csv("faqs.csv")
faq_questions = faq_df["question"].tolist()
faq_answers = faq_df["answer"].tolist()
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def retrieve_relevant_faq(user_query, threshold=0.7):
    # Increase threshold for stricter matching
    threshold = 0.8
    user_emb = model.encode(user_query, convert_to_tensor=True)
    similarities = util.cos_sim(user_emb, faq_embeddings)[0]
    best_idx = int(similarities.argmax())
    best_score = float(similarities[best_idx])
    if best_score < threshold:
        return "No relevant FAQ found for your question. Our team will get back to you soon.", ""
    return faq_questions[best_idx], faq_answers[best_idx]
