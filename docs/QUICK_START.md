# 🚀 QUICK START - 3 Comandi per Iniziare

## Setup Iniziale (Con Internet - Una Volta)

```powershell
# 1. Installa dipendenze
pip install -r BOT/requirements.txt

# 2. Login HuggingFace (per license Llama)
huggingface-cli login

# 3. Download Llama (13GB, 10-30 min)
python scripts/1_download_llama.py --verify

# 4. Genera embeddings RAG (1-3 min)
python scripts/2_generate_embeddings.py
```

---

## Usa Chatbot (100% Offline)

```powershell
python scripts/6_chatbot.py
```

**Prima volta mostra:**
```
✅ Modello BASE pre-addestrato caricato
   (Nessun fine-tuning trovato - usa modello vanilla)
```

---

## Miglioramento Continuo

### Dopo 20+ Conversazioni:

```powershell
# Crea dataset da conversazioni
python scripts/4_create_training_dataset.py

# Fine-tuning (1-3 ore)
python scripts/5_train_llama_rag.py --config llama-qlora --epochs 3
```

### Prossimo Avvio Chatbot:

```
✅ Modello FINE-TUNATO caricato
   Checkpoint: llama_rag_20251031/best_model/
```

---

## Update Settimanali

```powershell
# Rigenera dataset (nuove conversazioni)
python scripts/4_create_training_dataset.py

# Fine-tuning veloce (2 epoch)
python scripts/5_train_llama_rag.py --config llama-qlora --epochs 2
```

---

## 💡 Tips

- **GPU 6GB+** necessaria per training
- **Dopo setup iniziale → 100% OFFLINE**
- **Auto-detection** ultimo checkpoint
- **Conversazioni salvate** automaticamente

---

Leggi `README.md` per documentazione completa!
