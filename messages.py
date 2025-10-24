# messages.py

from uagents import Model  # ✅ Correct import path

class UserQuery(Model):
    text: str

class FAQResponse(Model):
    question: str
    answer: str
