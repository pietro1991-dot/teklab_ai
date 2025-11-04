# 🏠 Guida: Llama in Locale + Training con Conversazioni Utenti

Questa guida spiega come:
1. **Scaricare Llama in locale** (funziona offline)
2. **Fine-tunare con chunks RAG + conversazioni utenti reali**

---

## 🎯 Workflow Completo

```
1. Download Llama → 2. Usa in locale → 3. Raccogli conversazioni → 4. Fine-tuning → 5. Migliora nel tempo
```

---

## 1️⃣ Scaricare Llama in Locale (UNA VOLTA)

### Step 1: Login HuggingFace

```bash
# Installa CLI
pip install huggingface-hub

# Login (serve token da: https://huggingface.co/settings/tokens)
huggingface-cli login
```

### Step 2: Accetta License Llama

Vai su https://huggingface.co/meta-llama/Llama-2-7b-chat-hf e clicca **"Request Access"**

### Step 3: Scarica Modello

```bash
cd ai_system

# Scarica Llama 2 7B chat (default - ~13GB)
python download_llama.py

# Oppure Llama 3 8B
python download_llama.py --model meta-llama/Meta-Llama-3-8B-Instruct

# Con verifica automatica
python download_llama.py --verify
```

**Tempo stimato**: 10-30 minuti (dipende da connessione)  
**Spazio richiesto**: ~13GB per Llama 2 7B

### Step 4: Verifica Download

```bash
# Controlla che esista
dir ai_system\models\Llama-2-7b-chat-hf

# Dovresti vedere:
# - config.json
# - tokenizer_config.json
# - pytorch_model-*.bin (o model.safetensors)
```

✅ **Ora il modello è LOCALE e funziona OFFLINE!**

---

## 2️⃣ Usare Llama Locale nel Chatbot

Il sistema **rileva automaticamente** il modello locale:

```bash
# Avvia chatbot (usa automaticamente modello locale se disponibile)
python BOT\chatbot_llama.py
```

Output atteso:
```
✅ Uso modello LOCALE: ai_system/models/Llama-2-7b-chat-hf
🦙 Caricamento Llama RAG Model...
```

**Nessuna connessione internet richiesta dopo download!**

---

## 3️⃣ Raccogliere Conversazioni Utenti

Il chatbot **salva automaticamente** tutte le conversazioni in:
```
ai_system/training_data/conversations/YYYY-MM-DD/
```

Ogni conversazione include:
- Query utente
- Risposta assistente
- Chunks RAG usati
- Timestamp
- Modello usato

**Non fare nulla, succede automaticamente mentre usi il chatbot!**

---

## 4️⃣ Creare Dataset da Conversazioni + RAG

Quando hai raccolto abbastanza conversazioni (>10), crea il training dataset:

```bash
cd ai_system

# Crea dataset combinando:
# - Conversazioni utenti reali
# - Chunks RAG esistenti
python src\training\create_training_dataset.py
```

Questo script:
1. ✅ Carica **tutte le conversazioni salvate**
2. ✅ Carica **chunks RAG dalle Fonti**
3. ✅ Crea sample sintetici (se pochi dati utenti)
4. ✅ Split in train/validation/test (80/10/10)
5. ✅ Salva in `src/training/training_dataset/`

Output:
```
✅ Dataset creato!
   • Train: 150 samples
   • Validation: 20 samples
   • Test: 20 samples
```

---

## 5️⃣ Fine-Tuning con Dati Reali

Ora fine-tuna Llama con il dataset personalizzato:

```bash
cd ai_system

# Training QLoRA (GPU 6GB+)
python src\training\train_llama_rag.py --config llama-qlora --epochs 3

# Oppure specifica modello locale
python src\training\train_llama_rag.py --model-name "ai_system/models/Llama-2-7b-chat-hf" --epochs 5
```

**Cosa impara Llama:**
- ✅ Come rispondere alle **domande reali** degli utenti
- ✅ Stile e tono dalle **risposte salvate**
- ✅ Uso dei **chunks RAG specifici** del tuo dominio
- ✅ Pattern conversazionali **personalizzati**

**Tempo**: 1-3 ore (dipende da GPU e dataset size)

---

## 6️⃣ Miglioramento Continuo

### Workflow Iterativo

```
Usa chatbot → Conversazioni salvate → Rigenera dataset → Fine-tune → Chatbot migliorato → Ripeti
```

### Ogni N giorni:

```bash
# 1. Rigenera dataset (include nuove conversazioni)
python src\training\create_training_dataset.py

# 2. Fine-tune con dati aggiornati
python src\training\train_llama_rag.py --config llama-qlora --epochs 2

# 3. Chatbot usa automaticamente ultimo checkpoint
python BOT\chatbot_llama.py
```

---

## 📊 Vantaggi Sistema Locale + Conversazioni

| Feature | Beneficio |
|---------|-----------|
| 🏠 **Modello locale** | Funziona offline, nessun costo API |
| 💬 **Conversazioni reali** | Impara da interazioni vere degli utenti |
| 🎯 **Fine-tuning personalizzato** | Si adatta al tuo dominio specifico |
| 🔄 **Miglioramento continuo** | Più usi il chatbot, più diventa bravo |
| 📈 **Apprendimento incrementale** | Ogni sessione migliora il modello |

