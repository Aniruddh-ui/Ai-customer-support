# app.py
from langdetect import detect
from deep_translator import GoogleTranslator
import gradio as gr
import tempfile
from gtts import gTTS
import speech_recognition as sr

from classifier import classify_query
from sentiment import analyze_sentiment
from rag_helper import retrieve_relevant_faq
from groq_llm import generate_groq_response

from profile_manager import update_profile, get_profile, update_language
from action_agent import detect_action_intent, simulate_action_response

# Debug: Print API keys to verify loading from environment
import os
print("SERP KEY:", os.getenv("SERP_API_KEY"))
print("TAVILY KEY:", os.getenv("TAVILY_API_KEY"))

# Web search helpers
from tavily_helper import tavily_search
from serp_helper import search_google


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

def handle_support_query(text_input, audio_input, language):
    user_text = text_input.strip()
    update_language(language)
    if not user_text:
        # Return the correct number of outputs, with audio_reply as None
        return (
            "",     # category
            "",     # sentiment
            "",     # intent
            "",     # matched_q
            "",     # matched_ans
            "",     # tavily_answer
            "",     # serp_result
            "",     # answer_source
            "",     # ai_reply
            None,   # audio_reply (must be None or (bytes, mime_type))
            "",     # user_text
            ""      # profile_text
        )

    # Detect language (auto)
    auto_lang = detect(user_text)

    # Translate to English if needed (for classification + RAG only)
    translated_text = (
        GoogleTranslator(source='auto', target='en').translate(user_text)
        if auto_lang != "en"
        else user_text
    )

    # Classification & Sentiment
    category = classify_query(translated_text)
    sentiment = analyze_sentiment(translated_text)
    update_profile(user_text, sentiment, category)
    import json
    with open("user_profile.json", "r") as f:
        profile = json.load(f)
    profile_text = json.dumps(profile, indent=2)

    # Detect action-based intent
    intent = detect_action_intent(translated_text)
    action_response = ""
    if intent:
        action_response = simulate_action_response(intent, translated_text)


    # FAQ Retrieval (RAG) with fallback logic
    answer_source = "FAQ"
    if sentiment == "Positive" and category == "General Inquiry":
        matched_q, matched_ans = "", ""
        tavily_answer = ""
        serp_result = ""
    else:
        matched_q, matched_ans = retrieve_relevant_faq(translated_text)
        tavily_answer = ""
        serp_result = ""
        if not matched_q:
            matched_q = "\U0001F4E1 Tavily Web Summary:"
            answer_source = "Tavily"
            try:
                tavily_answer = tavily_search(user_text)
            except Exception as e:
                tavily_answer = f"Tavily Error: {e}"
            if (isinstance(tavily_answer, str) and ("Tavily Error" in tavily_answer or "No answer" in tavily_answer)):
                matched_q = "\U0001F50E SERP Web Result:"
                answer_source = "SERP"
                try:
                    matched_ans = search_google(user_text)
                except Exception as e:
                    matched_ans = f"SERP error: {e}"
            else:
                matched_ans = tavily_answer
        else:
            # For parallel UI display, still fetch Tavily and SERP
            try:
                tavily_answer = tavily_search(user_text)
            except Exception as e:
                tavily_answer = f"Tavily Error: {e}"
            try:
                serp_result = search_google(user_text)
            except Exception as e:
                serp_result = f"SERP error: {e}"


    # LLM Response
    ai_reply = generate_groq_response(
        user_query=user_text,
        category=category,
        sentiment=sentiment,
        matched_faq=f"{matched_q} → {matched_ans}" if matched_q else None,
        language=language
    )

    # Add action response to AI reply if present
    if action_response:
        ai_reply = action_response + "\n\n" + ai_reply

    # TTS with gTTS and fallback (with retry logic)
    import os
    audio_reply = None
    tts_success = False
    for attempt in range(2):
        try:
            tts = gTTS(text=ai_reply)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_reply_path = fp.name
            # Ensure file exists before returning
            if os.path.exists(audio_reply_path):
                audio_reply = (audio_reply_path, "audio/mp3")  # Gradio expects (filepath, mimetype) when type="filepath"
                tts_success = True
                break
            else:
                print(f"TTS file not found: {audio_reply_path}")
                audio_reply = None
                ai_reply += "\n\n(Note: AI voice reply unavailable due to a missing audio file.)"
        except Exception as e:
            audio_reply = None
            print(f"TTS generation failed (attempt {attempt+1}): {e}")
            if attempt == 1:
                ai_reply += "\n\n(Note: AI voice reply unavailable due to a temporary TTS issue.)"

    # Get user profile as pretty JSON string
    profile = get_profile()
    import json
    profile_str = json.dumps(profile, indent=2)

    # Ensure audio_reply is either None or (bytes, mime_type), never a string or other type
    if audio_reply is not None:
        if not (isinstance(audio_reply, tuple) and isinstance(audio_reply[0], (bytes, bytearray)) and isinstance(audio_reply[1], str)):
            print(f"[ERROR] audio_reply has invalid type or value: {type(audio_reply)} | {repr(audio_reply)}. Forcing to None.")
            audio_reply = None
    print(f"[DEBUG] Returning audio_reply type: {type(audio_reply)}, value type: {type(audio_reply[0]) if isinstance(audio_reply, tuple) else None}")
    return (
        category,           # Issue Category
        sentiment,          # Sentiment
        intent,             # Detected Action Intent
        matched_q,          # Closest FAQ (question)
        matched_ans,        # FAQ Answer
        tavily_answer,      # Web Summary (Tavily)
        serp_result,        # Top Link (Google)
        answer_source,      # Info Source (FAQ/Tavily/SERP)
        ai_reply,           # AI Response (Text)
        audio_reply,        # AI Voice Reply (must be None or (bytes, mime_type))
        user_text,          # User Query
        profile_text        # User Profile
    )


