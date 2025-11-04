"""
Verifica miglioramenti dopo rigenerazione embeddings
"""
import pickle
from pathlib import Path

cache_path = Path("ai_system/Embedding/embeddings_cache.pkl")

if not cache_path.exists():
    print("❌ Cache non trovata")
    exit(1)

with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})
chunk_embeddings = cache.get('chunk_embeddings', {})
qa_embeddings = cache.get('qa_embeddings', {})
summary_embeddings = cache.get('summary_embeddings', {})
summaries_data = cache.get('summaries_data', {})

print("="*80)
print("📊 VERIFICA EMBEDDINGS CACHE")
print("="*80)

# Test 1: original_text presente?
print("\n✅ TEST 1: ORIGINAL_TEXT")
chunks_with_text = 0
for chunk_id, chunk in chunks_data.items():
    if 'original_text' in chunk and chunk['original_text']:
        chunks_with_text += 1

print(f"   Chunks con 'original_text': {chunks_with_text}/{len(chunks_data)}")
if chunks_with_text == len(chunks_data):
    print("   ✅ PERFETTO! Tutti i chunk hanno original_text")
elif chunks_with_text > 0:
    print(f"   ⚠️  PARZIALE: {len(chunks_data) - chunks_with_text} chunk senza testo")
else:
    print("   ❌ CRITICO: Nessun chunk ha original_text!")

# Test 2: Conta natural questions negli embeddings
print("\n✅ TEST 2: NATURAL QUESTIONS EMBEDDINGS")
nq_count = sum(1 for qa_id in qa_embeddings.keys() if '|nq_' in qa_id)
qa_count = sum(1 for qa_id in qa_embeddings.keys() if '|qa_' in qa_id)
print(f"   Q&A pairs: {qa_count}")
print(f"   Natural Questions: {nq_count}")
print(f"   Totale Q&A embeddings: {len(qa_embeddings)}")

# Test 3: Metadata disponibili
print("\n✅ TEST 3: METADATA AVAILABILITY")
first_chunk = list(chunks_data.values())[0]
meta = first_chunk.get('metadata', {})

metadata_stats = {
    'keywords_primary': len(meta.get('keywords_primary', [])),
    'iconic_quotes': len(meta.get('iconic_quotes', [])),
    'key_concepts': len(meta.get('key_concepts', [])),
    'natural_questions': len(meta.get('natural_questions', [])),
    'qa_pairs': len(meta.get('qa_pairs', [])),
}

print("   Esempio metadata nel primo chunk:")
for field, count in metadata_stats.items():
    status = "✓" if count > 0 else "○"
    print(f"   {status} {field}: {count} items")

# Test 4: Sample embedding text (verifica arricchimento)
print("\n✅ TEST 4: EMBEDDING TEXT ENRICHMENT")
print("   Per verificare se gli embeddings includono keywords/quotes,")
print("   guardare gli embeddings durante la ricerca chatbot.")
print(f"   Totale embeddings chunks: {len(chunk_embeddings)}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"✓ Chunks totali: {len(chunks_data)}")
print(f"✓ Chunk embeddings: {len(chunk_embeddings)}")
print(f"✓ Q&A embeddings: {len(qa_embeddings)}")
print(f"  - Q&A pairs: {qa_count}")
print(f"  - Natural Questions: {nq_count}")
print(f"✓ Summary embeddings: {len(summary_embeddings)}")
print(f"✓ Summaries data: {len(summaries_data)}")
print(f"✓ Chunks con original_text: {chunks_with_text}/{len(chunks_data)}")

if chunks_with_text == len(chunks_data) and nq_count > 0 and len(summary_embeddings) > 0:
    print("\n✅ CACHE COMPLETAMENTE MIGLIORATA CON SUMMARIES!")
    print("   Pronto per testare il chatbot.")
elif chunks_with_text == len(chunks_data):
    print("\n⚠️  Cache con original_text ma senza Natural Questions o Summaries")
    print("   Funzionerà ma con meno fonti disponibili.")
else:
    print("\n❌ CACHE INCOMPLETA - Rigenerare embeddings!")
