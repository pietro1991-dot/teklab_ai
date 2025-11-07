"""
Verifica qualità chunking gerarchico
"""
import json
from pathlib import Path
from collections import defaultdict

def verify_hierarchical_chunks():
    """Verifica la qualità dei chunk generati"""
    base_path = Path(__file__).parent.parent / 'hierarchical_chunks'
    
    print("\n" + "="*60)
    print("🔍 VERIFICA CHUNKING GERARCHICO")
    print("="*60)
    
    # Carica statistiche
    with open(base_path / 'chunking_statistics.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    print("\n📊 STATISTICHE GENERALI:")
    print(f"   • Category chunks: {stats['summary']['total_category_chunks']}")
    print(f"   • Sub-chunks totali: {stats['summary']['total_sub_chunks']:,}")
    print(f"   • Max sub-chunk size: {stats['summary']['max_subchunk_size']} chars")
    
    print("\n📏 DISTRIBUZIONE DIMENSIONI SUB-CHUNK:")
    dist = stats['chunk_size_distribution']
    print(f"   • Min: {dist['min']} chars")
    print(f"   • Max: {dist['max']} chars")
    print(f"   • Media: {dist['avg']:.0f} chars")
    
    print("\n📁 STATISTICHE PER CATEGORIA:")
    for category, data in sorted(stats['by_category'].items()):
        print(f"\n   {category.upper()}:")
        print(f"      • Sub-chunks: {data['sub_chunks']:,}")
        print(f"      • Totale chars: {data['total_chars']:,}")
        print(f"      • Media chunk: {data['avg_chunk_size']:.0f} chars")
    
    # Carica e analizza sample di final chunks
    print("\n" + "="*60)
    print("🔍 SAMPLE FINAL CHUNKS")
    print("="*60)
    
    with open(base_path / 'final_chunks.json', 'r', encoding='utf-8') as f:
        final_chunks = json.load(f)
    
    # Raggruppa per categoria
    by_category = defaultdict(list)
    for chunk in final_chunks:
        by_category[chunk['category']].append(chunk)
    
    # Mostra sample da ogni categoria
    for category in ['products', 'support', 'applications']:
        if category not in by_category:
            continue
        
        chunks = by_category[category]
        sample = chunks[0]  # Primo chunk
        
        print(f"\n📄 SAMPLE: {category.upper()}")
        print(f"   Categoria: {sample['category']}")
        print(f"   Sub-categoria: {sample['sub_category']}")
        print(f"   Sub-chunk ID: {sample['sub_chunk_id']}")
        print(f"   Dimensione: {sample['chunk_length']} chars")
        print(f"   File sorgente: {', '.join(sample['source_files'][:2])}")
        
        # Preview contenuto
        preview = sample['chunk_text'][:300]
        print(f"\n   🔍 PREVIEW (primi 300 chars):")
        print(f"   {'-'*56}")
        print(f"   {preview}")
        print(f"   {'-'*56}")
    
    # Verifica chunk troppo piccoli o grandi
    print("\n" + "="*60)
    print("⚠️  ANALISI ANOMALIE")
    print("="*60)
    
    too_small = [c for c in final_chunks if c['chunk_length'] < 100]
    too_large = [c for c in final_chunks if c['chunk_length'] > 600]
    
    print(f"\n   • Chunk < 100 chars: {len(too_small)} ({len(too_small)/len(final_chunks)*100:.1f}%)")
    if too_small:
        print(f"     Esempio: {too_small[0]['sub_category']} - {too_small[0]['chunk_length']} chars")
    
    print(f"\n   • Chunk > 600 chars: {len(too_large)} ({len(too_large)/len(final_chunks)*100:.1f}%)")
    if too_large:
        print(f"     Esempio: {too_large[0]['sub_category']} - {too_large[0]['chunk_length']} chars")
    
    optimal = [c for c in final_chunks if 300 <= c['chunk_length'] <= 600]
    print(f"\n   ✅ Chunk ottimali (300-600): {len(optimal)} ({len(optimal)/len(final_chunks)*100:.1f}%)")
    
    # Verifica metadata
    print("\n" + "="*60)
    print("🏷️  VERIFICA METADATA")
    print("="*60)
    
    sample_chunk = final_chunks[100]
    print(f"\n   Sample chunk #{100}:")
    print(f"   • Category: {sample_chunk['category']}")
    print(f"   • Sub-category: {sample_chunk['sub_category']}")
    print(f"   • Sub-chunk ID: {sample_chunk['sub_chunk_id']}")
    print(f"   • Level: {sample_chunk['level']}")
    print(f"   • Num files: {sample_chunk['num_files']}")
    print(f"   • Source files: {len(sample_chunk['source_files'])} file")
    
    print("\n" + "="*60)
    print("✅ VERIFICA COMPLETATA")
    print("="*60)
    
    # Raccomandazioni
    print("\n💡 RACCOMANDAZIONI:")
    
    if len(too_small) / len(final_chunks) > 0.1:
        print("   ⚠️  Molti chunk troppo piccoli - considera di aumentare max_subchunk_size")
    
    if len(too_large) / len(final_chunks) > 0.1:
        print("   ⚠️  Molti chunk troppo grandi - considera di ridurre max_subchunk_size")
    
    if len(optimal) / len(final_chunks) > 0.7:
        print("   ✅ Ottima distribuzione dimensioni chunk!")
    
    print("\n   📌 Prossimi step:")
    print("   1. Genera embeddings per final_chunks.json")
    print("   2. Salva embeddings con metadata (categoria, sub_category)")
    print("   3. Integra nel sistema RAG esistente")

if __name__ == "__main__":
    verify_hierarchical_chunks()
