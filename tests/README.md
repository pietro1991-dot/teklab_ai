# 🧪 Test Suite - Spirituality AI

Test suite completa per verificare il funzionamento del sistema Spirituality AI.

---

## 📋 Test Disponibili

### 1. test_chunk_prompts.py
**Test del sistema di prompt configurabili per chunk creation**

```bash
python tests/test_chunk_prompts.py
```

**Verifica:**
- ✅ Import moduli prompt configuration
- ✅ System prompt caricato correttamente
- ✅ Tutte le varianti disponibili (default, concise, detailed, multilingual)
- ✅ Generazione prompt per ogni variante
- ✅ Validation prompt
- ✅ Error handling per varianti invalide
- ✅ Template validation (placeholder, lunghezza)
- ✅ Integration test workflow completo

**Output atteso:**
```
🧪 Testing Chunk Prompts Configuration System
======================================================================
✅ Import successful!
✅ System prompt loaded
✅ All variants available
✅ All prompts generated correctly
✅ Validation prompt working
✅ Error handling correct
✅ Templates valid
✅ Integration test successful
======================================================================
🎉 ALL TESTS PASSED!
```

---

### 2. test_api.py
**Test del backend Flask API**

```bash
python tests/test_api.py
```

**Verifica:**
- ✅ Endpoint `/health` - Status check
- ✅ Endpoint `/chat` - Invio messaggi
- ✅ Endpoint `/history` - Cronologia conversazioni
- ✅ Endpoint `/clear` - Pulizia cronologia
- ✅ Endpoint `/stats` - Statistiche sistema
- ✅ CORS headers
- ✅ Error handling

**Prerequisiti:**
- Backend Flask in esecuzione su `http://localhost:5000`
- Modello Llama caricato

**Come eseguire:**
```bash
# Terminal 1: Avvia backend
python backend_api/app.py

# Terminal 2: Esegui test
python tests/test_api.py
```

---

### 3. test_imports.py
**Test import moduli Python**

```bash
python tests/test_imports.py
```

**Verifica:**
- ✅ Import Flask e dipendenze backend
- ✅ Import Llama RAG wrapper
- ✅ Import configurazioni
- ✅ Import prompt system
- ✅ Versioni librerie corrette

**Output atteso:**
```
🧪 Testing Module Imports
✅ Flask imported
✅ LlamaRAGWrapper imported
✅ Configurations imported
✅ Prompt system imported
🎉 ALL IMPORTS SUCCESSFUL!
```

---

## 🚀 Esecuzione Completa

### Run All Tests
```bash
# Test singoli
python tests/test_chunk_prompts.py
python tests/test_imports.py

# Test API (richiede backend attivo)
# Terminal 1:
python backend_api/app.py

# Terminal 2:
python tests/test_api.py
```

### Quick Test (solo non-API)
```bash
python tests/test_chunk_prompts.py && python tests/test_imports.py
```

---

## 🔧 Setup Ambiente Test

### Dipendenze
```bash
pip install -r BOT/requirements.txt
pip install -r backend_api/requirements.txt
```

### Struttura Path
Assicurati che la struttura sia:
```
spirituality.ai/
├── tests/
│   ├── test_chunk_prompts.py
│   ├── test_api.py
│   └── test_imports.py
├── Prompt/
│   ├── prompts_config.py
│   └── chunk_prompts_config.py
├── ai_system/src/
│   ├── models/
│   └── config/
└── backend_api/
    └── app.py
```

---

## 📊 Test Coverage

| Componente | Test | Status |
|------------|------|--------|
| **Prompt System** | test_chunk_prompts.py | ✅ Completo |
| **Backend API** | test_api.py | ✅ Completo |
| **Module Imports** | test_imports.py | ✅ Completo |
| **Chunk Creation** | - | 🔄 Da aggiungere |
| **Training Pipeline** | - | 🔄 Da aggiungere |
| **RAG Retrieval** | - | 🔄 Da aggiungere |

---

## 🐛 Troubleshooting

### Test fallisce: "ModuleNotFoundError"
```bash
# Verifica PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/spirituality.ai"

# O esegui da root del progetto
cd spirituality.ai
python tests/test_*.py
```

### Test API fallisce: "Connection refused"
```bash
# Assicurati che backend sia attivo
python backend_api/app.py

# Verifica che sia su porta 5000
curl http://localhost:5000/health
```

### Test chunk prompts fallisce: "Import error"
```bash
# Verifica file esiste
ls Prompt/chunk_prompts_config.py

# Verifica sintassi
python -m py_compile Prompt/chunk_prompts_config.py
```

---

## 📝 Aggiungere Nuovi Test

### Template Test Base
```python
"""
Test [Component Name]
=====================
Descrizione cosa testa
"""

import sys
from pathlib import Path

# Setup path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("🧪 Testing [Component Name]")
print("=" * 70)

# Test 1
print("📝 Test 1: [Description]")
try:
    # Test logic
    print("✅ Test 1 passed")
except Exception as e:
    print(f"❌ Test 1 failed: {e}")

# ... più test ...

print("🎉 ALL TESTS PASSED!")
```

### Naming Convention
- `test_[component]_[feature].py`
- Esempio: `test_llama_generation.py`, `test_rag_retrieval.py`

---

## 🎯 Test Roadmap

### In Progress
- ✅ Prompt system testing
- ✅ Backend API testing  
- ✅ Module imports testing

### Planned
- 🔄 Chunk creation end-to-end test
- 🔄 Training pipeline test
- 🔄 RAG retrieval accuracy test
- 🔄 Performance benchmarks
- 🔄 Integration tests

### Future
- 📋 UI testing (Selenium/Playwright)
- 📋 Load testing (API stress test)
- 📋 Memory profiling
- 📋 GPU utilization tests

---

## 📚 Documentazione Correlata

- **Setup**: [docs/QUICK_START.md](../docs/QUICK_START.md)
- **Prompt System**: [docs/PROMPT_SYSTEM_GUIDE.md](../docs/PROMPT_SYSTEM_GUIDE.md)
- **Workflow**: [docs/WORKFLOW_GUIDA.md](../docs/WORKFLOW_GUIDA.md)

---

**Ultimo aggiornamento**: 31 Ottobre 2025
