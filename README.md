# RAG-Autotune
RAG‑Autotune – an open‑source, production‑ready Retrieval‑Augmented Generation stack that closes the loop: 
Flow: logs user feedback → nightly LoRA‑fine‑tunes a dual‑encoder retriever → hot‑swaps Qdrant embeddings with zero downtime → monitors quality & latency on Streamlit + W&B dashboards, all orchestrated by LangGraph and served via FastAPI/CI‑CD.


## Architecture:
![image](https://github.com/user-attachments/assets/bdab7446-ad54-472a-9e7e-61834efadf20)





