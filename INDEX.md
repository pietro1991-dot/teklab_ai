# 📑 Spirituality AI - Indice Completo Progetto

Navigazione rapida a tutte le risorse del progetto.

---

## 🚀 Start Here

### Per Nuovi Utenti
1. **[README.md](README.md)** - Overview progetto e quick start
2. **[docs/QUICK_START.md](docs/QUICK_START.md)** - Setup passo-passo
3. **[docs/WORKFLOW_GUIDA.md](docs/WORKFLOW_GUIDA.md)** - Workflow completo

### Per Sviluppatori
1. **[docs/](docs/)** - Tutta la documentazione tecnica
2. **[tests/](tests/)** - Test suite completa
3. **[scripts/](scripts/)** - Scripts operativi

---

## 📚 Documentazione (`docs/`)

| File | Descrizione | Usa quando... |
|------|-------------|---------------|
| **[README.md](docs/README.md)** | Indice documentazione | Cerchi una guida specifica |
| **[QUICK_START.md](docs/QUICK_START.md)** | Setup iniziale | Prima installazione |
| **[PROMPT_SYSTEM_GUIDE.md](docs/PROMPT_SYSTEM_GUIDE.md)** | Sistema prompt configurabili | Crei chunk o personalizzi metadata |
| **[LLAMA_LOCAL_TRAINING_GUIDE.md](docs/LLAMA_LOCAL_TRAINING_GUIDE.md)** | Fine-tuning Llama | Vuoi addestrare il modello |
| **[WORKFLOW_GUIDA.md](docs/WORKFLOW_GUIDA.md)** | Pipeline completa | Capire architettura end-to-end |
| **[ANALISI_FINALE.md](docs/ANALISI_FINALE.md)** | Analisi tecnica | Decisioni architetturali |
| **[CHECKLIST_VERIFICA.md](docs/CHECKLIST_VERIFICA.md)** | Checklist QA | Verifica/troubleshooting |

---

## 🧪 Testing (`tests/`)

| File | Descrizione | Comando |
|------|-------------|---------|
| **[README.md](tests/README.md)** | Guida test suite | - |
| **test_chunk_prompts.py** | Test prompt system | `python tests/test_chunk_prompts.py` |
| **test_api.py** | Test backend Flask | `python tests/test_api.py` |
| **test_imports.py** | Test import moduli | `python tests/test_imports.py` |

---

## 🛠️ Scripts Operativi (`scripts/`)

| Script | Funzione | Comando Esempio |
|--------|----------|-----------------|
| **1_download_llama.py** | Download modello Llama | `python scripts/1_download_llama.py` |
| **2_generate_embeddings.py** | Crea embeddings RAG | `python scripts/2_generate_embeddings.py` |
| **3_create_chunks_with_llama.py** | Genera chunk con Llama | `python scripts/3_create_chunks_with_llama.py --days 1 --prompt-variant detailed` |
| **4_create_training_dataset.py** | Crea dataset training | `python scripts/4_create_training_dataset.py` |
| **5_train_llama_rag.py** | Fine-tuning Llama | `python scripts/5_train_llama_rag.py` |
| **6_chatbot.py** | Chatbot interattivo CLI | `python scripts/6_chatbot.py` |

---

## 🎨 Frontend & Backend

### UI Experience (`UI_experience/`)
**ChatGPT-style Web Interface**

| File | Descrizione |
|------|-------------|
| **[README.md](UI_experience/README.md)** | Documentazione UI |
| **index.html** | Main interface |
| **assets/js/app.js** | Application logic |
| **assets/js/api.js** | Backend communication |
| **assets/css/main.css** | ChatGPT-style design |

**Avvio:**
1. Avvia backend: `python backend_api/app.py`
2. Apri: `UI_experience/index.html` nel browser

---

### Backend API (`backend_api/`)
**Flask REST API**

| File | Descrizione |
|------|-------------|
| **app.py** | Flask server (5 endpoints) |
| **requirements.txt** | Dipendenze backend |

**Endpoints:**
- `GET /health` - Health check
- `POST /chat` - Invia messaggio
- `GET /history` - Cronologia conversazioni
- `POST /clear` - Pulisci cronologia
- `GET /stats` - Statistiche sistema

**Avvio:**
```bash
python backend_api/app.py
```

---

## 🧠 AI System (`ai_system/`)

### Modelli (`ai_system/src/models/`)
- **llama_rag_model.py** - Implementazione base Llama RAG
- **llama_rag_wrapper.py** - Wrapper con auto-detection checkpoint
- **rag_logger.py** - Logging conversazioni

### Configurazione (`ai_system/src/config/`)
- **model_config.py** - Configurazioni modelli (Llama 2/3, QLoRA)

