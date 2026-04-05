import os
import faiss
import numpy as np
import pickle

def load_documents(data_dir):
    documents = []  # list of {"text": "...", "source": "filename"}
    
    # load placement report
    with open(f"{data_dir}/placement_report.txt", "r", encoding="utf-8") as f:
        documents.append({
            "text": f.read(),
            "source": "placement_report"
        })
    
    # load all blogs
    blog_dir = f"{data_dir}/blogs"
    for filename in os.listdir(blog_dir):
        if filename.endswith(".txt"):
            with open(f"{blog_dir}/{filename}", "r", encoding="utf-8") as f:
                documents.append({
                    "text": f.read(),
                    "source": filename.replace(".txt", "")
                })
    
    print(f"Loaded {len(documents)} documents")
    return documents

documents = load_documents("data")

def chunk_document(doc, chunk_size=200, overlap=50):
    words = doc["text"].split()
    chunks = []
    start = 0
    
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        
        chunks.append({
            "text": chunk_text,
            "source": doc["source"]
        })
        
        start += chunk_size - overlap  # overlap keeps context
    
    return chunks

# chunk all documents
all_chunks = []
for doc in documents:
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)

print(f"Total chunks created: {len(all_chunks)}")
# you should see somewhere between 400-600 chunks

from sentence_transformers import SentenceTransformer

print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# extract just the text from each chunk
texts = [chunk["text"] for chunk in all_chunks]

print("Embedding all chunks... (takes 1-2 mins)")
embeddings = model.encode(texts, show_progress_bar=True)

print(f"Embeddings shape: {embeddings.shape}")
# should print something like (500, 384)
# 500 chunks, each a 384-dim vector

# embeddings need to be float32 for FAISS
embeddings = np.array(embeddings).astype("float32")

# create FAISS index
# IndexFlatL2 = exact search using L2 distance
dimension = embeddings.shape[1]  # 384
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"FAISS index built with {index.ntotal} vectors")

# save the index to disk
faiss.write_index(index, "data/faiss_index")

# save chunks separately so we can retrieve the original text later
with open("data/chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)

print("Saved! data/faiss_index and data/chunks.pkl are ready")