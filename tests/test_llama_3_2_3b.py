#!/usr/bin/env python3
"""
Test Llama 3.2 3B - Ottimizzato per GTX 1050 Ti (4GB VRAM)
"""
import os
import torch
from pathlib import Path

# Setup
model_path = Path(__file__).parent / "ai_system" / "models" / "Llama-3.2-3B-Instruct"

print("="*70)
print("🦙 TEST LLAMA 3.2 3B INSTRUCT")
print("="*70)
print(f"\n📂 Model path: {model_path}")

if not model_path.exists():
    print("❌ Modello non trovato! Esegui prima: python download_llama_3_2_3b.py")
    exit(1)

print("✅ Directory modello trovata!")

# Check GPU
print(f"\n🖥️  GPU Info:")
print(f"   CUDA disponibile: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")
    vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"   VRAM totale: {vram_gb:.2f} GB")
    print(f"   VRAM libera: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()) / 1024**3:.2f} GB")

# Import transformers
print("\n📦 Caricando librerie...")
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import transformers
    print(f"✅ Transformers versione: {transformers.__version__}")
except ImportError as e:
    print(f"❌ Errore import: {e}")
    print("   Installa: pip install transformers>=4.45.0")
    exit(1)

# Load tokenizer
print("\n📝 Caricando tokenizer...")
try:
    tokenizer = AutoTokenizer.from_pretrained(str(model_path))
    print("✅ Tokenizer caricato!")
    print(f"   Vocab size: {tokenizer.vocab_size}")
    print(f"   Pad token: {tokenizer.pad_token}")
except Exception as e:
    print(f"❌ Errore caricamento tokenizer: {e}")
    exit(1)

# Load model with float16 (NO quantization - simpler for GTX 1050 Ti)
print("\n🦙 Caricando modello (float16)...")
print("   ⚙️  Configurazione: float16 per GPU 4GB")

try:
    model = AutoModelForCausalLM.from_pretrained(
        str(model_path),
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    )
    print("✅ Modello caricato!")
    print(f"   Device: {model.device}")
    
    # Check memory usage
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        memory_used = torch.cuda.memory_allocated() / 1024**3
        print(f"   📊 VRAM usata: {memory_used:.2f} GB")
        
except Exception as e:
    print(f"❌ Errore caricamento modello: {e}")
    print("\n💡 Suggerimenti:")
    print("   - Aggiorna transformers: pip install --upgrade transformers")
    print("   - Installa bitsandbytes: pip install bitsandbytes")
    exit(1)

# Test generation
print("\n🧪 Test generazione...")
try:
    # Prompt semplice
    messages = [
        {"role": "system", "content": "Sei un assistente spirituale gentile e saggio."},
        {"role": "user", "content": "Ciao! Come stai?"}
    ]
    
    # Apply chat template
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    print(f"📝 Prompt: {prompt[:100]}...")
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    print("🔄 Generando risposta...")
    
    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the assistant's response
    if "<|start_header_id|>assistant<|end_header_id|>" in response:
        response = response.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
    
    print(f"\n🤖 Risposta:\n{response}")
    
    print("\n✅ Test completato con successo!")
    print("🎉 Llama 3.2 3B è pronto per l'uso!")
    
except Exception as e:
    print(f"❌ Errore durante generazione: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*70)
print("📊 RIEPILOGO")
print("="*70)
print(f"✅ Modello: Llama 3.2 3B Instruct")
print(f"✅ Quantizzazione: 8-bit")
print(f"✅ VRAM usata: ~{memory_used:.2f} GB / {vram_gb:.2f} GB")
print(f"✅ Percentuale VRAM: {(memory_used/vram_gb)*100:.1f}%")
print("="*70)