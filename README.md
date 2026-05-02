# ⚖️ AI Legal Contract Analyzer (RAG-based)

An AI-powered legal assistant that analyzes contract documents using Retrieval-Augmented Generation (RAG).

## 🚀 Features
- Upload legal PDFs
- Detect risks (termination, liability, penalties)
- Ask questions in natural language
- Get simplified legal explanations

## 🧠 Tech Stack
- Python
- LangChain
- FAISS
- Hugging Face Transformers
- Streamlit

## ⚙️ How It Works
1. Extract text from PDF
2. Split into chunks
3. Convert to embeddings
4. Store in FAISS
5. Retrieve relevant clauses
6. Generate answers using LLM

## ▶️ Run Locally
```bash```
pip install -r requirements.txt
streamlit run app.py
