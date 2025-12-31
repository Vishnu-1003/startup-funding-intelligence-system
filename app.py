# ==========================================
# app.py — Startup Funding Intelligence System
# Conversational RAG + PREMIUM Light Chat UI
# ==========================================

import streamlit as st
import json
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from langdetect import detect

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Startup Funding Intelligence",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# PREMIUM CHATGPT‑STYLE LIGHT UI (UI ONLY)
# ==========================================
st.markdown("""
<style>
/* Page */
body {
    background-color: #f9fafb;
}
.block-container {
    max-width: 820px;
    padding-top: 1.5rem;
    padding-bottom: 6rem;
}

/* Chat rows */
.chat-row {
    display: flex;
    margin-bottom: 14px;
}

.chat-user {
    justify-content: flex-end;
}

.chat-bot {
    justify-content: flex-start;
}

/* Bubbles */
.bubble-user {
    background-color: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.5;
}

.bubble-bot {
    background-color: #ffffff;
    color: #0f172a;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.5;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

/* Role label */
.role {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 4px;
}

/* Input bar */
.input-wrapper {
    position: fixed;
    bottom: 16px;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 820px;
    background: #ffffff;
    border-radius: 14px;
    box-shadow: 0 -2px 14px rgba(0,0,0,0.08);
    padding: 10px;
    z-index: 100;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #e5e7eb;
    font-size: 15px;
}

/* Buttons */
.stButton button {
    border-radius: 12px;
    height: 44px;
}

/* Footer */
.footer {
    color: #64748b;
    font-size: 13px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("## 🚀 Startup Funding Intelligence System")
st.caption(
    "GenAI‑powered • RAG‑based • Multilingual • Policy‑backed funding assistant"
)

# ==========================================
# CHAT MEMORY
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_resource
def load_chunks():
    with open("funding_chunks_layered.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

@st.cache_resource
def load_vector_db(chunks):
    client = chromadb.Client()
    collection = client.create_collection("startup_funding_rag")

    documents, metadatas, ids = [], [], []
    for i, chunk in enumerate(chunks):
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])
        ids.append(str(i))

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    return collection

chunks = load_chunks()
embedding_model = load_embedding_model()
collection = load_vector_db(chunks)

# ==========================================
# LLM CONFIG
# ==========================================
genai.configure(api_key="AIzaSyCM05wNxYU395jsDE-LYz_I5-Eu5HVz3CU")
llm = genai.GenerativeModel("models/gemini-2.5-flash")

# ==========================================
# HELPERS (UNCHANGED)
# ==========================================
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def detect_intent(query):
    q = query.lower()
    if "compare" in q or "difference" in q:
        return "compare"
    elif "recommend" in q or "suggest" in q:
        return "recommend"
    elif "eligible" in q:
        return "eligibility"
    else:
        return "general"

def retrieve_chunks(query, k):
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return results["documents"][0]

def translate_to_english(text):
    prompt = f"""
Translate the following text to English.
Return ONLY the translated text.

Text:
{text}
"""
    response = llm.generate_content(prompt)
    return response.text.strip()

# ==========================================
# CORE CONVERSATIONAL RAG (UNCHANGED)
# ==========================================
def generate_answer(query):
    user_lang = detect_language(query)
    intent = detect_intent(query)

    if user_lang != "en":
        retrieval_query = translate_to_english(query)
    else:
        retrieval_query = query

    k = 8 if intent == "compare" else 5
    retrieved_chunks = retrieve_chunks(retrieval_query, k)
    context = "\n\n".join(retrieved_chunks)

    recent_history = st.session_state.chat_history[-4:]
    conversation_context = ""
    for turn in recent_history:
        conversation_context += f"User: {turn['user']}\n"
        conversation_context += f"Assistant: {turn['assistant']}\n"

    language_map = {
        "en": "Answer strictly in English.",
        "hi": "Answer strictly in Hindi.",
        "ta": "Answer strictly in Tamil.",
        "te": "Answer strictly in Telugu.",
        "ml": "Answer strictly in Malayalam."
    }

    language_instruction = language_map.get(user_lang, "Answer strictly in English.")

    prompt = f"""
You are an AI assistant for startup funding in India.

STRICT RULES:
- {language_instruction}
- Use ONLY the provided context.
- Do NOT invent schemes, amounts, or eligibility.
- Do NOT hallucinate.

ALLOWED REASONING:
- Compare schemes using retrieved facts.
- Provide stage-based or conditional guidance.
- Do NOT provide absolute rankings.

Conversation so far:
{conversation_context}

Retrieved Policy Context:
{context}

User Question:
{query}

Answer:
"""

    response = llm.generate_content(prompt)
    answer = response.text.strip()

    st.session_state.chat_history.append({
        "user": query,
        "assistant": answer
    })

    return answer

# ==========================================
# CHAT DISPLAY (PREMIUM)
# ==========================================
for chat in st.session_state.chat_history:
    st.markdown(
        f"""
        <div class="chat-row chat-user">
            <div>
                <div class="role">You</div>
                <div class="bubble-user">{chat['user']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="chat-row chat-bot">
            <div>
                <div class="role">Assistant</div>
                <div class="bubble-bot">{chat['assistant']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# INPUT BAR
# ==========================================
st.markdown("<div class='input-wrapper'>", unsafe_allow_html=True)

query = st.text_input(
    "",
    placeholder="Ask about startup funding, grants, eligibility...",
    key="chat_input"
)

col1, col2 = st.columns([6, 1])

with col1:
    send = st.button("Send 🚀")

with col2:
    clear = st.button("Clear")

if send and query.strip():
    with st.spinner("Thinking..."):
        generate_answer(query)
    st.rerun()

if clear:
    st.session_state.chat_history = []
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown(
    "<div class='footer'>Powered by Generative AI • RAG • Multilingual • Hackathon‑Ready</div>",
    unsafe_allow_html=True
)
