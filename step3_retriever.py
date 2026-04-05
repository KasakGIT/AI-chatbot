import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# load everything we built in day 2
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("data/faiss_index")

with open("data/chunks.pkl", "rb") as f:
    all_chunks = pickle.load(f)

print(f"Loaded index with {index.ntotal} vectors")
print(f"Loaded {len(all_chunks)} chunks")

def retrieve(query, top_k=3):
    # embed the query — same model, same vector space as your chunks
    query_vector = model.encode([query])
    query_vector = np.array(query_vector).astype("float32")
    
    # search FAISS — returns distances and indices
    distances, indices = index.search(query_vector, top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "text": all_chunks[idx]["text"],
            "source": all_chunks[idx]["source"],
            "distance": distances[0][i]
        })
    
    return results

test_queries = [
    "How did a Chemical Engineering student get into BCG consulting?",
    "What is the average salary at IIT Bombay placements?",
    "How to prepare for Goldman Sachs finance internship?",
    "What companies hire from IIT Bombay for quant roles?",
    "Should I do research internship or corporate internship?"
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}")
    
    results = retrieve(query, top_k=3)
    
    for i, result in enumerate(results):
        print(f"\nRank {i+1} | Source: {result['source']} | Distance: {result['distance']:.4f}")
        print(f"Text: {result['text'][:200]}...")  # first 200 chars