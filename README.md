# RAG‑Autotune   
Self‑improving Retrieval‑Augmented Generation with nightly LoRA retriever tuning & zero‑downtime vector‑store swaps.

---

## Why RAG‑Autotune?

Traditional retrievers grow stale, hurting answer relevance.  
**RAG‑Autotune closes the loop:**

1. **Logs** user 👍/👎 on every answer  
2. **Nightly fine‑tunes** a dual‑encoder retriever using LoRA  
3. **Re‑embeds** the corpus into a new shadow Qdrant collection  
4. **Smoke‑tests** quality & latency, then atomically **swaps** the alias — no downtime, easy rollback

**Target user:** solo devs / indie hackers building semantic search or chat widgets who need automated retriever freshness without ML ops overhead.

---

## Project Goal

> Boost **Precision@5 by ≥ 15 percentage points** within **48 hours** of feedback ingestion  
> while keeping **p99 latency ≤ 150 ms** on laptop-class CPU inference.

---

## Architecture

![Architecture Diagram](https://github.com/user-attachments/assets/bdab7446-ad54-472a-9e7e-61834efadf20)

[Full technical doc](https://docs.google.com/document/d/18SFZ9XuLBKdqYlIcdq99bkPmqZKkrWld9A9WuPLw1ys/edit?usp=sharing)

Key components:
- **FastAPI** HTTP interface (`/ask`, `/feedback`, `/health`)
- **LangGraph** LLM workflow engine
- **Retriever** using SentenceTransformer + Qdrant
- **Vector Store** (Qdrant with alias support)
- **Generator** (stubbed or LLM-backed)
- **Feedback Logger** (SQLite)
- **Fine-Tuner** (LoRA nightly job)
- **Smoke-Test Gate** with auto-promotion/rollback
- **Monitoring Dashboard** (W&B + Streamlit)


## Getting Started

```bash
# clone & create virtual environment
git clone https://github.com/TyPE333/RAG-Autotune.git
cd RAG-Autotune
python -m venv .venv && . .venv/Scripts/activate  # Windows
pip install -r requirements.txt
````

```bash
# run local server
make run-local  # or: uvicorn app.main:app --reload
```

```bash
# open endpoints
open http://localhost:8000       # Swagger UI
open http://localhost:8501       # Streamlit dashboard (Phase 3+)
```

```bash
# run tests
make test
```

---

[System Design & FR details (Google Doc)](https://docs.google.com/document/d/18SFZ9XuLBKdqYlIcdq99bkPmqZKkrWld9A9WuPLw1ys/edit?usp=sharing)

---

## Contributing

PRs are welcome after Phase 3. Please run `make format` and `make test` before submitting.

---

## License

MIT. See `LICENSE`.

---

## Acknowledgements

Inspired by:

* [Auto‑RAG (ICTNLP)](https://github.com/ictnlp/Auto-RAG)
* [RAGSys Blog (Crossing Minds)](https://www.crossingminds.com/blog/closing-the-loop-real-time-self-improvement-for-llms-with-rag)
* [Self-Improving RAG (arXiv)](https://arxiv.org/abs/2410.17952)

**RAG‑Autotune** extends these with retriever-level LoRA fine-tuning, zero-downtime hot-swaps, LangGraph orchestration, and full MLOps monitoring.

```
