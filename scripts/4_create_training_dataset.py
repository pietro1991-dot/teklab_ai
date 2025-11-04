"""
Converti conversazioni utenti salvate in formato training per Llama.
Combina chunks RAG + conversazioni reali per fine-tuning personalizzato.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

# Fix encoding Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')


def load_conversations(conversations_dir: Path) -> List[Dict[str, Any]]:
    """Carica tutte le conversazioni salvate dagli utenti."""
    print(f"📂 Caricamento conversazioni da: {conversations_dir}")
    
    conversations = []
    
    if not conversations_dir.exists():
        print(f"⚠️  Directory non trovata: {conversations_dir}")
        return conversations
    
    # Carica da tutte le date
    for date_dir in conversations_dir.iterdir():
        if not date_dir.is_dir():
            continue
        
        print(f"   📅 {date_dir.name}")
        
        # Carica aggregate file (contiene tutte le conversazioni del giorno)
        aggregate_file = date_dir / "daily_aggregate.jsonl"
        if aggregate_file.exists():
            with open(aggregate_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        conv = json.loads(line)
                        conversations.append(conv)
        
        # Fallback: carica file individuali
        else:
            for conv_file in date_dir.glob("*.json"):
                if conv_file.name == "daily_aggregate.json":
                    continue
                try:
                    with open(conv_file, 'r', encoding='utf-8') as f:
                        conv = json.load(f)
                        conversations.append(conv)
                except Exception as e:
                    print(f"      ⚠️  Errore caricamento {conv_file.name}: {e}")
    
    print(f"\n✅ Caricate {len(conversations)} conversazioni\n")
    return conversations


def extract_training_samples(conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Estrai sample di training dalle conversazioni.
    Formato output: {"query": "...", "context": [...], "response": "..."}
    """
    print("🔄 Estrazione training samples...")
    
    samples = []
    
    for conv in conversations:
        turns = conv.get('turns', [])
        
        for turn in turns:
            user_query = turn.get('user_query', '')
            assistant_response = turn.get('assistant_response', '')
            retrieved_chunks = turn.get('retrieved_chunks', [])
            
            if not user_query or not assistant_response:
                continue
            
            # Estrai context dai chunks
            context = []
            for chunk in retrieved_chunks[:5]:  # Max 5 chunks
                content = chunk.get('content', '')
                if content:
                    context.append(content)
            
            # Crea sample
            sample = {
                "query": user_query,
                "context": context,
                "response": assistant_response,
                "metadata": {
                    "session_id": conv.get('session_id', ''),
                    "timestamp": turn.get('timestamp', ''),
                    "model_used": turn.get('model_name', ''),
                    "source": "user_conversation"
                }
            }
            
            samples.append(sample)
    
    print(f"✅ Estratti {len(samples)} training samples\n")
    return samples


def load_rag_chunks(fonti_dir: Path) -> List[Dict[str, Any]]:
    """Carica chunks RAG esistenti per creare sample sintetici."""
    print(f"📂 Caricamento chunks RAG da: {fonti_dir}")
    
    chunks = []
    
    if not fonti_dir.exists():
        print(f"⚠️  Directory non trovata: {fonti_dir}")
        return chunks
    
    # Cerca tutti i file chunks
    for chunk_file in fonti_dir.rglob("*chunk*.json"):
        try:
            with open(chunk_file, 'r', encoding='utf-8') as f:
                chunk_data = json.load(f)
                
                # Estrai testo
                testo = chunk_data.get("testo", "")
                if not testo and "messages" in chunk_data:
                    messages = chunk_data.get("messages", [])
                    testo = " ".join([m.get("content", "") for m in messages if m.get("role") == "system"])
                
                if testo:
                    chunks.append({
                        "testo": testo,
                        "keywords": chunk_data.get("keywords", []) or chunk_data.get("metadata", {}).get("keywords_primarie", []),
                        "metadata": chunk_data.get("metadata", {})
                    })
        except Exception as e:
            pass
    
    print(f"✅ Caricati {len(chunks)} chunks RAG\n")
    return chunks


