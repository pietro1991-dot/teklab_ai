# 📚 Documentazione Spirituality AI

Benvenuto nella documentazione completa del progetto Spirituality AI!

---

## 🚀 Guide di Avvio Rapido

### [QUICK_START.md](QUICK_START.md)
**Setup e primo utilizzo del sistema**
- Installazione dipendenze
- Download modello Llama
- Generazione embeddings
- Avvio chatbot
- Esempi d'uso

📌 **Inizia da qui se è la prima volta!**

---

## 🎨 Guide Tecniche Specifiche

### [PROMPT_SYSTEM_GUIDE.md](PROMPT_SYSTEM_GUIDE.md)
**Sistema di Prompt Configurabili per Chunk Creation**
- 4 varianti prompt (default, concise, detailed, multilingual)
- Helper functions e API
- Confronto performance
- Workflow consigliato
- Esempi pratici

🎯 **Leggi questa guida per:**
- Creare chunk con qualità ottimale
- Personalizzare metadata extraction
- Validare chunk generati

---

### [LLAMA_LOCAL_TRAINING_GUIDE.md](LLAMA_LOCAL_TRAINING_GUIDE.md)
**Fine-Tuning Llama in Locale**
- Setup GPU e VRAM requirements
- Configurazione LoRA/QLoRA
- Training workflow completo
- Troubleshooting errori comuni

🎯 **Leggi questa guida per:**
- Fine-tunare Llama sul tuo dataset
- Ottimizzare performance training
- Risolvere problemi GPU/memoria

---

### [WORKFLOW_GUIDA.md](WORKFLOW_GUIDA.md)
**Workflow Completo del Progetto**
- Pipeline end-to-end
- Script da eseguire in ordine
- Best practices
- Integrazione componenti

🎯 **Leggi questa guida per:**
- Capire l'architettura completa
- Seguire il processo dall'inizio alla fine
- Integrare nuove features

---

## 📊 Analisi e Verifiche

### [ANALISI_FINALE.md](ANALISI_FINALE.md)
**Analisi Tecnica del Sistema**
- Architettura dettagliata
- Performance metrics
- Limiti e ottimizzazioni
- Roadmap futura

🎯 **Leggi questa guida per:**
- Comprendere decisioni architetturali
- Valutare performance sistema
- Pianificare miglioramenti

---

### [CHECKLIST_VERIFICA.md](CHECKLIST_VERIFICA.md)
**Checklist Verifica Progetto**
- Testing checklist
- Quality assurance
- Deployment readiness
- Troubleshooting common issues

🎯 **Leggi questa guida per:**
- Verificare completezza implementazione
- Debug problemi
- Prepararsi al deployment

---

## 🗺️ Navigazione Rapida per Caso d'Uso

### Sono un nuovo utente
1. ➡️ [QUICK_START.md](QUICK_START.md) - Setup iniziale
2. ➡️ [WORKFLOW_GUIDA.md](WORKFLOW_GUIDA.md) - Capire il sistema
3. ➡️ [CHECKLIST_VERIFICA.md](CHECKLIST_VERIFICA.md) - Verificare installazione

### Voglio creare chunks di qualità
1. ➡️ [PROMPT_SYSTEM_GUIDE.md](PROMPT_SYSTEM_GUIDE.md) - Sistema prompt
2. ➡️ Script: `python scripts/3_create_chunks_with_llama.py --help`
3. ➡️ Test: `python tests/test_chunk_prompts.py`

### Voglio addestrare Llama
1. ➡️ [LLAMA_LOCAL_TRAINING_GUIDE.md](LLAMA_LOCAL_TRAINING_GUIDE.md) - Setup training
2. ➡️ [WORKFLOW_GUIDA.md](WORKFLOW_GUIDA.md) - Pipeline completa
3. ➡️ Script: `python scripts/5_train_llama_rag.py`

### Ho problemi tecnici
1. ➡️ [CHECKLIST_VERIFICA.md](CHECKLIST_VERIFICA.md) - Troubleshooting
2. ➡️ [ANALISI_FINALE.md](ANALISI_FINALE.md) - Limiti noti
3. ➡️ Tests: `python tests/test_*.py`

### Voglio capire l'architettura
1. ➡️ [ANALISI_FINALE.md](ANALISI_FINALE.md) - Architettura completa
2. ➡️ [WORKFLOW_GUIDA.md](WORKFLOW_GUIDA.md) - Pipeline e componenti
3. ➡️ [PROMPT_SYSTEM_GUIDE.md](PROMPT_SYSTEM_GUIDE.md) - Sistema prompt

---

## 📁 Struttura Documentazione

```
docs/
├── README.md                          ← Stai qui!
├── QUICK_START.md                     ← Setup e primo utilizzo
├── PROMPT_SYSTEM_GUIDE.md             ← Sistema prompt configurabili
├── LLAMA_LOCAL_TRAINING_GUIDE.md      ← Fine-tuning Llama
├── WORKFLOW_GUIDA.md                  ← Pipeline completa
├── ANALISI_FINALE.md                  ← Analisi tecnica
└── CHECKLIST_VERIFICA.md              ← Checklist verifica
```

---

## 🔄 Guide Correlate

### Frontend/Backend
- **UI Experience**: `UI_experience/README.md` - ChatGPT-style interface
- **API Backend**: `backend_api/` - Flask REST API

### Testing
- **Tests**: `tests/` - Test suite completa
  - `test_chunk_prompts.py` - Sistema prompt
  - `test_api.py` - Backend API
  - `test_imports.py` - Import moduli

---

## 💡 Tips

### Lettura Consigliata (Ordine)
1. **QUICK_START.md** - Setup base
2. **WORKFLOW_GUIDA.md** - Visione d'insieme
3. **Guide specifiche** - Per approfondimenti

### Aggiornamenti
- Tutte le guide vengono aggiornate durante lo sviluppo
- Controlla data ultima modifica in fondo ad ogni guida
- Le guide più recenti hanno informazioni più aggiornate

### Contribuire
- Per segnalare errori o miglioramenti nelle guide
- Crea issue o pull request su GitHub
- Contatta il team di sviluppo

---

**Ultimo aggiornamento**: 31 Ottobre 2025
