"""
Generatore di Embeddings per RAG Chatbot - Teklab B2B AI
Genera embeddings di tutti i chunks (5 categorie: Oil_Level_Regulators, Level_Switches, Sensors, Support, General) e Q&A
Esegui quando aggiungi nuovi prodotti o contenuti tecnici
"""

import json
import pickle
from pathlib import Path

# Lazy import per velocizzare startup
SentenceTransformer = None

def import_sentence_transformers():
    """Import lazy di SentenceTransformer per velocizzare startup"""
    global SentenceTransformer
    if SentenceTransformer is None:
        try:
            print("🔄 Caricamento librerie (prima volta può richiedere 10-30 secondi)...")
            from sentence_transformers import SentenceTransformer as ST
            SentenceTransformer = ST
            print("✅ Librerie caricate\n")
            return True
        except ImportError:
            print("❌ Installare prima: pip install sentence-transformers scikit-learn")
            return False
    return True

# Configurazione (deve stare dopo gli import)
SCRIPT_DIR = Path(__file__).parent  # scripts/
PROJECT_ROOT = SCRIPT_DIR.parent  # Root del progetto (teklab_ai/)
FONTI_BASE_PATH = PROJECT_ROOT / "Fonti" / "Teklab" / "input" / "Dal Catalogo" / "Processati"  # ✅ Path corretto
EMBEDDINGS_CACHE_PATH = PROJECT_ROOT / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"  # ✅ TEKLAB cache

# Modello embeddings (puoi cambiarlo)
EMBEDDING_MODEL = 'all-mpnet-base-v2'  # Più preciso per contenuto tecnico (768-dim)
# Alternative:
# 'all-MiniLM-L6-v2'  # Più veloce ma meno preciso (384-dim)
# 'paraphrase-multilingual-MiniLM-L12-v2'  # Migliore per italiano (ma contenuto è in inglese)

