import pickle
from pathlib import Path

cache_path = Path("ai_system/Embedding/embeddings_cache.pkl")

with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

print(f"📊 Contenuto Cache:")
print(f"   • Chunk embeddings: {len(cache.get('chunk_embeddings', {}))}")
print(f"   • Q&A embeddings: {len(cache.get('qa_embeddings', {}))}")
print(f"   • Chunks data: {len(cache.get('chunks_data', {}))}")
print(f"\n🔍 Primi 3 chunk IDs:")
for i, chunk_id in enumerate(list(cache.get('chunks_data', {}).keys())[:3], 1):
    print(f"   {i}. {chunk_id}")

print(f"\n📝 Esempio chunk data:")
if cache.get('chunks_data'):
    first_id = list(cache.get('chunks_data', {}).keys())[0]
    chunk = cache['chunks_data'][first_id]
    print(f"   ID: {first_id}")
    print(f"   Keys: {list(chunk.keys())}")
    if 'original_text' in chunk:
        print(f"   Text length: {len(chunk['original_text'])} chars")
    if 'metadata' in chunk:
        metadata = chunk['metadata']
        print(f"   Author: {metadata.get('author', 'N/A')}")
        print(f"   Work: {metadata.get('work', 'N/A')}")