### Training (`ai_system/src/training/`)
- **conversation_logger.py** - Log training conversations
- **training_dataset/** - Dataset preparati per fine-tuning

### Embeddings (`ai_system/Embedding/`)
- Vector database e embeddings per RAG retrieval

---

## 💬 Prompt System (`Prompt/`)

| File | Descrizione |
|------|-------------|
| **prompts_config.py** | System prompt chatbot principale |
| **chunk_prompts_config.py** | Prompt configurabili chunk creation |
| **chunk_creation_instructions.txt** | Istruzioni manuali creazione chunk (per Copilot) |

**Varianti prompt disponibili:**
- `default` - Bilanciato qualità/velocità
- `concise` - Estrazione rapida
- `detailed` - Massima qualità
- `multilingual` - Language-aware

---

## 📂 Knowledge Base (`Fonti/`)

### Struttura
```
Fonti/
└── Autori/
    └── Mathias de Stefano/
        ├── Originali/
        │   └── Pyramid.mathias/
        │       ├── Day_1_Transcript.txt
        │       ├── Day_2_Transcript.txt
        │       └── ...
        └── Processati/
            └── Pyramid Course/
                ├── chunks/
                │   ├── day01/
                │   ├── day02/
                │   └── ...
                ├── metadata/
                ├── keywords/
                ├── quotes/
                └── qa_pairs/
```

**Originali**: Trascrizioni raw  
**Processati**: Chunk strutturati JSON generati da script 3

---

## 🔧 Configurazione

### File Principali
- **START_CHATBOT.bat** - Avvio rapido chatbot (Windows)
- **.gitignore** - Git ignore rules
- **README_OLD.md** - Documentazione legacy

### Requirements
- **BOT/requirements.txt** - Dipendenze bot principale
- **backend_api/requirements.txt** - Dipendenze Flask API

---

## 🎯 Workflow Tipici

### 1. Setup Iniziale
```bash
# 1. Installa dipendenze
pip install -r BOT/requirements.txt

# 2. Login HuggingFace
huggingface-cli login

# 3. Download Llama
python scripts/1_download_llama.py

# 4. Genera embeddings
python scripts/2_generate_embeddings.py
```

### 2. Creazione Chunk
```bash
# Genera chunk per Day 1 con qualità massima
python scripts/3_create_chunks_with_llama.py --days 1 --prompt-variant detailed

# Test sistema prompt
python tests/test_chunk_prompts.py
```

### 3. Training
```bash
# 1. Crea dataset
python scripts/4_create_training_dataset.py

# 2. Fine-tuning
python scripts/5_train_llama_rag.py

# 3. Usa modello fine-tunato
python scripts/6_chatbot.py
```

### 4. Deploy Web Interface
```bash
# Terminal 1: Backend
python backend_api/app.py

# Terminal 2: Apri UI
# Apri UI_experience/index.html nel browser
```

---

## 📊 Struttura Completa Progetto

```
spirituality.ai/
│
├── 📄 INDEX.md                           ← Stai qui!
├── 📄 README.md                          ← Overview progetto
├── 📄 START_CHATBOT.bat                  ← Quick launch
│
├── 📚 docs/                              ← Documentazione
│   ├── README.md
│   ├── QUICK_START.md
│   ├── PROMPT_SYSTEM_GUIDE.md
│   ├── LLAMA_LOCAL_TRAINING_GUIDE.md
│   ├── WORKFLOW_GUIDA.md
│   ├── ANALISI_FINALE.md
│   └── CHECKLIST_VERIFICA.md
│
├── 🧪 tests/                             ← Test suite
│   ├── README.md
│   ├── test_chunk_prompts.py
│   ├── test_api.py
│   └── test_imports.py
│
├── 🛠️ scripts/                           ← Scripts operativi
│   ├── 1_download_llama.py
│   ├── 2_generate_embeddings.py
│   ├── 3_create_chunks_with_llama.py
│   ├── 4_create_training_dataset.py
│   ├── 5_train_llama_rag.py
│   └── 6_chatbot.py
│
├── 🎨 UI_experience/                     ← Frontend web
│   ├── README.md
│   ├── index.html
│   └── assets/
│       ├── css/
│       └── js/
│
├── 🔌 backend_api/                       ← Backend Flask
│   ├── app.py
│   └── requirements.txt
│
├── 🧠 ai_system/                         ← Core AI
│   ├── Embedding/
│   └── src/
│       ├── models/
│       ├── config/
│       └── training/
│
├── 💬 Prompt/                            ← Prompt system
│   ├── prompts_config.py
│   ├── chunk_prompts_config.py
│   └── chunk_creation_instructions.txt
│
├── 📂 Fonti/                             ← Knowledge base
│   └── Autori/
│       └── Mathias de Stefano/
│           ├── Originali/
│           └── Processati/
│
└── 🤖 BOT/                               ← Bot config
    └── requirements.txt
```

---

## 🆘 Help

### Ho bisogno di...

| Bisogno | Vai a... |
|---------|----------|
| **Setup iniziale** | [docs/QUICK_START.md](docs/QUICK_START.md) |
| **Creare chunk** | [docs/PROMPT_SYSTEM_GUIDE.md](docs/PROMPT_SYSTEM_GUIDE.md) |
| **Addestrare Llama** | [docs/LLAMA_LOCAL_TRAINING_GUIDE.md](docs/LLAMA_LOCAL_TRAINING_GUIDE.md) |
| **Capire architettura** | [docs/WORKFLOW_GUIDA.md](docs/WORKFLOW_GUIDA.md) |
| **Risolvere problemi** | [docs/CHECKLIST_VERIFICA.md](docs/CHECKLIST_VERIFICA.md) |
| **Testare sistema** | [tests/README.md](tests/README.md) |
| **API reference** | `backend_api/app.py` (commenti inline) |

---

## 🔗 Links Utili

### Esterni
- **HuggingFace Llama**: https://huggingface.co/meta-llama
- **LoRA Paper**: https://arxiv.org/abs/2106.09685
- **RAG Tutorial**: https://python.langchain.com/docs/use_cases/question_answering/

### Interni Progetto
- **Repository**: [GitHub Link if available]
- **Issues**: [GitHub Issues if available]
- **Discussions**: [GitHub Discussions if available]

---

**Ultimo aggiornamento**: 31 Ottobre 2025  
**Versione Progetto**: 2.0.0  
**Status**: ✅ Produzione
