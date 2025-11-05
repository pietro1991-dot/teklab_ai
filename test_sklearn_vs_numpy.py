"""Confronto sklearn vs numpy cosine similarity"""

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Carica cache
with open('ai_system/Embedding/embeddings_cache.pkl', 'rb') as f:
    cache = pickle.load(f)

chunk_embeddings = cache.get('chunk_embeddings', {})

print("="*70)
print("🔍 CONFRONTO SKLEARN vs NUMPY - Query 'cosa sai del tk3?'")
print("="*70)

# Carica modello
print("\n🧠 Caricamento modello...")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device='cpu')

# Query
query = "cosa sai del tk3?"
query_emb = model.encode([query])[0]

print(f"\n📝 Query: '{query}'")
print(f"   Query embedding shape: {query_emb.shape}")
print(f"   Query embedding norm: {np.linalg.norm(query_emb):.4f}")

# Prendi primo chunk TK3+
tk3_chunks = [cid for cid in chunk_embeddings.keys() if 'tk3' in cid.lower()]

if tk3_chunks:
    chunk_id = tk3_chunks[0]
    chunk_emb = chunk_embeddings[chunk_id]
    
    print(f"\n📦 Test chunk: {chunk_id}")
    print(f"   Chunk embedding shape: {chunk_emb.shape}")
    print(f"   Chunk embedding norm: {np.linalg.norm(chunk_emb):.4f}")
    
    # NUMPY (come nel test)
    sim_numpy = np.dot(query_emb, chunk_emb) / (
        np.linalg.norm(query_emb) * np.linalg.norm(chunk_emb)
    )
    
    # SKLEARN (come nello script)
    sim_sklearn = cosine_similarity([query_emb], [chunk_emb])[0][0]
    
    print(f"\n📊 RISULTATI:")
    print(f"   Numpy cosine similarity:   {sim_numpy:.6f}")
    print(f"   Sklearn cosine similarity: {sim_sklearn:.6f}")
    print(f"   Differenza:                {abs(sim_numpy - sim_sklearn):.6f}")
    
    if abs(sim_numpy - sim_sklearn) > 0.0001:
        print(f"\n⚠️  PROBLEMA: Differenza significativa tra numpy e sklearn!")
    else:
        print(f"\n✅ Numpy e sklearn danno risultati identici")
    
    # Test top 5 chunk
    print(f"\n📋 TOP 5 CHUNK (sklearn):")
    similarities = []
    for cid, cemb in chunk_embeddings.items():
        sim = cosine_similarity([query_emb], [cemb])[0][0]
        similarities.append((cid, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    for i, (cid, sim) in enumerate(similarities[:5], 1):
        ok = "✅" if sim >= 0.25 else "❌"
        print(f"   {ok} [{i}] {sim:.4f} - {cid[:50]}")
else:
    print("\n❌ Nessun chunk TK3+ trovato!")

print("\n" + "="*70)
