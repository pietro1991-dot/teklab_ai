#!/usr/bin/env python3
"""
Test Llama RAG senza quantizzazione (per GTX 1050 Ti)
"""
import sys
from pathlib import Path
import torch

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))

print("🔧 Test caricamento Llama RAG Model (NO quantization)...")

try:
    # Test import
    print("📦 Importing modules...")
    from models.llama_rag_model import LlamaRAGModel, create_llama_rag_model
    print("✅ Import successful!")
    
    # Test config
    print("⚙️  Loading config...")
    from config.model_config import get_config
    config = get_config('llama-2-7b')  # Config base senza quantizzazione
    print("✅ Config loaded!")
    
    # Test model path
    model_path = PROJECT_ROOT / "ai_system" / "models" / "Llama-2-7b-chat-hf"
    print(f"📂 Model path: {model_path}")
    print(f"   Exists: {'✅' if model_path.exists() else '❌'}")
    
    if model_path.exists():
        print("\n🦙 Creating LlamaRAGModel (NO quantization)...")
        
        # Crea modello SENZA quantizzazione per evitare problemi bitsandbytes
        model = LlamaRAGModel(
            llama_model_name=str(model_path),
            use_quantization=False,  # DISABILITA quantizzazione
            use_lora=False,          # DISABILITA LoRA per ora
            torch_dtype=torch.float16,  # Usa float16 per risparmiare memoria
            device_map="cuda" if torch.cuda.is_available() else "cpu"
        )
        
        print("✅ Model created successfully!")
        print(f"   Model name: {model.llama_model_name}")
        print(f"   Device: {model.llama.device}")
        
        # Test simple generation
        print("\n🧪 Testing generation...")
        test_response = model.generate(
            query="Ciao, come stai?",
            context_chunks=["Questo è un test di generazione."],
            max_new_tokens=20  # Ridotto per test veloce
        )
        print(f"✅ Generation test: {test_response}")
        
        print("\n🎉 Test completato con successo!")
        
    else:
        print(f"❌ Model directory not found: {model_path}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all dependencies are installed:")
    print("   pip install transformers accelerate sentence-transformers")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()