---

## 🔧 Esempi Pratici

### Esempio 1: Setup Completo da Zero

```bash
# 1. Download Llama
cd ai_system
python download_llama.py --verify

# 2. Usa chatbot e fai 20+ conversazioni
cd ..
python BOT\chatbot_llama.py

# 3. Crea dataset
cd ai_system
python src\training\create_training_dataset.py

# 4. Fine-tune
python src\training\train_llama_rag.py --config llama-qlora --epochs 3

# 5. Usa modello migliorato
cd ..
python BOT\chatbot_llama.py
```

### Esempio 2: Update Settimanale

```bash
# Ogni lunedì, aggiorna il modello con nuove conversazioni
cd ai_system

# Rigenera dataset (include conversazioni della settimana)
python src\training\create_training_dataset.py

# Fine-tune veloce (2 epoch sufficienti per update)
python src\training\train_llama_rag.py --config llama-qlora --epochs 2

# Test
cd ..
python BOT\chatbot_llama.py
```

---

## 📁 Struttura File

```
spirituality.ai/
├── ai_system/
│   ├── models/                          # Modelli Llama locali
│   │   └── Llama-2-7b-chat-hf/         # Scaricato da HuggingFace
│   │       ├── config.json
│   │       ├── tokenizer_config.json
│   │       └── pytorch_model*.bin
│   ├── training_data/
│   │   └── conversations/               # Conversazioni salvate automaticamente
│   │       └── 2025-10-30/
│   │           ├── session1.json
│   │           ├── session2.json
│   │           └── daily_aggregate.jsonl
│   ├── src/training/
│   │   ├── create_training_dataset.py   # Genera dataset da conversazioni
│   │   ├── train_llama_rag.py          # Training script
│   │   └── training_dataset/            # Dataset generato
│   │       ├── train_data.json
│   │       ├── validation_data.json
│   │       └── test_data.json
│   ├── checkpoints/                     # Modelli fine-tunati
│   │   └── llama_rag_20251030/
│   │       └── best_model/              # Usato automaticamente
│   └── download_llama.py                # Script download
└── BOT/
    └── chatbot_llama.py                 # Entry point
```

---

## 🎓 Best Practices

### ✅ DO

- **Usa modello locale** dopo primo download (funziona offline)
- **Fai molte conversazioni** prima di fine-tunare (minimo 20-30)
- **Fine-tuna regolarmente** (es. ogni settimana) con nuove conversazioni
- **Usa QLoRA** per risparmiare VRAM (funziona su GPU 6GB)
- **Monitora quality** delle risposte e ri-fine-tuna se necessario

### ❌ DON'T

- Non fine-tunare con <10 conversazioni (troppo pochi dati)
- Non usare sempre HuggingFace online (scarica una volta, poi locale)
- Non cancellare cartella `training_data/conversations/` (contiene dati preziosi!)
- Non fare over-fitting (max 3-5 epoch per update)

---

## 🔍 Monitoring Quality

### Controlla miglioramenti nel tempo

```bash
# Visualizza statistiche conversazioni
python ai_system\src\training\analyze_conversations.py

# Output:
# Total conversations: 150
# Average response length: 250 words
# Most common topics: meditazione (45), chakra (30), ...
```

### Test qualità modello

Fai le stesse domande prima e dopo fine-tuning:
```python
# Prima del fine-tuning
"Cos'è la meditazione?"
→ Risposta generica

# Dopo fine-tuning con conversazioni
"Cos'è la meditazione?"
→ Risposta personalizzata con terminologia specifica dei tuoi chunks
```

---

## 🆘 Troubleshooting

### ❌ "Model not found in local directory"
```bash
# Scarica modello
python ai_system\download_llama.py --verify
```

### ❌ "No conversations found"
```bash
# Usa chatbot per creare conversazioni
python BOT\chatbot_llama.py
# Fai almeno 10-20 domande/risposte
```

### ❌ "CUDA out of memory" durante training
```bash
# Usa QLoRA con batch size minimo
python src\training\train_llama_rag.py --config llama-qlora --batch-size 1 --accumulation-steps 32
```

---

## 📈 Roadmap Miglioramenti

### Fase 1: Setup Iniziale (Week 1)
- ✅ Download Llama locale
- ✅ Prime 50 conversazioni
- ✅ Primo fine-tuning

### Fase 2: Raccolta Dati (Week 2-4)
- 📊 100+ conversazioni
- 🔄 Fine-tuning settimanale
- 📈 Monitoring quality

### Fase 3: Produzione (Week 5+)
- 🚀 Modello stabile
- 🔄 Update automatici
- 📊 Analytics avanzati

---

## 🎯 Riepilogo Comandi Essenziali

```bash
# Setup iniziale (UNA VOLTA)
huggingface-cli login
python ai_system\download_llama.py --verify

# Uso quotidiano
python BOT\chatbot_llama.py

# Update settimanale (dopo 20+ nuove conversazioni)
python ai_system\src\training\create_training_dataset.py
python ai_system\src\training\train_llama_rag.py --config llama-qlora --epochs 2
```

---

**Creato**: Ottobre 2025  
**Versione**: 2.0 (Locale + Conversazioni)
