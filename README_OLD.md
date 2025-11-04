# 🦙 Spirituality AI - Sistema RAG con Llama

Sistema di chatbot spirituale basato su **Llama pre-addestrato + RAG** (Retrieval-Augmented Generation).

## 🚀 Quick Start

### 1. Installazione

```bash
# Installa dipendenze
pip install -r BOT/requirements.txt

# Login HuggingFace (per scaricare Llama)
huggingface-cli login
# Inserisci token da: https://huggingface.co/settings/tokens
```

### 2. Accetta license Llama

Vai su https://huggingface.co/meta-llama/Llama-2-7b-chat-hf e clicca "Request Access"

### 3. Avvia chatbot

```bash
# Usa Llama (usa automaticamente ultimo modello fine-tunato se disponibile)
python BOT/chatbot_llama.py
```

---

## 📚 Fine-tuning (Opzionale ma Consigliato)

Per specializzare Llama sui tuoi dati spirituali:

### 1. Prepara training data

```bash
cd ai_system
python src/training/augment_training_data.py
```

### 2. Avvia training

```bash
# Training con QLoRA (GPU 6GB+)
python src/training/train_llama_rag.py --config llama-qlora --epochs 3

# Training con Llama 2 7B full (GPU 16GB+)
python src/training/train_llama_rag.py --config llama-2-7b --epochs 5
```

### 3. Il chatbot userà automaticamente l'ultimo checkpoint

Dopo training, esegui di nuovo:
```bash
python BOT/chatbot_llama.py
```

Il sistema troverà automaticamente l'ultimo modello fine-tunato in `ai_system/checkpoints/llama_rag_*/best_model/`

---

## 🏗️ Architettura

```
User Query
    ↓
RAG Search (semantic + keyword)
    ↓
Top-K Relevant Chunks
    ↓
Context Adapter (384 → 4096 dim)
    ↓
Llama Decoder (pre-trained + LoRA)
    ↓
Generated Response
```

**Componenti**:
- **Sentence Transformers**: Embeddings per ricerca semantica
- **ContextAdapter**: Converte chunks RAG in soft prompts per Llama
- **Llama 2/3**: Modello linguistico pre-addestrato (7B/8B parametri)
- **LoRA**: Fine-tuning efficiente (solo 1-2% parametri trainabili)

---

## 📁 Struttura Progetto

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
