#!/usr/bin/env python3
"""
Test semplificato per verificare che il modello Llama RAG si carichi correttamente
"""
import sys
import os
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))

print("🔧 Test caricamento Llama RAG Model...")

try:
    # Test import
    print("📦 Importing modules...")
    from models.llama_rag_model import LlamaRAGModel, create_llama_rag_model
    print("✅ Import successful!")
    
    # Test config
    print("⚙️  Loading config...")
    from config.model_config import get_config
    config = get_config('llama-qlora')  # Config ottimizzato per 4GB VRAM
    print("✅ Config loaded!")
    
    # Test model path
    model_path = PROJECT_ROOT / "ai_system" / "models" / "Llama-2-7b-chat-hf"
    print(f"📂 Model path: {model_path}")
    print(f"   Exists: {'✅' if model_path.exists() else '❌'}")
    
    if model_path.exists():
        print("\n🦙 Creating LlamaRAGModel...")
        
        # Crea modello con configurazione minimale per test
        model = create_llama_rag_model(
            config_name='llama-qlora',
            llama_model_name=str(model_path),
            use_quantization=True,
            quantization_bits=4,
            use_lora=True
        )
        
        print("✅ Model created successfully!")
        print(f"   Model name: {model.llama_model_name}")
        print(f"   Device: {model.llama.device}")
        
        # Test simple generation
        print("\n🧪 Testing generation...")
        test_response = model.generate(
            query="Ciao, come stai?",
            context_chunks=["Questo è un test."],
            max_new_tokens=50
        )
        print(f"✅ Generation test: {test_response[:100]}...")
        
        print("\n🎉 Test completato con successo!")
        
    else:
        print(f"❌ Model directory not found: {model_path}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all dependencies are installed:")
    print("   pip install transformers accelerate bitsandbytes peft sentence-transformers")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()