class EmbeddingsGenerator:
    def __init__(self):
        # Non caricare subito il modello, solo quando serve
        self.model = None
        self.chunks = {}
        self.qa_pairs = {}
        self.summaries = {}  # NUOVO: Summary files per giorno/capitolo
        self.chunk_embeddings = {}
        self.qa_embeddings = {}
        self.summary_embeddings = {}  # NUOVO: Embeddings per summaries
    
    def _load_model(self):
        """Carica modello embeddings (lazy loading)"""
        if self.model is None:
            if not import_sentence_transformers():
                return False
            print("🧠 Inizializzazione modello embeddings...")
            print(f"   Modello: {EMBEDDING_MODEL}")
            print("   Device: CPU (GPU riservata per Llama)")
            # FORZA CPU per risparmiare VRAM GPU
            self.model = SentenceTransformer(EMBEDDING_MODEL, device='cpu')
            print("✅ Modello caricato su CPU\n")
        return True
    
    def find_all_rag_folders(self):
        """Trova tutte le cartelle chunks in Fonti/Autori/Teklab/Processati/"""
        rag_data = {
            "chunks_folders": [],
            "metadata_files": [],
            "keywords_file": None,
            "qa_file": None
        }
        
        if not FONTI_BASE_PATH.exists():
            print(f"❌ Cartella Processati non trovata: {FONTI_BASE_PATH}")
            return rag_data
        
        # Struttura Teklab aggiornata:
        # Fonti/Teklab/input/Dal Catalogo/Processati/
        #   ├── chunks/
        #   │   ├── oil_level_regulators/
        #   │   ├── level_switches/
        #   │   └── ... (altre categorie)
        #   ├── summaries/
        #   └── .checkpoints/
        
        chunks_base = FONTI_BASE_PATH / "chunks"
        
        # Trova cartelle chunks (le categorie di prodotti)
        if chunks_base.exists():
            for category_dir in chunks_base.iterdir():
                if category_dir.is_dir():
                    rag_data["chunks_folders"].append({
                        "path": category_dir,
                        "category": category_dir.name,
                        "source": "Teklab"
                    })
        
        # I file metadata, keywords e qa_pairs non sono più aggregati,
        # quindi non li cerchiamo più qui.
        
        return rag_data
    
    def load_all_data(self):
        """Carica tutti i chunks e Q&A da struttura Teklab"""
        print("📚 Caricamento dati Teklab da Fonti...\n")
        
        rag_data = self.find_all_rag_folders()
        
        chunks_folders = rag_data["chunks_folders"]
        
        if not chunks_folders:
            print("❌ Nessuna cartella chunks trovata!")
            print(f"   Verifica che esista: {FONTI_BASE_PATH / 'chunks'}")
            return False
        
        print(f"✅ Trovate {len(chunks_folders)} categorie:\n")
        
        # Carica chunks da ogni categoria
        total_chunks = 0
        total_qa_pairs = 0
        for folder_info in chunks_folders:
            category_path = folder_info["path"]
            category = folder_info["category"]
            
            print(f"   - {category}/")
            
            # Carica tutti i JSON nella categoria
            chunk_files = sorted(category_path.glob("*.json"))
            category_chunk_count = 0
            category_qa_count = 0
            
            for chunk_file in chunk_files:
                try:
                    with open(chunk_file, "r", encoding="utf-8") as f:
                        chunk_data = json.load(f)
                        
                        # L'ID del chunk è già nel file
                        chunk_id = chunk_data.get("id", chunk_file.stem)
                        
                        # Aggiungi metadata di categoria per coerenza
                        chunk_data["metadata"]["category_folder"] = category
                        chunk_data["metadata"]["source"] = "Teklab"
                        
                        # Salva in self.chunks
                        if chunk_id not in self.chunks:
                            self.chunks[chunk_id] = chunk_data
                            category_chunk_count += 1
                            total_chunks += 1

                        # Estrai e salva le Q&A da questo chunk
                        qa_pairs = chunk_data.get("metadata", {}).get("qa_pairs", [])
                        if qa_pairs:
                            self.qa_pairs[chunk_id] = qa_pairs
                            category_qa_count += len(qa_pairs)
                            total_qa_pairs += len(qa_pairs)
                        
                except Exception as e:
                    print(f"      ⚠️  Errore {chunk_file.name}: {e}")
            
            print(f"      → {category_chunk_count} chunks, {category_qa_count} Q&A pairs")
        
        print(f"\n{'='*60}")
        print("📊 DATI CARICATI:")
        print(f"   • Categorie: {len(chunks_folders)}")
        print(f"   • Chunks totali: {total_chunks}")
        print(f"   • Q&A totali: {total_qa_pairs}")
        print(f"   • Testi da codificare: {total_chunks + total_qa_pairs}")
        print(f"{'='*60}\n")
        
        return True
    
    def generate_embeddings(self):
        """Genera embeddings per tutti i testi Teklab"""
        print("🔄 GENERAZIONE EMBEDDINGS IN CORSO...\n")
        
        # Carica modello ora (lazy loading)
        if not self._load_model():
            return False
        
        texts_to_encode = []
        text_ids = []
        
        # Prepara testi chunks da categorie Teklab
        print("📝 Preparazione chunks Teklab...")
        for chunk_id, chunk in self.chunks.items():
            
            # Estrai contenuto dal formato Teklab (original_text)
            original_text = chunk.get('original_text', '')
            
            # Estrai metadata Teklab
            metadata = chunk.get('metadata', {})
            
            # Dati specifici Teklab
            product_category = metadata.get('product_category', '')
            chunk_title = metadata.get('chunk_title', '')
            
            # Keywords e concetti
            keywords = metadata.get('keywords_primary', [])
            keywords_text = ', '.join(keywords[:10]) if keywords else ''
            
            concepts = metadata.get('key_concepts', [])
            concepts_text = ', '.join(concepts[:5]) if concepts else ''

            # Costruisci testo arricchito per embedding
            enriched_parts = [
                "Source: Teklab",
                f"Category: {product_category}",
                f"Title: {chunk_title}"
            ]
            
            if concepts_text:
                enriched_parts.append(f"Key Concepts: {concepts_text}")
            if keywords_text:
                enriched_parts.append(f"Keywords: {keywords_text}")
            
            # Aggiungi contenuto principale
            enriched_parts.append(f"\nContent:\n{original_text}")
            
            text = '\n'.join(enriched_parts)
            
            if text.strip():
                texts_to_encode.append(text)
                text_ids.append(('chunk', chunk_id))
        
        chunk_count = len([x for x in text_ids if x[0] == 'chunk'])
        print(f"   ✅ {chunk_count} chunks preparati")
        
        # Prepara testi Q&A estratti dai chunk
        print("📝 Preparazione Q&A...")
        for chunk_id, qa_list in self.qa_pairs.items():
            for idx, qa in enumerate(qa_list):
                qa_id = f"{chunk_id}|qa_{idx}"
                question = qa.get('question', '')
                answer = qa.get('answer', '')
                
                # Combina domanda + risposta per embedding
                text = f"Q: {question}\nA: {answer}"
                
                if text.strip():
                    texts_to_encode.append(text)
                    text_ids.append(('qa', qa_id))
        
        qa_count = len([x for x in text_ids if x[0] == 'qa'])
        print(f"   ✅ {qa_count} Q&A preparati")
        print(f"   📊 Totale testi: {len(texts_to_encode)}\n")
        
        if not texts_to_encode:
            print("❌ Nessun testo da codificare!")
            return False
        
        # Genera embeddings con progress bar
        print(f"🧠 Codifica {len(texts_to_encode)} testi...")
        print("   (Può richiedere 1-3 minuti a seconda della CPU)\n")
        
        embeddings = self.model.encode(
            texts_to_encode, 
            show_progress_bar=True,
            batch_size=32  # Regola in base alla RAM
        )
        
        # Salva embeddings
        print("\n💾 Salvataggio embeddings...")
        
        # Prepara dati chunks per salvataggio (i chunk sono già nel formato corretto)
        chunks_data = self.chunks
        
        # Assegna embeddings agli ID corrispondenti
        for (text_type, text_id), embedding in zip(text_ids, embeddings):
            if text_type == 'chunk':
                self.chunk_embeddings[text_id] = embedding
            elif text_type == 'qa':
                self.qa_embeddings[text_id] = embedding
        
        print(f"   ✅ Chunks: {len(self.chunk_embeddings)}")
        print(f"   ✅ Q&A: {len(self.qa_embeddings)}")
        
        # Salva cache
        print(f"\n💾 Salvataggio cache in {EMBEDDINGS_CACHE_PATH.name}...")
        try:
            # Crea directory se non esiste
            EMBEDDINGS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            with open(EMBEDDINGS_CACHE_PATH, 'wb') as f:
                pickle.dump({
                    'chunk_embeddings': self.chunk_embeddings,
                    'qa_embeddings': self.qa_embeddings,
                    'chunks_data': chunks_data,  # Dati originali chunks
                    'model': EMBEDDING_MODEL
                }, f)
            
            # Mostra dimensione file
            size_mb = EMBEDDINGS_CACHE_PATH.stat().st_size / (1024 * 1024)
            print(f"   ✅ Cache salvata ({size_mb:.1f} MB)\n")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Errore salvataggio: {e}\n")
            return False
    
    def verify_cache(self):
        """Verifica che la cache sia valida"""
        if not EMBEDDINGS_CACHE_PATH.exists():
            return False
        
        try:
            with open(EMBEDDINGS_CACHE_PATH, 'rb') as f:
                cache = pickle.load(f)
            
            chunk_emb = cache.get('chunk_embeddings', {})
            qa_emb = cache.get('qa_embeddings', {})
            model_used = cache.get('model', 'unknown')
            
            print("\n✅ CACHE VALIDA:")
            print(f"   • Modello: {model_used}")
            print(f"   • Chunks: {len(chunk_emb)}")
            print(f"   • Q&A: {len(qa_emb)}")
            
            # Mostra dimensione file
            size_mb = EMBEDDINGS_CACHE_PATH.stat().st_size / (1024 * 1024)
            print(f"   • Dimensione: {size_mb:.1f} MB\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Cache corrotta: {e}")
            return False


