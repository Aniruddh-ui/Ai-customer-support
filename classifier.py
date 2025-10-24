# classifier.py

def classify_query(query):
    query = query.lower()
    if "refund" in query or "money back" in query:
        return "Refund Request"
    elif "cancel" in query:
        return "Order Cancellation"
    elif "order" in query and ("not received" in query or "delayed" in query or "late" in query):
        return "Order Issue"
    elif "return" in query:
        return "Return Request"
    elif "track" in query or "tracking" in query:
        return "Order Tracking"
    elif "payment" in query or "bill" in query:
        return "Payment Issue"
    elif "support" in query or "contact" in query:
        return "Customer Support"
    elif "thank" in query or "happy" in query or "love" in query:
        return "Positive Feedback"
    else:
        return "General Inquiry"
