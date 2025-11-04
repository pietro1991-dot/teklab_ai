#!/usr/bin/env python3
"""
Test rapido dello script di creazione chunk con Llama 3.2 3B
"""
import sys
from pathlib import Path

# Setup path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

print("="*70)
print("🧪 TEST CREAZIONE CHUNK CON LLAMA 3.2 3B")
print("="*70)

# Verifica che il modello esista
model_path = SCRIPT_DIR / "ai_system" / "models" / "Llama-3.2-3B-Instruct"
if not model_path.exists():
    print(f"\n❌ Modello non trovato: {model_path}")
    print("   Esegui: python download_llama_3_2_3b.py")
    exit(1)

print(f"\n✅ Modello trovato: {model_path}")

# Verifica che esistano le trascrizioni
transcripts_dir = SCRIPT_DIR / "Fonti" / "Autori" / "Mathias de Stefano" / "Originali" / "Pyramid.mathias"
if not transcripts_dir.exists():
    print(f"\n❌ Directory trascrizioni non trovata: {transcripts_dir}")
    exit(1)

transcripts = list(transcripts_dir.glob("Day_*_Transcript.txt"))
print(f"\n✅ Trovate {len(transcripts)} trascrizioni")

if transcripts:
    print(f"\n📄 Esempio: {transcripts[0].name}")
    
    # Mostra prime righe
    with open(transcripts[0], 'r', encoding='utf-8') as f:
        content = f.read()
        preview = content[:300]
        print(f"\n📖 Preview contenuto:")
        print(f"   {preview}...")
        print(f"   Lunghezza totale: {len(content)} caratteri")

print("\n" + "="*70)
print("📋 COME USARE:")
print("="*70)
print("\n1. Genera chunk per un singolo giorno (più veloce per test):")
print("   python scripts/3_create_chunks_with_llama.py --days 1")

print("\n2. Genera chunk per un range di giorni:")
print("   python scripts/3_create_chunks_with_llama.py --range 1 3")

print("\n3. Genera chunk per tutti i giorni:")
print("   python scripts/3_create_chunks_with_llama.py")

print("\n4. Limita numero di chunk per test rapido:")
print("   python scripts/3_create_chunks_with_llama.py --days 1 --max-chunks 2")

print("\n⏱️  Tempo stimato:")
print("   - 1 chunk: ~1-2 minuti")
print("   - 1 giorno completo: ~10-30 minuti")
print("   - Tutti i giorni: ~3-8 ore")

print("\n💡 Suggerimento: inizia con --days 1 --max-chunks 1 per testare!")
print("="*70)