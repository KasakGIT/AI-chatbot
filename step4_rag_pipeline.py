import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

# ── LOAD ──────────────────────────────────────────────────
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss_index")

with open("data/chunks.pkl", "rb") as f:
    all_chunks = pickle.load(f)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)
print("Ready!")

# ── RETRIEVER ─────────────────────────────────────────────
def retrieve(query, top_k=3):
    query_vector = embedding_model.encode([query])
    query_vector = np.array(query_vector).astype("float32")
    distances, indices = index.search(query_vector, top_k)
    return [{"text": all_chunks[idx]["text"], "source": all_chunks[idx]["source"]} 
            for i, idx in enumerate(indices[0])]

# ── PROMPT BUILDER ────────────────────────────────────────
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

# ── GENERATOR ─────────────────────────────────────────────
def generate_answer(prompt):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    answer = response.choices[0].message.content
    if not answer or answer.strip() == "None":
        return "The context contains relevant experiences but I couldn't generate a complete answer. Try rephrasing your question."
    return answer
    
# ── FULL PIPELINE ─────────────────────────────────────────
def ask(question):
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}")
    chunks = retrieve(question, top_k=3)
    print(f"Retrieved from: {[c['source'] for c in chunks]}")
    answer = generate_answer(build_prompt(question, chunks))
    print(f"\nANSWER:\n{answer}")
    return answer

ask("How did a Chemical Engineering student get into BCG consulting?")
ask("What is the average salary at IIT Bombay placements 2024?")
ask("Should I do a research internship or corporate internship as a 2nd year?")