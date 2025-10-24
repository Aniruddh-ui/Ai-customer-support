import re

def detect_action_intent(user_text: str) -> str:
    text = user_text.lower()

    if "track" in text and ("order" in text or "package" in text):
        return "Track Order"
    elif "cancel" in text and "order" in text:
        return "Cancel Order"
    elif "refund" in text:
        return "Request Refund"
    elif "return" in text:
        return "Return Product"
    elif "address" in text and ("change" in text or "modify" in text):
        return "Modify Address"
    elif "invoice" in text:
        return "Request Invoice"
    else:
        return None


def simulate_action_response(intent: str, user_text: str) -> str:
    match = re.search(r"#?(\d{4,})", user_text)
    order_id = match.group(1) if match else "[order number]"

    if intent == "Track Order":
        return f"📦 Order #{order_id} is currently in transit. Expected delivery in 2 days."

    elif intent == "Cancel Order":
        return f"❌ Order #{order_id} has been submitted for cancellation. Confirmation will be emailed to you."

    elif intent == "Request Refund":
        return f"💸 Refund process started for order #{order_id}. The amount will be credited within 3–5 business days."

    elif intent == "Return Product":
        return f"🔄 A return request for item #{order_id} has been registered. You’ll receive pickup details soon."

    elif intent == "Modify Address":
        return f"✍️ We’ve received your address modification request. Kindly confirm your new address via email."

    elif intent == "Request Invoice":
        return f"📧 Invoice for order #{order_id} has been sent to your registered email."

    return "✅ Request received. Our team will take action shortly."