def main():
    """Script principale"""
    print("\n" + "="*60)
    print("🚀 GENERATORE EMBEDDINGS - RAG CHATBOT")
    print("="*60 + "\n")
    
    # Check dipendenze prima di procedere
    print("🔍 Verifica dipendenze...")
    if not import_sentence_transformers():
        print("\n❌ Dipendenze mancanti! Installa con:")
        print("   pip install sentence-transformers scikit-learn torch\n")
        return
    print("✅ Dipendenze OK\n")
    
    # Verifica cache esistente
    if EMBEDDINGS_CACHE_PATH.exists():
        print("⚠️  Cache embeddings già presente!\n")
        print("Opzioni:")
        print("  [R] Rigenera (sovrascrive cache esistente)")
        print("  [V] Verifica cache (leggi info)")
        print("  [Q] Esci")
        
        choice = input("\nScegli [R/V/Q]: ").strip().upper()
        
        if choice == 'Q':
            print("\n👋 Uscita\n")
            return
        elif choice == 'V':
            generator = EmbeddingsGenerator()
            generator.verify_cache()
            return
        elif choice != 'R':
            print("❌ Scelta non valida")
            return
        
        print()
    
    # Inizializza generator
    generator = EmbeddingsGenerator()
    
    # Carica dati
    if not generator.load_all_data():
        print("❌ Errore caricamento dati")
        return
    
    # Conferma prima di generare
    print("⚠️  ATTENZIONE: La generazione può richiedere 1-3 minuti")
    confirm = input("Procedere? [S/n]: ").strip().upper()
    
    if confirm and confirm != 'S':
        print("\n❌ Operazione annullata\n")
        return
    
    print()
    
    # Genera embeddings
    if generator.generate_embeddings():
        print("="*60)
        print("✅ EMBEDDINGS GENERATI CON SUCCESSO!")
        print("="*60)
        print("\n💡 Ora puoi usare il chatbot con ricerca semantica:")
        print("   python test_rag_chatbot.py\n")
    else:
        print("❌ Errore durante la generazione")


if __name__ == "__main__":
    main()

