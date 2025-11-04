#!/usr/bin/env python3
"""
Verifica e mostra conversazioni salvate
"""
import json
from pathlib import Path
from datetime import datetime

# Directory conversazioni
conv_dir = Path(__file__).parent / "ai_system" / "training_data" / "conversations"

print("="*70)
print("💾 CONVERSAZIONI SALVATE PER TRAINING")
print("="*70)

if not conv_dir.exists():
    print("\n❌ Nessuna conversazione salvata ancora")
    print("   Le conversazioni verranno salvate dopo aver usato il chatbot")
    exit(0)

# Conta conversazioni per data
date_dirs = sorted([d for d in conv_dir.iterdir() if d.is_dir()], reverse=True)

total_conversations = 0
total_turns = 0

print(f"\n📂 Directory: {conv_dir}\n")

for date_dir in date_dirs:
    conv_files = list(date_dir.glob("*.json"))
    if not conv_files:
        continue
    
    print(f"📅 {date_dir.name}")
    
    for conv_file in conv_files:
        try:
            with open(conv_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            num_turns = len(data.get('turns', []))
            total_conversations += 1
            total_turns += num_turns
            
            timestamp = data.get('timestamp', 'N/A')
            session_id = data.get('session_id', conv_file.stem)
            
            print(f"   • {session_id[:8]}... - {num_turns} scambi - {timestamp[:19]}")
            
        except Exception as e:
            print(f"   ⚠️  Errore lettura {conv_file.name}: {e}")
    
    print()

print("="*70)
print(f"📊 TOTALE:")
print(f"   Conversazioni: {total_conversations}")
print(f"   Scambi totali: {total_turns}")
print("="*70)

if total_turns >= 20:
    print("\n✅ Hai abbastanza dati per il training!")
    print("   Prossimi passi:")
    print("   1. python scripts/4_create_training_dataset.py")
    print("   2. python scripts/5_train_llama_rag.py")
else:
    print(f"\n📈 Continua a chattare! ({total_turns}/20 scambi raccolti)")
    print("   Servono almeno 20 scambi per un training efficace")
