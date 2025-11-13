"""
Inspect embeddings cache to debug missing TK3+ 80 bar variant
"""
import pickle
from pathlib import Path

# Load cache
cache_path = Path(__file__).parent.parent / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"

print(f"📂 Loading cache from: {cache_path}")
with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

print(f"\n✅ Cache loaded successfully")
print(f"\n� Cache keys: {list(cache.keys())}")
print(f"\n�📊 Cache structure:")
for key in cache.keys():
    value = cache[key]
    if isinstance(value, dict):
        print(f"   {key}: dict with {len(value)} items")
    elif isinstance(value, list):
        print(f"   {key}: list with {len(value)} items")
    elif hasattr(value, 'shape'):
        print(f"   {key}: tensor/array with shape {value.shape}")
    else:
        print(f"   {key}: {type(value).__name__}")

# Try to find chunks
if 'chunks_data' in cache and 'chunk_texts' in cache:
    print(f"\n✅ Using chunks_data for metadata and chunk_texts for content")
    chunks_data = cache['chunks_data']
    chunk_texts = cache['chunk_texts']
    
    print(f"\n📊 Chunks_data structure (first 2 items):")
    for i, (key, value) in enumerate(list(chunks_data.items())[:2]):
        print(f"   [{i}] {key}: {type(value).__name__}")
        if isinstance(value, dict):
            print(f"       Keys: {list(value.keys())[:5]}")
    
    print(f"\n📊 Chunk_texts structure (first 3 items):")
    for i, (key, text) in enumerate(list(chunk_texts.items())[:3]):
        print(f"   [{i}] {key}: {text[:80]}...")
    
    chunks = chunk_texts
elif 'chunk_texts' in cache:
    chunks = cache['chunk_texts']
    chunks_data = None
else:
    print(f"\n❌ Could not find chunks in cache")
    exit(1)

print(f"📊 Total chunks: {len(chunks)}")
if 'embeddings' in cache:
    if hasattr(cache['embeddings'], 'shape'):
        print(f"📊 Total embeddings: {cache['embeddings'].shape}")
    else:
        print(f"📊 Total embeddings: {len(cache['embeddings'])} items")
print(f"🏷️  Model used: {cache.get('model', 'unknown')}")

# Filter TK3 chunks
tk3_chunks = []

if isinstance(chunks, dict):
    chunk_items = chunks.items()
else:
    chunk_items = enumerate(chunks)

for i, item in chunk_items:
    if isinstance(item, tuple):
        chunk_id, text = item
    else:
        chunk_id = i
        text = item
    
    # Handle different chunk formats
    if isinstance(text, dict):
        text_content = text.get('text', text.get('content', str(text)))
    else:
        text_content = str(text)
    
    text_lower = text_content.lower()
    
    if 'tk3' in text_lower:
        # Get metadata from chunks_data if available
        if chunks_data and chunk_id in chunks_data:
            metadata = chunks_data[chunk_id]
            category = metadata.get('category', 'unknown')
            title = metadata.get('title', 'unknown')
        else:
            category = 'unknown'
            title = 'unknown'
        
        tk3_chunks.append({
            'index': i if not isinstance(i, str) else chunk_id,
            'chunk_id': chunk_id,
            'category': category,
            'title': title,
            'text': text_content,
            'text_preview': text_content[:300],
            'length': len(text_content)
        })

print(f"\n🔍 Found {len(tk3_chunks)} TK3-related chunks:")
print("=" * 80)

for chunk in tk3_chunks:
    print(f"\n[{chunk['chunk_id']}]")
    print(f"   Category: {chunk['category']}")
    print(f"   Title: {chunk['title']}")
    print(f"   Length: {chunk['length']} chars")
    print(f"   Preview: {chunk['text_preview']}")
    
    # Check for pressure variants
    text = chunk['text'].lower()
    has_46 = '46 bar' in text or 'tk3+ 46' in text or 'tk3 46' in text
    has_80 = '80 bar' in text or 'tk3+ 80' in text or 'tk3 80' in text
    has_130 = '130 bar' in text or 'tk3+ 130' in text or 'tk3 130' in text
    
    variants = []
    if has_46:
        variants.append('46')
    if has_80:
        variants.append('80')
    if has_130:
        variants.append('130')
    
    if variants:
        print(f"   🎯 Variants detected: {', '.join(variants)} bar")

print("\n" + "=" * 80)
print(f"\n📋 SUMMARY:")
print(f"   Total chunks: {len(chunks)}")
print(f"   TK3 chunks: {len(tk3_chunks)}")

# Check if 80 bar dedicated chunk exists
has_80_dedicated = any('80 bar' in c['text'].lower() and 'tk3' in c['text'].lower() 
                       for c in tk3_chunks)
print(f"   Has 80 bar chunk: {'✅ YES' if has_80_dedicated else '❌ NO - THIS IS THE PROBLEM!'}")
