#!/usr/bin/env python3
"""
Test rapido del chatbot Llama 3.2 3B con RAG
"""
import sys
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

print("="*70)
print("🧪 TEST CHATBOT LLAMA 3.2 3B + RAG")
print("="*70)

# Import chatbot
print("\n📦 Importing chatbot...")
try:
    import os
    os.chdir(str(SCRIPT_DIR / "scripts"))
    sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
    
    # Now import from 6_chatbot.py
    from pathlib import Path
    import pickle
    import uuid
    from datetime import datetime
    
    # Import needed modules
    from prompts_config import SYSTEM_PROMPT
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print("✅ Imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Load model
print("\n🦙 Caricamento Llama 3.2 3B...")
try:
    model_path = PROJECT_ROOT / "ai_system" / "models" / "Llama-3.2-3B-Instruct"
    
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    )
    
    print(f"✅ Modello caricato!")
    print(f"   Device: {model.device}")
    
    if torch.cuda.is_available():
        vram_used = torch.cuda.memory_allocated() / 1024**3
        vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"   VRAM: {vram_used:.2f} GB / {vram_total:.2f} GB")
    
except Exception as e:
    print(f"❌ Errore: {e}")
    exit(1)

# Test generation
print("\n🧪 Test generazione...")
test_questions = [
    "Ciao! Chi sei?",
    "Cos'è la meditazione?",
]

for question in test_questions:
    print(f"\n❓ Domanda: {question}")
    
    try:
        messages = [
            {"role": "system", "content": "Sei un assistente spirituale gentile e saggio."},
            {"role": "user", "content": question}
        ]
        
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
        
        full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "<|start_header_id|>assistant<|end_header_id|>" in full_response:
            response = full_response.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
        else:
            response = full_response
        
        print(f"🤖 Risposta: {response[:200]}...")
        
    except Exception as e:
        print(f"❌ Errore: {e}")

print("\n" + "="*70)
print("✅ Test completato!")
print("="*70)