"""Debug embeddings cache - verifica contenuto"""

import pickle
import os

cache_path = 'ai_system/Embedding/embeddings_cache.pkl'

print("="*70)
print("🔍 DEBUG EMBEDDINGS CACHE")
print("="*70)

# Verifica file esiste
if not os.path.exists(cache_path):
    print(f"❌ File cache non trovato: {cache_path}")
    exit(1)

# Carica cache
print(f"\n📂 Caricamento cache: {cache_path}")
print(f"   Dimensione: {os.path.getsize(cache_path) / 1024:.1f} KB")

with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

print(f"\n📊 Chiavi cache:")
for key in cache.keys():
    print(f"   • {key}")

# Analizza chunks_data
chunks_data = cache.get('chunks_data', {})
chunk_embeddings = cache.get('chunk_embeddings', {})

print(f"\n📦 CHUNKS DATA:")
print(f"   Totale chunks: {len(chunks_data)}")
print(f"   Totale embeddings: {len(chunk_embeddings)}")

# Mostra primi 10 chunk IDs e metadata
print(f"\n📋 Primi 10 chunk:")
for i, (chunk_id, chunk_data) in enumerate(list(chunks_data.items())[:10], 1):
    metadata = chunk_data.get('metadata', {})
    product = metadata.get('product', 'Unknown')
    category = metadata.get('category', 'unknown')
    text_preview = chunk_data.get('original_text', chunk_data.get('testo', ''))[:80]
    
    print(f"\n   [{i}] ID: {chunk_id}")
    print(f"       Product: {product}")
    print(f"       Category: {category}")
    print(f"       Text: {text_preview}...")
    print(f"       Has embedding: {chunk_id in chunk_embeddings}")

# Cerca chunk TK3+ specifici
print(f"\n🔍 CHUNK TK3+ (ricerca):")
tk3_chunks = []
for chunk_id, chunk_data in chunks_data.items():
    metadata = chunk_data.get('metadata', {})
    product = metadata.get('product', '')
    if 'TK3' in product or 'tk3' in product.lower():
        tk3_chunks.append((chunk_id, product, metadata.get('category', 'unknown')))

if tk3_chunks:
    print(f"   Trovati {len(tk3_chunks)} chunk TK3+:")
    for chunk_id, product, category in tk3_chunks:
        print(f"   • {chunk_id:30s} | {product:25s} | {category}")
else:
    print(f"   ❌ NESSUN chunk TK3+ trovato!")

# Cerca chunk TK4 specifici
print(f"\n🔍 CHUNK TK4 (ricerca):")
tk4_chunks = []
for chunk_id, chunk_data in chunks_data.items():
    metadata = chunk_data.get('metadata', {})
    product = metadata.get('product', '')
    if 'TK4' in product or 'tk4' in product.lower():
        tk4_chunks.append((chunk_id, product, metadata.get('category', 'unknown')))

if tk4_chunks:
    print(f"   Trovati {len(tk4_chunks)} chunk TK4:")
    for chunk_id, product, category in tk4_chunks:
        print(f"   • {chunk_id:30s} | {product:25s} | {category}")
else:
    print(f"   ❌ NESSUN chunk TK4 trovato!")

# Q&A
qa_data = cache.get('qa_data', {})
qa_embeddings = cache.get('qa_embeddings', {})

print(f"\n📋 Q&A DATA:")
print(f"   Totale Q&A: {len(qa_data)}")
print(f"   Totale embeddings: {len(qa_embeddings)}")

if qa_data:
    print(f"\n   Primi 5 Q&A:")
    for i, (qa_id, qa_item) in enumerate(list(qa_data.items())[:5], 1):
        question = qa_item.get('question', '')[:60]
        answer = qa_item.get('answer', '')[:60]
        print(f"   [{i}] {qa_id}")
        print(f"       Q: {question}...")
        print(f"       A: {answer}...")

print("\n" + "="*70)
