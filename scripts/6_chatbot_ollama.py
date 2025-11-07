#!/usr/bin/env python3
"""
Chatbot RAG con Ollama (VELOCE - 100% Locale) - TEKLAB B2B
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
    from prompts_config import SYSTEM_PROMPT, build_rag_prompt, build_simple_prompt
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


class TeklabAIChatbotOllama:
    """Chatbot RAG Ollama completamente locale (VELOCE) - Teklab B2B"""
    
    # Context window management
    MAX_HISTORY_TOKENS = 6000
    MAX_HISTORY_TURNS = 10
    
    # Ollama settings
    OLLAMA_MODEL = "llama3.2:3b"
    OLLAMA_URL = "http://localhost:11434/api/generate"
    
    def __init__(self):
        print("\n" + "="*70)
        print("🔧 TEKLAB B2B AI - CHATBOT OLLAMA RAG (VELOCE)")
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
        """Carica embeddings cache per RAG - NUOVA STRUTTURA TEKLAB"""
        embeddings_path = PROJECT_ROOT / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"
        
        print("\n📚 Caricamento Knowledge Base RAG (TEKLAB chunks)...")
        
        if not embeddings_path.exists():
            print(f"⚠️  Cache embeddings non trovata: {embeddings_path}")
            print("   Esegui prima: python scripts/generate_teklab_embeddings.py")
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
            
            # Carica modello embeddings (FORZA CPU)
            from sentence_transformers import SentenceTransformer
            model_name = cache.get('model', 'all-MiniLM-L6-v2')
            print(f"   • Modello embeddings: {model_name}")
            print(f"   • Device: CPU (GPU riservata per Llama)")
            self.embedding_model = SentenceTransformer(model_name, device='cpu')
            
            total = len(self.chunk_embeddings) + len(self.qa_embeddings) + len(self.summary_embeddings)
            print(f"✅ Caricati {total} embeddings RAG")
            print(f"   • Chunks: {len(self.chunk_embeddings)}")
            print(f"   • Q&A: {len(self.qa_embeddings)}")
            print(f"   • Summaries: {len(self.summary_embeddings)}")
            
        except Exception as e:
            print(f"❌ Errore caricamento embeddings: {e}")
            self.embeddings = None
            self.embedding_model = None
    
    def retrieve_context(self, query: str, top_k: int = 5, include_summaries: bool = True, min_similarity: float = 0.33) -> tuple[str, list[dict]]:
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
            
            # DEBUG: Stampa top 5 similarities PRIMA del filtro
            print(f"\n🔍 DEBUG retrieve_context:")
            print(f"   Query: '{query[:50]}'")
            print(f"   min_similarity: {min_similarity}")
            print(f"   top_k: {top_k}")
            similarities_sorted = sorted(similarities, key=lambda x: x[1], reverse=True)
            print(f"   Top 5 similarities BEFORE filter:")
            for i, (cid, sim, _) in enumerate(similarities_sorted[:5], 1):
                ok = "✅" if sim >= min_similarity else "❌"
                print(f"      {ok} [{i}] sim={sim:.4f} - {cid[:50]}")
            
            if include_summaries and self.summary_embeddings:
                for summary_id, summary_emb in self.summary_embeddings.items():
                    sim = cosine_similarity([query_emb], [summary_emb])[0][0]
                    similarities.append((summary_id, sim, 'summary'))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Filtra per similarity threshold PRIMA, poi prendi top_k
            filtered = [(item_id, score, item_type) for item_id, score, item_type in similarities if score >= min_similarity]
            top_items = filtered[:top_k]
            
            if not top_items:
                print(f"⚠️  Nessun chunk rilevante (tutti <{min_similarity:.2f} similarity)")
                return "", []
            
            context_parts = []
            retrieved_metadata = []
            
            for item_id, score, item_type in top_items:
                if item_type == 'chunk':
                    chunk_data = self.chunks_data.get(item_id, {})
                    
                    # ARCHITETTURA TEKLAB OTTIMIZZATA: usa messages[2] (assistant formatted)
                    # messages[0] = system prompt template
                    # messages[1] = user prompt (SEMANTIC CONCEPT)
                    # messages[2] = assistant (FORMATTED RESPONSE) ← QUESTO è il contenuto da usare
                    chunk_text = ''
                    if 'messages' in chunk_data:
                        # Priorità: assistant message (formatted response)
                        if len(chunk_data['messages']) > 2:
                            chunk_text = chunk_data['messages'][2].get('content', '')
                        # Fallback: user content (raw prompt) se manca assistant
                        elif len(chunk_data['messages']) > 1:
                            chunk_text = chunk_data['messages'][1].get('content', '')
                    
                    # Fallback per vecchi chunk (libri meditazione)
                    if not chunk_text:
                        chunk_text = chunk_data.get('original_text', chunk_data.get('testo', ''))
                    
                    if chunk_text:
                        metadata = chunk_data.get('metadata', {})
                        
                        # ARCHITETTURA TEKLAB: metadata.product_model + category separato
                        product_model = metadata.get('product_model', 'Unknown')
                        category = chunk_data.get('category', 'unknown')
                        chunk_type = metadata.get('chunk_type', 'unknown')
                        
                        # Fallback per vecchi chunk libri meditazione (se presenti)
                        if product_model == 'Unknown':
                            author = metadata.get('author', metadata.get('autore', 'Unknown'))
                            file_title = metadata.get('file_title', '')
                            work = file_title if file_title else metadata.get('work', metadata.get('opera', metadata.get('libro', 'Unknown')))
                            product_model = f"{author} - {work}"
                        
                        source_info = chunk_data.get('source', item_id.split('/')[0] if '/' in item_id else 'Unknown')
                        context_parts.append(f"[Product: {product_model}]\n{chunk_text}\n")
                        
                        retrieved_metadata.append({
                            "chunk_id": item_id,
                            "similarity_score": round(float(score), 4),
                            "source": source_info,
                            "product": product_model,
                            "category": category,
                            "chunk_type": chunk_type,
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
        
        # Retrieve RAG context - ALLINEATO a backend_api/app.py
        start_retrieval = time.time()
        rag_context, retrieved_chunks = self.retrieve_context(user_message, top_k=3, min_similarity=0.28)  # ⚡ STESSO THRESHOLD di app.py
        retrieval_time = time.time() - start_retrieval
        
        # DEBUG: Stampa chunk recuperati
        print(f"🔍 RAG Search: '{user_message[:50]}'")
        print(f"   Chunks trovati: {len(retrieved_chunks)}")
        for i, chunk_meta in enumerate(retrieved_chunks[:3]):
            # Recupera chunk_id dal metadata
            chunk_id = chunk_meta.get('chunk_id', 'Unknown')
            # Recupera chunk_data completo per leggere metadata
            chunk_data = self.chunks_data.get(chunk_id, {})
            metadata = chunk_data.get('metadata', {})
            
            # Per chunk Teklab: metadata.product_model + category separato
            product = metadata.get('product_model', metadata.get('product', 'Unknown'))
            category = chunk_data.get('category', 'unknown')
            sim = chunk_meta.get('similarity_score', 0)
            print(f"   [{i+1}] {product:25s} | {category:12s} | sim={sim:.3f}")
        
        # Costruisci prompt con cronologia LIMITATA
        history_context = self._get_conversation_context()
        
        if rag_context:
            # ⚡ OTTIMIZZATO: Ridotto per velocità (3 chunk @ 800 chars = ~2400)
            # Con top_k=3 chunks, context più compatto e veloce
            max_context_length = 2500  # ⚡ Allineato a backend_api (era 4000)
            if len(rag_context) > max_context_length:
                rag_context = rag_context[:max_context_length] + "\n\n[... Additional technical details available on request ...]"
            
            # 🎯 USA TEMPLATE CENTRALIZZATO da prompts_config.py
            full_prompt = build_rag_prompt(rag_context, user_message)
            
            # Aggiungi cronologia conversazione se presente
            if history_context:
                full_prompt = full_prompt.replace("TEKLAB ASSISTANT RESPONSE:", f"{history_context}\n\nTEKLAB ASSISTANT RESPONSE:")
        else:
            # Nessun RAG context - prompt semplice
            full_prompt = build_simple_prompt(user_message)
            if history_context:
                full_prompt = f"{history_context}\n\n{full_prompt}"
        
        # Genera risposta con Ollama
        try:
            print("⏳ Generazione in corso (Ollama)...", flush=True)
            start_generation = time.time()
            
            # 🎯 GENERAZIONE COMPLETA in un solo colpo (no retry/continue)
            # num_predict ALTO per evitare troncamenti
            payload = {
                "model": self.OLLAMA_MODEL,
                "prompt": full_prompt,
                "system": SYSTEM_PROMPT,
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 800,  # Token sufficienti per risposta completa
                    "top_p": 0.85,
                    "num_ctx": 4096,
                    "repeat_penalty": 1.1,
                    "stop": ["\n\n\n", "CUSTOMER:", "QUESTION:", "---"]
                }
            }
            
            timeout = 240  # 4 minuti max
            response = requests.post(self.OLLAMA_URL, json=payload, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result.get('response', '').strip()
            done_reason = result.get('done_reason', 'stop')
            
            # Log se troncato
            if done_reason == 'length':
                print("\n⚠️  Risposta troncata a 800 token - considera di aumentare num_predict")
            
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
                "generation_mode": "single_shot",  # Generazione completa in un colpo
                "num_predict": 800,
                "done_reason": done_reason,
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
                            # ARCHITETTURA TEKLAB: usa product + category invece di author/work
                            product = chunk.get('product', 'Unknown')
                            category = chunk.get('category', 'unknown')
                            chunk_id = chunk.get('chunk_id', 'unknown')
                            sim = chunk['similarity_score']
                            item_type = chunk.get('type', 'chunk')
                            
                            # Display compatto: [num] Product | Category | sim
                            print(f"      {i}. {product} | {category} | sim={sim:.3f}")
                    
                    # Metriche generazione adattiva
                    adaptive = last_turn.get('adaptive_generation', {})
                    num_predict_used = adaptive.get('num_predict_used', 0)
                    level = adaptive.get('level_reached', 1)
                    retries = adaptive.get('retries', 0)
                    
                    adaptive_info = f"livello {level}/4 ({num_predict_used} token)"
                    if retries > 0:
                        adaptive_info += f" 🔄 +{retries} retry"
                    
                    print(f"   • Timing: retrieval {timing.get('retrieval_time', 0):.2f}s + generation {timing.get('generation_time', 0):.2f}s = {timing.get('total_time', 0):.2f}s")
                    print(f"   • Engine: Ollama (llama.cpp) - {adaptive_info}")
                
                print("\n" + "-" * 70 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interruzione utente")
        
        finally:
            self.save_conversation()
            print()


def main():
    """Entry point"""
    print("\n" + "="*70)
    print("🔧 OLLAMA RAG CHATBOT - Teklab B2B AI (VELOCE)")
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
    
    chatbot = TeklabAIChatbotOllama()
    chatbot.run()


if __name__ == "__main__":
    main()
