"""
Llama RAG Wrapper - Interfaccia compatibile Groq API per Llama
Mantiene stessa interfaccia: client.chat.completions.create()
"""

import torch
import time
import uuid
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass

from .llama_rag_model import LlamaRAGModel, create_llama_rag_model, TRANSFORMERS_AVAILABLE
# Import SentenceTransformer solo quando necessario per evitare problemi di compatibilità
# from sentence_transformers import SentenceTransformer


@dataclass
class Message:
    """Messaggio chat compatibile Groq"""
    role: str
    content: str


@dataclass
class Choice:
    """Choice compatibile Groq response"""
    index: int
    message: Message
    finish_reason: str


@dataclass
class Usage:
    """Token usage stats"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatCompletion:
    """Response compatibile Groq API"""
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class LlamaRAGWrapper:
    """
    Wrapper che replica interfaccia Groq API per Llama RAG Model.
    
    Usage:
        # Auto-detect ultimo checkpoint fine-tunato
        client = LlamaRAGWrapper()
        
        # Oppure specifica checkpoint
        client = LlamaRAGWrapper(checkpoint_path="checkpoints/llama_rag/best_model")
        
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are..."},
                {"role": "user", "content": "Question"}
            ],
            model="llama-rag",
            temperature=0.7,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
    """
    
    @staticmethod
    def find_latest_checkpoint(checkpoints_dir: Optional[Path] = None) -> Optional[Path]:
        """Trova automaticamente l'ultimo checkpoint fine-tunato."""
        if checkpoints_dir is None:
            # Default path
            checkpoints_dir = Path(__file__).parent.parent.parent.parent / "checkpoints"
        
        if not checkpoints_dir.exists():
            return None
        
        # Cerca cartelle llama_rag_*
        llama_checkpoints = sorted(
            [d for d in checkpoints_dir.glob("llama_rag_*") if d.is_dir()],
            key=lambda x: x.name,
            reverse=True
        )
        
        for checkpoint_dir in llama_checkpoints:
            # Priorità: best_model > final_model
            best_model = checkpoint_dir / "best_model"
            if best_model.exists():
                return best_model
            final_model = checkpoint_dir / "final_model"
            if final_model.exists():
                return final_model
        
        return None
    
    def __init__(
        self,
        checkpoint_path: Optional[str] = None,
        config: str = 'llama-qlora',
        llama_model_name: Optional[str] = None,
        device: Optional[str] = None,
        embedding_model: str = 'all-MiniLM-L6-v2',
        use_lora: bool = True,
        use_quantization: bool = True,
        quantization_bits: int = 4,
        auto_find_checkpoint: bool = True,
    ):
        """
        Args:
            checkpoint_path: Path checkpoint fine-tunato. Se None e auto_find_checkpoint=True, cerca automaticamente
            config: 'llama-2-7b', 'llama-3-8b', 'llama-qlora' (default)
            llama_model_name: Override model name (es. "meta-llama/Llama-2-7b-chat-hf")
            device: 'cuda', 'cpu', o None (auto-detect)
            embedding_model: Modello sentence-transformers per embeddings
            use_lora: Se usare LoRA per fine-tuning
            use_quantization: Se usare quantization 4-bit/8-bit
            quantization_bits: 4 o 8
            auto_find_checkpoint: Se True, cerca automaticamente ultimo checkpoint se checkpoint_path=None
        """
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers non installato! Installa con:\n"
                "pip install transformers accelerate bitsandbytes peft"
            )
        
        # Device
        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        
        print(f"🔧 LlamaRAGWrapper init su {self.device}")
        
        # Auto-detect checkpoint se non specificato
        if checkpoint_path is None and auto_find_checkpoint:
            print(f"🔍 Ricerca automatica ultimo checkpoint fine-tunato...")
            checkpoint_path = self.find_latest_checkpoint()
            if checkpoint_path:
                print(f"✅ Trovato: {checkpoint_path}")
                checkpoint_path = str(checkpoint_path)
            else:
                print(f"⚠️  Nessun checkpoint trovato")
        
        # Modello embeddings (per RAG chunks)
        print(f"📦 Caricamento embedding model: {embedding_model}")
        # Import lazy per evitare problemi di compatibilità
        from sentence_transformers import SentenceTransformer
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_model.to(self.device)
        
        # Carica o crea Llama RAG Model
        if checkpoint_path and Path(checkpoint_path).exists():
            print(f"📦 Caricamento checkpoint fine-tunato: {checkpoint_path}")
            self.model = LlamaRAGModel.from_pretrained(
                load_path=checkpoint_path,
                llama_model_name=llama_model_name,
            )
            self.checkpoint_name = Path(checkpoint_path).parent.name
            print(f"✅ Checkpoint caricato: {self.checkpoint_name}")
        else:
            if checkpoint_path:
                print(f"⚠️  Checkpoint non trovato: {checkpoint_path}")
            print(f"🦙 Caricamento Llama vanilla (NON fine-tunato su RAG)")
            print(f"   Per fine-tuning: python ai_system/src/training/train_llama_rag.py\n")
            
            # Crea modello vanilla - prepara kwargs
            model_kwargs = {
                'config_name': config,
                'use_lora': use_lora,
                'use_quantization': use_quantization,
                'quantization_bits': quantization_bits,
            }
            
            # Aggiungi llama_model_name solo se specificato (non None)
            if llama_model_name is not None:
                model_kwargs['llama_model_name'] = llama_model_name
            
            self.model = create_llama_rag_model(**model_kwargs)
            self.checkpoint_name = "vanilla"
        
        self.model.eval()
        
        # Stats
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        print(f"\n✅ Llama RAG Model pronto!")
        print(f"   Parametri totali: {total_params:,}")
        print(f"   Parametri trainabili: {trainable_params:,} ({100*trainable_params/total_params:.2f}%)")
        print(f"   Modello: {self.model.llama_model_name}\n")
        
        # Compatibilità API Groq
        self.chat = self  # Per sintassi client.chat.completions.create()
        self.completions = self
        
        # Cache per chunks (evita ricomputare embeddings)
        self._chunks_cache = {}
    
    def _extract_context_from_messages(
        self,
        messages: List[Dict[str, str]]
    ) -> tuple[str, str, Optional[List[str]]]:
        """
        Estrae query, system prompt e context chunks dai messaggi.
        
        Args:
            messages: Lista messaggi formato Groq API
        
        Returns:
            (query, system_prompt, context_chunks)
        """
        system_prompt = None
        query = None
        context_chunks = []
        
        for msg in messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            
            if role == 'system':
                system_prompt = content
            elif role == 'user':
                # Prova a estrarre context dal messaggio user
                # Formato: "Context: ...\n\nQuestion: ..."
                if "Context:" in content or "Contesto:" in content:
                    parts = content.split("Question:" if "Question:" in content else "Domanda:")
                    if len(parts) == 2:
                        context_text = parts[0].replace("Context:", "").replace("Contesto:", "").strip()
                        query = parts[1].strip()
                        
                        # Split context in chunks
                        context_chunks = [
                            chunk.strip()
                            for chunk in context_text.split("---")
                            if chunk.strip()
                        ]
                else:
                    query = content
        
        return query or "", system_prompt, context_chunks if context_chunks else None
    
    def _estimate_tokens(self, text: str) -> int:
        """Stima token count (approssimato)"""
        # Llama tokenizer: ~1 token per 4 caratteri
        return len(text) // 4
    
    def create(
        self,
        messages: List[Dict[str, str]],
        model: str = "llama-rag",
        temperature: float = 0.7,
        max_tokens: int = 500,
        top_p: float = 0.9,
        top_k: int = 50,
        **kwargs
    ) -> ChatCompletion:
        """
        Genera risposta in stile Groq API.
        
        Args:
            messages: Lista messaggi [{"role": "...", "content": "..."}]
            model: Nome modello (ignorato, usa sempre Llama)
            temperature: Sampling temperature
            max_tokens: Max token da generare
            top_p: Nucleus sampling
            top_k: Top-k sampling
        
        Returns:
            ChatCompletion object compatibile Groq
        """
        start_time = time.time()
        
        # Estrai query, system prompt e context
        query, system_prompt, context_chunks = self._extract_context_from_messages(messages)
        
        if not query:
            raise ValueError("Nessuna query trovata nei messaggi!")
        
        # Se non ci sono context chunks, usa lista vuota
        if context_chunks is None:
            context_chunks = []
        
        # Genera risposta con Llama
        with torch.no_grad():
            risposta = self.model.generate(
                query=query,
                context_chunks=context_chunks,
                system_prompt=system_prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
            )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        # Calcola token usage (approssimato)
        prompt_text = " ".join([msg['content'] for msg in messages])
        prompt_tokens = self._estimate_tokens(prompt_text)
        completion_tokens = self._estimate_tokens(risposta)
        total_tokens = prompt_tokens + completion_tokens
        
        # Costruisci response compatibile Groq
        completion = ChatCompletion(
            id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
            object="chat.completion",
            created=int(time.time()),
            model=f"llama-rag ({self.model.llama_model_name})",
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=risposta),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
        )
        
        # Log stats (solo tempo, non token per non confondere l'output)
        print(f"\r✅ Completato in {latency_ms/1000:.1f}s | Tokens: {total_tokens}", flush=True)
        
        return completion
    
    def generate_with_chunks(
        self,
        query: str,
        chunks: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """
        Genera risposta dato query e chunks RAG (formato raw).
        
        Args:
            query: Domanda utente
            chunks: Lista chunks RAG (dict con 'testo', 'metadata', etc.)
            system_prompt: System prompt opzionale
            max_tokens: Max token output
            temperature: Sampling temperature
        
        Returns:
            risposta: Risposta generata
        """
        # Estrai testo da chunks
        context_chunks = []
        for chunk in chunks:
            if isinstance(chunk, dict):
                # Supporta formato vecchio (testo) e nuovo (messages)
                testo = chunk.get("testo", "")
                if not testo and "messages" in chunk:
                    # Nuovo formato
                    messages = chunk.get("messages", [])
                    testo = " ".join([msg.get("content", "") for msg in messages if msg.get("role") == "system"])
                
                if testo:
                    # Aggiungi metadata se disponibile
                    metadata = chunk.get("metadata", {})
                    autore = metadata.get("autore", "Unknown")
                    libro = metadata.get("libro", "Unknown")
                    header = f"[{autore} - {libro}]"
                    context_chunks.append(f"{header}\n{testo}")
            elif isinstance(chunk, str):
                context_chunks.append(chunk)
        
        # Genera risposta
        with torch.no_grad():
            risposta = self.model.generate(
                query=query,
                context_chunks=context_chunks,
                system_prompt=system_prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
            )
        
        return risposta


def test_llama_rag_wrapper():
    """Test wrapper"""
    print("\n" + "="*60)
    print("🧪 TEST LLAMA RAG WRAPPER")
    print("="*60 + "\n")
    
    try:
        # Crea wrapper con Llama 2 7B quantized
        wrapper = LlamaRAGWrapper(
            config='llama-qlora',
            llama_model_name='meta-llama/Llama-2-7b-chat-hf',
            use_quantization=True,
            quantization_bits=4,
        )
        
        # Test con API Groq-style
        print("\n📝 Test 1: API Groq-style\n")
        
        messages = [
            {
                "role": "system",
                "content": "Sei una guida spirituale esperta. Rispondi in modo empatico e profondo."
            },
            {
                "role": "user",
                "content": (
                    "Contesto:\n"
                    "[Fonte 1]\nLa meditazione è una pratica per calmare la mente.\n\n"
                    "[Fonte 2]\nAttraverso la meditazione si raggiunge la pace interiore.\n\n"
                    "Domanda: Cos'è la meditazione e come si pratica?"
                )
            }
        ]
        
        response = wrapper.chat.completions.create(
            messages=messages,
            model="llama-rag",
            temperature=0.7,
            max_tokens=300
        )
        
        print(f"✨ Risposta:\n{response.choices[0].message.content}\n")
        print(f"📊 Token usage: {response.usage.total_tokens}")
        print(f"   Input: {response.usage.prompt_tokens} | Output: {response.usage.completion_tokens}\n")
        
        # Test con chunks RAG raw
        print("\n📝 Test 2: Chunks RAG raw\n")
        
        chunks = [
            {
                "testo": "I chakra sono centri energetici del corpo che regolano il flusso vitale.",
                "metadata": {"autore": "Maestro Yoga", "libro": "Chakra Guide"}
            },
            {
                "testo": "Il primo chakra, Muladhara, è la radice della stabilità e sicurezza.",
                "metadata": {"autore": "Maestro Yoga", "libro": "Chakra Guide"}
            }
        ]
        
        risposta = wrapper.generate_with_chunks(
            query="Cosa sono i chakra?",
            chunks=chunks,
            max_tokens=200
        )
        
        print(f"✨ Risposta:\n{risposta}\n")
        
        print("✅ Test completato con successo!\n")
        
    except Exception as e:
        print(f"\n❌ Errore durante test: {e}")
        print("\n💡 Assicurati di aver installato:")
        print("   pip install transformers accelerate bitsandbytes peft")
        print("   E di avere accesso ai modelli Llama su HuggingFace")
        print("   (Richiede accettare license Meta Llama)\n")


if __name__ == "__main__":
    test_llama_rag_wrapper()
