# startup-funding-intelligence-system
GenAI-Powered Startup Funding Intelligence System
================================================

A Generative AI + Retrieval-Augmented Generation (RAG) based conversational system
that helps students and startup founders discover, compare, and understand
government funding schemes using official policy documents.

------------------------------------------------
PROBLEM STATEMENT
------------------------------------------------
Startup founders and students face difficulty in:
- Finding relevant government funding schemes
- Understanding complex policy documents
- Comparing Central and State funding options
- Accessing information in regional languages

Most existing solutions are static, English-only, and non-conversational.

------------------------------------------------
SOLUTION OVERVIEW
------------------------------------------------
This project provides a conversational, policy-backed assistant that:
- Uses Retrieval-Augmented Generation (RAG)
- Avoids hallucination by relying only on official documents
- Supports comparison between funding schemes
- Works in multiple Indian languages
- Maintains short-term conversational memory

------------------------------------------------
SYSTEM ARCHITECTURE (HIGH LEVEL)
------------------------------------------------
User
 -> Streamlit Chat UI
 -> Language & Intent Detection
 -> Semantic Embeddings
 -> Vector Database (ChromaDB)
 -> RAG Orchestration
 -> GenAI Reasoning (Google Gemini)
 -> Explainable Answer

------------------------------------------------
REPOSITORY STRUCTURE
------------------------------------------------
app.py
funding_chunks_layered.json
data_chunking.ipynb
retrieval.ipynb
requirements.txt
README.txt

------------------------------------------------
FILE EXPLANATION
------------------------------------------------

1. app.py
----------
- Main Streamlit application
- ChatGPT-style UI
- Conversational memory using session state
- Language detection and translation
- Intent detection (general / compare / recommend)
- Vector search using ChromaDB
- RAG orchestration
- GenAI reasoning using Google Gemini API

This is the final deployed application.

2. data_chunking.ipynb
---------------------
- Used in Google Colab
- Cleans and preprocesses government policy documents
- Splits documents into meaningful text chunks
- Adds metadata (scheme name, state, category)
- Outputs funding_chunks_layered.json

Used only during data preparation.

3. retrieval.ipynb
------------------
- Used for experimentation and validation
- Tests semantic search and retrieval accuracy
- Experiments with top-K retrieval values
- Validates the embedding and RAG pipeline

Used during development and testing.

4. funding_chunks_layered.json
------------------------------
- Stores chunked policy text
- Includes metadata for each chunk
- Acts as the main knowledge source for the system

------------------------------------------------
AI TECHNOLOGIES USED
------------------------------------------------
- Google Gemini API (Gemini 2.5 Flash) for Generative AI
- Retrieval-Augmented Generation (RAG)
- Sentence-Transformers (paraphrase-multilingual-MiniLM-L12-v2)
- ChromaDB (Vector Database)
- langdetect for language detection

------------------------------------------------
MULTILINGUAL SUPPORT
------------------------------------------------
- Detects user input language automatically
- Non-English queries are translated internally
- Retrieval is done using English policy documents
- Answers are returned in the original user language

------------------------------------------------
SAFETY AND ANTI-HALLUCINATION
------------------------------------------------
- GenAI is restricted to retrieved policy context only
- No external knowledge or guessing is allowed
- Explicitly states when information is not available
- Ensures ethical and responsible use of GenAI

------------------------------------------------
HOW TO RUN THE PROJECT
------------------------------------------------
1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   streamlit run app.py

3. Add your Gemini API key inside app.py:
   genai.configure(api_key="YOUR_API_KEY")

------------------------------------------------
FEATURES
------------------------------------------------
- Conversational Chat Interface
- Funding Scheme Discovery
- Scheme Comparison
- Multilingual Queries
- Policy-Backed Answers
- Short-Term Conversational Memory

------------------------------------------------
FUTURE SCOPE
------------------------------------------------
- Automated policy change tracking
- Personalized funding recommendations
- Advanced eligibility scoring
- Live integration with government portals

------------------------------------------------
CONCLUSION
------------------------------------------------
This project demonstrates responsible use of Generative AI by combining
vector databases and RAG to provide accurate, explainable, and multilingual
startup funding guidance.

------------------------------------------------
ONE-LINE DESCRIPTION
------------------------------------------------
A GenAI-powered RAG system for conversational, multilingual, and policy-backed
startup funding intelligence.