def create_synthetic_samples_from_chunks(chunks: List[Dict[str, Any]], num_samples: int = 100) -> List[Dict[str, Any]]:
    """Crea sample sintetici dai chunks RAG usando keywords."""
    print(f"🎲 Creazione {num_samples} sample sintetici da chunks RAG...")
    
    import random
    samples = []
    
    # Template domande generiche
    question_templates = [
        "Cosa significa {keyword}?",
        "Spiegami il concetto di {keyword}",
        "Come si pratica la {keyword}?",
        "Quali sono i benefici della {keyword}?",
        "Parlami di {keyword}",
        "In che modo la {keyword} aiuta nella crescita spirituale?",
    ]
    
    for _ in range(num_samples):
        if not chunks:
            break
        
        # Scegli chunk random
        chunk = random.choice(chunks)
        keywords = chunk.get("keywords", [])
        
        if not keywords:
            continue
        
        # Scegli keyword random
        keyword = random.choice(keywords).lower()
        
        # Genera domanda
        template = random.choice(question_templates)
        query = template.format(keyword=keyword)
        
        # Usa chunk come context e response
        sample = {
            "query": query,
            "context": [chunk["testo"]],
            "response": chunk["testo"],  # Usa il chunk stesso come risposta base
            "metadata": {
                "source": "synthetic_from_rag",
                "keyword": keyword
            }
        }
        
        samples.append(sample)
    
    print(f"✅ Creati {len(samples)} sample sintetici\n")
    return samples


def merge_and_split_dataset(
    user_samples: List[Dict[str, Any]],
    synthetic_samples: List[Dict[str, Any]],
    train_ratio: float = 0.8,
    val_ratio: float = 0.1
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Combina sample utenti + sintetici e splitta in train/val/test.
    """
    print("🔀 Merge e split dataset...")
    
    import random
    
    # Merge
    all_samples = user_samples + synthetic_samples
    random.shuffle(all_samples)
    
    total = len(all_samples)
    train_size = int(total * train_ratio)
    val_size = int(total * val_ratio)
    
    dataset = {
        "train": all_samples[:train_size],
        "validation": all_samples[train_size:train_size + val_size],
        "test": all_samples[train_size + val_size:]
    }
    
    print(f"✅ Dataset split:")
    print(f"   • Train: {len(dataset['train'])} samples")
    print(f"   • Validation: {len(dataset['validation'])} samples")
    print(f"   • Test: {len(dataset['test'])} samples")
    print(f"   • Total: {total} samples\n")
    
    return dataset


def save_dataset(dataset: Dict[str, List[Dict[str, Any]]], output_dir: Path):
    """Salva dataset in formato JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Salvataggio dataset in: {output_dir}")
    
    for split_name, samples in dataset.items():
        output_file = output_dir / f"{split_name}_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(samples, f, indent=2, ensure_ascii=False)
        print(f"   ✅ {output_file.name} ({len(samples)} samples)")
    
    # Salva stats
    stats = {
        "total_samples": sum(len(samples) for samples in dataset.values()),
        "splits": {name: len(samples) for name, samples in dataset.items()},
        "created_at": datetime.now().isoformat()
    }
    
    stats_file = output_dir / "dataset_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    print(f"   ✅ {stats_file.name}\n")


def main():
    print("\n" + "="*60)
    print("📊 CREAZIONE DATASET TRAINING DA CONVERSAZIONI + RAG")
    print("="*60 + "\n")
    
    # Paths
    project_root = Path(__file__).parent.parent
    conversations_dir = project_root / "ai_system" / "training_data" / "conversations"
    fonti_dir = project_root / "Fonti"
    output_dir = project_root / "ai_system" / "src" / "training" / "training_dataset"
    
    # 1. Carica conversazioni utenti
    conversations = load_conversations(conversations_dir)
    user_samples = extract_training_samples(conversations)
    
    # 2. Carica chunks RAG
    rag_chunks = load_rag_chunks(fonti_dir)
    
    # 3. Crea sample sintetici (solo se pochi dati utenti)
    if len(user_samples) < 50:
        print(f"⚠️  Pochi sample utenti ({len(user_samples)}), creo sample sintetici...\n")
        synthetic_samples = create_synthetic_samples_from_chunks(rag_chunks, num_samples=200)
    else:
        print(f"✅ Sufficienti sample utenti ({len(user_samples)}), skip sintetici\n")
        synthetic_samples = []
    
    # 4. Merge e split
    dataset = merge_and_split_dataset(user_samples, synthetic_samples)
    
    # 5. Salva
    save_dataset(dataset, output_dir)
    
    print("="*60)
    print("✅ DATASET CREATO!")
    print("="*60)
    print(f"\n💡 Prossimi passi:")
    print(f"   1. Verifica dataset: {output_dir}")
    print(f"   2. Avvia training: python src/training/train_llama_rag.py")
    print(f"   3. Il modello imparerà dalle conversazioni reali degli utenti!\n")


if __name__ == "__main__":
    main()
