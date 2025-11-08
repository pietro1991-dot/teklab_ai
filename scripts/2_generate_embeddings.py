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
EMBEDDING_MODEL = 'BAAI/bge-base-en-v1.5' # Modello SOTA per retrieval, 768-dim
# Alternative:
# 'all-mpnet-base-v2'  # Buon tuttofare, ma meno specializzato
# 'all-MiniLM-L6-v2'  # Più veloce ma meno preciso (384-dim)

class EmbeddingsGenerator:
    """
    Generatore di Embeddings ottimizzato per RAG basato su domande.
    Crea vettori specifici per ogni domanda e coppia Q&A, mappandoli 
    al chunk di testo originale.
    """
    def __init__(self):
        self.model = None
        self.chunks_data = {}           # {chunk_id: chunk_data}
        self.embeddings = {}            # {embedding_id: vector}
        self.embedding_to_chunk_id = {} # {embedding_id: chunk_id}
    
    def _load_model(self):
        """Carica modello embeddings (lazy loading)"""
        if self.model is None:
            if not import_sentence_transformers():
                return False
            print("🧠 Inizializzazione modello embeddings...")
            print(f"   Modello: {EMBEDDING_MODEL}")
            print("   Device: CPU (GPU riservata per Llama)")
            self.model = SentenceTransformer(EMBEDDING_MODEL, device='cpu')
            print("✅ Modello caricato su CPU\n")
        return True
    
    def find_all_rag_folders(self):
        """Trova tutte le cartelle dei chunk in Processati/"""
        chunks_folders = []
        chunks_base = FONTI_BASE_PATH / "chunks"
        
        if not chunks_base.exists():
            print(f"❌ Cartella chunks non trovata: {chunks_base}")
            return []
        
        for category_dir in chunks_base.iterdir():
            if category_dir.is_dir():
                chunks_folders.append({
                    "path": category_dir,
                    "category": category_dir.name,
                    "source": "Teklab"
                })
        return chunks_folders
    
    def load_all_data(self):
        """Carica tutti i dati dei chunk dalla struttura di cartelle Teklab."""
        print("📚 Caricamento dati Teklab da Fonti...\n")
        
        chunks_folders = self.find_all_rag_folders()
        
        if not chunks_folders:
            print("❌ Nessuna cartella chunks trovata!")
            print(f"   Verifica che esista: {FONTI_BASE_PATH / 'chunks'}")
            return False
        
        print(f"✅ Trovate {len(chunks_folders)} categorie di chunk:\n")
        
        total_chunks = 0
        for folder_info in chunks_folders:
            category_path = folder_info["path"]
            category = folder_info["category"]
            
            print(f"   - Caricamento da: {category}/")
            
            chunk_files = sorted(category_path.glob("*.json"))
            category_chunk_count = 0
            
            for chunk_file in chunk_files:
                try:
                    with open(chunk_file, "r", encoding="utf-8") as f:
                        chunk_data = json.load(f)
                        chunk_id = chunk_data.get("id", chunk_file.stem)
                        
                        if chunk_id not in self.chunks_data:
                            self.chunks_data[chunk_id] = chunk_data
                            category_chunk_count += 1
                except Exception as e:
                    print(f"      ⚠️  Errore lettura {chunk_file.name}: {e}")
            
            print(f"      → {category_chunk_count} chunk caricati.")
            total_chunks += category_chunk_count
        
        print(f"\n{'='*60}")
        print("📊 DATI CARICATI:")
        print(f"   • Chunks totali: {total_chunks}")
        print(f"{'='*60}\n")
        
        return total_chunks > 0
    
    def generate_embeddings(self):
        """
        Genera embeddings specifici per le domande (Q&A e Natural Questions)
        associate a ogni chunk, per una ricerca semantica più precisa.
        """
        print("🔄 GENERAZIONE EMBEDDINGS BASATI SULLE DOMANDE...\n")
        
        if not self._load_model():
            return False
        
        texts_to_encode = []
        embedding_ids = []
        
        print("📝 Preparazione testi da vettorizzare (Q&A e Domande Naturali)...")
        
        for chunk_id, chunk_data in self.chunks_data.items():
            metadata = chunk_data.get("metadata", {})
            
            # 1. Processa le coppie Domanda/Risposta (qa_pairs)
            qa_pairs = metadata.get("qa_pairs", [])
            for i, qa in enumerate(qa_pairs):
                question = qa.get("question", "")
                answer = qa.get("answer", "")
                if question and answer:
                    # L'embedding combina domanda e risposta per un contesto ricco
                    text = f"Question: {question}\nAnswer: {answer}"
                    embedding_id = f"{chunk_id}|qa_{i}"
                    
                    texts_to_encode.append(text)
                    embedding_ids.append(embedding_id)
                    self.embedding_to_chunk_id[embedding_id] = chunk_id

            # 2. Processa le Domande Naturali (natural_questions)
            natural_questions = metadata.get("natural_questions", [])
            for i, nq in enumerate(natural_questions):
                if nq:
                    # L'embedding rappresenta solo la domanda
                    text = f"Question: {nq}"
                    embedding_id = f"{chunk_id}|nq_{i}"

                    texts_to_encode.append(text)
                    embedding_ids.append(embedding_id)
                    self.embedding_to_chunk_id[embedding_id] = chunk_id

        print(f"   ✅ Preparati {len(texts_to_encode)} testi totali da vettorizzare.\n")
        
        if not texts_to_encode:
            print("❌ Nessun testo (Q&A o Domande Naturali) trovato nei chunk!")
            return False
        
        # Genera embeddings con progress bar
        print(f"🧠 Codifica di {len(texts_to_encode)} testi in corso...")
        print("   (Può richiedere 1-5 minuti a seconda della CPU e del numero di testi)\n")
        
        generated_embeddings = self.model.encode(
            texts_to_encode, 
            show_progress_bar=True,
            batch_size=32
        )
        
        # Popola il dizionario di embeddings
        self.embeddings = {eid: emb for eid, emb in zip(embedding_ids, generated_embeddings)}
        
        print(f"\n✅ Generati {len(self.embeddings)} vettori di embedding.")
        
        # Salva la cache aggiornata
        print(f"\n💾 Salvataggio nuova cache in {EMBEDDINGS_CACHE_PATH.name}...")
        try:
            EMBEDDINGS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            with open(EMBEDDINGS_CACHE_PATH, 'wb') as f:
                pickle.dump({
                    'embeddings': self.embeddings,
                    'embedding_to_chunk_id': self.embedding_to_chunk_id,
                    'chunks_data': self.chunks_data,
                    'model': EMBEDDING_MODEL
                }, f)
            
            size_mb = EMBEDDINGS_CACHE_PATH.stat().st_size / (1024 * 1024)
            print(f"   ✅ Cache salvata con successo ({size_mb:.1f} MB)\n")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Errore durante il salvataggio della cache: {e}\n")
            return False
    
    def verify_cache(self):
        """Verifica che la cache sia valida e mostri le nuove informazioni."""
        if not EMBEDDINGS_CACHE_PATH.exists():
            print("❌ La cache non esiste.")
            return False
        
        try:
            with open(EMBEDDINGS_CACHE_PATH, 'rb') as f:
                cache = pickle.load(f)
            
            embeddings = cache.get('embeddings', {})
            emb_to_chunk = cache.get('embedding_to_chunk_id', {})
            chunks = cache.get('chunks_data', {})
            model_used = cache.get('model', 'unknown')
            
            print("\n✅ CACHE VALIDA (Nuova Struttura):")
            print(f"   • Modello Utilizzato: {model_used}")
            print(f"   • Numero di Vettori (Embeddings): {len(embeddings)}")
            print(f"   • Numero di Chunk Originali: {len(chunks)}")
            print(f"   • Mapping Vettore->Chunk: {len(emb_to_chunk)} voci")
            
            size_mb = EMBEDDINGS_CACHE_PATH.stat().st_size / (1024 * 1024)
            print(f"   • Dimensione Cache: {size_mb:.1f} MB\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Cache corrotta o in formato vecchio: {e}")
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

