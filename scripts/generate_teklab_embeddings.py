#!/usr/bin/env python3
"""
Generatore Embeddings per TEKLAB RAG System
============================================
Genera embeddings dai chunk creati da 3_create_chunks_with_llama_ollama.py

INPUT: Fonti/Autori/Teklab/Processati/chunks/**/*.json (nuova struttura)
OUTPUT: ai_system/Embedding/teklab_embeddings_cache.pkl

Esegui dopo aver creato i chunk con lo script 3_create_chunks_with_llama_ollama.py
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List
import sys

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Percorsi Teklab
CHUNKS_BASE = PROJECT_ROOT / "Fonti" / "Autori" / "Teklab" / "Processati" / "chunks"
EMBEDDINGS_OUTPUT = PROJECT_ROOT / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"

# Modello embeddings
EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'


class TeklabEmbeddingsGenerator:
    """Genera embeddings dai nuovi chunk Teklab"""
    
    def __init__(self):
        self.model = None
        self.chunks_data = {}  # chunk_id -> chunk completo
        self.chunk_embeddings = {}  # chunk_id -> embedding
        self.qa_embeddings = {}  # qa_id -> embedding
        
    def load_model(self):
        """Carica modello SentenceTransformer"""
        try:
            from sentence_transformers import SentenceTransformer
            print("\n🧠 Caricamento modello embeddings...")
            print(f"   Modello: {EMBEDDING_MODEL}")
            print("   Device: CPU (GPU riservata per Ollama)")
            
            self.model = SentenceTransformer(
                EMBEDDING_MODEL,
                device='cpu'
            )
            
            print("✅ Modello caricato\n")
            return True
            
        except Exception as e:
            print(f"❌ Errore caricamento modello: {e}")
            print("   Installa con: pip install sentence-transformers")
            return False
    
    def discover_chunks(self) -> List[Path]:
        """Trova tutti i file JSON chunk nelle sottodirectory"""
        if not CHUNKS_BASE.exists():
            print(f"❌ Directory chunks non trovata: {CHUNKS_BASE}")
            return []
        
        chunks = list(CHUNKS_BASE.glob("**/*.json"))
        print(f"📚 Trovati {len(chunks)} chunk files")
        
        # Raggruppa per categoria
        categories = {}
        for chunk_path in chunks:
            category = chunk_path.parent.name
            categories[category] = categories.get(category, 0) + 1
        
        print("\n📂 Distribuzione per categoria:")
        for cat, count in sorted(categories.items()):
            print(f"   • {cat}: {count} chunks")
        
        return chunks
    
    def load_chunk(self, chunk_path: Path) -> Dict:
        """Carica un file chunk JSON"""
        try:
            with open(chunk_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Errore lettura {chunk_path.name}: {e}")
            return None
    
    def generate_embeddings(self):
        """Genera tutti gli embeddings"""
        print("\n" + "="*70)
        print("🔧 TEKLAB EMBEDDINGS GENERATOR")
        print("="*70)
        
        # 1. Carica modello
        if not self.load_model():
            return False
        
        # 2. Scopri chunks
        chunk_files = self.discover_chunks()
        if not chunk_files:
            print("\n❌ Nessun chunk trovato!")
            return False
        
        print(f"\n⚙️  Generazione embeddings per {len(chunk_files)} chunks...")
        print("="*70)
        
        # 3. Processa ogni chunk
        processed = 0
        skipped = 0
        
        for i, chunk_path in enumerate(chunk_files, 1):
            chunk_data = self.load_chunk(chunk_path)
            
            if not chunk_data:
                skipped += 1
                continue
            
            chunk_id = chunk_data.get('id', chunk_path.stem)
            
            # Salva chunk completo
            self.chunks_data[chunk_id] = chunk_data
            
            # ARCHITETTURA TEKLAB: usa messages[2].content (assistant formatted)
            messages = chunk_data.get('messages', [])
            text_to_embed = ""
            
            if len(messages) > 2:
                # Priorità: assistant message (formatted response)
                text_to_embed = messages[2].get('content', '')
            elif len(messages) > 1:
                # Fallback: user content (semantic concept)
                text_to_embed = messages[1].get('content', '')
            else:
                # Fallback finale: original_text
                text_to_embed = chunk_data.get('original_text', '')
            
            if not text_to_embed:
                print(f"   ⚠️  [{i}/{len(chunk_files)}] Skip {chunk_id[:50]}... (no text)")
                skipped += 1
                continue
            
            # Genera embedding per chunk
            try:
                embedding = self.model.encode([text_to_embed])[0]
                self.chunk_embeddings[chunk_id] = embedding
                processed += 1
                
                # Progress ogni 10 chunks
                if processed % 10 == 0:
                    print(f"   ✅ [{processed}/{len(chunk_files)}] Processati {processed} chunks...")
            
            except Exception as e:
                print(f"   ❌ Errore embedding {chunk_id}: {e}")
                skipped += 1
                continue
            
            # Genera embeddings per Q&A pairs
            metadata = chunk_data.get('metadata', {})
            qa_pairs = metadata.get('qa_pairs', [])
            
            for qa_idx, qa in enumerate(qa_pairs):
                qa_id = f"{chunk_id}_qa_{qa_idx}"
                question = qa.get('question', '')
                answer = qa.get('answer', '')
                
                if question and answer:
                    # Embedding sul testo question + answer
                    qa_text = f"{question} {answer}"
                    try:
                        qa_embedding = self.model.encode([qa_text])[0]
                        self.qa_embeddings[qa_id] = qa_embedding
                    except Exception as e:
                        print(f"   ⚠️  Errore QA embedding {qa_id}: {e}")
        
        print(f"\n✅ Processati {processed} chunks")
        print(f"⚠️  Saltati {skipped} chunks")
        print(f"📝 Q&A embeddings: {len(self.qa_embeddings)}")
        
        # 4. Salva cache
        return self.save_cache()
    
    def save_cache(self) -> bool:
        """Salva cache embeddings"""
        print(f"\n💾 Salvataggio cache embeddings...")
        
        # Crea directory se non esiste
        EMBEDDINGS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        
        cache_data = {
            'model': EMBEDDING_MODEL,
            'chunks_data': self.chunks_data,
            'chunk_embeddings': self.chunk_embeddings,
            'qa_embeddings': self.qa_embeddings,
            'summary_embeddings': {},  # Vuoto per ora (summaries non implementate)
            'summaries_data': {},  # Vuoto per ora
            'version': '2.0_teklab'
        }
        
        try:
            with open(EMBEDDINGS_OUTPUT, 'wb') as f:
                pickle.dump(cache_data, f)
            
            print(f"✅ Cache salvata: {EMBEDDINGS_OUTPUT}")
            print(f"\n📊 Statistiche:")
            print(f"   • Chunks: {len(self.chunks_data)}")
            print(f"   • Chunk embeddings: {len(self.chunk_embeddings)}")
            print(f"   • Q&A embeddings: {len(self.qa_embeddings)}")
            
            # Calcola dimensione file
            file_size_mb = EMBEDDINGS_OUTPUT.stat().st_size / (1024 * 1024)
            print(f"   • Dimensione cache: {file_size_mb:.2f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore salvataggio cache: {e}")
            return False


def main():
    """Entry point"""
    print("\n" + "="*70)
    print("🔧 TEKLAB EMBEDDINGS GENERATOR")
    print("="*70)
    print()
    print("Questo script genera embeddings dai chunk creati da:")
    print("  scripts/3_create_chunks_with_llama_ollama.py")
    print()
    print(f"📂 Input:  {CHUNKS_BASE}")
    print(f"💾 Output: {EMBEDDINGS_OUTPUT}")
    print()
    print("="*70 + "\n")
    
    generator = TeklabEmbeddingsGenerator()
    success = generator.generate_embeddings()
    
    if success:
        print("\n" + "="*70)
        print("✅ EMBEDDINGS GENERATI CON SUCCESSO")
        print("="*70)
        print()
        print("📋 Prossimi passi:")
        print("   1. Avvia backend: python backend_api/app.py")
        print("   2. Apri UI: UI_experience/index.html")
        print("   3. Testa chatbot: python scripts/6_chatbot_ollama.py")
        print()
    else:
        print("\n❌ Generazione embeddings fallita")
        sys.exit(1)


if __name__ == "__main__":
    main()
