"""
Configurazioni per Custom RAG Model.
Preset ottimizzati per diversi scenari di utilizzo e hardware disponibile.
"""

import torch
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Configurazione modello RAG custom."""
    
    # Architecture
    vocab_size: int = 50000
    embedding_dim: int = 384  # Match sentence-transformers all-MiniLM-L6-v2
    hidden_dim: int = 512
    num_layers: int = 2
    num_heads: int = 8
    dropout: float = 0.1
    max_seq_length: int = 512
    
    # Training
    batch_size: int = 16
    learning_rate: float = 3e-4
    weight_decay: float = 0.01
    max_epochs: int = 50
    warmup_steps: int = 1000
    gradient_clip_norm: float = 1.0
    
    # Optimization
    use_amp: bool = True  # Automatic Mixed Precision
    accumulation_steps: int = 1
    
    # Regularization
    label_smoothing: float = 0.1
    attention_dropout: float = 0.1
    
    # Early Stopping
    patience: int = 5
    min_delta: float = 0.001
    
    # Checkpointing
    save_every_n_epochs: int = 5
    keep_last_n_checkpoints: int = 3
    
    # Device
    device: str = field(default_factory=lambda: 'cuda' if torch.cuda.is_available() else 'cpu')
    num_workers: int = 4
    pin_memory: bool = True
    
    # Logging
    log_every_n_steps: int = 10
    eval_every_n_steps: int = 100
    use_tensorboard: bool = True
    use_wandb: bool = False
    wandb_project: Optional[str] = None
    
    # RAG Specific
    num_retrieved_chunks: int = 5
    context_window: int = 2048
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ModelConfig':
        """Create from dictionary."""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})


# ==================== PRESET CONFIGURATIONS ====================

BASE_CONFIG = ModelConfig(
    # Architecture - Leggera per CPU
    vocab_size=30000,
    embedding_dim=384,
    hidden_dim=256,
    num_layers=1,
    num_heads=4,
    dropout=0.1,
    max_seq_length=256,
    
    # Training - Fast iteration
    batch_size=8,
    learning_rate=5e-4,
    max_epochs=20,
    warmup_steps=500,
    use_amp=False,  # CPU-friendly
    
    # Device
    device='cpu',
    num_workers=2,
    
    # Logging
    log_every_n_steps=20,
    eval_every_n_steps=200,
    use_tensorboard=False,
    
    # RAG
    num_retrieved_chunks=3,
    context_window=512,
)

ADVANCED_CONFIG = ModelConfig(
    # Architecture - Balanced GPU
    vocab_size=50000,
    embedding_dim=384,
    hidden_dim=512,
    num_layers=2,
    num_heads=8,
    dropout=0.15,
    max_seq_length=512,
    
    # Training - Production quality
    batch_size=16,
    learning_rate=3e-4,
    weight_decay=0.01,
    max_epochs=50,
    warmup_steps=1000,
    use_amp=True,
    accumulation_steps=2,
    
    # Regularization
    label_smoothing=0.1,
    attention_dropout=0.1,
    
    # Early Stopping
    patience=5,
    min_delta=0.001,
    
    # Device
    device='cuda' if torch.cuda.is_available() else 'cpu',
    num_workers=4,
    pin_memory=True,
    
    # Logging
    log_every_n_steps=10,
    eval_every_n_steps=100,
    use_tensorboard=True,
    
    # RAG
    num_retrieved_chunks=5,
    context_window=2048,
    temperature=0.7,
)

EXPERIMENTAL_CONFIG = ModelConfig(
    # Architecture - Large model per GPU potenti
    vocab_size=100000,
    embedding_dim=768,  # GPT-2 size
    hidden_dim=1024,
    num_layers=4,
    num_heads=16,
    dropout=0.2,
    max_seq_length=1024,
    
    # Training - Extensive
    batch_size=32,
    learning_rate=1e-4,
    weight_decay=0.02,
    max_epochs=100,
    warmup_steps=2000,
    use_amp=True,
    accumulation_steps=4,
    
    # Regularization
    label_smoothing=0.15,
    attention_dropout=0.15,
    
    # Early Stopping
    patience=10,
    min_delta=0.0005,
    
    # Checkpointing
    save_every_n_epochs=3,
    keep_last_n_checkpoints=5,
    
    # Device
    device='cuda' if torch.cuda.is_available() else 'cpu',
    num_workers=8,
    pin_memory=True,
    
    # Logging
    log_every_n_steps=5,
    eval_every_n_steps=50,
    use_tensorboard=True,
    use_wandb=True,
    wandb_project='spirituality-ai-rag',
    
    # RAG
    num_retrieved_chunks=7,
    context_window=4096,
    temperature=0.8,
    top_k=100,
    top_p=0.95,
)

# ==================== LLAMA CONFIGS (NEW) ====================

LLAMA_2_7B_CONFIG = ModelConfig(
    # Architecture - Llama 2 7B optimized for RAG
    vocab_size=32000,  # Llama tokenizer
    embedding_dim=4096,  # Llama 2 7B hidden size
    hidden_dim=4096,
    num_layers=32,  # Llama layers
    num_heads=32,
    dropout=0.1,
    max_seq_length=4096,  # Llama context window
    
    # Training - Fine-tuning (LoRA recommended)
    batch_size=2,  # Small per memoria
    learning_rate=2e-5,  # Learning rate basso per fine-tuning
    weight_decay=0.01,
    max_epochs=10,  # Poche epoch per fine-tuning
    warmup_steps=100,
    use_amp=True,  # Mixed precision essenziale
    accumulation_steps=8,  # Simula batch_size=16
    
    # Regularization
    label_smoothing=0.05,
    attention_dropout=0.1,
    
    # Early Stopping
    patience=3,
    min_delta=0.001,
    
    # Checkpointing
    save_every_n_epochs=2,
    keep_last_n_checkpoints=3,
    
    # Device
    device='cuda' if torch.cuda.is_available() else 'cpu',
    num_workers=4,
    pin_memory=True,
    
    # Logging
    log_every_n_steps=10,
    eval_every_n_steps=100,
    use_tensorboard=True,
    
    # RAG
    num_retrieved_chunks=5,
    context_window=4096,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
)

LLAMA_3_8B_CONFIG = ModelConfig(
    # Architecture - Llama 3 8B optimized for RAG
    vocab_size=128256,  # Llama 3 tokenizer (expanded)
    embedding_dim=4096,  # Llama 3 8B hidden size
    hidden_dim=4096,
    num_layers=32,
    num_heads=32,
    dropout=0.1,
    max_seq_length=8192,  # Llama 3 extended context
    
    # Training - Fine-tuning avanzato
    batch_size=2,
    learning_rate=1e-5,  # Ancora più basso per Llama 3
    weight_decay=0.01,
    max_epochs=5,  # Poche epoch sufficienti
    warmup_steps=50,
    use_amp=True,
    accumulation_steps=16,  # Simula batch_size=32
    
    # Regularization
    label_smoothing=0.03,
    attention_dropout=0.1,
    
    # Early Stopping
    patience=2,
    min_delta=0.0005,
    
    # Checkpointing
    save_every_n_epochs=1,
    keep_last_n_checkpoints=3,
    
    # Device
    device='cuda' if torch.cuda.is_available() else 'cpu',
    num_workers=4,
    pin_memory=True,
    
    # Logging
    log_every_n_steps=5,
    eval_every_n_steps=50,
    use_tensorboard=True,
    use_wandb=False,
    
    # RAG
    num_retrieved_chunks=7,
    context_window=8192,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
)

LLAMA_QLORA_CONFIG = ModelConfig(
    # Architecture - QLoRA (Quantized LoRA) per risparmiare memoria
    vocab_size=32000,
    embedding_dim=4096,
    hidden_dim=4096,
    num_layers=32,
    num_heads=32,
    dropout=0.1,
    max_seq_length=4096,
    
    # Training - QLoRA ottimizzato
    batch_size=1,  # Minimo per 4-bit quantization
    learning_rate=2e-4,  # LoRA può permettersi LR più alto
    weight_decay=0.0,  # QLoRA non usa weight decay
    max_epochs=5,
    warmup_steps=50,
    use_amp=False,  # QLoRA gestisce precision internamente
    accumulation_steps=16,  # Compensa batch_size=1
    
    # Regularization
    label_smoothing=0.0,
    attention_dropout=0.05,
    
    # Early Stopping
    patience=2,
    min_delta=0.001,
    
    # Checkpointing
    save_every_n_epochs=1,
    keep_last_n_checkpoints=2,
    
    # Device
    device='cuda' if torch.cuda.is_available() else 'cpu',
    num_workers=2,
    pin_memory=True,
    
    # Logging
    log_every_n_steps=10,
    eval_every_n_steps=100,
    use_tensorboard=True,
    
    # RAG
    num_retrieved_chunks=5,
    context_window=4096,
    temperature=0.7,
    top_k=40,
    top_p=0.85,
)


# ==================== HELPER FUNCTIONS ====================

def get_config(name: str = 'base') -> ModelConfig:
    """
    Ottieni configurazione per nome.
    
    Args:
        name: 'base', 'advanced', 'experimental', 'llama-2-7b', 'llama-3-8b', 'llama-qlora'
    
    Returns:
        ModelConfig instance
    """
    configs = {
        'base': BASE_CONFIG,
        'advanced': ADVANCED_CONFIG,
        'experimental': EXPERIMENTAL_CONFIG,
        'llama-2-7b': LLAMA_2_7B_CONFIG,
        'llama-3-8b': LLAMA_3_8B_CONFIG,
        'llama-qlora': LLAMA_QLORA_CONFIG,
    }
    
    if name.lower() not in configs:
        raise ValueError(f"Config '{name}' non trovata. Opzioni: {list(configs.keys())}")
    
    return configs[name.lower()]


def auto_config() -> ModelConfig:
    """
    Seleziona automaticamente config ottimale per l'hardware disponibile.
    
    Returns:
        ModelConfig instance
    """
    if torch.cuda.is_available():
        # Check VRAM disponibile
        total_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
        
        if total_memory >= 16:
            print(f"🚀 GPU detected ({total_memory:.1f}GB VRAM) - Using EXPERIMENTAL config")
            return EXPERIMENTAL_CONFIG
        elif total_memory >= 8:
            print(f"⚡ GPU detected ({total_memory:.1f}GB VRAM) - Using ADVANCED config")
            return ADVANCED_CONFIG
        else:
            print(f"💻 GPU detected ({total_memory:.1f}GB VRAM) - Using BASE config")
            return BASE_CONFIG
    else:
        print("🖥️  CPU detected - Using BASE config")
        return BASE_CONFIG


def print_config(config: ModelConfig):
    """Pretty print configurazione."""
    print("\n" + "="*60)
    print("📊 MODEL CONFIGURATION")
    print("="*60)
    
    sections = {
        "Architecture": [
            'vocab_size', 'embedding_dim', 'hidden_dim', 'num_layers', 
            'num_heads', 'dropout', 'max_seq_length'
        ],
        "Training": [
            'batch_size', 'learning_rate', 'weight_decay', 'max_epochs',
            'warmup_steps', 'gradient_clip_norm', 'use_amp'
        ],
        "Device": ['device', 'num_workers', 'pin_memory'],
        "RAG": [
            'num_retrieved_chunks', 'context_window', 'temperature',
            'top_k', 'top_p'
        ],
    }
    
    for section, keys in sections.items():
        print(f"\n{section}:")
        for key in keys:
            if hasattr(config, key):
                value = getattr(config, key)
                print(f"  • {key}: {value}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Test configurations
    print("Testing configuration presets...\n")
    
    # Auto-detect
    config = auto_config()
    print_config(config)
    
    # Test all presets
    for name in ['base', 'advanced', 'experimental']:
        cfg = get_config(name)
        print(f"\n{name.upper()} Config:")
        print(f"  Params (approx): {cfg.vocab_size * cfg.embedding_dim + cfg.hidden_dim**2 * cfg.num_layers:,}")
        print(f"  Device: {cfg.device}")
        print(f"  Batch size: {cfg.batch_size}")
        print(f"  Max epochs: {cfg.max_epochs}")
