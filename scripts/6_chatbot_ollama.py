#!/usr/bin/env python3
"""
Chatbot RAG con Ollama (VELOCE - 100% Locale)
==============================================

Usa Ollama + llama.cpp per inferenza VELOCE (30-90 secondi vs 6-8 minuti)
- Funziona COMPLETAMENTE in locale (no API online)
- Engine C++ ottimizzato (llama.cpp)
- Quantizzazione automatica 4-bit
- Salva conversazioni per training continuo
"""

import sys
import os
import pickle
from pathlib import Path
from datetime import datetime
import uuid
import json

# Fix encoding Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

try:
    from prompts_config import SYSTEM_PROMPT
except ImportError as e:
    print(f"❌ Errore import moduli: {e}")
    print("Assicurati che ai_system/src/ e Prompt/ esistano")
    sys.exit(1)

# Ollama client
try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  requests non disponibile - installa con: pip install requests")


class SpiritualityAIChatbotOllama:
    """Chatbot RAG Ollama completamente locale (VELOCE)"""
    
    # Context window management
    MAX_HISTORY_TOKENS = 6000
    MAX_HISTORY_TURNS = 10
    
    # Ollama settings
    OLLAMA_MODEL = "llama3.2:3b"
    OLLAMA_URL = "http://localhost:11434/api/generate"
    
    def __init__(self):
        print("\n" + "="*70)
        print("🦙 SPIRITUALITY AI - CHATBOT OLLAMA RAG (VELOCE)")
        print("="*70)
        
        # Verifica Ollama
        self._check_ollama()
        
        # Carica embeddings RAG
        self._load_embeddings()
        
        # Session tracking
        self.session_id = str(uuid.uuid4())
        self.conversation_history = []
        
        print("="*70)
        print()
    
    def _check_ollama(self):
        """Verifica che Ollama sia installato e in esecuzione"""
        print("\n🔍 Verifica Ollama...")
        
        if not OLLAMA_AVAILABLE:
            print("❌ requests non disponibile!")
            sys.exit(1)
        
        try:
            # Test connessione
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if self.OLLAMA_MODEL in model_names:
                    print(f"✅ Ollama attivo - Modello {self.OLLAMA_MODEL} disponibile")
                else:
                    print(f"❌ Modello {self.OLLAMA_MODEL} non trovato")
                    print(f"   Modelli disponibili: {', '.join(model_names) if model_names else 'nessuno'}")
                    print(f"\n   Scarica con: ollama pull {self.OLLAMA_MODEL}")
                    sys.exit(1)
            else:
                print("❌ Ollama non risponde correttamente")
                sys.exit(1)
                
        except requests.exceptions.ConnectionError:
            print("❌ Ollama non in esecuzione!")
            print("   Avvia Ollama e riprova")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Errore verifica Ollama: {e}")
            sys.exit(1)
    
    def _load_embeddings(self):
        """Carica embeddings cache per RAG"""
        embeddings_path = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl"
        
        print("\n📚 Caricamento Knowledge Base RAG...")
        
        if not embeddings_path.exists():
            print(f"⚠️  Cache embeddings non trovata: {embeddings_path}")
            print("   Esegui prima: python scripts/2_generate_embeddings.py")
            self.chunk_embeddings = {}
            self.qa_embeddings = {}
            self.summary_embeddings = {}
            self.chunks_data = {}
            self.summaries_data = {}
            self.embedding_model = None
            return
        
        try:
            with open(embeddings_path, 'rb') as f:
                cache = pickle.load(f)
            
            self.chunk_embeddings = cache.get('chunk_embeddings', {})
            self.qa_embeddings = cache.get('qa_embeddings', {})
            self.summary_embeddings = cache.get('summary_embeddings', {})
            self.chunks_data = cache.get('chunks_data', {})
            self.summaries_data = cache.get('summaries_data', {})
            
            # Carica modello embeddings
            from sentence_transformers import SentenceTransformer
            model_name = cache.get('model', 'all-MiniLM-L6-v2')
            print(f"   • Modello embeddings: {model_name}")
            self.embedding_model = SentenceTransformer(model_name)
            
            total = len(self.chunk_embeddings) + len(self.qa_embeddings) + len(self.summary_embeddings)
            print(f"✅ Caricati {total} embeddings RAG")
            print(f"   • Chunks: {len(self.chunk_embeddings)}")
            print(f"   • Q&A: {len(self.qa_embeddings)}")
            print(f"   • Summaries: {len(self.summary_embeddings)}")
            
        except Exception as e:
            print(f"❌ Errore caricamento embeddings: {e}")
            self.embeddings = None
            self.embedding_model = None
    
    def retrieve_context(self, query: str, top_k: int = 5, include_summaries: bool = True, min_similarity: float = 0.4) -> tuple[str, list[dict]]:
        """Recupera contesto RAG rilevante con filtro qualità"""
        if not self.embedding_model or not self.chunk_embeddings:
            return "", []
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            query_emb = self.embedding_model.encode([query])[0]
            
            similarities = []
            for chunk_id, chunk_emb in self.chunk_embeddings.items():
                sim = cosine_similarity([query_emb], [chunk_emb])[0][0]
                similarities.append((chunk_id, sim, 'chunk'))
            
            if include_summaries and self.summary_embeddings:
                for summary_id, summary_emb in self.summary_embeddings.items():
                    sim = cosine_similarity([query_emb], [summary_emb])[0][0]
                    similarities.append((summary_id, sim, 'summary'))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Filtra per similarity threshold
            top_items = [(item_id, score, item_type) for item_id, score, item_type in similarities[:top_k] if score >= min_similarity]
            
            if not top_items:
                print(f"⚠️  Nessun chunk rilevante (tutti <{min_similarity:.2f} similarity)")
                return "", []
            
            context_parts = []
            retrieved_metadata = []
            
            for item_id, score, item_type in top_items:
                if item_type == 'chunk':
                    chunk_data = self.chunks_data.get(item_id, {})
                    chunk_text = chunk_data.get('original_text', chunk_data.get('testo', ''))
                    
                    if chunk_text:
                        metadata = chunk_data.get('metadata', {})
                        author = metadata.get('author', metadata.get('autore', 'Unknown'))
                        # Usa file_title (es. "Day 11") invece di work generico
                        file_title = metadata.get('file_title', '')
                        work = file_title if file_title else metadata.get('work', metadata.get('opera', metadata.get('libro', 'Unknown')))
                        chunk_title = metadata.get('chunk_title', metadata.get('titolo_capitolo', ''))
                        
                        source_info = item_id.split('|')[0] if '|' in item_id else "Unknown"
                        context_parts.append(f"[Source: {source_info}]\n{chunk_text}\n")
                        
                        retrieved_metadata.append({
                            "chunk_id": item_id,
                            "similarity_score": round(float(score), 4),
                            "source": source_info,
                            "author": author,
                            "work": work,
                            "title": chunk_title,
                            "type": "chunk"
                        })
                
                elif item_type == 'summary':
                    summary_data = self.summaries_data.get(item_id, {})
                    
                    if summary_data:
                        unit_label = summary_data.get('unit_label', '')
                        work_name = summary_data.get('work_name', '')
                        unit_meta = summary_data.get('unit_metadata', {})
                        overview = unit_meta.get('summary', '')
                        aggregated = summary_data.get('aggregated_metadata', {})
                        key_concepts = ', '.join(aggregated.get('all_concepts', [])[:5])
                        
                        summary_text = f"{unit_label} Overview:\n{overview}\n\nKey Concepts: {key_concepts}"
                        context_parts.append(f"[Summary: {unit_label}]\n{summary_text}\n")
                        
                        retrieved_metadata.append({
                            "chunk_id": item_id,
                            "similarity_score": round(float(score), 4),
                            "source": unit_label,
                            "author": unit_meta.get('author', 'Unknown'),
                            "work": work_name,
                            "title": f"{unit_label} Summary",
                            "type": "summary"
                        })
            
            context_text = "\n---\n".join(context_parts) if context_parts else ""
            return context_text, retrieved_metadata
            
        except Exception as e:
            print(f"⚠️  Errore retrieve RAG: {e}")
            return "", []
    
    def _get_conversation_context(self) -> str:
        """Restituisce cronologia conversazione formattata per Ollama"""
        if not self.conversation_history:
            return ""
        
        recent_history = self.conversation_history[-self.MAX_HISTORY_TURNS:]
        
        context_parts = []
        for turn in recent_history:
            context_parts.append(f"User: {turn['user']}")
            context_parts.append(f"Assistant: {turn['assistant']}")
        
        return "\n".join(context_parts)
    
    def chat(self, user_message: str) -> str:
        """Genera risposta a messaggio utente usando Ollama"""
        
        import time
        
        start_total = time.time()
        
        # Retrieve RAG context
        start_retrieval = time.time()
        rag_context, retrieved_chunks = self.retrieve_context(user_message)
        retrieval_time = time.time() - start_retrieval
        
        # Costruisci prompt con cronologia
        history_context = self._get_conversation_context()
        
        if rag_context:
            context_message = f"""Informative context (DON'T cite authors in response):

{rag_context}

---"""
            full_prompt = f"{context_message}\n\n{history_context}\n\nUser: {user_message}\n\nAssistant:"
        else:
            full_prompt = f"{history_context}\n\nUser: {user_message}\n\nAssistant:"
        
        # Genera risposta con Ollama
        try:
            print("⏳ Generazione in corso (Ollama)...", flush=True)
            
            start_generation = time.time()
            
            payload = {
                "model": self.OLLAMA_MODEL,
                "prompt": full_prompt,
                "system": SYSTEM_PROMPT,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 50,
                    "num_predict": 512,  # max_new_tokens - aumentato per evitare troncamento
                    "repeat_penalty": 1.1
                }
            }
            
            response = requests.post(self.OLLAMA_URL, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result.get('response', '').strip()
            
            # Avvisa se risposta potrebbe essere troncata
            if result.get('done_reason') == 'length':
                assistant_message += "\n\n⚠️ [Risposta troncata - limite token raggiunto]"
            
            generation_time = time.time() - start_generation
            total_time = time.time() - start_total
            
            # Salva in conversazione
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_message,
                "assistant": assistant_message,
                "rag_context": rag_context,
                "retrieved_chunks": retrieved_chunks,
                "timing_metrics": {
                    "retrieval_time": round(retrieval_time, 3),
                    "generation_time": round(generation_time, 3),
                    "total_time": round(total_time, 3)
                },
                "engine": "ollama"
            })
            
            return assistant_message
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"❌ Errore generazione risposta: {e}"
    
    def save_conversation(self):
        """Salva conversazione per training futuro"""
        if not self.conversation_history:
            return
        
        conv_dir = PROJECT_ROOT / "ai_system" / "training_data" / "conversations"
        date_dir = conv_dir / datetime.now().strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        conv_file = date_dir / f"{self.session_id}_ollama.json"
        
        try:
            data = {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "total_turns": len(self.conversation_history),
                "engine": "ollama",
                "turns": self.conversation_history
            }
            
            with open(conv_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Conversazione salvata: {len(self.conversation_history)} scambi → {conv_file.name}")
            
        except Exception as e:
            print(f"⚠️  Errore salvataggio conversazione: {e}")
    
    def run(self):
        """Loop conversazione interattiva"""
        print("💬 Chatbot Ollama pronto! Comandi disponibili:")
        print("   • 'quit' / 'exit' - Esci e salva conversazione")
        print("   • 'reset' / 'nuovo' - Resetta cronologia")
        print("   • 'clear' - Pulisci schermo")
        print("-" * 70)
        print()
        
        try:
            while True:
                user_input = input("🧘 Tu: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Arrivederci!")
                    break
                
                if user_input.lower() == 'clear':
                    print("\n" * 50)
                    continue
                
                if user_input.lower() in ['reset', 'nuovo', 'new']:
                    if self.conversation_history:
                        self.save_conversation()
                    self.session_id = str(uuid.uuid4())
                    self.conversation_history = []
                    print("\n🔄 Cronologia resettata. Nuova sessione avviata.\n")
                    continue
                
                print("\n🦙 Ollama: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                
                # Log metriche RAG
                if self.conversation_history:
                    last_turn = self.conversation_history[-1]
                    chunks = last_turn.get('retrieved_chunks', [])
                    timing = last_turn.get('timing_metrics', {})
                    
                    print("\n📊 Metriche RAG:")
                    print(f"   • Cronologia: {len(self.conversation_history)} turni")
                    print(f"   • Chunk recuperati: {len(chunks)}")
                    if chunks:
                        for i, chunk in enumerate(chunks, 1):
                            author = chunk.get('author', 'Unknown')
                            work = chunk.get('work', 'Unknown')
                            title = chunk.get('title', '')
                            sim = chunk['similarity_score']
                            item_type = chunk.get('type', 'chunk')
                            
                            print(f"      {i}. 📚 {author} - {work}")
                            if title:
                                type_indicator = " [SUMMARY]" if item_type == "summary" else ""
                                print(f"         📄 {title}{type_indicator} (sim: {sim:.3f})")
                    print(f"   • Timing: retrieval {timing.get('retrieval_time', 0):.2f}s + generation {timing.get('generation_time', 0):.2f}s = {timing.get('total_time', 0):.2f}s")
                    print(f"   • Engine: Ollama (llama.cpp)")
                
                print("\n" + "-" * 70 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interruzione utente")
        
        finally:
            self.save_conversation()
            print()


def main():
    """Entry point"""
    print("\n" + "="*70)
    print("🦙 OLLAMA RAG CHATBOT - Spirituality AI (VELOCE)")
    print("="*70)
    print()
    print("Modalità: Ollama + llama.cpp (30-90 secondi per risposta)")
    print()
    print("⚡ VANTAGGI OLLAMA:")
    print("   ✅ 10x più veloce di PyTorch (30-90s vs 6-8 min)")
    print("   ✅ Engine C++ ottimizzato (llama.cpp)")
    print("   ✅ Quantizzazione automatica 4-bit")
    print("   ✅ 100% locale (no internet)")
    print()
    print("📋 REQUISITI:")
    print("   • Ollama installato e in esecuzione")
    print("   • Modello llama3.2:3b scaricato")
    print("   • Embeddings generati → python scripts/2_generate_embeddings.py")
    print()
    print("="*70 + "\n")
    
    chatbot = SpiritualityAIChatbotOllama()
    chatbot.run()


if __name__ == "__main__":
    main()
