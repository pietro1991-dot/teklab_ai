# 🦙 WORKFLOW COMPLETO - SPIRITUALITY AI

## 📋 ORDINE DI ESECUZIONE SCRIPT

Gli script sono numerati per indicare la sequenza corretta di esecuzione.

---

## 🔄 SETUP INIZIALE (UNA VOLTA)

### **1️⃣ Download Modello Llama (OBBLIGATORIO)**
```powershell
python scripts\1_download_llama.py --verify
```
**Cosa fa:**
- Scarica Llama 2 7B da HuggingFace (~13GB)
- Salva in `ai_system/models/Llama-2-7b-chat-hf/`
- Verifica funzionamento modello

**Quando eseguire:**
- ✅ Una volta all'inizio
- ⏭️ Mai più necessario dopo il primo download

**Output atteso:**
```
✅ Modello scaricato: ai_system/models/Llama-2-7b-chat-hf/
✅ Verifica completata: tokenizer e config OK
```

---

## 📚 CREAZIONE KNOWLEDGE BASE

### **2️⃣ Genera Embeddings RAG (Dopo avere chunk)**
```powershell
python scripts\2_generate_embeddings.py
```
**Cosa fa:**
- Legge tutti i chunk da `Fonti/Autori/.../Processati/*/chunks/`
- Genera embeddings vettoriali (384-dim)
- Salva cache in `ai_system/Embedding/embeddings_cache.pkl`

**Quando eseguire:**
- ✅ Dopo aver creato nuovi chunk (manualmente o con script 3)
- ✅ Ogni volta che aggiungi nuove trascrizioni processate
- ⏭️ Non serve se non hai modificato i chunk

**Output atteso:**
```
📚 Caricamento dati da Fonti...
✅ Trovate 1 fonti
📊 DATI CARICATI:
   • Capitoli: 60
   • Chunks: 450
🧠 Codifica 450 testi...
💾 Cache salvata (12.3 MB)
```

---

### **3️⃣ Crea Chunk con Llama (OPZIONALE - Automatizzazione)**
```powershell
# Esempio: crea chunk per Day 50-55
python scripts\3_create_chunks_with_llama.py --range 50 55

# Oppure singolo giorno
python scripts\3_create_chunks_with_llama.py --days 100

# Test con pochi chunk
python scripts\3_create_chunks_with_llama.py --days 50 --max-chunks 3
```
**Cosa fa:**
- Legge trascrizioni originali da `Fonti/.../Originali/Pyramid.mathias/Day_X_Transcript.txt`
- Usa Llama per generare automaticamente:
  - Metadata (titoli, concetti, keywords)
  - Domande e risposte spirituali
  - Quote iconiche, formulas
- Salva chunk JSON in `Fonti/.../Processati/Pyramid Course/chunks/dayXX/`

**Quando eseguire:**
- ✅ Quando vuoi processare nuove trascrizioni automaticamente
- ✅ Alternativa alla creazione manuale con Copilot
- ⏭️ Non necessario se hai già chunk manuali

**Note:**
- Usa automaticamente ultimo modello fine-tunato (se disponibile)
- Altrimenti usa Llama base pre-addestrato

**Output atteso:**
```
🦙 Inizializzazione Chunk Creator con Llama...
✅ Modello FINE-TUNATO caricato
   Checkpoint: ai_system/checkpoints/llama_rag_20251030/best_model/
📄 Processamento: Day 50
   📦 Sezioni create: 5
   🤖 Generazione chunk con Llama...
✅ Day 50 completato: 5 chunk creati
```

---

## 🎓 TRAINING E MIGLIORAMENTO MODELLO

### **4️⃣ Crea Dataset Training (Ogni settimana/mese)**
```powershell
python scripts\4_create_training_dataset.py
```
**Cosa fa:**
- Carica conversazioni utenti da `ai_system/training_data/conversations/`
- Carica chunk RAG da `Fonti/.../chunks/`
- Crea campioni sintetici se poche conversazioni (<50)
- Split 80/10/10 (train/val/test)
- Salva in `ai_system/src/training/training_dataset/`

**Quando eseguire:**
- ✅ Dopo aver raccolto 20+ conversazioni utenti
- ✅ Ogni settimana per aggiornare dataset
- ✅ Prima di ogni fine-tuning (script 5)

