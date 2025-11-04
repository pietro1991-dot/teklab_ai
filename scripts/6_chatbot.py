#!/usr/bin/env python3
"""
Chatbot RAG con Llama Pre-addestrato (100% Locale)
===================================================

Usa Llama 2/3 pre-addestrato + RAG context injection
- Funziona COMPLETAMENTE in locale (no API online)
- Auto-detection: usa ultimo checkpoint fine-tunato se disponibile, altrimenti modello base
- Salva conversazioni per training continuo
"""

import sys
import os
import pickle
from pathlib import Path
from datetime import datetime
import uuid

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


class SpiritualityAIChatbot:
    """Chatbot RAG Llama completamente locale"""
    
    # Context window management
    MAX_HISTORY_TOKENS = 6000  # Lascia spazio per RAG context + risposta
    MAX_HISTORY_TURNS = 10     # Massimo 10 scambi recenti
    
    def __init__(self):
        print("\n" + "="*70)
        print("🦙 SPIRITUALITY AI - CHATBOT LLAMA RAG (100% Locale)")
        print("="*70)
        
        # Carica embeddings RAG
        self._load_embeddings()
        
        # Inizializza modello Llama
        self._init_model()
        
        # Session tracking
        self.session_id = str(uuid.uuid4())
        self.conversation_history = []
        
        print("="*70)
        print()
    
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
            self.summary_embeddings = cache.get('summary_embeddings', {})  # NUOVO
            self.chunks_data = cache.get('chunks_data', {})  # Dati originali dei chunk
            self.summaries_data = cache.get('summaries_data', {})  # NUOVO: Dati summaries
            
            # Carica modello embeddings
            from sentence_transformers import SentenceTransformer
            model_name = cache.get('model', 'all-MiniLM-L6-v2')
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
    
    def _init_model(self):
        """Inizializza Llama 3.2 3B ottimizzato per velocità su Windows"""
        print("\n🦙 Inizializzazione Llama 3.2 3B...")
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            # Path modello locale Llama 3.2 3B
            model_path = PROJECT_ROOT / "ai_system" / "models" / "Llama-3.2-3B-Instruct"
            
            if not model_path.exists():
                print(f"❌ Modello non trovato: {model_path}")
                print("   Esegui: python download_llama_3_2_3b.py")
                sys.exit(1)
            
            print(f"📂 Caricamento da: {model_path}")
            print("⚙️  OTTIMIZZATO: float16 + torch.compile + flash attention")
            
            # Carica tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(str(model_path))
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Carica modello con MASSIME ottimizzazioni PyTorch
            print("   Caricamento modello sulla GPU...")
            self.model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                device_map="cuda:0",
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                max_memory={0: "3.5GB"},
                use_cache=True,  # KV-cache
                attn_implementation="sdpa",  # Scaled Dot Product Attention veloce
            )
            
            # IMPORTANTE: Compila il modello per velocità (PyTorch 2.x)
            print("   🚀 Compilazione modello (migliora velocità 30-40%)...")
            try:
                self.model = torch.compile(self.model, mode="reduce-overhead")
                print("   ✅ Modello compilato!")
            except Exception as e:
                print(f"   ⚠️  Compilazione non disponibile: {e}")
            
            print("✅ Llama 3.2 3B caricato e ottimizzato!")

            
        except Exception as e:
            print(f"❌ Errore caricamento Llama: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def retrieve_context(self, query: str, top_k: int = 2, include_summaries: bool = True) -> tuple[str, list[dict]]:
        """Recupera contesto RAG rilevante
        
        Args:
            query: Query utente
            top_k: Numero chunk da recuperare
            include_summaries: Se True, include anche summary embeddings nella ricerca
        
        Returns:
            tuple: (context_text, retrieved_chunks_metadata)
                - context_text: testo formattato dei chunk
                - retrieved_chunks_metadata: lista di dict con {chunk_id, similarity_score, source, type}
        """
        if not self.embedding_model or not self.chunk_embeddings:
            return "", []
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Genera embedding query
            query_emb = self.embedding_model.encode([query])[0]
            
            # Calcola similarità con tutti i chunk
            similarities = []
            for chunk_id, chunk_emb in self.chunk_embeddings.items():
                sim = cosine_similarity([query_emb], [chunk_emb])[0][0]
                similarities.append((chunk_id, sim, 'chunk'))
            
            # NUOVO: Se richiesto, aggiungi anche summaries
            if include_summaries and self.summary_embeddings:
                for summary_id, summary_emb in self.summary_embeddings.items():
                    sim = cosine_similarity([query_emb], [summary_emb])[0][0]
                    similarities.append((summary_id, sim, 'summary'))
            
            # Top-K più simili (combinando chunk e summaries)
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_items = similarities[:top_k]
            
            if not top_items:
                return "", []
            
            # Costruisci context string CON IL CONTENUTO + metadata
            context_parts = []
            retrieved_metadata = []
            
            for item_id, score, item_type in top_items:
                if item_type == 'chunk':
                    # Recupera chunk
                    chunk_data = self.chunks_data.get(item_id, {})
                    chunk_text = chunk_data.get('original_text', chunk_data.get('testo', ''))
                    
                    if chunk_text:
                        metadata = chunk_data.get('metadata', {})
                        author = metadata.get('author', metadata.get('autore', 'Unknown'))
                        work = metadata.get('work', metadata.get('opera', metadata.get('libro', 'Unknown')))
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
                    # Recupera summary
                    summary_data = self.summaries_data.get(item_id, {})
                    
                    if summary_data:
                        unit_label = summary_data.get('unit_label', '')
                        work_name = summary_data.get('work_name', '')
                        
                        # Estrai overview dal summary
                        unit_meta = summary_data.get('unit_metadata', {})
                        overview = unit_meta.get('summary', '')
                        
                        # Aggrega concetti chiave
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
    
    def _get_conversation_context(self) -> list[dict]:
        """Restituisce cronologia conversazione con gestione context window
        
        Returns:
            Lista di messaggi (user/assistant) da includere nel prompt
            Tronca automaticamente se eccede MAX_HISTORY_TOKENS
        """
        if not self.conversation_history:
            return []
        
        # Strategia: prendi ultimi N turni
        recent_history = self.conversation_history[-self.MAX_HISTORY_TURNS:]
        
        # Converti in formato messages
        messages = []
        for turn in recent_history:
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["assistant"]})
        
        # TODO: Se serve ottimizzazione, calcola token effettivi e tronca
        # total_tokens = sum(len(self.tokenizer.encode(m["content"])) for m in messages)
        # if total_tokens > self.MAX_HISTORY_TOKENS: ...
        
        return messages
    
    def chat(self, user_message: str) -> str:
        """Genera risposta a messaggio utente"""
        
        import time
        
        # Timing: start totale
        start_total = time.time()
        
        # Retrieve RAG context
        start_retrieval = time.time()
        rag_context, retrieved_chunks = self.retrieve_context(user_message)
        retrieval_time = time.time() - start_retrieval
        
        # Costruisci messages per Llama 3.2 CON CRONOLOGIA
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Aggiungi conversazioni precedenti (ultimi 10 turni)
        history_messages = self._get_conversation_context()
        messages.extend(history_messages)
        
        # Aggiungi domanda corrente con RAG context
        if rag_context:
            context_message = f"""Informative context (DON'T cite authors in response):

{rag_context}

---"""
            current_question = f"{context_message}\n\nUser Question: {user_message}"
        else:
            current_question = user_message
        
        messages.append({"role": "user", "content": current_question})
        
        # Genera risposta con Llama 3.2
        try:
            import torch
            
            print("⏳ Generazione in corso...", flush=True)
            
            # Timing: start generation
            start_generation = time.time()
            
            # Apply chat template (Llama 3 format)
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
            input_tokens = inputs['input_ids'].shape[1]
            
            # Generate con PyTorch ottimizzato
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=350,  # AUMENTATO: 350 token per risposte complete (era 200)
                    temperature=0.7,
                    do_sample=True,
                    top_p=0.9,
                    top_k=50,  # Limita scelte per velocità
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1,
                )
            
            # Decode - RIMUOVI il prompt dall'output
            input_length = inputs['input_ids'].shape[1]
            generated_tokens = outputs[0][input_length:]  # Solo i nuovi token generati
            output_tokens = len(generated_tokens)
            assistant_message = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            
            # Timing: end generation
            generation_time = time.time() - start_generation
            total_time = time.time() - start_total
            
            # Pulizia finale - rimuovi eventuali tag rimasti
            if assistant_message.startswith("<|start_header_id|>assistant<|end_header_id|>"):
                assistant_message = assistant_message.replace("<|start_header_id|>assistant<|end_header_id|>", "").strip()
            if assistant_message.endswith("<|eot_id|>"):
                assistant_message = assistant_message.replace("<|eot_id|>", "").strip()
            
            # Salva in conversazione CON METRICHE RAG
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user": user_message,
                "assistant": assistant_message,
                "rag_context": rag_context,
                "retrieved_chunks": retrieved_chunks,  # IDs + similarity scores
                "timing_metrics": {
                    "retrieval_time": round(retrieval_time, 3),
                    "generation_time": round(generation_time, 3),
                    "total_time": round(total_time, 3)
                },
                "token_usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                }
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
        
        # Directory conversazioni
        conv_dir = PROJECT_ROOT / "ai_system" / "training_data" / "conversations"
        date_dir = conv_dir / datetime.now().strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Salva conversazione
        conv_file = date_dir / f"{self.session_id}.json"
        
        try:
            import json
            data = {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "total_turns": len(self.conversation_history),
                "turns": self.conversation_history
            }
            
            with open(conv_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Conversazione salvata: {len(self.conversation_history)} scambi → {conv_file.name}")
            print(f"   Per training futuro: python scripts/4_create_training_dataset.py")
            
        except Exception as e:
            print(f"⚠️  Errore salvataggio conversazione: {e}")
            
            with open(conv_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Conversazione salvata: {conv_file.name}")
            
        except Exception as e:
            print(f"⚠️  Errore salvataggio conversazione: {e}")
    
    def run(self):
        """Loop conversazione interattiva"""
        print("💬 Chatbot pronto! Comandi disponibili:")
        print("   • 'quit' / 'exit' - Esci e salva conversazione")
        print("   • 'reset' / 'nuovo' - Resetta cronologia (inizia nuova sessione)")
        print("   • 'clear' - Pulisci schermo")
        print("-" * 70)
        print()
        
        try:
            while True:
                # Input utente
                user_input = input("🧘 Tu: ").strip()
                
                if not user_input:
                    continue
                
                # Comandi speciali
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Arrivederci!")
                    break
                
                if user_input.lower() == 'clear':
                    print("\n" * 50)  # Clear screen
                    continue
                
                if user_input.lower() in ['reset', 'nuovo', 'new']:
                    # Salva conversazione corrente prima di resettare
                    if self.conversation_history:
                        self.save_conversation()
                    # Inizia nuova sessione
                    self.session_id = str(uuid.uuid4())
                    self.conversation_history = []
                    print("\n🔄 Cronologia resettata. Nuova sessione avviata.")
                    print("   (Conversazione precedente salvata)\n")
                    continue
                
                # Genera risposta
                print("\n🦙 Llama: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                
                # Log metriche RAG (ultima conversazione)
                if self.conversation_history:
                    last_turn = self.conversation_history[-1]
                    chunks = last_turn.get('retrieved_chunks', [])
                    timing = last_turn.get('timing_metrics', {})
                    tokens = last_turn.get('token_usage', {})
                    
                    print("\n📊 Metriche RAG:")
                    print(f"   • Cronologia: {len(self.conversation_history)} turni (ultimi {min(len(self.conversation_history), self.MAX_HISTORY_TURNS)} nel contesto)")
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
                            else:
                                print(f"         (sim: {sim:.3f})")
                    print(f"   • Timing: retrieval {timing.get('retrieval_time', 0):.2f}s + generation {timing.get('generation_time', 0):.2f}s = {timing.get('total_time', 0):.2f}s")
                    print(f"   • Token: {tokens.get('input_tokens', 0)} input + {tokens.get('output_tokens', 0)} output = {tokens.get('total_tokens', 0)} totali")
                
                print("\n" + "-" * 70 + "\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interruzione utente")
        
        finally:
            # Salva conversazione prima di uscire
            self.save_conversation()
            print()


def main():
    """Entry point"""
    print("\n" + "="*70)
    print("🦙 LLAMA RAG CHATBOT - Spirituality AI")
    print("="*70)
    print()
    print("Modalità: Llama Pre-addestrato + RAG (100% Locale)")
    print()
    print("⚠️  REQUISITI:")
    print("   • GPU con almeno 6GB VRAM (per 4-bit quantization)")
    print("   • Modello Llama scaricato → python scripts/1_download_llama.py")
    print("   • Embeddings generati → python scripts/2_generate_embeddings.py")
    print()
    print("💡 FUNZIONALITÀ:")
    print("   ✅ Funzionamento 100% locale (no internet)")
    print("   ✅ Auto-detection ultimo fine-tuning")
    print("   ✅ RAG context injection")
    print("   ✅ Salvataggio conversazioni per miglioramento continuo")
    print()
    print("📚 Dopo 20+ conversazioni, migliora il modello:")
    print("   python scripts/4_create_training_dataset.py")
    print("   python scripts/5_train_llama_rag.py --config llama-qlora --epochs 3")
    print()
    print("="*70 + "\n")
    
    # Avvia chatbot
    chatbot = SpiritualityAIChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
