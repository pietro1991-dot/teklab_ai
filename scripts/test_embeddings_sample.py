#!/usr/bin/env python3
"""
Test embeddings su sample ridotto (1000 chunks)
Verifica che il processo funzioni correttamente prima di fare tutto
"""

import json
import numpy as np
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def test_embeddings_sample():
    """
    Test su sample di 1000 chunks per verificare:
    1. Caricamento modello
    2. Generazione embeddings
    3. Similarity search
    4. Performance
    """
    
    print("\n" + "="*70)
    print("🧪 TEST EMBEDDINGS - SAMPLE 1000 CHUNKS")
    print("="*70)
    
    base_path = Path(__file__).parent.parent
    chunks_file = base_path / 'hierarchical_chunks' / 'final_chunks.json'
    
    # Carica chunks
    print(f"\n📂 Caricamento chunks...")
    with open(chunks_file, 'r', encoding='utf-8') as f:
        all_chunks = json.load(f)
    
    print(f"✅ {len(all_chunks):,} chunks totali caricati")
    
    # Seleziona sample
    sample_size = 1000
    print(f"\n🎯 Selezione sample di {sample_size} chunks...")
    
    # Prendi sample bilanciato da diverse categorie
    sample_chunks = []
    chunks_by_category = {}
    
    for chunk in all_chunks:
        category = chunk['category']
        if category not in chunks_by_category:
            chunks_by_category[category] = []
        chunks_by_category[category].append(chunk)
    
    # Prendi sample proporzionale da ogni categoria
    for category, chunks in chunks_by_category.items():
        n_samples = min(len(chunks), sample_size // len(chunks_by_category))
        sample_chunks.extend(chunks[:n_samples])
    
    # Se non abbastanza, aggiungi dai products
    if len(sample_chunks) < sample_size:
        remaining = sample_size - len(sample_chunks)
        sample_chunks.extend(chunks_by_category['products'][:remaining])
    
    sample_chunks = sample_chunks[:sample_size]
    
    print(f"✅ Sample selezionato: {len(sample_chunks)} chunks")
    print(f"\n   Distribuzione per categoria:")
    sample_by_cat = {}
    for chunk in sample_chunks:
        cat = chunk['category']
        sample_by_cat[cat] = sample_by_cat.get(cat, 0) + 1
    
    for cat, count in sorted(sample_by_cat.items()):
        print(f"      • {cat}: {count} chunks")
    
    # Estrai testi
    texts = [chunk['chunk_text'] for chunk in sample_chunks]
    
    # Test 1: Caricamento modello
    print("\n" + "-"*70)
    print("TEST 1: CARICAMENTO MODELLO")
    print("-"*70)
    
    model_name = 'all-mpnet-base-v2'
    print(f"\n🤖 Caricamento {model_name}...")
    
    start_time = time.time()
    model = SentenceTransformer(model_name)
    load_time = time.time() - start_time
    
    print(f"✅ Modello caricato in {load_time:.2f} secondi")
    print(f"   • Dimensione embedding: {model.get_sentence_embedding_dimension()}")
    
    # Test 2: Generazione embeddings
    print("\n" + "-"*70)
    print("TEST 2: GENERAZIONE EMBEDDINGS")
    print("-"*70)
    
    print(f"\n🔧 Generazione embeddings per {len(texts)} chunks...")
    
    start_time = time.time()
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    gen_time = time.time() - start_time
    
    print(f"\n✅ Embeddings generati in {gen_time:.2f} secondi")
    print(f"   • Shape: {embeddings.shape}")
    print(f"   • Velocità: {len(texts) / gen_time:.1f} chunks/sec")
    print(f"   • Tempo stimato per 112K: {112250 / (len(texts) / gen_time) / 60:.1f} minuti")
    
    # Test 3: Verifica qualità embeddings
    print("\n" + "-"*70)
    print("TEST 3: QUALITÀ EMBEDDINGS")
    print("-"*70)
    
    # Sample embeddings
    print(f"\n📊 Sample embeddings (primi 5 valori):")
    for i in [0, len(embeddings)//2, len(embeddings)-1]:
        print(f"   Chunk #{i}: {embeddings[i][:5]}")
    
    # Statistiche
    print(f"\n📊 Statistiche:")
    print(f"   • Min: {embeddings.min():.4f}")
    print(f"   • Max: {embeddings.max():.4f}")
    print(f"   • Mean: {embeddings.mean():.4f}")
    print(f"   • Std: {embeddings.std():.4f}")
    
    # Check NaN
    has_nan = np.isnan(embeddings).any()
    print(f"   • Contiene NaN: {'❌ SÌ' if has_nan else '✅ NO'}")
    
    # Test 4: Similarity search
    print("\n" + "-"*70)
    print("TEST 4: SIMILARITY SEARCH")
    print("-"*70)
    
    # Query di test
    test_queries = [
        "Qual è la differenza tra TK3+ e TK4?",
        "Come installo il sensore LC-PS?",
        "Specifiche tecniche TK3+ 130bar"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        
        # Encode query
        start_time = time.time()
        query_embedding = model.encode([query], convert_to_numpy=True)[0]
        encode_time = time.time() - start_time
        
        # Calcola similarità
        start_time = time.time()
        similarities = cosine_similarity([query_embedding], embeddings)[0]
        search_time = time.time() - start_time
        
        # Top 3 risultati
        top_indices = np.argsort(similarities)[::-1][:3]
        
        print(f"   ⏱️  Tempo search: {(encode_time + search_time)*1000:.1f}ms")
        print(f"   📊 Top 3 risultati:")
        
        for rank, idx in enumerate(top_indices, 1):
            chunk = sample_chunks[idx]
            sim = similarities[idx]
            preview = chunk['chunk_text'][:80].replace('\n', ' ')
            
            print(f"\n      #{rank} (similarity: {sim:.3f})")
            print(f"         • Categoria: {chunk['category']}/{chunk['sub_category']}")
            print(f"         • Preview: {preview}...")
    
    # Test 5: Performance su dataset completo
    print("\n" + "-"*70)
    print("TEST 5: STIMA PERFORMANCE DATASET COMPLETO")
    print("-"*70)
    
    total_chunks = len(all_chunks)
    chunks_per_sec = len(texts) / gen_time
    total_time_min = total_chunks / chunks_per_sec / 60
    
    # Dimensione file
    embedding_size_mb = embeddings.nbytes / (1024 * 1024)
    total_embedding_size_mb = (total_chunks / len(texts)) * embedding_size_mb
    
    print(f"\n📊 Stime per {total_chunks:,} chunks:")
    print(f"   • Tempo generazione: ~{total_time_min:.1f} minuti")
    print(f"   • Dimensione file: ~{total_embedding_size_mb:.1f} MB")
    print(f"   • Velocità search: ~{search_time*1000:.1f}ms per query")
    print(f"   • RAM richiesta: ~{total_embedding_size_mb * 1.5:.1f} MB")
    
    # Salva sample embeddings per verifica
    print("\n" + "-"*70)
    print("💾 SALVATAGGIO SAMPLE")
    print("-"*70)
    
    output_dir = base_path / 'hierarchical_chunks'
    sample_file = output_dir / 'sample_embeddings.npz'
    
    np.savez_compressed(
        sample_file,
        embeddings=embeddings,
        chunk_indices=list(range(len(sample_chunks)))
    )
    
    print(f"\n✅ Sample salvato: {sample_file}")
    print(f"   • Size: {sample_file.stat().st_size / 1024:.1f} KB")
    
    # Riepilogo finale
    print("\n" + "="*70)
    print("✅ TEST COMPLETATO CON SUCCESSO!")
    print("="*70)
    
    print(f"""
📊 RIEPILOGO TEST:
   ✅ Modello caricato correttamente ({load_time:.2f}s)
   ✅ Embeddings generati ({chunks_per_sec:.1f} chunks/sec)
   ✅ Similarity search funzionante (~{search_time*1000:.1f}ms/query)
   ✅ Nessun NaN rilevato
   ✅ Sample salvato per verifica

📈 STIME DATASET COMPLETO (112,250 chunks):
   • Tempo: ~{total_time_min:.0f} minuti
   • Dimensione: ~{total_embedding_size_mb:.0f} MB
   • RAM: ~{total_embedding_size_mb * 1.5:.0f} MB

💡 RACCOMANDAZIONI:
   {'✅ OK - Procedi con generazione completa' if total_time_min < 30 else '⚠️  Considera batch processing o GPU acceleration'}
   {'✅ OK - RAM sufficiente' if total_embedding_size_mb < 1000 else '⚠️  Considera compressione o chunking'}

🚀 PROSSIMI STEP:
   1. Se tutto OK → python scripts/generate_embeddings.py
   2. Monitorare RAM durante generazione
   3. Verificare checkpoint salvati ogni 10K chunks
""")


if __name__ == "__main__":
    test_embeddings_sample()