**Output atteso:**
```
📚 Caricamento conversazioni...
✅ Conversazioni caricate: 45
📖 Caricamento chunk RAG...
✅ Chunk caricati: 450
📊 DATASET CREATO:
   • Train: 480 samples
   • Val: 60 samples
   • Test: 60 samples
💾 Salvato in: ai_system/src/training/training_dataset/
```

---

### **5️⃣ Fine-Tuning Llama (Training)**
```powershell
# Training completo (3 epoch)
python scripts\5_train_llama_rag.py --config llama-qlora --epochs 3

# Update veloce (2 epoch)
python scripts\5_train_llama_rag.py --config llama-qlora --epochs 2

# Training con più VRAM
python scripts\5_train_llama_rag.py --config llama-2-7b --epochs 3
```
**Cosa fa:**
- Carica Llama base (o ultimo checkpoint)
- Fine-tuning LoRA/QLoRA su dataset training
- Salva checkpoint in `ai_system/checkpoints/llama_rag_YYYYMMDD/`
- Early stopping se loss non migliora

**Quando eseguire:**
- ✅ Dopo aver creato/aggiornato dataset (script 4)
- ✅ Prima volta: 3 epoch (training completo)
- ✅ Aggiornamenti: 2 epoch (fine-tuning incrementale)

**Requisiti:**
- GPU con 6GB+ VRAM (config `llama-qlora`)
- GPU con 16GB+ VRAM (config `llama-2-7b`)
- Tempo: 1-3 ore

**Output atteso:**
```
🦙 Caricamento modello Llama...
✅ Modello caricato: Llama-2-7b-chat-hf
📊 Dataset caricato: 480 train, 60 val
🎓 Inizio training (3 epoch)...

Epoch 1/3:
  Train Loss: 1.234
  Val Loss: 1.156

Epoch 2/3:
  Train Loss: 0.987
  Val Loss: 0.945

Epoch 3/3:
  Train Loss: 0.876
  Val Loss: 0.912

✅ Training completato!
💾 Best model salvato: ai_system/checkpoints/llama_rag_20251030/best_model/
```

---

## 🤖 USO CHATBOT

### **6️⃣ Chatbot con Llama**
```powershell
python scripts\6_chatbot.py
```
**Cosa fa:**
- Carica embeddings RAG (`2_generate_embeddings.py`)
- Carica Llama:
  - ✅ Ultimo checkpoint fine-tunato (se disponibile)
  - ✅ Modello base altrimenti
- Conversazione interattiva
- Salva conversazioni in `ai_system/training_data/conversations/`

**Auto-detection modello:**
- Script cerca automaticamente in `ai_system/checkpoints/llama_rag_*/`
- Usa checkpoint più recente
- Messaggio indica quale modello è in uso

---

## 📊 WORKFLOW COMPLETO

### **Setup Iniziale (Una volta):**
```powershell
# 1. Download Llama (obbligatorio)
python scripts\1_download_llama.py --verify

# 2. Genera embeddings (se hai chunk pronti)
python scripts\2_generate_embeddings.py
```

### **Primo Fine-Tuning:**
```powershell
# 3. (Opzionale) Crea chunk automatici
python scripts\3_create_chunks_with_llama.py --range 1 10

# 4. Rigenera embeddings se hai creato nuovi chunk
python scripts\2_generate_embeddings.py

# 5. Usa chatbot per 20+ conversazioni
python scripts\6_chatbot.py

# 6. Crea dataset da conversazioni
python scripts\4_create_training_dataset.py

# 7. Fine-tuning (3 epoch)
python scripts\5_train_llama_rag.py --config llama-qlora --epochs 3
```

### **Ciclo di Miglioramento Continuo (Settimanale/Mensile):**
```powershell
# 1. Usa chatbot normalmente (salva conversazioni automaticamente)
python scripts\6_chatbot.py

# 2. Ogni 20-30 nuove conversazioni, rigenera dataset
python scripts\4_create_training_dataset.py

# 3. Fine-tuning incrementale (2 epoch)
python scripts\5_train_llama_rag.py --config llama-qlora --epochs 2

# Il chatbot userà automaticamente il nuovo checkpoint
```

---

## 🗂️ STRUTTURA FILE DOPO SETUP

