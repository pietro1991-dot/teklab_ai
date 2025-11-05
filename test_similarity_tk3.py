"""Test similarity embeddings per query 'tk3'"""

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Carica cache embeddings
with open('ai_system/Embedding/embeddings_cache.pkl', 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})
chunk_embeddings = cache.get('chunk_embeddings', {})

# Carica modello
print("🧠 Caricamento modello embeddings...")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device='cpu')

# Test queries
queries = [
    "cosa sai del tk3?",
    "'cosa sai del tk3?'",  # Con virgolette
    "tk3",
    "TK3+",
    "what is tk3+ for r410a?"
]

print("\n" + "="*70)
print("TEST SIMILARITY EMBEDDINGS")
print("="*70)

for query in queries:
    print(f"\n📝 Query: '{query}'")
    query_emb = model.encode([query])[0]
    
    similarities = []
    for chunk_id, chunk_emb in chunk_embeddings.items():
        chunk_data = chunks_data.get(chunk_id, {})
        product = chunk_data.get('metadata', {}).get('product', 'Unknown')
        category = chunk_data.get('metadata', {}).get('category', 'unknown')
        
        # Cosine similarity
        sim = np.dot(query_emb, chunk_emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(chunk_emb)
        )
        
        if 'TK3' in product or 'tk3' in product.lower():
            similarities.append((product, category, sim))
    
    # Ordina per similarity
    similarities.sort(key=lambda x: x[2], reverse=True)
    
    print(f"   Top 5 chunk TK3:")
    for i, (product, category, sim) in enumerate(similarities[:5], 1):
        threshold_ok = "✅" if sim >= 0.3 else "❌"
        print(f"   {threshold_ok} [{i}] {product:20s} | {category:12s} | sim={sim:.4f}")
    
    if similarities and similarities[0][2] < 0.3:
        print(f"   ⚠️  PROBLEMA: Top chunk sotto threshold 0.3!")

print("\n" + "="*70)
