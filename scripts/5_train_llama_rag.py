"""
Training script per Llama RAG Model.
Fine-tuning di Llama pre-addestrato con dataset RAG spirituality.ai

Supporta:
- LoRA/QLoRA per fine-tuning efficiente
- 4-bit/8-bit quantization
- Gradient accumulation
- Mixed precision training
- Tensorboard logging
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import warnings

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import get_linear_schedule_with_warmup
from tqdm import tqdm

# Fix encoding Windows
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

# Local imports
sys.path.append(str(Path(__file__).parent.parent))
from src.models.llama_rag_model import LlamaRAGModel, create_llama_rag_model
from src.config.model_config import get_config

warnings.filterwarnings('ignore')


class RAGTrainingDataset(Dataset):
    """Dataset per fine-tuning Llama con RAG context."""
    
    def __init__(
        self,
        data_path: Path,
        tokenizer,
        max_length: int = 2048,
    ):
        """
        Args:
            data_path: Path al file JSON con training data
            tokenizer: Llama tokenizer
            max_length: Max sequence length
        """
        self.tokenizer = tokenizer
        self.max_length = max_length
        
        # Carica dati
        print(f"📂 Caricamento training data da: {data_path}")
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        print(f"✅ Caricati {len(self.data)} esempi di training")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        """
        Ogni sample ha formato:
        {
            "query": "Domanda utente",
            "context": ["chunk1", "chunk2", ...],
            "response": "Risposta attesa"
        }
        """
        sample = self.data[idx]
        
        # Costruisci prompt (context + query)
        context_text = "\n\n".join([
            f"[Fonte {i+1}]\n{chunk}"
            for i, chunk in enumerate(sample['context'][:5])  # Max 5 chunks
        ])
        
        # Llama 2 chat format
        prompt = (
            f"<s>[INST] <<SYS>>\n"
            f"Sei una guida spirituale esperta. Rispondi basandoti sul contesto fornito.\n"
            f"<</SYS>>\n\n"
            f"Contesto:\n{context_text}\n\n"
            f"Domanda: {sample['query']} [/INST] "
        )
        
        # Response
        response = sample['response'] + " </s>"
        
        # Full text (prompt + response)
        full_text = prompt + response
        
        # Tokenize
        encodings = self.tokenizer(
            full_text,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        
        input_ids = encodings['input_ids'].squeeze(0)
        attention_mask = encodings['attention_mask'].squeeze(0)
        
        # Labels: solo response (prompt masked con -100)
        labels = input_ids.clone()
        
        # Trova dove inizia la response (dopo [/INST])
        prompt_tokens = self.tokenizer(prompt, add_special_tokens=False)['input_ids']
        prompt_length = len(prompt_tokens)
        
        # Mask prompt (no loss su prompt)
        labels[:prompt_length] = -100
        
        # Mask padding
        labels[attention_mask == 0] = -100
        
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }


def train_llama_rag(
    config_name: str = 'llama-qlora',
    train_data_path: Optional[Path] = None,
    val_data_path: Optional[Path] = None,
    output_dir: Optional[Path] = None,
    num_epochs: int = 3,
    batch_size: int = 1,
    gradient_accumulation_steps: int = 16,
    learning_rate: float = 2e-4,
    warmup_steps: int = 100,
    max_grad_norm: float = 1.0,
    save_steps: int = 500,
    eval_steps: int = 100,
    logging_steps: int = 10,
    llama_model_name: Optional[str] = None,
):
    """
    Train Llama RAG model.
    
    Args:
        config_name: 'llama-2-7b', 'llama-3-8b', 'llama-qlora'
        train_data_path: Path training data JSON
        val_data_path: Path validation data JSON
        output_dir: Output directory per checkpoints
        num_epochs: Numero epoch
        batch_size: Batch size (1 per QLoRA)
        gradient_accumulation_steps: Accumulation steps
        learning_rate: Learning rate
        warmup_steps: Warmup steps
        max_grad_norm: Gradient clipping
        save_steps: Save ogni N steps
        eval_steps: Eval ogni N steps
        logging_steps: Log ogni N steps
        llama_model_name: Override model name
    """
    print("\n" + "="*60)
    print("🦙 LLAMA RAG TRAINING")
    print("="*60 + "\n")
    
    # Setup paths
    if train_data_path is None:
        train_data_path = Path(__file__).parent.parent / "ai_system" / "src" / "training" / "training_dataset" / "train_data.json"
    
    if val_data_path is None:
        val_data_path = Path(__file__).parent.parent / "ai_system" / "src" / "training" / "training_dataset" / "validation_data.json"
    
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "ai_system" / "checkpoints" / f"llama_rag_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Training data: {train_data_path}")
    print(f"📂 Validation data: {val_data_path}")
    print(f"📂 Output dir: {output_dir}\n")
    
    # Carica config
    config = get_config(config_name)
    print(f"⚙️  Config: {config_name}")
    print(f"   Batch size: {batch_size}")
    print(f"   Gradient accumulation: {gradient_accumulation_steps}")
    print(f"   Effective batch size: {batch_size * gradient_accumulation_steps}")
    print(f"   Learning rate: {learning_rate}")
    print(f"   Epochs: {num_epochs}\n")
    
    # Crea modello
    print("🦙 Caricamento Llama RAG Model...")
    model = create_llama_rag_model(
        config_name=config_name,
        llama_model_name=llama_model_name,
    )
    
    tokenizer = model.tokenizer
    
    # Crea datasets
    print("\n📚 Caricamento datasets...")
    train_dataset = RAGTrainingDataset(
        data_path=train_data_path,
        tokenizer=tokenizer,
        max_length=config.max_seq_length,
    )
    
    val_dataset = RAGTrainingDataset(
        data_path=val_data_path,
        tokenizer=tokenizer,
        max_length=config.max_seq_length,
    ) if val_data_path.exists() else None
    
    # DataLoaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,  # Windows-friendly
        pin_memory=torch.cuda.is_available(),
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=torch.cuda.is_available(),
    ) if val_dataset else None
    
    # Optimizer (solo parametri trainabili)
    trainable_params = [p for p in model.parameters() if p.requires_grad]
    optimizer = AdamW(trainable_params, lr=learning_rate, weight_decay=0.01)
    
    # Scheduler
    total_steps = len(train_loader) * num_epochs // gradient_accumulation_steps
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps
    )
    
    print(f"\n✅ Setup completato!")
    print(f"   Training steps: {total_steps}")
    print(f"   Warmup steps: {warmup_steps}")
    print(f"   Trainable parameters: {sum(p.numel() for p in trainable_params):,}\n")
    
    # Training loop
    model.train()
    global_step = 0
    best_val_loss = float('inf')
    
    for epoch in range(num_epochs):
        print(f"\n{'='*60}")
        print(f"📊 Epoch {epoch + 1}/{num_epochs}")
        print(f"{'='*60}\n")
        
        epoch_loss = 0
        optimizer.zero_grad()
        
        pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}")
        
        for step, batch in enumerate(pbar):
            # Move to device
            input_ids = batch['input_ids'].to(model.llama.device)
            attention_mask = batch['attention_mask'].to(model.llama.device)
            labels = batch['labels'].to(model.llama.device)
            
            # Forward
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs['loss']
            loss = loss / gradient_accumulation_steps
            
            # Backward
            loss.backward()
            
            epoch_loss += loss.item()
            
            # Update weights ogni gradient_accumulation_steps
            if (step + 1) % gradient_accumulation_steps == 0:
                # Gradient clipping
                torch.nn.utils.clip_grad_norm_(trainable_params, max_grad_norm)
                
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                
                global_step += 1
                
                # Logging
                if global_step % logging_steps == 0:
                    avg_loss = epoch_loss / (step + 1)
                    lr = scheduler.get_last_lr()[0]
                    pbar.set_postfix({
                        'loss': f'{avg_loss:.4f}',
                        'lr': f'{lr:.2e}'
                    })
                
                # Validation
                if val_loader and global_step % eval_steps == 0:
                    val_loss = evaluate(model, val_loader)
                    print(f"\n📊 Step {global_step} | Val Loss: {val_loss:.4f}")
                    
                    # Save best model
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        save_path = output_dir / "best_model"
                        model.save_pretrained(str(save_path))
                        print(f"💾 Best model saved! Val Loss: {val_loss:.4f}\n")
                    
                    model.train()
                
                # Save checkpoint
                if global_step % save_steps == 0:
                    save_path = output_dir / f"checkpoint-{global_step}"
                    model.save_pretrained(str(save_path))
                    print(f"💾 Checkpoint saved at step {global_step}\n")
        
        # End of epoch
        avg_epoch_loss = epoch_loss / len(train_loader)
        print(f"\n✅ Epoch {epoch+1} completato | Avg Loss: {avg_epoch_loss:.4f}")
        
        # Validation at end of epoch
        if val_loader:
            val_loss = evaluate(model, val_loader)
            print(f"📊 Validation Loss: {val_loss:.4f}\n")
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                save_path = output_dir / "best_model"
                model.save_pretrained(str(save_path))
                print(f"💾 Best model saved!\n")
    
    # Final save
    final_save_path = output_dir / "final_model"
    model.save_pretrained(str(final_save_path))
    print(f"\n✅ Training completato!")
    print(f"💾 Modello finale salvato in: {final_save_path}")
    print(f"💾 Best model in: {output_dir / 'best_model'}")
    print(f"📊 Best validation loss: {best_val_loss:.4f}\n")


@torch.no_grad()
def evaluate(model, dataloader):
    """Evaluate model on validation set."""
    model.eval()
    total_loss = 0
    
    for batch in tqdm(dataloader, desc="Validation", leave=False):
        input_ids = batch['input_ids'].to(model.llama.device)
        attention_mask = batch['attention_mask'].to(model.llama.device)
        labels = batch['labels'].to(model.llama.device)
        
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        
        total_loss += outputs['loss'].item()
    
    return total_loss / len(dataloader)


def main():
    parser = argparse.ArgumentParser(description="Train Llama RAG Model")
    
    parser.add_argument(
        '--config',
        type=str,
        default='llama-qlora',
        choices=['llama-2-7b', 'llama-3-8b', 'llama-qlora'],
        help='Config preset'
    )
    parser.add_argument('--train-data', type=str, help='Path training data JSON')
    parser.add_argument('--val-data', type=str, help='Path validation data JSON')
    parser.add_argument('--output-dir', type=str, help='Output directory')
    parser.add_argument('--epochs', type=int, default=3, help='Numero epoch')
    parser.add_argument('--batch-size', type=int, default=1, help='Batch size')
    parser.add_argument('--accumulation-steps', type=int, default=16, help='Gradient accumulation')
    parser.add_argument('--learning-rate', type=float, default=2e-4, help='Learning rate')
    parser.add_argument('--model-name', type=str, help='Llama model name (HuggingFace ID)')
    
    args = parser.parse_args()
    
    train_llama_rag(
        config_name=args.config,
        train_data_path=Path(args.train_data) if args.train_data else None,
        val_data_path=Path(args.val_data) if args.val_data else None,
        output_dir=Path(args.output_dir) if args.output_dir else None,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.accumulation_steps,
        learning_rate=args.learning_rate,
        llama_model_name=args.model_name,
    )


if __name__ == "__main__":
    main()
