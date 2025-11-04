# 🦙 Spirituality AI - Sistema RAG con Llama

Sistema di chatbot spirituale basato su **Llama pre-addestrato + RAG** (Retrieval-Augmented Generation).

---

## 📚 Documentazione

Tutta la documentazione è ora organizzata nella cartella **`docs/`**:

- **[QUICK_START.md](docs/QUICK_START.md)** - Guida rapida setup e uso
- **[PROMPT_SYSTEM_GUIDE.md](docs/PROMPT_SYSTEM_GUIDE.md)** - Sistema prompt configurabili per chunk creation
- **[LLAMA_LOCAL_TRAINING_GUIDE.md](docs/LLAMA_LOCAL_TRAINING_GUIDE.md)** - Guida training Llama locale
- **[WORKFLOW_GUIDA.md](docs/WORKFLOW_GUIDA.md)** - Workflow completo del progetto
- **[ANALISI_FINALE.md](docs/ANALISI_FINALE.md)** - Analisi tecnica sistema
- **[CHECKLIST_VERIFICA.md](docs/CHECKLIST_VERIFICA.md)** - Checklist verifica progetto

---

## 🧪 Testing

I test sono organizzati nella cartella **`tests/`**:

- **test_chunk_prompts.py** - Test sistema prompt configurabili
- **test_api.py** - Test backend API Flask
- **test_imports.py** - Verifica import moduli

---

## 🚀 Quick Start

### 1. Installazione



✅ **100% Locale** - Funziona offline dopo setup iniziale  ```bash

✅ **Llama Pre-addestrato** - Meta Llama 2/3 (7B-8B parametri)  # Installa dipendenze

✅ **RAG (Retrieval-Augmented Generation)** - Risponde usando knowledge base personalizzata  pip install -r BOT/requirements.txt

✅ **Fine-Tuning LoRA/QLoRA** - Addestrabile su GPU consumer (6GB+ VRAM)  

✅ **Miglioramento Continuo** - Impara dalle conversazioni reali  # Login HuggingFace (per scaricare Llama)

✅ **Auto-Detection Checkpoint** - Usa automaticamente ultimo modello fine-tunato  huggingface-cli login

# Inserisci token da: https://huggingface.co/settings/tokens

---```



## 📋 Requisiti### 2. Accetta license Llama



### HardwareVai su https://huggingface.co/meta-llama/Llama-2-7b-chat-hf e clicca "Request Access"

- **GPU**: 6GB+ VRAM (RTX 3060 o superiore)

  - 6GB: Llama 7B 4-bit (QLoRA)### 3. Avvia chatbot

  - 16GB: Llama 7B 8-bit o Llama 8B 4-bit

  - 24GB+: Llama 13B 4-bit```bash

# Usa Llama (usa automaticamente ultimo modello fine-tunato se disponibile)

### Softwarepython BOT/chatbot_llama.py

- **Python**: 3.9+```

- **CUDA**: 11.8+ (per GPU NVIDIA)

---

---

## 📚 Fine-tuning (Opzionale ma Consigliato)

## 🚀 Setup Rapido

Per specializzare Llama sui tuoi dati spirituali:

### 1. Installa Dipendenze

### 1. Prepara training data

```bash

pip install -r BOT/requirements.txt```bash

```cd ai_system

python src/training/augment_training_data.py

### 2. Download Modello Llama```



```bash### 2. Avvia training

# Login HuggingFace (license Meta Llama)

huggingface-cli login```bash

# Training con QLoRA (GPU 6GB+)

python scripts/1_download_llama.py --verifypython src/training/train_llama_rag.py --config llama-qlora --epochs 3

```

# Training con Llama 2 7B full (GPU 16GB+)

### 3. Genera Embeddings RAGpython src/training/train_llama_rag.py --config llama-2-7b --epochs 5

```

```bash

python scripts/2_generate_embeddings.py### 3. Il chatbot userà automaticamente l'ultimo checkpoint

```

Dopo training, esegui di nuovo:

### 4. Avvia Chatbot```bash

python BOT/chatbot_llama.py

```bash```

python scripts/6_chatbot.py

```Il sistema troverà automaticamente l'ultimo modello fine-tunato in `ai_system/checkpoints/llama_rag_*/best_model/`



------



## 📚 Miglioramento Continuo## 🏗️ Architettura



### Dopo 20+ Conversazioni```

User Query

```bash    ↓

# Crea datasetRAG Search (semantic + keyword)

python scripts/4_create_training_dataset.py    ↓

Top-K Relevant Chunks

# Fine-tuning (1-3 ore)    ↓

python scripts/5_train_llama_rag.py --config llama-qlora --epochs 3Context Adapter (384 → 4096 dim)

```    ↓

