# 🎓 IITB Career Intelligence Assistant

An end-to-end RAG (Retrieval-Augmented Generation) pipeline built from scratch — no LangChain — to answer career and placement queries specific to IIT Bombay.

---

## What It Does

Students can ask natural language questions like:

- *"What companies visit IITB for placements?"*
- *"What CPI is needed for consulting roles?"*
- *"Which sectors hire the most from IITB?"*

...and get accurate, grounded answers drawn from real IITB placement data.

---

## Pipeline Overview

```
User Query
    │
    ▼
Query Embedding (MiniLM)
    │
    ▼
FAISS Similarity Search
    │
    ▼
Top-k Chunk Retrieval (from 380 chunks across 45 docs)
    │
    ▼
Prompt Construction
    │
    ▼
Llama 3.3 70B (via OpenRouter API)
    │
    ▼
Grounded Response
```

- **Data Sources:** 45 scraped documents — IITB placement reports + InsightIITB blogs
- **Chunking:** Overlapping text chunks → 380 total chunks
- **Embeddings:** MiniLM sentence-transformers → 384-dimensional vectors
- **Vector Store:** FAISS nearest-neighbour index
- **LLM:** Llama 3.3 70B via OpenRouter API
- **UI:** Gradio → deployed on HuggingFace Spaces

---

## Tech Stack

| Component | Tool |
|---|---|
| Embeddings | `sentence-transformers` (MiniLM) |
| Vector Store | `FAISS` |
| LLM | Llama 3.3 70B via OpenRouter API |
| Scraping | `BeautifulSoup`, `PyMuPDF` |
| UI | `Gradio` |
| Deployment | HuggingFace Spaces |

---

## Why No LangChain?

Built the retrieval pipeline from scratch to understand every component deeply — chunking strategy, embedding, similarity search, and prompt engineering — rather than relying on abstractions. This means full control over:

- How documents are chunked and overlapped
- How embeddings are computed and indexed
- How retrieved context is injected into the prompt
- How the LLM is called and the response is parsed

---

## Project Structure

```
├── app.py                        # Gradio UI entry point
├── setup.py                      # Environment & index setup
├── step1_collect_data.py         # BeautifulSoup + PyMuPDF scraping
├── step2_build_knowledge_base.py # Overlapping text chunking + FAISS indexing
├── step3_retriever.py            # FAISS similarity search
├── step4_rag_pipeline.py         # Prompt construction + OpenRouter API call
├── data/                         # Scraped documents + serialized FAISS index
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/KasakGIT/AI-chatbot.git
cd AI-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your OpenRouter API key

```bash
export OPENROUTER_API_KEY=your_api_key_here
```

Or create a `.env` file:

```
OPENROUTER_API_KEY=your_api_key_here
```

### 4. Run the pipeline steps in order

```bash
python step1_collect_data.py
python step2_build_knowledge_base.py
python step3_retriever.py       # optional: test retrieval
python step4_rag_pipeline.py    # optional: test end-to-end
python app.py                   # launch Gradio UI
```

---

## Live Demo

🤗 Deployed on HuggingFace Spaces → [**Try it here**](https://huggingface.co/spaces/Kasakkhere/iitb-career-assistant)

---

## Future Work

- Fine-tune MiniLM on IITB-specific QA pairs for better retrieval
- Add reranking step (cross-encoder) before generation
- Expand data sources (more placement seasons, department-wise reports)
- Add conversational memory for multi-turn queries

---

## Author

Built by **Kasak** — 2nd year Chemical Engineering, IIT Bombay
Part of ongoing work in ML/NLP systems and information retrieval.
