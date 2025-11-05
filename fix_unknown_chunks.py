"""Fix chunk Unknown - aggiungi product_model mancanti"""

import pickle
import os
from pathlib import Path

# Mappa chunk_id pattern → product_model
CHUNK_ID_TO_PRODUCT = {
    # TK3+ variants
    'tk3_130bar': 'TK3+ 130bar',
    'tk3_80bar': 'TK3+ 80bar',
    'tk3_46bar': 'TK3+ 46bar',
    'tk3_plus_130bar': 'TK3+ 130bar',
    'tk3_plus_80bar': 'TK3+ 80bar',
    'tk3_plus_46bar': 'TK3+ 46bar',
    
    # TK4 MODBUS
    'tk4': 'TK4 MODBUS',
    
    # TK1+
    'tk1': 'TK1+',
    
    # LC Series
    'lc_ps': 'LC-PS',
    'lc_ph': 'LC-PH',
    'lc_xp': 'LC-XP',
    'lc_xt': 'LC-XT',
    
    # ATEX
    'atex': 'ATEX Metallic IR',
    
    # Support/Guide chunks
    'comparison_guide': 'TK3+ vs TK4 Comparison',
    'troubleshooting_guide': 'Troubleshooting Guide',
    'selection_guide': 'Product Selection Guide',
    'pressure_rating': 'Pressure Rating Guide',
    
    # Technology
    'ir_technology': 'IR Technology',
    'optical_sensor': 'Optical Sensor Technology',
    
    # Applications
    'oil_management': 'Oil Management Application',
    'compressor': 'Compressor Application',
}

def infer_product_model(chunk_id):
    """Inferisci product_model dal chunk_id"""
    chunk_id_lower = chunk_id.lower()
    
    # Cerca pattern nel chunk_id
    for pattern, product_model in CHUNK_ID_TO_PRODUCT.items():
        if pattern in chunk_id_lower:
            return product_model
    
    # Fallback: usa ultima parte del path
    parts = chunk_id.split('/')
    if len(parts) >= 2:
        category = parts[1]  # 'products', 'support', 'technology', 'applications'
        return f"{category.capitalize()} Document"
    
    return "Teklab Product"

# Carica cache
cache_path = 'ai_system/Embedding/embeddings_cache.pkl'
print("="*70)
print("🔧 FIX CHUNK UNKNOWN - Aggiungi product_model mancanti")
print("="*70)

print(f"\n📂 Caricamento cache: {cache_path}")
with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

chunks_data = cache.get('chunks_data', {})

print(f"\n📊 STATISTICHE PRE-FIX:")
unknown_count = sum(1 for chunk_data in chunks_data.values() 
                    if chunk_data.get('metadata', {}).get('product_model', 'Unknown') == 'Unknown')
print(f"   Totale chunks: {len(chunks_data)}")
print(f"   Chunk Unknown: {unknown_count}")

# Fix chunk Unknown
fixed_count = 0
for chunk_id, chunk_data in chunks_data.items():
    metadata = chunk_data.get('metadata', {})
    
    if metadata.get('product_model', 'Unknown') == 'Unknown':
        # Inferisci product_model dal chunk_id
        inferred_product = infer_product_model(chunk_id)
        metadata['product_model'] = inferred_product
        
        print(f"\n✅ Fixed: {chunk_id[:60]}")
        print(f"   → product_model: {inferred_product}")
        
        fixed_count += 1

print(f"\n📊 STATISTICHE POST-FIX:")
print(f"   Chunk fixati: {fixed_count}")

unknown_count_after = sum(1 for chunk_data in chunks_data.values() 
                          if chunk_data.get('metadata', {}).get('product_model', 'Unknown') == 'Unknown')
print(f"   Chunk Unknown rimanenti: {unknown_count_after}")

if unknown_count_after == 0:
    print(f"\n🎉 TUTTI i chunk hanno ora product_model!")

# Backup vecchia cache
backup_path = cache_path + '.backup'
if not os.path.exists(backup_path):
    print(f"\n💾 Backup cache originale → {backup_path}")
    with open(cache_path, 'rb') as f_in:
        with open(backup_path, 'wb') as f_out:
            f_out.write(f_in.read())

# Salva cache aggiornata
print(f"\n💾 Salvataggio cache aggiornata...")
with open(cache_path, 'wb') as f:
    pickle.dump(cache, f)

print(f"\n✅ Cache aggiornata salvata: {cache_path}")
print(f"   (Backup originale: {backup_path})")

print("\n" + "="*70)
print("🎉 FIX COMPLETATO!")
print("="*70)
print("\n📝 PROSSIMI PASSI:")
print("   1. Riavvia il chatbot: python scripts/6_chatbot_ollama.py")
print("   2. Testa query: 'cosa sai del tk3?'")
print("   3. Verifica che ora mostri product names invece di 'Unknown'")
print("\n" + "="*70)
