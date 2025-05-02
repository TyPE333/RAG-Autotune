# RAG-Autotune
RAG‑Autotune – an open‑source, production‑ready Retrieval‑Augmented Generation stack that closes the loop: 
Flow: logs user feedback → nightly LoRA‑fine‑tunes a dual‑encoder retriever → hot‑swaps Qdrant embeddings with zero downtime → monitors quality & latency on Streamlit + W&B dashboards, all orchestrated by LangGraph and served via FastAPI/CI‑CD.







