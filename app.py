import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import gradio as gr
import os
from setup import build_knowledge_base
build_knowledge_base()

# ── LOAD ──────────────────────────────────────────────────
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss_index")

with open("data/chunks.pkl", "rb") as f:
    all_chunks = pickle.load(f)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

# ── PIPELINE ──────────────────────────────────────────────
def retrieve(query, top_k=3):
    query_vector = embedding_model.encode([query])
    query_vector = np.array(query_vector).astype("float32")
    distances, indices = index.search(query_vector, top_k)
    return [{"text": all_chunks[idx]["text"], "source": all_chunks[idx]["source"]}
            for i, idx in enumerate(indices[0])]

def build_prompt(query, chunks):
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n\n"
    return f"""You are a helpful career guidance assistant for IIT Bombay students.
Use ONLY the context below to answer the question.
Be specific, mention names and details from the context.
If context is insufficient, say so honestly.

Context:
{context}

Question: {query}

Answer:"""

def ask(question):
    if not question.strip():
        return "Please ask a question!"
    chunks = retrieve(question, top_k=3)
    sources = [c['source'] for c in chunks]
    prompt = build_prompt(question, chunks)
    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    answer = response.choices[0].message.content
    return answer 

# ── GRADIO UI ─────────────────────────────────────────────
demo = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(label="Your Question", placeholder="e.g. How did a ChemE student get into BCG?", lines=2),
    outputs=gr.Textbox(label="Answer", lines=10),
    title="🎓 IIT Bombay Career Assistant",
    description="Ask anything about internships, placements, and career paths at IIT Bombay.",
    examples=[
        "How did a Chemical Engineering student get into BCG consulting?",
        "What is the average salary at IIT Bombay placements?",
        "Should I do a research internship or corporate internship as a 2nd year?",
        "How to prepare for Goldman Sachs finance internship?",
        "What companies hire from IIT Bombay for quant roles?"
    ]
)

if __name__ == "__main__":
    demo.launch()