Llama Decoder (pre-trained + LoRA)

Il chatbot usa automaticamente l'ultimo checkpoint!    ↓

Generated Response

---```



## 📖 Documentazione**Componenti**:

- **Sentence Transformers**: Embeddings per ricerca semantica

- **WORKFLOW_GUIDA.md** - Guida completa workflow- **ContextAdapter**: Converte chunks RAG in soft prompts per Llama

- **LLAMA_LOCAL_TRAINING_GUIDE.md** - Guida training dettagliata- **Llama 2/3**: Modello linguistico pre-addestrato (7B/8B parametri)

- **LoRA**: Fine-tuning efficiente (solo 1-2% parametri trainabili)

---

---

**Versione**: 2.0 (Llama Locale)  

**Ultimo aggiornamento**: 31 Ottobre 2025## 📁 Struttura Progetto


```
spirituality.ai/
├── BOT/
│   ├── chatbot_llama.py         # Entry point principale
│   └── requirements.txt          # Dipendenze
├── ai_system/
│   ├── src/
│   │   ├── models/
│   │   │   ├── llama_rag_model.py     # Llama + RAG integration
│   │   │   └── llama_rag_wrapper.py   # Wrapper API compatibile
│   │   ├── training/
│   │   │   └── train_llama_rag.py     # Training script
│   │   └── config/
│   │       └── model_config.py        # Configurazioni (llama-qlora, llama-2-7b, etc.)
│   ├── checkpoints/                   # Modelli fine-tunati
│   │   └── llama_rag_YYYYMMDD/
│   │       └── best_model/
│   └── Embedding/
│       └── generate_embeddings.py     # Genera cache embeddings
├── Fonti/                             # Dati RAG (autori, libri)
└── Prompt/
    └── prompts_config.py              # Configurazione prompt sistema
```

---

## ⚙️ Configurazioni Disponibili

### 1. **llama-qlora** (CONSIGLIATO - GPU 6GB+)
```python
# 4-bit quantization + LoRA
# Memoria minima, training veloce
config = 'llama-qlora'
```

### 2. **llama-2-7b** (GPU 16GB+)
```python
# Llama 2 7B chat
# Maggiore qualità, più memoria
config = 'llama-2-7b'
```

### 3. **llama-3-8b** (GPU 24GB+)
```python
# Llama 3 8B instruct
# Contesto esteso (8192 token)
config = 'llama-3-8b'
```

---

## 🛠️ Comandi Utili

```bash
# Genera embeddings per ricerca semantica
python ai_system/Embedding/generate_embeddings.py

# Analizza conversazioni salvate
python ai_system/src/training/analyze_conversations.py

# Test modello
python ai_system/src/models/llama_rag_wrapper.py
```

---

## 🔧 Troubleshooting

### ❌ "CUDA out of memory"
```bash
# Usa 4-bit quantization
python src/training/train_llama_rag.py --config llama-qlora --batch-size 1
```

### ❌ "Access denied to meta-llama/Llama-2-7b-chat-hf"
1. Vai su https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
2. Clicca "Request Access"
3. Attendi approvazione (pochi minuti)
4. Login: `huggingface-cli login`

### ❌ "bitsandbytes not available on Windows"
```bash
# Windows: usa pre-built wheel
pip install https://github.com/jllllll/bitsandbytes-windows-webui/releases/download/wheels/bitsandbytes-0.41.0-py3-none-win_amd64.whl
```

---

## 📊 Performance

| Modello | VRAM | Tempo risposta | Qualità |
|---------|------|----------------|---------|
| Llama 2 7B (4-bit) | 6GB | 500ms | ⭐⭐⭐⭐⭐ |
| Llama 3 8B (4-bit) | 8GB | 600ms | ⭐⭐⭐⭐⭐ |

---

## 📖 Documentazione Completa

- [Guida Integrazione Llama](LLAMA_INTEGRATION_GUIDE.md) - Dettagli tecnici completi
- [Multilingual Support](MULTILINGUAL_IMPLEMENTATION.md) - Supporto multilingua

---

## 🤝 Supporto

Per problemi:
1. Controlla [Troubleshooting](#-troubleshooting)
2. Verifica requisiti hardware (GPU 6GB+ per QLoRA)
3. Apri issue su GitHub

---

**Versione**: 2.0 (Llama-based)  
**Data**: Ottobre 2025  
**Autore**: Spirituality AI Team
