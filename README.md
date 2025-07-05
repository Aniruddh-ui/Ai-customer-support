
# 🛒 AI Customer Support Assistant for E-Commerce

An AI-powered multilingual assistant designed to automate and personalize customer support in e-commerce platforms. It uses LLMs, semantic FAQ search, voice interaction, and real-time web search to generate empathetic, helpful responses — all from natural input.

🔗 **Live App on Hugging Face:**  
👉 [Click to Try the App](https://huggingface.co/spaces/Aniruddh-ui/ai-customer-support)

---

## 🚀 Features

- 🎙️ **Voice Input Support** — Speak or type your query
- 🌍 **Multilingual Input** — Supports English, Hindi, Spanish, French
- 🎯 **Smart Classification** — Identifies if it's a complaint, order issue, or inquiry
- 💬 **Sentiment Analysis** — Understands customer emotions
- 🔍 **FAQ Matching (RAG)** — Retrieves closest match using semantic similarity
- 🌐 **Live Web Search** — Uses Tavily & SerpAPI when FAQ fails
- 🤖 **LLM-Powered Responses** — Generates friendly, tailored replies (Groq LLaMA3)
- 🔊 **Text-to-Speech** — Speaks response using gTTS
- 👤 **User Profiling** — Tracks past queries, preferences, and mood history
- 🧠 **Agent Support (Optional)** — Modular agent for FAQ using Fetch.ai uAgents

---

## 🧠 How It Works

1. User speaks or types a query  
2. Language is detected and translated if not English  
3. Text is classified (e.g., order issue, feedback)  
4. Sentiment is analyzed (positive, negative, etc.)  
5. Closest FAQ is retrieved using Sentence Transformers  
6. If no match → Web search via Tavily or SerpAPI  
7. Groq LLaMA3 generates a final empathetic reply  
8. Voice response is generated and shown  
9. User profile is updated with preferences, tone, history

---

## 🛠️ Tech Stack

| Layer              | Tools / APIs                          |
|--------------------|----------------------------------------|
| 🧠 LLM              | Groq LLaMA3-8B                         |
| 📚 RAG (FAQ Match)  | SentenceTransformers (MiniLM)          |
| 🌍 Language & TTS   | gTTS, langdetect, deep_translator       |
| 🗣️ STT              | speech_recognition (Google STT)        |
| 🔍 Web Search       | Tavily API, SerpAPI                    |
| 🎛️ UI               | Gradio                                 |
| 👥 Agent Layer       | Fetch.ai uAgents (FAQ agent)           |
| 📊 Hosting          | Hugging Face Spaces                    |

---

## 🗂️ File Structure

ai-customer-support/
├── app.py # Main Gradio UI + AI pipeline
├── classifier.py # Issue classifier
├── sentiment.py # Sentiment detection
├── rag_helper.py # RAG logic for FAQs
├── groq_llm.py # Groq LLaMA3 integration
├── serp_helper.py # Google search API (SerpAPI)
├── tavily_helper.py # Web search API (Tavily)
├── profile_manager.py # User profile updater
├── action_agent.py # Detect actionable queries
├── messages.py # Agent schemas (for Fetch.ai)
├── faq_agent.py # Optional micro FAQ agent
├── faqs.csv # Preloaded FAQ knowledge base
├── requirements.txt # All required Python packages
└── .env # Secure API keys (not pushed)


---

## 🔧 Local Setup

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/ai-customer-support.git
cd ai-customer-support
Example Queries
Example Input         	Output Type
“Where is my order?”  	FAQ Match
“iPhone 15 offers?”   	Live Web Search
“Cancel my delivery”	  Action Detected
“Quiero saber cuándo llega mi pedido” (Spanish)	Translated → Matched
