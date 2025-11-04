"""Test rapido per verificare che Llama si carichi"""
import os
os.environ['HF_HUB_OFFLINE'] = '1'  # Skip online checks

print("Loading transformers...")
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("Transformers loaded!")

model_path = r"D:\spirituality.ai\ai_system\models\Llama-2-7b-chat-hf"
print(f"\nLoading model from: {model_path}")

# Test if model exists
if os.path.exists(model_path):
    print("✅ Model directory found!")
    
    # List files
    files = os.listdir(model_path)
    print(f"Files in model dir: {len(files)}")
    
    # Load tokenizer (faster than model)
    print("\nLoading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print("✅ Tokenizer loaded!")
    
    # Check GPU
    print(f"\nCUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    
    print("\n✅ Test completato! Il modello è accessibile.")
else:
    print(f"❌ Model directory not found: {model_path}")
