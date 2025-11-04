"""
Test import moduli backend
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent  # Go up to project root
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

print("🧪 Testing backend imports...\n")

# Test 1: Flask
try:
    from flask import Flask
    from flask_cors import CORS
    print("✅ Flask imports OK")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    print("   Install: pip install flask flask-cors")
    exit(1)

# Test 2: Prompts
try:
    # Prova import diretto
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "prompts_config", 
        PROJECT_ROOT / "Prompt" / "prompts_config.py"
    )
    prompts_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prompts_module)
    SYSTEM_PROMPT = prompts_module.SYSTEM_PROMPT
    print(f"✅ Prompts import OK ({len(SYSTEM_PROMPT)} chars)")
except Exception as e:
    print(f"❌ Prompts import failed: {e}")
    exit(1)

# Test 3: Model config
try:
    from config.model_config import get_config
    config = get_config("llama-qlora")
    print(f"✅ Model config OK (vocab_size: {config.vocab_size})")
except ImportError as e:
    print(f"❌ Model config import failed: {e}")
    exit(1)

# Test 4: Llama wrapper
try:
    from models.llama_rag_wrapper import LlamaRAGWrapper
    print("✅ Llama wrapper import OK")
    print("\n🎉 All imports successful! Backend ready to start.")
    print("\n📝 Next steps:")
    print("   1. Download Llama: python scripts/1_download_llama.py")
    print("   2. Generate embeddings: python scripts/2_generate_embeddings.py")
    print("   3. Start backend: python backend_api/app.py")
except ImportError as e:
    print(f"⚠️ Llama wrapper import warning: {e}")
    print("\n📝 This is OK if you haven't downloaded the model yet.")
    print("   Run: python scripts/1_download_llama.py")
