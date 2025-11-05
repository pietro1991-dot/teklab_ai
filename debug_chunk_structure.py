"""Verifica struttura chunk TK3+"""

import pickle
import json

cache_path = 'ai_system/Embedding/embeddings_cache.pkl'

with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})

# Trova chunk TK3+ dall'ID
tk3_chunks = [
    chunk_id for chunk_id in chunks_data.keys() 
    if 'tk3' in chunk_id.lower()
]

print("="*70)
print("🔍 STRUTTURA CHUNK TK3+")
print("="*70)

for chunk_id in tk3_chunks[:5]:  # Primi 5
    chunk_data = chunks_data[chunk_id]
    
    print(f"\n📦 Chunk ID: {chunk_id}")
    print(f"   Chiavi disponibili: {list(chunk_data.keys())}")
    
    # Mostra contenuto completo
    print(f"\n   Contenuto completo:")
    for key, value in chunk_data.items():
        if key == 'original_text' or key == 'testo':
            print(f"   • {key}: {value[:100]}..." if len(str(value)) > 100 else f"   • {key}: {value}")
        elif key == 'metadata':
            print(f"   • metadata:")
            if isinstance(value, dict):
                for meta_key, meta_val in value.items():
                    print(f"      - {meta_key}: {meta_val}")
            else:
                print(f"      {value}")
        else:
            print(f"   • {key}: {value}")

print("\n" + "="*70)
