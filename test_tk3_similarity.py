"""Test similarity per query TK3"""

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Carica cache
with open('ai_system/Embedding/embeddings_cache.pkl', 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})
chunk_embeddings = cache.get('chunk_embeddings', {})

print("="*70)
print("🔍 TEST SIMILARITY - Query 'cosa sai del tk3?'")
print("="*70)

# Carica modello
print("\n🧠 Caricamento modello embeddings...")
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device='cpu')

# Query
query = "cosa sai del tk3?"
print(f"\n📝 Query: '{query}'")
query_emb = model.encode([query])[0]

# Calcola similarity per TUTTI i chunk
similarities = []
for chunk_id, chunk_emb in chunk_embeddings.items():
    chunk_data = chunks_data.get(chunk_id, {})
    metadata = chunk_data.get('metadata', {})
    
    # Cosine similarity
    sim = np.dot(query_emb, chunk_emb) / (
        np.linalg.norm(query_emb) * np.linalg.norm(chunk_emb)
    )
    
    product_model = metadata.get('product_model', 'Unknown')
    category = chunk_data.get('category', 'unknown')
    
    similarities.append((chunk_id, product_model, category, sim))

# Ordina per similarity (discendente)
similarities.sort(key=lambda x: x[3], reverse=True)

# Mostra top 10
print(f"\n📊 TOP 10 CHUNK (ordinati per similarity):")
print(f"{'#':<3} {'Product Model':<30} {'Category':<12} {'Similarity':<10} {'>=0.3?'}")
print("-"*70)

for i, (chunk_id, product, category, sim) in enumerate(similarities[:10], 1):
    ok = "✅" if sim >= 0.3 else "❌"
    print(f"{i:<3} {product:<30} {category:<12} {sim:.4f}     {ok}")

# Mostra chunk TK3+ specifici
print(f"\n🔍 CHUNK TK3+ (filtrati):")
tk3_chunks = [
    (chunk_id, product, category, sim) 
    for chunk_id, product, category, sim in similarities 
    if 'TK3' in product or 'tk3' in product.lower()
]

if tk3_chunks:
    print(f"   Trovati {len(tk3_chunks)} chunk TK3+:")
    for chunk_id, product, category, sim in tk3_chunks:
        ok = "✅" if sim >= 0.3 else "❌"
        print(f"   {ok} {product:<30} | {category:<12} | sim={sim:.4f}")
else:
    print(f"   ❌ NESSUN chunk TK3+ trovato nei risultati!")

# Diagnostica threshold
print(f"\n📉 DIAGNOSTICA THRESHOLD:")
print(f"   Threshold attuale: 0.3")
print(f"   Top chunk similarity: {similarities[0][3]:.4f}")
print(f"   Chunk sopra 0.3: {sum(1 for _, _, _, sim in similarities if sim >= 0.3)}")
print(f"   Chunk sopra 0.2: {sum(1 for _, _, _, sim in similarities if sim >= 0.2)}")
print(f"   Chunk sopra 0.1: {sum(1 for _, _, _, sim in similarities if sim >= 0.1)}")

if similarities[0][3] < 0.3:
    print(f"\n⚠️  PROBLEMA: Top chunk similarity {similarities[0][3]:.4f} < 0.3!")
    print(f"   Suggerimento: Abbassa threshold a 0.2 o rigenera embeddings")

print("\n" + "="*70)