```
spirituality.ai/
├── scripts/                              # ← TUTTI GLI SCRIPT QUI
│   ├── 1_download_llama.py              # ← Setup iniziale
│   ├── 2_generate_embeddings.py         # ← Genera embeddings RAG
│   ├── 3_create_chunks_with_llama.py    # ← Automatizzazione chunk
│   ├── 4_create_training_dataset.py     # ← Prepara dati training
│   ├── 5_train_llama_rag.py             # ← Fine-tuning
│   └── 6_chatbot.py                     # ← Chatbot principale
│
├── ai_system/
│   ├── Embedding/
│   │   └── embeddings_cache.pkl         # ← Cache vettori
│   │
│   ├── src/
│   │   └── training/
│   │       └── training_dataset/        # ← Dataset generato
│   │           ├── train_data.json
│   │           ├── val_data.json
│   │           └── test_data.json
│   │
│   ├── models/
│   │   └── Llama-2-7b-chat-hf/          # ← Modello base (da script 1)
│   │
│   ├── checkpoints/
│   │   ├── llama_rag_20251030/          # ← Primo fine-tuning
│   │   │   └── best_model/
│   │   └── llama_rag_20251107/          # ← Secondo fine-tuning
│   │       └── best_model/
│   │
│   └── training_data/
│       └── conversations/                # ← Conversazioni salvate
│           └── 2025-10-30/
│
├── BOT/
│   └── chatbot.py                       # ← Core chatbot (usato da script 6)
│
└── Fonti/
    └── Autori/
        └── Mathias de Stefano/
            ├── Originali/
            │   └── Pyramid.mathias/      # ← Trascrizioni grezze
            │       ├── Day_1_Transcript.txt
            │       └── ...
            │
            └── Processati/
                └── Pyramid Course/       # ← Chunk processati
                    ├── chunks/
                    │   ├── day01/
                    │   │   ├── day01_chunk_001_tema.json
                    │   │   └── ...
                    │   └── day02/
                    └── metadata/
```

---

## ⚙️ CONFIGURAZIONI MODELLO

```powershell
# QLoRA (6GB VRAM) - Consigliato
--config llama-qlora

# Llama 2 (16GB VRAM) - Più veloce ma più VRAM
--config llama-2-7b

# Llama 3 (16GB VRAM) - Modello più recente
--config llama-3-8b
```

---

## 🆘 TROUBLESHOOTING

### **Errore: CUDA out of memory**
```powershell
# Usa QLoRA invece di full precision
--config llama-qlora

# Riduci batch size (modifica model_config.py)
batch_size = 1
gradient_accumulation_steps = 16
```

### **Errore: Model not found**
```powershell
# Assicurati di aver eseguito script 1
python scripts\1_download_llama.py --verify
```

### **Chatbot usa modello base invece di fine-tunato**
```powershell
# Verifica esistenza checkpoint
dir ai_system\checkpoints\llama_rag_*\best_model

# Se non esiste, esegui training
python scripts\5_train_llama_rag.py --config llama-qlora --epochs 3
```

---

## 📈 METRICHE DI SUCCESSO

**Primo Fine-Tuning:**
- Loss finale < 1.0
- Val Loss stabile (non aumenta)
- Chatbot risponde in modo coerente

**Miglioramento Continuo:**
- Loss diminuisce ad ogni training
- Risposte più pertinenti e contestuali
- Meno allucinazioni/errori

---

## 💡 BEST PRACTICES

1. **Prima volta:** Usa 3 epoch per training completo
2. **Aggiornamenti:** Usa 2 epoch per fine-tuning incrementale
3. **Raccogli 20-30 conversazioni** prima di ogni training update
4. **Rigenera embeddings** ogni volta che crei nuovi chunk
5. **Backup checkpoint** importanti (copia cartella `checkpoints/`)
6. **Monitora loss:** se aumenta, riduci learning rate

---

## 🎯 QUICK START

**Setup completo in 3 comandi:**
```powershell
# 1. Download Llama
python scripts\1_download_llama.py --verify

# 2. Genera embeddings
python scripts\2_generate_embeddings.py

# 3. Avvia chatbot
python scripts\6_chatbot.py
```

**Dopo 20+ conversazioni, migliora il modello:**
```powershell
# 4. Crea dataset
python scripts\4_create_training_dataset.py

# 5. Fine-tuning
python scripts\5_train_llama_rag.py --config llama-qlora --epochs 3
```

---

✅ **Sistema pronto!** Ora hai un workflow chiaro e numerato per ogni operazione.