# 🎛️ Gradio UI
with gr.Blocks(title="AI Customer Support (Transcribe + Submit)") as demo:
    gr.Markdown("## 🛎️ AI Customer Support\n### 🎤 Speak ➝ 📝 Edit ➝ ✅ Submit")

    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak Your Query")
            transcribe_btn = gr.Button("Transcribe to Text")
            text_input = gr.Textbox(lines=2, label="📝 Transcribed or Typed Query")
            language_selector = gr.Dropdown(
                choices=["English", "Hindi", "Spanish", "French"],
                value="English",
                label="🌐 Preferred Language"
            )
            submit_btn = gr.Button("Submit")

        with gr.Column():
            category_out = gr.Textbox(label="🗂️ Issue Category")
            sentiment_out = gr.Textbox(label="😊 Sentiment")
            intent_out = gr.Textbox(label="🎯 Detected Action Intent")
            faq_q_out = gr.Textbox(label="📄 Closest FAQ")
            faq_a_out = gr.Textbox(label="📘 FAQ Answer")
            tavily_out = gr.Textbox(label="🌐 Web Summary (Tavily)")
            serp_out = gr.Textbox(label="🔗 Top Link (Google)")
            answer_source_out = gr.Textbox(label="🧭 Info Source")
            ai_reply_out = gr.Textbox(label="🤖 AI Response (Text)")
            voice_out = gr.Audio(label="🔊 AI Voice Reply", autoplay=False, type="filepath")
            profile_out = gr.Textbox(label="📋 User Profile", lines=10, interactive=False, visible=False, show_copy_button=True, elem_id="profile-box")
            show_profile_btn = gr.Button("Show User Profile", size="sm")
    # Add custom CSS for scrollable profile box
    demo.stylesheets.append("""
    #profile-box textarea, [data-testid='textbox'] textarea, .svelte-drgfj2 textarea {
        overflow-y: auto !important;
        max-height: 350px !important;
        min-height: 120px;
        resize: vertical !important;
        scrollbar-width: thin !important;
    }
    #profile-box {
        overflow-y: auto !important;
        max-height: 350px !important;
        min-height: 120px;
    }
    """)

    # Step 1: Transcribe
    transcribe_btn.click(fn=transcribe_audio, inputs=audio_input, outputs=text_input)

    # Step 2: Submit
    submit_btn.click(
        fn=handle_support_query,
        inputs=[text_input, audio_input, language_selector],
        outputs=[
            category_out,      # Issue Category
            sentiment_out,     # Sentiment
            intent_out,        # Detected Action Intent
            faq_q_out,         # Closest FAQ
            faq_a_out,         # FAQ Answer
            tavily_out,        # Web Summary (Tavily)
            serp_out,          # Top Link (Google)
            answer_source_out, # Info Source (FAQ/Tavily/SERP)
            ai_reply_out,      # AI Response (Text)
            voice_out,         # AI Voice Reply
            text_input,        # User Query
            profile_out        # User Profile
        ]
    )

    def show_user_profile():
        from profile_manager import load_profile
        profile = load_profile()
        # Ensure all expected fields are present
        profile.setdefault("user_id", "user_001")
        profile.setdefault("preferred_language", "English")
        profile.setdefault("previous_queries", [])
        profile.setdefault("sentiment_history", [])
        profile.setdefault("common_issues", [])
        profile.setdefault("top_issues", [])
        import json
        return json.dumps(profile, indent=2)

    def show_and_reveal_profile():
        from profile_manager import load_profile
        profile = load_profile()
        # Ensure all expected fields are present
        profile.setdefault("user_id", "user_001")
        profile.setdefault("preferred_language", "English")
        profile.setdefault("previous_queries", [])
        profile.setdefault("sentiment_history", [])
        profile.setdefault("common_issues", [])
        profile.setdefault("top_issues", [])
        import json
        return gr.update(visible=True, value=json.dumps(profile, indent=2))

    show_profile_btn.click(fn=show_and_reveal_profile, inputs=None, outputs=profile_out)

if __name__ == "__main__":
    demo.launch()
