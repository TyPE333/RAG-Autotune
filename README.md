# RAG‑Autotune   
Self‑improving Retrieval‑Augmented Generation with nightly LoRA retriever tuning & zero‑downtime vector‑store swaps.

---

## Why RAG‑Autotune?
Traditional retrievers grow stale, hurting answer relevance.  
RAG‑Autotune closes the loop:
1. **Logs** user 👍/👎 on every answer  
2. **Nightly fine‑tunes** a dual‑encoder with LoRA using that feedback  
3. **Re‑embeds** the corpus in a shadow Qdrant collection  
4. **Smoke‑tests** quality & latency, then atomically **swaps** the alias—no downtime, easy rollback  

Target user: **solo devs / indie hackers** building chat or search widgets who need an auto‑fresh retriever without heavy ops.

---

## Project Goal
> Boost Precision@5 by **≥ 15 percentage‑points** within **48 h** of feedback ingestion while keeping **p99 latency ≤ 150 ms** on laptop‑class hardware.

---

## High‑Level Architecture

## Architecture:
![image](https://github.com/user-attachments/assets/bdab7446-ad54-472a-9e7e-61834efadf20)

[Full details in google doc](https://docs.google.com/document/d/18SFZ9XuLBKdqYlIcdq99bkPmqZKkrWld9A9WuPLw1ys/edit?usp=sharing)

Key components: FastAPI edge, LangGraph pipeline, Retriever, VectorStore wrapper, Generator (LLM), Feedback DB, Fine‑Tuner, Smoke‑Test Gate, Monitoring Dashboard.

---

## Features

* `/ask`, `/feedback`, `/health` endpoints (FastAPI)
* Dual‑encoder retriever + optional cross‑encoder reranker
* Live answer streaming with citations
* SQLite feedback logging w/ 1‑h dedupe
* Nightly LoRA fine‑tune & shadow‑index embedding
* Atomic alias swap on **pass/fail** smoke test
* Metrics to Weights & Biases + Streamlit latency dashboard
* One‑command local run & GitHub Actions CI

---

## Getting Started

```bash
# clone & create env
git clone https://github.com/TyPE333/RAG-Autotune.git
cd RAG-Autotune
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # 🔧 TODO: update as deps grow

# run locally
make run-local     # uvicorn app.main:app --reload

# open demo
open http://localhost:8000       # Swagger UI
open http://localhost:8501       # Streamlit chat (after Phase 1)
```

Run tests:

```bash
make test          # pytest -q
```

---

## Functional Requirements (v1)

| ID   | Requirement                                               | Status |
| ---- | --------------------------------------------------------- | ------ |
| FR‑1 | Expose `/ask`, `/feedback`, `/health`                     | ✅      |
| FR‑2 | Retrieve → (Optionally Rerank) → Generate → Stream answer | ⬜      |
| FR‑3 | Log user feedback with dedupe                             | ⬜      |
| FR‑4 | Nightly fine‑tune & re‑embed corpus                       | ⬜      |
| FR‑5 | Smoke‑test + zero‑downtime alias swap                     | ⬜      |

[Full details in google doc](https://docs.google.com/document/d/18SFZ9XuLBKdqYlIcdq99bkPmqZKkrWld9A9WuPLw1ys/edit?usp=sharing)

---

## Roadmap

| Phase           | Target Date      | Deliverable                          |
| --------------- | ---------------- | ------------------------------------ |
| 1 MVP           | 🔧 TODO (Day 3)  | Live query path + feedback logging   |
| 2 Loop          | 🔧 TODO (Day 7)  | Nightly fine‑tune & alias swap       |
| 3 Observability | 🔧 TODO (Day 11) | Streamlit/W\&B dashboards            |
| 4 Polish & Blog | 🔧 TODO (Day 14) | CI badge, README polish, launch post |

---

## Contributing

PRs welcome once v1 stabilizes. Run `make format` before committing.

---

## License

MIT. See `LICENSE`.

---

## Acknowledgements

Inspired by *Auto‑RAG (ICTNLP)*, *RAGSys* blog, and *Self‑Improving RAG* research.
RAG‑Autotune extends these ideas with nightly LoRA tuning, Qdrant alias swaps, and full MLOps polish.

```


