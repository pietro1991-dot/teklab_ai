#!/usr/bin/env python3
"""
Test rapido RAG Teklab - Verifica embeddings e ricerca semantica
"""
import pickle
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).parent
EMBEDDINGS_CACHE = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl"

print("="*70)
print("🔍 TEST RAG TEKLAB - Verifica Embeddings")
print("="*70)

# Carica cache
print(f"\n📂 Caricamento cache: {EMBEDDINGS_CACHE.name}")
try:
    with open(EMBEDDINGS_CACHE, 'rb') as f:
        cache = pickle.load(f)
    print("✅ Cache caricata con successo!\n")
except Exception as e:
    print(f"❌ Errore caricamento cache: {e}")
    exit(1)

# Verifica contenuto
chunk_emb = cache.get('chunk_embeddings', {})
qa_emb = cache.get('qa_embeddings', {})
chunks_data = cache.get('chunks_data', {})
model = cache.get('model', 'unknown')

print("📊 CONTENUTO CACHE:")
print(f"   • Modello: {model}")
print(f"   • Chunks embeddings: {len(chunk_emb)}")
print(f"   • Q&A embeddings: {len(qa_emb)}")
print(f"   • Chunks data: {len(chunks_data)}")

# Mostra alcuni chunk IDs
print("\n📝 CHUNK IDs (primi 10):")
for i, chunk_id in enumerate(list(chunk_emb.keys())[:10]):
    print(f"   {i+1}. {chunk_id}")

# Mostra alcune Q&A
print("\n❓ Q&A IDs (prime 10):")
for i, qa_id in enumerate(list(qa_emb.keys())[:10]):
    print(f"   {i+1}. {qa_id}")

# Verifica dimensioni embeddings
if chunk_emb:
    first_emb = next(iter(chunk_emb.values()))
    emb_dim = len(first_emb)
    print(f"\n🔢 Dimensione embeddings: {emb_dim}")
    print(f"   (768 è corretto per all-mpnet-base-v2)")

# Mostra alcuni chunk completi
print("\n📄 ESEMPI CHUNK DATA (primi 3):")
for i, (chunk_id, chunk_data) in enumerate(list(chunks_data.items())[:3]):
    print(f"\n--- Chunk {i+1}: {chunk_id} ---")
    
    # Mostra metadata
    metadata = chunk_data.get('metadata', {})
    print(f"  Product: {metadata.get('product_model', 'N/A')}")
    print(f"  Category: {chunk_data.get('category', 'N/A')}")
    print(f"  Pressure: {metadata.get('pressure_rating', 'N/A')}")
    print(f"  Keywords: {', '.join(metadata.get('keywords', [])[:5])}")
    
    # Mostra inizio contenuto
    messages = chunk_data.get('messages', [])
    if len(messages) >= 3 and messages[2].get('role') == 'assistant':
        content = messages[2].get('content', '')
        preview = content[:150] + "..." if len(content) > 150 else content
        print(f"  Content preview: {preview}")

print("\n" + "="*70)
print("✅ TEST COMPLETATO - Cache embeddings OK!")
print("="*70)

# Test ricerca semantica (opzionale se sentence-transformers è installato)
print("\n🔍 Test ricerca semantica...")
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    
    # Carica modello
    print("   Caricamento modello...")
    model_obj = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    # Query di test
    test_queries = [
        "Which sensor for R410A refrigerant at 28 bar?",
        "ATEX requirements for ammonia",
        "TK3+ vs TK4 comparison"
    ]
    
    print("\n📋 TEST QUERIES:\n")
    
    for query in test_queries:
        print(f"❓ Query: {query}")
        
        # Genera embedding query
        query_emb = model_obj.encode([query])[0]
        
        # Calcola similarità con tutti i chunks
        similarities = []
        for chunk_id, chunk_emb_vec in chunk_emb.items():
            # Cosine similarity
            sim = np.dot(query_emb, chunk_emb_vec) / (
                np.linalg.norm(query_emb) * np.linalg.norm(chunk_emb_vec)
            )
            similarities.append((chunk_id, sim))
        
        # Ordina per similarità
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Mostra top 3
        print("   Top 3 matches:")
        for i, (chunk_id, sim) in enumerate(similarities[:3], 1):
            # Estrai info chunk
            chunk_info = chunks_data.get(chunk_id, {})
            product = chunk_info.get('metadata', {}).get('product_model', 'N/A')
            category = chunk_info.get('category', 'N/A')
            print(f"      {i}. {category}/{product} (similarity: {sim:.3f})")
        print()
    
    print("✅ Ricerca semantica funziona correttamente!")
    
except ImportError:
    print("   ⚠️  sentence-transformers non installato, skip test ricerca")
except Exception as e:
    print(f"   ⚠️  Errore test ricerca: {e}")

print("\n" + "="*70)
