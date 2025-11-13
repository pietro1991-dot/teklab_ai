"""
Test semantic similarity scores for TK3 query
"""
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load cache
cache = pickle.load(open('ai_system/Embedding/teklab_embeddings_cache.pkl', 'rb'))
print(f"Cache model: {cache['model']}")

# Load embedding model
model = SentenceTransformer(cache['model'])

# Test query
query = "quali tipi di tk3 ci sono?"
print(f"\n🔍 Query: {query}")

# Generate query embedding
query_embedding = model.encode([query])[0]

# Check TK3 variant chunks
tk3_chunks = {
    'chunk_2_46bar': 'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_2',
    'chunk_3_80bar': 'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_3',
    'chunk_4_130bar': 'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_4'
}

print("\n" + "="*60)
print("SEMANTIC SIMILARITY SCORES:")
print("="*60)

scores = []
for name, chunk_id in tk3_chunks.items():
    if chunk_id in cache['chunk_texts']:
        # Get chunk embedding
        chunk_embedding = cache['embeddings'][chunk_id]
        
        # Calculate cosine similarity
        cosine_sim = np.dot(query_embedding, chunk_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
        )
        
        scores.append((cosine_sim, name, chunk_id))
        
        # Get chunk preview
        chunk_text = cache['chunk_texts'][chunk_id]
        preview = chunk_text[:200].replace('\n', ' ')
        
        print(f"\n{name}:")
        print(f"  Score: {cosine_sim:.4f}")
        print(f"  Preview: {preview}...")
    else:
        print(f"\n{name}: ❌ NOT FOUND IN CACHE")

# Sort by score
scores.sort(reverse=True, key=lambda x: x[0])

print("\n" + "="*60)
print("RANKING:")
print("="*60)
for rank, (score, name, chunk_id) in enumerate(scores, 1):
    print(f"{rank}. {name}: {score:.4f}")

# Calculate adaptive threshold
if scores:
    top_score = scores[0][0]
    threshold_70 = top_score * 0.70
    threshold_85 = top_score * 0.85
    
    print("\n" + "="*60)
    print("ADAPTIVE THRESHOLD ANALYSIS:")
    print("="*60)
    print(f"Top score: {top_score:.4f}")
    print(f"70% threshold: {threshold_70:.4f}")
    print(f"85% threshold: {threshold_85:.4f}")
    
    print("\nChunks passing 70% threshold:")
    for score, name, _ in scores:
        if score >= threshold_70:
            print(f"  ✅ {name}: {score:.4f}")
        else:
            print(f"  ❌ {name}: {score:.4f} (below {threshold_70:.4f})")
