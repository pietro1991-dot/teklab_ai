"""
Script per scaricare Llama da HuggingFace e salvarlo in locale.
Esegui questo script UNA VOLTA per scaricare il modello.
Poi puoi usare il modello offline senza dipendere da HuggingFace.
"""

import os
import sys
from pathlib import Path
import argparse
from transformers import BitsAndBytesConfig
import torch

# Fix encoding Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from huggingface_hub import snapshot_download
except ImportError:
    print("❌ transformers non installato!")
    print("   Installa con: pip install transformers huggingface-hub")
    sys.exit(1)


def download_llama_model(
    model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    local_dir: Path = None,
    token: str = None,
    quantization: bool = False
):
    """
    Scarica modello Llama da HuggingFace e salva in locale.
    
    Args:
        model_name: Nome modello HuggingFace (default: TinyLlama 1.1B Chat - COMPLETAMENTE LIBERO)
        local_dir: Directory locale dove salvare (default: ai_system/models/MODEL_NAME)
        token: HuggingFace token (opzionale, NON necessario per TinyLlama)
    """
    print("\n" + "="*60)
    print("🦙 DOWNLOAD LLAMA MODEL IN LOCALE")
    print("="*60 + "\n")
    
    # Default local directory
    if local_dir is None:
        project_root = Path(__file__).parent.parent
        model_folder = model_name.split('/')[-1]  # es: "Llama-2-7b-chat-hf"
        local_dir = project_root / "ai_system" / "models" / model_folder
    
    local_dir = Path(local_dir)
    local_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Modello: {model_name}")
    print(f"💾 Destinazione: {local_dir}")
    
    # Check if model requires authentication
    is_gated = model_name.startswith("meta-llama/")
    
    if is_gated:
        print("\n⚠️  ATTENZIONE - Modello Meta Llama con accesso limitato:")
        print("   • Richiede accettazione della license Meta Llama")
        print(f"   • Vai su: https://huggingface.co/{model_name}")
        print("   • Clicca 'Request Access' e attendi approvazione")
        print("   • Fai login: huggingface-cli login")
    else:
        print("\n✅ Modello OPEN ACCESS - Nessun token richiesto!")
        print("   • Download diretto senza autenticazione")
        print(f"   • Modello: {model_name}")
    print()
    
    # Controlla se già scaricato
    if (local_dir / "config.json").exists():
        print(f"✅ Modello già scaricato in: {local_dir}")
        risposta = input("\n🔄 Vuoi ri-scaricare? (s/n): ").strip().lower()
        if risposta not in ['s', 'si', 'y', 'yes']:
            print("⏭️  Download saltato")
            return local_dir
    
    print("🚀 Inizio download...")
    print("   (Questo richiederà 5-10 minuti e ~2.2GB di spazio per TinyLlama)\n")
    
    try:
        # Metodo 1: Usa snapshot_download (più veloce, scarica tutti i file)
        print("📥 Download con snapshot_download...")
        snapshot_download(
            repo_id=model_name,
            local_dir=str(local_dir),
            token=token,
            ignore_patterns=["*.msgpack", "*.h5", "*.ot"],  # Skip file non necessari
        )
        
        print("✅ Download completato!")
        print("   Prova a ri-eseguire lo script")
        
        # Verifica file essenziali
        required_files = ["config.json", "tokenizer_config.json"]
        missing = [f for f in required_files if not (local_dir / f).exists()]
        
        if missing:
            print(f"\n⚠️  File mancanti: {missing}")
            print("   Prova a ri-eseguire lo script")
        else:
            print("✅ Tutti i file essenziali presenti")
            
            # Mostra dimensione totale
            total_size = sum(f.stat().st_size for f in local_dir.rglob('*') if f.is_file())
            total_size_gb = total_size / (1024**3)
            print(f"💾 Dimensione totale: {total_size_gb:.2f} GB")
        
        # Quantizzazione 4-bit con bitsandbytes
        if quantization:
            print("⚙️  Abilitazione quantizzazione 4-bit con bitsandbytes...")
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
            model.save_pretrained(local_dir)
            print("✅ Modello quantizzato salvato in:", local_dir)
            return local_dir
        
        return local_dir
        
    except Exception as e:
        print(f"\n❌ Errore durante download: {e}")
        print("💡 Possibili soluzioni:")
        print("   1. Verifica di aver accettato la license Llama")
        print("   2. Fai login: huggingface-cli login")
        print("   3. Controlla connessione internet")
        print("   4. Verifica spazio su disco (serve ~13GB)")
        return None


def verify_model(local_dir: Path):
    """Verifica che il modello locale funzioni."""
    print(f"\n🧪 Test caricamento modello da: {local_dir}")
    
    try:
        # Prova a caricare tokenizer
        print("📦 Caricamento tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(str(local_dir))
        print(f"✅ Tokenizer OK (vocab size: {len(tokenizer)})")
        
        # Test tokenization
        test_text = "Ciao, come stai?"
        tokens = tokenizer.encode(test_text)
        print(f"✅ Test tokenization OK ({len(tokens)} token)")
        
        # Prova a caricare model config (senza caricare pesi - troppo lento)
        print("📦 Verifica config modello...")
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained(str(local_dir))
        print("✅ Config OK:")
        print(f"   • Hidden size: {config.hidden_size}")
        print(f"   • Num layers: {config.num_hidden_layers}")
        print(f"   • Vocab size: {config.vocab_size}")
        
        print(f"\n✅ Modello locale pronto per l'uso!")
        print(f"\n💡 Per usarlo nel chatbot, specifica il path:")
        print(f"   LlamaRAGWrapper(llama_model_name='{local_dir}')")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore test: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Scarica Llama da HuggingFace in locale")
    
    parser.add_argument(
        '--model',
        type=str,
        default='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        help='Nome modello HuggingFace (default: TinyLlama 1.1B Chat - NO TOKEN)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory output (default: ai_system/models/MODEL_NAME)'
    )
    parser.add_argument(
        '--token',
        type=str,
        help='HuggingFace token (opzionale se hai fatto login)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verifica modello dopo download'
    )
    parser.add_argument(
        '--quantization',
        action='store_true',
        help='Abilita quantizzazione 4-bit con bitsandbytes'
    )
    
    args = parser.parse_args()
    
    # Download
    local_dir = download_llama_model(
        model_name=args.model,
        local_dir=Path(args.output_dir) if args.output_dir else None,
        token=args.token,
        quantization=args.quantization
    )
    
    if local_dir and args.verify:
        verify_model(local_dir)
    
    print("\n" + "="*60)
    print("✅ COMPLETATO!")
    print("="*60)
    print(f"\n💡 Prossimi passi:")
    print(f"   1. Usa il modello locale nel wrapper:")
    print(f"      LlamaRAGWrapper(llama_model_name='{local_dir}')")
    print(f"   2. Fine-tuna con i tuoi dati:")
    print(f"      python src/training/train_llama_rag.py --model-name '{local_dir}'\n")


if __name__ == "__main__":
    main()
