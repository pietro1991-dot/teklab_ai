# Teklab Telegram Bot

Bot Telegram per il sistema di assistenza AI Teklab che utilizza lo stesso sistema RAG del backend Flask.

## Funzionalità

- **Consulenza tecnica sui prodotti Teklab**
- **Sistema RAG integrato** per risposte precise
- **Supporto multilingua** (Italiano, Inglese, Spagnolo, Tedesco)
- **Cronologia conversazioni** per ogni utente
- **Selezione guidata prodotti**
- **Supporto tecnico specializzato**

## Prodotti supportati

### TK Series - Controllori Livello Olio
- TK1+ (monitoraggio)
- TK3+ (controllo automatico) 
- TK4 (versione avanzata + MODBUS)

### LC Series - Interruttori di Livello
- LC-PS (pressostato sicurezza)
- LC-XP (antideflagrante ATEX)
- LC-XT (alta temperatura)

### Sensori ATEX
- Certificazione antideflagrante
- Zone 1/2 (gas) e 21/22 (polveri)

## Installazione

### Prerequisiti
- Python 3.8+
- Ollama con modello llama3.2:3b
- Sistema RAG embeddings già generati
- Backend Flask Teklab funzionante

### Setup

1. **Installa dipendenze:**
```bash
cd telegram_bot
pip install -r requirements.txt
```

2. **Configura token:**
Il token è già configurato nel file `telegram_bot.py`

3. **Verifica sistema RAG:**
Assicurati che esistano:
- `ai_system/Embedding/embeddings_cache.pkl`
- `ai_system/Embedding/chunks_data.pkl`

4. **Avvia Ollama:**
```bash
ollama serve
ollama pull llama3.2:3b
ollama pull nomic-embed-text:latest
```

5. **Avvia il bot:**
```bash
python telegram_bot.py
```

O usa il file batch:
```bash
START_TELEGRAM_BOT.bat
```

## Utilizzo

### Comandi Bot

- `/start` - Messaggio di benvenuto e menu principale
- `/help` - Guida completa
- `/clear` - Cancella cronologia conversazione
- `/status` - Stato sistema AI

### Menu Interattivo

**🔍 Catalogo Prodotti**
- Panoramica completa gamma Teklab
- Specifiche tecniche principali

**📊 Selezione Guidata**
- Assistenza nella scelta del prodotto giusto
- Domande specifiche per l'applicazione

**🛠️ Supporto Tecnico**
- Troubleshooting
- Installazione e configurazione
- Integrazione sistemi

### Esempi di Domande

```
"Serve sensore livello olio per compressore 46 bar R404A"
"Differenza tra TK3+ e TK4?"
"Che sensore per serbatoio ammoniaca?" 
"Come configurare MODBUS su TK4?"
"Specifiche ATEX per zona 1 gas"
```

## Architettura

### Componenti Principali

1. **RAG System**
   - Carica embeddings e chunks da cache
   - Ricerca semantica nei documenti Teklab
   - Top-3 chunks più rilevanti per contesto

2. **Ollama Integration**
   - Modello llama3.2:3b per generazione risposte
   - Embeddings nomic-embed-text per ricerca
   - Timeout e gestione errori

3. **Telegram Handlers**
   - Comandi (/start, /help, /clear, /status)
   - Messaggi di testo
   - Callback inline keyboards

4. **Session Management**
   - Cronologia per utente (max 10 scambi)
   - Persistenza in memoria
   - Reset manuale

### Flusso Operativo

1. **Utente invia messaggio**
2. **Ricerca RAG** → chunks rilevanti
3. **Costruzione prompt** con contesto
4. **Ollama genera risposta**
5. **Invio con fonti utilizzate**
6. **Salvataggio in cronologia**

## Configurazione

### Variabili Principali

```python
TELEGRAM_TOKEN = "8209626692:AAFJ6g5oFEDSS5U5aN_5UOLMetFzLPCUUnE"
BACKEND_URL = "http://localhost:5000"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"
```

### Parametri RAG

- **Threshold similarità:** 0.28
- **Top chunks:** 3
- **Max context length:** 4000 caratteri
- **Cronologia utente:** 10 scambi

### Parametri Ollama

- **Temperature:** 0.7 (creatività bilanciata)
- **Num predict:** 512 token
- **Top P:** 0.9
- **Timeout:** 60 secondi

## Troubleshooting

### Errori Comuni

**❌ Import "telegram" could not be resolved**
```bash
pip install python-telegram-bot==20.7
```

**❌ Ollama non disponibile**
```bash
ollama serve
# In altro terminale:
ollama pull llama3.2:3b
```

**❌ RAG System non caricato**
Verifica paths:
- `ai_system/Embedding/embeddings_cache.pkl`
- `ai_system/Embedding/chunks_data.pkl`

**❌ ModuleNotFoundError prompts_config**
Assicurati che `Prompt/prompts_config.py` esista nel progetto principale.

### Log e Debug

Il bot logga automaticamente:
- Messaggi ricevuti (primi 100 caratteri)
- Chunks RAG trovati
- Errori Ollama/embeddings
- Stato sistema

### Prestazioni

- **Latenza media:** 3-8 secondi
- **Carico RAM:** ~200MB (embeddings)
- **Utenti simultanei:** Illimitati (gestione asincrona)

## Sicurezza

- **Token hardcoded:** Solo per sviluppo
- **Rate limiting:** Gestito da Telegram
- **Input validation:** Gestione automatica caratteri speciali
- **Error handling:** Nessun crash su errori Ollama

## Produzione

### Deploy Consigliato

1. **Token in variabile ambiente:**
```python
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
```

2. **Logging persistente:**
```python
logging.basicConfig(
    filename='telegram_bot.log',
    level=logging.INFO
)
```

3. **Restart automatico:**
```bash
# systemd service o supervisord
```

4. **Monitoring:**
- Stato Ollama
- Carico sistema
- Errori frequenti

## Supporto

Per problemi tecnici:
- Email: info@teklab.it
- Tel: +39 0376 663588
- Web: www.teklab.it

## License

Proprietario Teklab Srl