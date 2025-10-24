# faq_agent.py

from uagents import Agent, Context, Protocol
from messages import UserQuery, FAQResponse
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# ✅ Replace with your own generated seed string
FAQ_AGENT_SEED = "3d9c84f1a0371607a9070d7f8285f84ecf3b518d61891ad9acd4486799f3ce2f"

# Load FAQs and generate embeddings
faq_df = pd.read_csv("faqs.csv")
faq_questions = faq_df["question"].tolist()
faq_answers = faq_df["answer"].tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

# FAQ agent setup
faq_agent = Agent(name="FAQ Agent", seed=FAQ_AGENT_SEED, endpoint="http://127.0.0.1:8000/")

faq_protocol = Protocol(name="FAQProtocol")

@faq_protocol.on_message(model=UserQuery)
async def handle_query(ctx: Context, sender: str, msg: UserQuery):
    ctx.logger.info(f"Received query from {sender}: {msg.text}")
    
    user_emb = model.encode(msg.text, convert_to_tensor=True)
    similarities = util.cos_sim(user_emb, faq_embeddings)[0]
    best_idx = int(similarities.argmax())
    best_score = float(similarities[best_idx])
    threshold = 0.75

    if best_score >= threshold:
        question = faq_questions[best_idx]
        answer = faq_answers[best_idx]
    else:
        question = "No relevant FAQ found for your question."
        answer = "—"

    await ctx.send(sender, FAQResponse(question=question, answer=answer))

# Register protocol and run
faq_agent.include(faq_protocol)

if __name__ == "__main__":
    faq_agent.run()
