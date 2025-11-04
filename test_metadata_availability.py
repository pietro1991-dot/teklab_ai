"""
Test per verificare quali metadata sono disponibili nella cache embeddings
"""
import pickle

# Carica cache
with open('ai_system/Embedding/embeddings_cache.pkl', 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})
chunk_ids = list(chunks_data.keys())

print(f"📊 Total chunks in cache: {len(chunk_ids)}\n")
print("Sample chunk IDs:")
for cid in chunk_ids[:5]:
    print(f"  - {cid}")

# Analizza primo chunk
first_chunk = chunks_data[chunk_ids[0]]
meta = first_chunk.get('metadata', {})

print("\n" + "="*70)
print("METADATA FIELDS IN FIRST CHUNK:")
print("="*70)

# Check campi critici
fields = {
    'qa_pairs': meta.get('qa_pairs', []),
    'keywords_primary': meta.get('keywords_primary', []),
    'iconic_quotes': meta.get('iconic_quotes', []),
    'key_concepts': meta.get('key_concepts', []),
    'natural_questions': meta.get('natural_questions', []),
    'author': meta.get('author', meta.get('autore', '')),
    'work': meta.get('work', meta.get('opera', '')),
    'chunk_title': meta.get('chunk_title', ''),
}

for field_name, field_value in fields.items():
    if isinstance(field_value, list):
        print(f"✓ {field_name}: {len(field_value)} items")
        if field_value:
            print(f"    Example: {field_value[0]}")
    else:
        print(f"✓ {field_name}: '{field_value}'")

# Verifica se original_text è presente
print("\n" + "="*70)
print("ORIGINAL TEXT CHECK:")
print("="*70)
print(f"Has 'original_text': {'original_text' in first_chunk}")
print(f"Has 'testo': {'testo' in first_chunk}")
if 'messages' in first_chunk:
    print(f"Has 'messages': Yes ({len(first_chunk['messages'])} messages)")

# Statistiche Q&A
print("\n" + "="*70)
print("Q&A STATISTICS:")
print("="*70)
total_qa = 0
chunks_with_qa = 0
for chunk_id, chunk in chunks_data.items():
    qa_count = len(chunk.get('metadata', {}).get('qa_pairs', []))
    if qa_count > 0:
        chunks_with_qa += 1
        total_qa += qa_count

print(f"Chunks with Q&A: {chunks_with_qa}/{len(chunks_data)}")
print(f"Total Q&A pairs: {total_qa}")

# Cache Q&A embeddings
qa_embeddings = cache.get('qa_embeddings', {})
print(f"Q&A embeddings in cache: {len(qa_embeddings)}")

print("\n" + "="*70)
print("SUMMARY FILES CHECK:")
print("="*70)
print("⚠️  Summary files are NOT loaded in cache (they're separate JSON files)")
print("   Location: Fonti/Autori/*/Processati/*/summaries/")
