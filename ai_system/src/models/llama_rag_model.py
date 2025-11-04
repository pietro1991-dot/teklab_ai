"""
Llama RAG Model - Integrazione Llama pre-addestrato con sistema RAG custom
Architettura: RAG Context Encoder → Llama Pre-trained Decoder

Supporta:
- Llama 2 (7B, 13B, 70B)
- Llama 3/3.1 (8B, 70B, 405B)
- Fine-tuning con LoRA/QLoRA
- 4-bit/8-bit quantization per risparmiare memoria
"""

import torch
import torch.nn as nn
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import warnings

# Transformers per Llama
try:
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        GenerationConfig
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    warnings.warn(
        "⚠️  transformers non installato. Installa con: pip install transformers accelerate bitsandbytes",
        ImportWarning
    )

# PEFT per LoRA/QLoRA (optional ma consigliato)
try:
    from peft import (
        LoraConfig,
        get_peft_model,
        prepare_model_for_kbit_training,
        TaskType
    )
    PEFT_AVAILABLE = True
except ImportError:
    PEFT_AVAILABLE = False
    warnings.warn(
        "⚠️  peft non installato. Fine-tuning full model (alta memoria). Installa con: pip install peft",
        ImportWarning
    )


class ContextAdapter(nn.Module):
    """
    Adapter che trasforma RAG context embeddings in input compatibili con Llama.
    
    Input: sentence-transformers embeddings (384 dim)
    Output: Llama hidden states (4096 dim)
    """
    
    def __init__(
        self,
        input_dim: int = 384,  # sentence-transformers
        llama_hidden_dim: int = 4096,  # Llama 2/3 7B/8B
        num_context_tokens: int = 8,  # Numero soft prompts per context
        dropout: float = 0.1
    ):
        super().__init__()
        self.num_context_tokens = num_context_tokens
        
        # Projection layers
        self.context_projection = nn.Sequential(
            nn.Linear(input_dim, llama_hidden_dim),
            nn.LayerNorm(llama_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(llama_hidden_dim, llama_hidden_dim * num_context_tokens),
        )
        
        # Learnable attention pooling per combinare chunks
        self.attention_pool = nn.MultiheadAttention(
            embed_dim=llama_hidden_dim,
            num_heads=8,
            dropout=dropout,
            batch_first=True
        )
        
    def forward(self, chunk_embeddings: torch.Tensor) -> torch.Tensor:
        """
        Args:
            chunk_embeddings: (batch, num_chunks, 384) - RAG chunks
        
        Returns:
            context_vectors: (batch, num_context_tokens, llama_hidden_dim)
        """
        batch_size, num_chunks, _ = chunk_embeddings.shape
        
        # Project each chunk to Llama space
        projected = self.context_projection(chunk_embeddings)  # (B, num_chunks, llama_dim * num_tokens)
        projected = projected.view(batch_size, num_chunks, self.num_context_tokens, -1)
        
        # Flatten to (B, num_chunks * num_tokens, llama_dim)
        projected = projected.view(batch_size, -1, projected.size(-1))
        
        # Attention pooling to reduce to fixed number of context tokens
        query = projected[:, :self.num_context_tokens, :]  # First N tokens as query
        context_vectors, _ = self.attention_pool(query, projected, projected)
        
        return context_vectors


class LlamaRAGModel(nn.Module):
    """
    Modello RAG completo con Llama pre-addestrato come generatore.
    
    Pipeline:
    1. RAG chunks → ContextAdapter → Context vectors (soft prompts)
    2. Context vectors + User query → Llama decoder
    3. Llama genera risposta (con RAG context integrato)
    
    Vantaggi:
    - ✅ Llama pre-addestrato (conoscenza generale)
    - ✅ Fine-tuning leggero con LoRA (efficiente)
    - ✅ RAG context injection tramite soft prompts
    - ✅ Supporto quantization 4-bit/8-bit
    """
    
    def __init__(
        self,
        llama_model_name: str = "meta-llama/Llama-2-7b-chat-hf",
        use_lora: bool = True,
        use_quantization: bool = True,
        quantization_bits: int = 4,
        lora_r: int = 16,
        lora_alpha: int = 32,
        lora_dropout: float = 0.05,
        context_adapter_tokens: int = 8,
        load_in_8bit: bool = False,
        load_in_4bit: bool = True,
        device_map: str = "auto",
        torch_dtype: torch.dtype = torch.bfloat16,
        trust_remote_code: bool = False,
    ):
        """
        Args:
            llama_model_name: HuggingFace model ID (es. "meta-llama/Llama-2-7b-chat-hf")
            use_lora: Se usare LoRA per fine-tuning efficiente
            use_quantization: Se usare quantization (4-bit o 8-bit)
            quantization_bits: 4 o 8 bit quantization
            lora_r: LoRA rank (più basso = meno parametri trainabili)
            lora_alpha: LoRA scaling factor
            lora_dropout: Dropout per LoRA layers
            context_adapter_tokens: Numero soft prompts per RAG context
            device_map: Device mapping ("auto", "cuda", "cpu")
            torch_dtype: Data type (bfloat16 consigliato per Llama)
        """
        super().__init__()
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "transformers non installato! Installa con:\n"
                "pip install transformers accelerate bitsandbytes"
            )
        
        self.llama_model_name = llama_model_name
        self.use_lora = use_lora and PEFT_AVAILABLE
        self.use_quantization = use_quantization
        
        print(f"\n🦙 Caricamento Llama: {llama_model_name}")
        print(f"   LoRA: {'✅' if self.use_lora else '❌'}")
        print(f"   Quantization: {'✅ ' + str(quantization_bits) + '-bit' if use_quantization else '❌'}")
        
        # Configurazione quantization (per risparmiare VRAM)
        quantization_config = None
        if use_quantization:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=load_in_4bit and quantization_bits == 4,
                load_in_8bit=load_in_8bit and quantization_bits == 8,
                bnb_4bit_compute_dtype=torch_dtype,
                bnb_4bit_use_double_quant=True,  # Nested quantization
                bnb_4bit_quant_type="nf4",  # Normalized Float 4
            )
        
        # Carica modello Llama pre-addestrato
        self.llama = AutoModelForCausalLM.from_pretrained(
            llama_model_name,
            quantization_config=quantization_config,
            device_map=device_map,
            torch_dtype=torch_dtype,  # Ripristinato torch_dtype invece di dtype
            trust_remote_code=trust_remote_code,
            low_cpu_mem_usage=True,
        )
        
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            llama_model_name,
            trust_remote_code=trust_remote_code,
            use_fast=True,
        )
        
        # Fix tokenizer se non ha pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.llama.config.pad_token_id = self.tokenizer.eos_token_id
        
        # Context Adapter (RAG → Llama)
        llama_hidden_dim = self.llama.config.hidden_size
        self.context_adapter = ContextAdapter(
            input_dim=384,  # sentence-transformers
            llama_hidden_dim=llama_hidden_dim,
            num_context_tokens=context_adapter_tokens,
            dropout=0.1
        )
        
        # Prepare for LoRA fine-tuning
        if self.use_lora:
            print("🔧 Configurazione LoRA per fine-tuning efficiente...")
            
            # Prepare model for k-bit training (se quantized)
            if use_quantization:
                self.llama = prepare_model_for_kbit_training(self.llama)
            
            # LoRA configuration
            lora_config = LoraConfig(
                r=lora_r,
                lora_alpha=lora_alpha,
                target_modules=[
                    "q_proj",  # Query projection
                    "k_proj",  # Key projection
                    "v_proj",  # Value projection
                    "o_proj",  # Output projection
                    "gate_proj",  # MLP gate
                    "up_proj",    # MLP up
                    "down_proj",  # MLP down
                ],
                lora_dropout=lora_dropout,
                bias="none",
                task_type=TaskType.CAUSAL_LM,
            )
            
            self.llama = get_peft_model(self.llama, lora_config)
            self.llama.print_trainable_parameters()
        
        # Generation config
        self.generation_config = GenerationConfig(
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            repetition_penalty=1.1,
        )
        
        print(f"✅ Llama RAG Model pronto!\n")
    
    def prepare_context_prompt(
        self,
        query: str,
        context_chunks: List[str],
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Prepara prompt formattato per Llama con RAG context.
        
        Args:
            query: Domanda utente
            context_chunks: Lista chunks RAG rilevanti
            system_prompt: System prompt opzionale
        
        Returns:
            prompt: Prompt formattato per Llama
        """
        # System prompt default
        if system_prompt is None:
            system_prompt = (
                "Sei una guida spirituale esperta. Rispondi basandoti sul contesto fornito. "
                "Sii empatico, chiaro e approfondito."
            )
        
        # Costruisci context
        context_text = "\n\n".join([
            f"[Fonte {i+1}]\n{chunk}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        # Prompt template (Llama 2 chat format)
        if "Llama-2" in self.llama_model_name or "llama-2" in self.llama_model_name:
            prompt = (
                f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n"
                f"Contesto:\n{context_text}\n\n"
                f"Domanda: {query} [/INST]"
            )
        # Llama 3 format (diverso)
        elif "Llama-3" in self.llama_model_name or "llama-3" in self.llama_model_name:
            prompt = (
                f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
                f"{system_prompt}<|eot_id|>\n"
                f"<|start_header_id|>user<|end_header_id|>\n\n"
                f"Contesto:\n{context_text}\n\n"
                f"Domanda: {query}<|eot_id|>\n"
                f"<|start_header_id|>assistant<|end_header_id|>\n\n"
            )
        else:
            # Generic format
            prompt = (
                f"System: {system_prompt}\n\n"
                f"Context:\n{context_text}\n\n"
                f"User: {query}\n\n"
                f"Assistant:"
            )
        
        return prompt
    
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        context_embeddings: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        """
        Forward pass per training.
        
        Args:
            input_ids: (batch, seq_len) - Token IDs
            attention_mask: (batch, seq_len) - Attention mask
            context_embeddings: (batch, num_chunks, 384) - RAG chunks embeddings
            labels: (batch, seq_len) - Labels per training (opzionale)
        
        Returns:
            output: Dict con loss, logits, etc.
        """
        # Inject RAG context come soft prompts
        if context_embeddings is not None:
            context_vectors = self.context_adapter(context_embeddings)
            # TODO: Concatenare context_vectors agli input embeddings di Llama
            # (Richiede modifica embedding layer - implementazione avanzata)
        
        # Forward through Llama
        outputs = self.llama(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
            return_dict=True,
        )
        
        return {
            'loss': outputs.loss if labels is not None else None,
            'logits': outputs.logits,
            'hidden_states': outputs.hidden_states if hasattr(outputs, 'hidden_states') else None,
        }
    
    @torch.no_grad()
    def generate(
        self,
        query: str,
        context_chunks: List[str],
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
    ) -> str:
        """
        Genera risposta usando Llama con RAG context.
        
        Args:
            query: Domanda utente
            context_chunks: Chunks RAG rilevanti
            system_prompt: System prompt opzionale
            max_new_tokens: Max token da generare
            temperature: Temperature sampling
            top_p: Nucleus sampling
            top_k: Top-k sampling
        
        Returns:
            risposta: Risposta generata
        """
        self.eval()
        
        # Prepara prompt
        prompt = self.prepare_context_prompt(query, context_chunks, system_prompt)
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.llama.config.max_position_embeddings - max_new_tokens,
        )
        inputs = {k: v.to(self.llama.device) for k, v in inputs.items()}
        
        # Update generation config
        gen_config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            repetition_penalty=1.1,
        )
        
        # Generate
        outputs = self.llama.generate(
            **inputs,
            generation_config=gen_config,
        )
        
        # Decode (rimuovi prompt)
        prompt_length = inputs['input_ids'].shape[1]
        generated_tokens = outputs[0][prompt_length:]
        risposta = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        return risposta.strip()
    
    def save_pretrained(self, save_path: str):
        """Salva modello fine-tunato"""
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Salva LoRA adapter (se usato)
        if self.use_lora:
            self.llama.save_pretrained(save_path / "lora_adapter")
            print(f"💾 LoRA adapter salvato in: {save_path / 'lora_adapter'}")
        else:
            # Salva full model
            self.llama.save_pretrained(save_path / "llama_model")
            print(f"💾 Llama model salvato in: {save_path / 'llama_model'}")
        
        # Salva context adapter
        torch.save(
            self.context_adapter.state_dict(),
            save_path / "context_adapter.pth"
        )
        print(f"💾 Context adapter salvato in: {save_path / 'context_adapter.pth'}")
        
        # Salva tokenizer
        self.tokenizer.save_pretrained(save_path / "tokenizer")
        print(f"✅ Salvataggio completato!")
    
    @classmethod
    def from_pretrained(
        cls,
        load_path: str,
        llama_model_name: Optional[str] = None,
        **kwargs
    ):
        """Carica modello fine-tunato"""
        load_path = Path(load_path)
        
        # Detect model name from saved files
        if llama_model_name is None:
            # Try to read from config
            config_path = load_path / "lora_adapter" / "adapter_config.json"
            if config_path.exists():
                import json
                with open(config_path) as f:
                    config = json.load(f)
                    llama_model_name = config.get("base_model_name_or_path", "meta-llama/Llama-2-7b-chat-hf")
            else:
                raise ValueError("llama_model_name must be specified or found in saved config")
        
        # Create model
        model = cls(llama_model_name=llama_model_name, **kwargs)
        
        # Load LoRA adapter
        if (load_path / "lora_adapter").exists():
            from peft import PeftModel
            model.llama = PeftModel.from_pretrained(
                model.llama,
                str(load_path / "lora_adapter")
            )
            print(f"📦 LoRA adapter caricato da: {load_path / 'lora_adapter'}")
        
        # Load context adapter
        adapter_path = load_path / "context_adapter.pth"
        if adapter_path.exists():
            model.context_adapter.load_state_dict(
                torch.load(adapter_path, map_location=model.llama.device)
            )
            print(f"📦 Context adapter caricato da: {adapter_path}")
        
        print(f"✅ Modello caricato con successo!")
        return model


def create_llama_rag_model(
    config_name: str = "llama-2-7b",
    **override_kwargs
) -> LlamaRAGModel:
    """
    Factory function per creare LlamaRAGModel con config preset.
    
    Args:
        config_name: Nome config ('llama-2-7b', 'llama-3-8b', 'llama-qlora')
        **override_kwargs: Override parametri config
    
    Returns:
        LlamaRAGModel instance
    """
    # Import con try/except per gestire sia esecuzione come modulo che come script
    try:
        from config.model_config import get_config
    except ImportError:
        # Fallback se l'import relativo non funziona
        import sys
        config_path = Path(__file__).parent.parent / "config"
        if str(config_path) not in sys.path:
            sys.path.insert(0, str(config_path.parent))
        from config.model_config import get_config
    
    config = get_config(config_name)
    
    # Prova prima a usare modello locale, poi fallback a HuggingFace
    def get_model_path(hf_name: str) -> str:
        """Trova modello locale o usa HuggingFace ID."""
        # Path è già importato globalmente
        local_model_dir = Path(__file__).parent.parent.parent / "models" / hf_name.split('/')[-1]
        
        if local_model_dir.exists() and (local_model_dir / "config.json").exists():
            print(f"✅ Uso modello LOCALE: {local_model_dir}")
            return str(local_model_dir)
        else:
            print(f"⚠️  Modello locale non trovato in: {local_model_dir}")
            print(f"   Uso HuggingFace: {hf_name}")
            print(f"   💡 Per usare offline: python ai_system/download_llama.py")
            return hf_name
    
    # Map config to model parameters
    model_map = {
        'llama-2-7b': "meta-llama/Llama-2-7b-chat-hf",
        'llama-3-8b': "meta-llama/Meta-Llama-3-8B-Instruct",
        'llama-qlora': "Qwen/Qwen2.5-1.5B-Instruct",  # Modello multilingua per italiano
    }
    
    hf_model_name = model_map.get(config_name, "Qwen/Qwen2.5-1.5B-Instruct")
    model_name = get_model_path(hf_model_name)
    
    # Determina quantization settings
    use_quantization = config_name == 'llama-qlora'
    quantization_bits = 4 if use_quantization else None
    
    model = LlamaRAGModel(
        llama_model_name=override_kwargs.get('llama_model_name', model_name),
        use_lora=override_kwargs.get('use_lora', True),
        use_quantization=override_kwargs.get('use_quantization', use_quantization),
        quantization_bits=override_kwargs.get('quantization_bits', quantization_bits or 4),
        lora_r=override_kwargs.get('lora_r', 16),
        lora_alpha=override_kwargs.get('lora_alpha', 32),
        lora_dropout=override_kwargs.get('lora_dropout', 0.05),
        context_adapter_tokens=override_kwargs.get('context_adapter_tokens', 8),
        device_map=override_kwargs.get('device_map', 'auto'),
        torch_dtype=override_kwargs.get('torch_dtype', torch.bfloat16),
    )
    
    return model


if __name__ == "__main__":
    # Test caricamento
    print("🧪 Test LlamaRAGModel\n")
    
    # Test con Llama 2 7B + LoRA + 4-bit quantization
    try:
        model = create_llama_rag_model(
            config_name='llama-qlora',
            llama_model_name='meta-llama/Llama-2-7b-chat-hf'
        )
        
        # Test generation
        query = "Cos'è la meditazione?"
        context = [
            "La meditazione è una pratica mentale che porta alla consapevolezza.",
            "Attraverso la meditazione si raggiunge uno stato di pace interiore."
        ]
        
        print("\n🧪 Test generazione:")
        print(f"Query: {query}")
        print(f"Context chunks: {len(context)}")
        
        risposta = model.generate(
            query=query,
            context_chunks=context,
            max_new_tokens=200
        )
        
        print(f"\n✨ Risposta:\n{risposta}\n")
        
    except Exception as e:
        print(f"❌ Errore test: {e}")
        print("\n💡 Per usare questo modello serve:")
        print("   1. pip install transformers accelerate bitsandbytes peft")
        print("   2. Accesso a modelli Llama su HuggingFace")
        print("   3. GPU con almeno 6GB VRAM (per 4-bit quantization)")
