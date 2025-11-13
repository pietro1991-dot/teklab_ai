"""
Test ALL chunk similarities for TK3 query
"""
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load cache
cache = pickle.load(open('ai_system/Embedding/teklab_embeddings_cache.pkl', 'rb'))
model = SentenceTransformer(cache['model'])

# Test query
query = "quali tipi di tk3 ci sono?"
query_embedding = model.encode([query])[0]

print(f"🔍 Query: {query}\n")

# Calculate ALL similarities
all_scores = []
for chunk_id, chunk_embedding in cache['embeddings'].items():
    cosine_sim = np.dot(query_embedding, chunk_embedding) / (
        np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
    )
    all_scores.append((cosine_sim, chunk_id))

# Sort by score
all_scores.sort(reverse=True, key=lambda x: x[0])

# Show top 20
print("="*80)
print("TOP 20 CHUNKS BY SEMANTIC SIMILARITY:")
print("="*80)
for rank, (score, chunk_id) in enumerate(all_scores[:20], 1):
    # Check if it's a TK3 variant chunk
    is_tk3_variant = chunk_id in [
        'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_2',
        'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_3',
        'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_4'
    ]
    
    marker = "🎯 TK3 VARIANT" if is_tk3_variant else ""
    
    # Get chunk preview
    chunk_text = cache['chunk_texts'].get(chunk_id, "")
    preview = chunk_text[:100].replace('\n', ' ') if chunk_text else "No text"
    
    print(f"{rank:2d}. Score: {score:.4f} {marker}")
    print(f"    ID: {chunk_id}")
    print(f"    Preview: {preview}...")
    print()

# Show TK3 variant positions
print("="*80)
print("TK3 VARIANT CHUNKS POSITIONS:")
print("="*80)
tk3_variants = {
    'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_2': '46 bar',
    'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_3': '80 bar',
    'Oil_Level_Regulators_TK3_SERIES_COMPLETE|chunk_4': '130 bar'
}

for chunk_id, variant in tk3_variants.items():
    for rank, (score, cid) in enumerate(all_scores, 1):
        if cid == chunk_id:
            print(f"{variant:8s}: Rank #{rank:2d} with score {score:.4f}")
            break

# Adaptive threshold analysis
top_score = all_scores[0][0]
threshold_70 = top_score * 0.70
threshold_85 = top_score * 0.85

print(f"\n{'='*80}")
print("ADAPTIVE THRESHOLD ANALYSIS:")
print("="*80)
print(f"Top score: {top_score:.4f}")
print(f"70% threshold: {threshold_70:.4f} (current backend setting)")
print(f"85% threshold: {threshold_85:.4f} (old backend setting)")

print(f"\nChunks passing 70% threshold: {sum(1 for s, _ in all_scores if s >= threshold_70)}")
print(f"Chunks passing 85% threshold: {sum(1 for s, _ in all_scores if s >= threshold_85)}")
