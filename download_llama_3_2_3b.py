#!/usr/bin/env python3
"""
Download Llama 3.2 3B Instruct - Ottimizzato per 4GB VRAM
Scarica il modello da HuggingFace e lo salva localmente.
"""

import os
import sys
from pathlib import Path
import argparse

# Fix encoding Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from huggingface_hub import snapshot_download, login
    import torch
except ImportError as e:
    print(f"❌ Dipendenze mancanti: {e}")
    print("   Installa con: pip install transformers huggingface-hub torch")
    sys.exit(1)


def load_hf_token():
    """Carica il token HuggingFace dal file .env"""
    env_path = Path(__file__).parent / ".env"
    
    if not env_path.exists():
        print("⚠️  File .env non trovato. Crealo con il token HF_TOKEN")
        return None
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('HF_TOKEN='):
                    return line.split('=', 1)[1].strip()
        return None
    except Exception as e:
        print(f"❌ Errore lettura token: {e}")
        return None


def download_llama_3_2_3b():
    """
    Scarica Llama 3.2 3B Instruct da HuggingFace.
    Modello perfetto per 4GB VRAM (GTX 1050 Ti).
    """
    print("\n" + "="*70)
    print("🦙 DOWNLOAD LLAMA 3.2 3B INSTRUCT")
    print("="*70 + "\n")
    
    # Carica token HuggingFace
    token = load_hf_token()
    if not token:
        print("❌ Token HuggingFace non trovato nel file .env")
        print("   Aggiungi: HF_TOKEN=il_tuo_token")
        return None
    
    print(f"🔑 Token HF trovato: {token[:8]}...{token[-8:]}")
    
    # Login automatico
    try:
        from huggingface_hub import login
        login(token=token)
        print("✅ Login HuggingFace completato!")
    except Exception as e:
        print(f"⚠️  Login automatico fallito: {e}")
        print("   Procedo comunque con il token...")
    
    # Configurazione
    model_name = "meta-llama/Llama-3.2-3B-Instruct"
    project_root = Path(__file__).parent
    local_dir = project_root / "ai_system" / "models" / "Llama-3.2-3B-Instruct"
    
    print(f"🏷️  Modello: {model_name}")
    print(f"📂 Destinazione: {local_dir}")
    print("💾 Dimensione: ~6GB")
    print("🖥️  Ottimizzato per: 4GB VRAM (GTX 1050 Ti)")
    print("")
    
    # Controlla se esiste già
    if local_dir.exists() and (local_dir / "config.json").exists():
        print("✅ Modello già presente!")
        print("   Se vuoi ri-scaricare, cancella la cartella:")
        print(f"   {local_dir}")
        
        # Verifica dimensione
        total_size = sum(f.stat().st_size for f in local_dir.rglob('*') if f.is_file())
        total_size_gb = total_size / (1024**3)
        print(f"💾 Dimensione attuale: {total_size_gb:.2f} GB")
        
        return local_dir
    
    # Controlla spazio disponibile
    disk_usage = os.statvfs(str(local_dir.parent)) if hasattr(os, 'statvfs') else None
    if disk_usage:
        free_space_gb = (disk_usage.f_frsize * disk_usage.f_bavail) / (1024**3)
        if free_space_gb < 8:
            print(f"⚠️  Spazio disponibile: {free_space_gb:.1f}GB")
            print("   Servono almeno 8GB liberi")
            return None
    
    # Conferma download
    print("❓ Procedere con il download? (s/n): ", end="")
    risposta = input().lower().strip()
    if risposta not in ['s', 'si', 'y', 'yes']:
        print("⏭️  Download saltato")
        return None
    
    print("\n🚀 Inizio download...")
    print("   (Questo richiederà 10-20 minuti e ~6GB di spazio)\n")
    
    try:
        # Crea cartella
        local_dir.mkdir(parents=True, exist_ok=True)
        
        # Download con snapshot_download
        print("📥 Download con snapshot_download...")
        snapshot_download(
            repo_id=model_name,
            local_dir=str(local_dir),
            token=token,  # Usa token dal .env
            ignore_patterns=["*.msgpack", "*.h5", "*.ot", "*.gguf"],  # Skip file non necessari
        )
        
        print("✅ Download completato!")
        
        # Verifica file essenziali
        required_files = ["config.json", "tokenizer_config.json", "tokenizer.json"]
        missing = [f for f in required_files if not (local_dir / f).exists()]
        
        if missing:
            print(f"\n⚠️  File mancanti: {missing}")
            print("   Il modello potrebbe non funzionare correttamente")
        else:
            print("✅ Tutti i file essenziali presenti")
            
            # Mostra dimensione totale
            total_size = sum(f.stat().st_size for f in local_dir.rglob('*') if f.is_file())
            total_size_gb = total_size / (1024**3)
            print(f"💾 Dimensione totale: {total_size_gb:.2f} GB")
        
        return local_dir
        
    except Exception as e:
        print(f"\n❌ Errore durante download: {e}")
        print("💡 Possibili soluzioni:")
        print("   1. Verifica connessione internet")
        print("   2. Fai login HuggingFace: huggingface-cli login")
        print("   3. Accetta la license Llama su HuggingFace")
        print("   4. Controlla spazio su disco")
        return None


def verify_model(local_dir: Path):
    """Verifica che il modello locale funzioni."""
    print(f"\n🧪 Test caricamento modello da: {local_dir}")
    
    if not local_dir.exists():
        print("❌ Directory modello non trovata")
        return False
    
    try:
        # Test tokenizer (veloce)
        print("📝 Caricamento tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(str(local_dir))
        print("✅ Tokenizer caricato!")
        
        # Test modello (più lento)
        print("🦙 Caricamento modello...")
        model = AutoModelForCausalLM.from_pretrained(
            str(local_dir),
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        print("✅ Modello caricato!")
        
        # Info GPU
        if torch.cuda.is_available():
            print(f"🖥️  GPU: {torch.cuda.get_device_name(0)}")
            print(f"💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
            
            # Check memoria usata
            torch.cuda.empty_cache()
            memory_used = torch.cuda.memory_allocated() / 1024**3
            print(f"📊 Memoria modello: {memory_used:.2f} GB")
        
        # Test generazione veloce
        print("\n🧪 Test generazione...")
        inputs = tokenizer("Ciao!", return_tensors="pt")
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=10,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"📝 Output test: {response}")
        
        print("\n🎉 Modello funziona correttamente!")
        return True
        
    except Exception as e:
        print(f"❌ Errore test modello: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Download Llama 3.2 3B Instruct')
    parser.add_argument('--verify', action='store_true', help='Verifica modello esistente')
    args = parser.parse_args()
    
    # Path modello
    project_root = Path(__file__).parent.parent
    model_dir = project_root / "ai_system" / "models" / "Llama-3.2-3B-Instruct"
    
    if args.verify:
        # Solo verifica
        if verify_model(model_dir):
            print("\n✅ Modello pronto per l'uso!")
        else:
            print("\n❌ Problemi con il modello")
            return 1
    else:
        # Download
        result = download_llama_3_2_3b()
        if result:
            print("\n🎯 Download completato!")
            print("   Puoi ora usare il modello offline")
            
            # Auto-verifica
            if verify_model(result):
                print("\n✅ Modello pronto per l'uso!")
            else:
                print("\n⚠️  Modello scaricato ma verifiche fallite")
                return 1
        else:
            print("\n❌ Download fallito")
            return 1
    
    return 0


if __name__ == "__main__":
    exit(main())