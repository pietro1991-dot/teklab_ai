import pickle
from pathlib import Path

cache_path = Path("ai_system/Embedding/embeddings_cache.pkl")

with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

# Prendi primo chunk
first_id = list(cache.get('chunks_data', {}).keys())[0]
chunk = cache['chunks_data'][first_id]

print("🔍 Struttura completa chunk:")
print(f"\nID: {first_id}")
print(f"\nKeys top-level: {list(chunk.keys())}")

if 'messages' in chunk:
    print(f"\n📨 Messages ({len(chunk['messages'])} items):")
    for i, msg in enumerate(chunk['messages']):
        print(f"   {i}. role={msg.get('role')}, content_length={len(msg.get('content', ''))}")

if 'metadata' in chunk:
    print(f"\n📊 Metadata keys: {list(chunk['metadata'].keys())}")
    
# Cerca dove sta il testo originale
print("\n🔎 Cercando 'original_text'...")
if 'original_text' in chunk:
    print(f"✅ Trovato in chunk['original_text']")
elif 'metadata' in chunk and 'original_text' in chunk['metadata']:
    print(f"✅ Trovato in chunk['metadata']['original_text']")
else:
    print(f"❌ 'original_text' non trovato!")
    print("Contenuto 'messages[2]' (assistant):")
    if len(chunk.get('messages', [])) > 2:
        print(chunk['messages'][2]['content'][:200] + "...")
