"""Trova chunk con product_model Unknown"""

import pickle

# Carica cache
with open('ai_system/Embedding/embeddings_cache.pkl', 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})

print("="*70)
print("🔍 ANALISI CHUNK CON PRODUCT_MODEL UNKNOWN")
print("="*70)

unknown_chunks = []
valid_chunks = []

for chunk_id, chunk_data in chunks_data.items():
    metadata = chunk_data.get('metadata', {})
    product_model = metadata.get('product_model', 'Unknown')
    category = chunk_data.get('category', 'unknown')
    
    if product_model == 'Unknown':
        unknown_chunks.append((chunk_id, category, metadata))
    else:
        valid_chunks.append((chunk_id, product_model, category))

print(f"\n📊 STATISTICHE:")
print(f"   Totale chunks: {len(chunks_data)}")
print(f"   Chunk VALIDI (con product_model): {len(valid_chunks)}")
print(f"   Chunk UNKNOWN (senza product_model): {len(unknown_chunks)}")

if unknown_chunks:
    print(f"\n❌ CHUNK CON PRODUCT_MODEL UNKNOWN:")
    for chunk_id, category, metadata in unknown_chunks:
        print(f"\n   Chunk ID: {chunk_id}")
        print(f"   Category: {category}")
        print(f"   Metadata keys: {list(metadata.keys())}")
        
        # Prova a estrarre info dal chunk_id
        if '/' in chunk_id:
            parts = chunk_id.split('/')
            print(f"   Path parts: {parts}")
            
            # Cerca pattern tipo "tk3_130bar", "tk4_modbus", ecc.
            for part in parts:
                if 'tk3' in part.lower():
                    print(f"   💡 Suggerimento: Potrebbe essere TK3+ (da '{part}')")
                elif 'tk4' in part.lower():
                    print(f"   💡 Suggerimento: Potrebbe essere TK4 MODBUS (da '{part}')")
                elif 'tk1' in part.lower():
                    print(f"   💡 Suggerimento: Potrebbe essere TK1+ (da '{part}')")
                elif 'lc' in part.lower():
                    print(f"   💡 Suggerimento: Potrebbe essere LC series (da '{part}')")
                elif 'atex' in part.lower():
                    print(f"   💡 Suggerimento: Potrebbe essere ATEX (da '{part}')")

print(f"\n✅ CHUNK VALIDI (esempi):")
for chunk_id, product_model, category in valid_chunks[:5]:
    print(f"   • {product_model:30s} | {category:12s} | {chunk_id[:50]}")

print("\n" + "="*70)
