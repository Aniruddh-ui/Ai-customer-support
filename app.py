# app.py

import gradio as gr
import tempfile
from gtts import gTTS
import speech_recognition as sr

from classifier import classify_query
from sentiment import analyze_sentiment
from rag_helper import retrieve_relevant_faq
from groq_llm import generate_groq_response


# Step 1: Voice to Text (Transcription Only)
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except Exception:
        return "Could not understand audio."


# Step 2: Run AI pipeline and generate TTS audio
def handle_support_query(user_text):
    user_text = user_text.strip()
    if not user_text:
        return "", "", "", "", "", None

    # Classification & Sentiment
    category = classify_query(user_text)
    sentiment = analyze_sentiment(user_text)

    # FAQ Retrieval
    if sentiment == "Positive" and category == "General Inquiry":
        matched_q, matched_ans = "", ""
    else:
        matched_q, matched_ans = retrieve_relevant_faq(user_text)

    if not matched_q:
        matched_q = "No relevant FAQ found for your question. Our team will get back to you soon."
    if not matched_ans:
        matched_ans = "—"

    # LLM Response
    ai_reply = generate_groq_response(
        user_query=user_text,
        category=category,
        sentiment=sentiment,
        matched_faq=f"{matched_q} → {matched_ans}" if matched_q else None
    )

    # TTS with gTTS and fallback
    try:
        tts = gTTS(text=ai_reply)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            audio_reply = fp.name
    except Exception as e:
        print("TTS Error:", e)
        audio_reply = None
        ai_reply += "\n\n(Note: AI voice reply unavailable due to a temporary TTS issue.)"

    return category, sentiment, matched_q, matched_ans, ai_reply, audio_reply


# 🎛️ Gradio UI
with gr.Blocks(title="AI Customer Support (Transcribe + Submit)") as demo:
    gr.Markdown("## 🛎️ AI Customer Support\n### 🎤 Speak ➝ 📝 Edit ➝ ✅ Submit")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak Your Query")
            transcribe_btn = gr.Button("Transcribe to Text")
            text_input = gr.Textbox(lines=2, label="📝 Transcribed or Typed Query")
            submit_btn = gr.Button("Submit")

        with gr.Column():
            category_out = gr.Textbox(label="🗂️ Issue Category")
            sentiment_out = gr.Textbox(label="😊 Sentiment")
            faq_q_out = gr.Textbox(label="📄 Closest FAQ")
            faq_a_out = gr.Textbox(label="📘 FAQ Answer")
            ai_reply_out = gr.Textbox(label="🤖 AI Response (Text)")
            voice_out = gr.Audio(label="🔊 AI Voice Reply", autoplay=False)

    # Step 1: Transcribe
    transcribe_btn.click(fn=transcribe_audio, inputs=audio_input, outputs=text_input)

    # Step 2: Submit
    submit_btn.click(fn=handle_support_query, inputs=text_input, outputs=[
        category_out, sentiment_out, faq_q_out, faq_a_out, ai_reply_out, voice_out
    ])

if __name__ == "__main__":
    demo.launch()
