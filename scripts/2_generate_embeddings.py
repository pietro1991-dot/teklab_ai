"""
Generatore di Embeddings per RAG Chatbot - Spirituality AI
Genera embeddings di tutti i chunks e Q&A e li salva in cache
Esegui SOLO quando aggiungi nuovi libri/capitoli sugli autori
"""

import json
import os
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
PROJECT_ROOT = SCRIPT_DIR.parent  # Root del progetto (spirituality.ai/)
FONTI_BASE_PATH = PROJECT_ROOT / "Fonti"
EMBEDDINGS_CACHE_PATH = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl"  # Cache in ai_system/Embedding/

# Modello embeddings (puoi cambiarlo)
EMBEDDING_MODEL = 'all-mpnet-base-v2'  # Più preciso per contenuto spirituale (768-dim)
# Alternative:
# 'all-MiniLM-L6-v2'  # Più veloce ma meno preciso (384-dim)
# 'paraphrase-multilingual-MiniLM-L12-v2'  # Migliore per italiano

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
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            print("✅ Modello caricato\n")
        return True
    
    def find_all_rag_folders(self):
        """Trova tutte le cartelle 'libri_processati' in Fonti/"""
        rag_folders = []
        
        if not FONTI_BASE_PATH.exists():
            print(f"❌ Cartella Fonti non trovata: {FONTI_BASE_PATH}")
            return rag_folders
        
        # Cerchiamo sia cartelle chiamate 'libri_processati' sia 'Processati' (varianti)
        for root, dirs, files in os.walk(FONTI_BASE_PATH):
            # controlla directory di processo tipiche
            candidates = [d for d in dirs if d.lower() in ("libri_processati", "processati")]
            for cand in candidates:
                processati_path = Path(root) / cand
                if not processati_path.exists():
                    continue

                for libro_dir in processati_path.iterdir():
                    if libro_dir.is_dir() and (libro_dir / "chunks").exists():
                        # estrai autore dalla struttura: Fonti/Autori/<Autore>/Processati/<Opera>
                        # relative parts rispetto a FONTI_BASE_PATH
                        parts = libro_dir.relative_to(FONTI_BASE_PATH).parts
                        autore = "Sconosciuto"
                        # se esiste 'Autori' prendi l'elemento successivo, altrimenti fallback al secondo elemento
                        if 'Autori' in parts:
                            try:
                                idx = parts.index('Autori')
                                autore = parts[idx + 1] if len(parts) > idx + 1 else 'Sconosciuto'
                            except Exception:
                                autore = parts[1] if len(parts) > 1 else 'Sconosciuto'
                        else:
                            autore = parts[1] if len(parts) > 1 else 'Sconosciuto'

                        libro = libro_dir.name

                        rag_folders.append({
                            "path": libro_dir,
                            "autore": autore,
                            "libro": libro
                        })
        
        return rag_folders
    
    def load_all_data(self):
        """Carica tutti i chunks e Q&A"""
        print("📚 Caricamento dati da Fonti...\n")
        
        rag_folders = self.find_all_rag_folders()
        
        if not rag_folders:
            print("❌ Nessuna fonte trovata!")
            return False
        
        print(f"✅ Trovate {len(rag_folders)} fonti:\n")
        
        for fonte in rag_folders:
            rag_path = fonte["path"]
            autore = fonte["autore"]
            libro = fonte["libro"]
            source_key = f"{autore}/{libro}"
            
            print(f"   📖 {source_key}")
            
            # Carica chunks
            chunks_dir = rag_path / "chunks"
            chunk_count = 0
            if chunks_dir.exists():
                for cap_dir in chunks_dir.iterdir():
                    if cap_dir.is_dir():
                        cap_name = f"{source_key}/{cap_dir.name}"
                        self.chunks[cap_name] = []
                        # Cerca file che contengono "_chunk_" nel nome
                        for chunk_file in sorted(cap_dir.glob("*_chunk_*.json")):
                            try:
                                with open(chunk_file, "r", encoding="utf-8") as f:
                                    chunk_data = json.load(f)
                                    # preserva chunk_id se presente, altrimenti usa stem
                                    chunk_data["chunk_id"] = chunk_data.get("chunk_id", chunk_file.stem)
                                    chunk_data["capitolo"] = cap_name
                                    self.chunks[cap_name].append(chunk_data)
                                    chunk_count += 1
                            except Exception as e:
                                print(f"      ⚠️  Errore {chunk_file.name}: {e}")
            
            # Carica Q&A dai chunk (nuovo formato: metadata.qa_pairs)
            # NON usa più i file separati qa_pairs/*.json (vecchio formato)
            qa_count = 0
            for cap_name, chunks_list in self.chunks.items():
                for chunk in chunks_list:
                    # Estrai qa_pairs dal metadata del chunk
                    metadata = chunk.get('metadata', {})
                    qa_pairs = metadata.get('qa_pairs', [])
                    
                    if qa_pairs:
                        # Salva Q&A con chiave unica per chunk
                        chunk_id = chunk.get('chunk_id', chunk.get('id', 'unknown'))
                        qa_key = f"{cap_name}|{chunk_id}"
                        self.qa_pairs[qa_key] = {"qa_pairs": qa_pairs}
                        qa_count += len(qa_pairs)
            
            # NUOVO: Carica summary files
            summaries_dir = rag_path / "summaries"
            summary_count = 0
            if summaries_dir.exists():
                for summary_file in sorted(summaries_dir.glob("*_summary.json")):
                    try:
                        with open(summary_file, "r", encoding="utf-8") as f:
                            summary_data = json.load(f)
                            summary_id = f"{source_key}/{summary_file.stem}"
                            self.summaries[summary_id] = summary_data
                            summary_count += 1
                    except Exception as e:
                        print(f"      ⚠️  Errore {summary_file.name}: {e}")
            
            print(f"      → {chunk_count} chunks, {qa_count} Q&A, {summary_count} summaries")
        
        total_chunks = sum(len(chunks) for chunks in self.chunks.values())
        total_qa = sum(len(qa.get("qa_pairs", [])) for qa in self.qa_pairs.values())
        total_summaries = len(self.summaries)
        
        print(f"\n{'='*60}")
        print("📊 DATI CARICATI:")
        print(f"   • Capitoli: {len(self.chunks)}")
        print(f"   • Chunks: {total_chunks}")
        print(f"   • Q&A: {total_qa}")
        print(f"   • Summaries: {total_summaries}")
        print(f"   • Totale testi da codificare: {total_chunks + total_qa + total_summaries}")
        print(f"{'='*60}\n")
        
        return True
    
    def generate_embeddings(self):
        """Genera embeddings per tutti i testi"""
        print("🔄 GENERAZIONE EMBEDDINGS IN CORSO...\n")
        
        # Carica modello ora (lazy loading)
        if not self._load_model():
            return False
        
        texts_to_encode = []
        text_ids = []
        
        # Prepara testi chunks
        print("📝 Preparazione chunks...")
        for cap_name, chunks in self.chunks.items():
            for chunk in chunks:
                chunk_id = f"{cap_name}|{chunk.get('chunk_id', '')}"
                
                # Estrai metadata
                metadata = chunk.get('metadata', {})
                author = metadata.get('author', chunk.get('autore', ''))
                work = metadata.get('work', chunk.get('opera', chunk.get('libro', '')))
                section = chunk.get('sezione', '')
                chunk_title = metadata.get('chunk_title', chunk.get('titolo_capitolo', chunk.get('titolo_giorno', '')))
                
                # Supporta sia 'original_text' (nuovo formato) che 'testo' (vecchio formato)
                body = chunk.get('original_text', chunk.get('testo', ''))
                
                # ARRICCHISCI CON METADATA per migliorare ricerca semantica
                keywords = metadata.get('keywords_primary', [])
                # Gestisci keywords sia come lista di stringhe che lista di dict
                if keywords and isinstance(keywords[0], dict):
                    keywords_text = ', '.join([kw.get('term', '') for kw in keywords[:5]])
                elif keywords:
                    keywords_text = ', '.join(keywords[:5])
                else:
                    keywords_text = ''
                
                quotes = metadata.get('iconic_quotes', [])
                quotes_text = ' | '.join(quotes[:3]) if quotes else ''
                
                concepts = metadata.get('key_concepts', [])
                concepts_text = ', '.join(concepts[:5]) if concepts else ''
                
                # Costruisci testo arricchito per embedding
                enriched_parts = [
                    f"Autore: {author}",
                    f"Opera: {work}",
                    f"Sezione: {section}",
                    f"Titolo: {chunk_title}"
                ]
                
                if keywords_text:
                    enriched_parts.append(f"Keywords: {keywords_text}")
                if concepts_text:
                    enriched_parts.append(f"Concetti: {concepts_text}")
                if quotes_text:
                    enriched_parts.append(f"Citazioni: {quotes_text}")
                
                enriched_parts.append(f"\nContenuto:\n{body}")
                
                text = '\n'.join(enriched_parts)
                
                if text:
                    texts_to_encode.append(text)
                    text_ids.append(('chunk', chunk_id))
        
        print(f"   ✅ {len([x for x in text_ids if x[0] == 'chunk'])} chunks preparati")
        
        # Prepara testi Q&A
        print("📝 Preparazione Q&A...")
        for qa_key, qa_data in self.qa_pairs.items():
            qa_list = qa_data.get('qa_pairs', [])
            
            for idx, qa in enumerate(qa_list):
                qa_id = f"{qa_key}|qa_{idx}"
                # Nuovo formato: 'question' e 'answer'
                # Vecchio formato: 'domanda' e 'risposta' (fallback)
                question = qa.get('question', qa.get('domanda', ''))
                answer = qa.get('answer', qa.get('risposta', ''))
                # Combina domanda + risposta per embedding più ricco
                text = f"{question} {answer}"
                if text.strip():
                    texts_to_encode.append(text)
                    text_ids.append(('qa', qa_id))
        
        # NUOVO: Aggiungi natural_questions come embeddings separati
        print("📝 Preparazione Natural Questions...")
        natural_q_count = 0
        for cap_name, chunks in self.chunks.items():
            for chunk in chunks:
                chunk_id = f"{cap_name}|{chunk.get('chunk_id', '')}"
                metadata = chunk.get('metadata', {})
                natural_qs = metadata.get('natural_questions', [])
                
                for idx, nq in enumerate(natural_qs):
                    if nq.strip():
                        nq_id = f"{chunk_id}|nq_{idx}"
                        # Per natural questions, includi anche il titolo del chunk per contesto
                        chunk_title = metadata.get('chunk_title', '')
                        text = f"Question: {nq} (Related to: {chunk_title})"
                        texts_to_encode.append(text)
                        text_ids.append(('natural_q', nq_id))
                        natural_q_count += 1
        
        print(f"   ✅ {len([x for x in text_ids if x[0] == 'qa'])} Q&A preparati")
        print(f"   ✅ {natural_q_count} Natural Questions preparate")
        
        # NUOVO: Prepara testi Summary
        print("📝 Preparazione Summaries...")
        for summary_id, summary_data in self.summaries.items():
            # Estrai metadata aggregati
            unit_label = summary_data.get('unit_label', '')
            unit_type = summary_data.get('unit_type', 'unit')
            work_name = summary_data.get('work_name', '')
            
            aggregated = summary_data.get('aggregated_metadata', {})
            all_keywords = ', '.join(aggregated.get('all_keywords', [])[:10])
            all_concepts = ', '.join(aggregated.get('all_concepts', [])[:10])
            all_quotes = ' | '.join(aggregated.get('iconic_quotes', [])[:5])
            all_questions = '; '.join(aggregated.get('natural_questions', [])[:5])
            
            # Costruisci testo ricco per summary
            summary_parts = [
                f"Summary: {unit_label}",
                f"Work: {work_name}",
                f"Total Chunks: {summary_data.get('total_chunks', 0)}"
            ]
            
            if all_keywords:
                summary_parts.append(f"Keywords: {all_keywords}")
            if all_concepts:
                summary_parts.append(f"Concepts: {all_concepts}")
            if all_quotes:
                summary_parts.append(f"Key Quotes: {all_quotes}")
            if all_questions:
                summary_parts.append(f"Questions: {all_questions}")
            
            # Aggiungi summary del summary se esiste
            unit_meta = summary_data.get('unit_metadata', {})
            unit_summary = unit_meta.get('summary', '')
            if unit_summary:
                summary_parts.append(f"\nOverview: {unit_summary}")
            
            text = '\n'.join(summary_parts)
            
            if text:
                texts_to_encode.append(text)
                text_ids.append(('summary', summary_id))
        
        print(f"   ✅ {len([x for x in text_ids if x[0] == 'summary'])} Summaries preparati")
        
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
        
        # Prepara dati chunks per salvataggio (con contenuto originale)
        chunks_data = {}
        for cap_name, chunks in self.chunks.items():
            for chunk in chunks:
                chunk_id = f"{cap_name}|{chunk.get('chunk_id', '')}"
                
                # IMPORTANTE: Assicura che ci sia 'original_text' per il chatbot
                if 'original_text' not in chunk:
                    # Estrai da messages[1] (user prompt) se non c'è
                    messages = chunk.get('messages', [])
                    if len(messages) > 1 and messages[1].get('role') == 'user':
                        # Il testo originale è nel prompt user dopo "Complete text:"
                        user_content = messages[1].get('content', '')
                        if 'Complete text:' in user_content:
                            original_text = user_content.split('Complete text:')[-1].strip()
                            chunk['original_text'] = original_text
                        else:
                            chunk['original_text'] = user_content
                
                chunks_data[chunk_id] = chunk  # Salva chunk con original_text aggiunto
        
        for (text_type, text_id), embedding in zip(text_ids, embeddings):
            if text_type == 'chunk':
                self.chunk_embeddings[text_id] = embedding
            elif text_type == 'qa':
                self.qa_embeddings[text_id] = embedding
            elif text_type == 'natural_q':
                # Natural questions condividono lo spazio con Q&A
                self.qa_embeddings[text_id] = embedding
            elif text_type == 'summary':
                # Summary embeddings in spazio dedicato
                self.summary_embeddings[text_id] = embedding
        
        print(f"   ✅ Chunks: {len(self.chunk_embeddings)}")
        print(f"   ✅ Q&A + Natural Questions: {len(self.qa_embeddings)}")
        print(f"   ✅ Summaries: {len(self.summary_embeddings)}")
        
        # Salva cache
        print(f"\n💾 Salvataggio cache in {EMBEDDINGS_CACHE_PATH.name}...")
        try:
            # Crea directory se non esiste
            EMBEDDINGS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            with open(EMBEDDINGS_CACHE_PATH, 'wb') as f:
                pickle.dump({
                    'chunk_embeddings': self.chunk_embeddings,
                    'qa_embeddings': self.qa_embeddings,
                    'summary_embeddings': self.summary_embeddings,  # NUOVO
                    'chunks_data': chunks_data,  # Dati originali chunks
                    'summaries_data': self.summaries,  # NUOVO: Dati summaries
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
            summary_emb = cache.get('summary_embeddings', {})
            model_used = cache.get('model', 'unknown')
            
            print("\n✅ CACHE VALIDA:")
            print(f"   • Modello: {model_used}")
            print(f"   • Chunks: {len(chunk_emb)}")
            print(f"   • Q&A: {len(qa_emb)}")
            print(f"   • Summaries: {len(summary_emb)}")
            
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

