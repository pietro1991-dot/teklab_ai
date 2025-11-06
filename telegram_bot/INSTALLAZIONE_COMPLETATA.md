# 🤖 BOT TELEGRAM TEKLAB - INSTALLAZIONE COMPLETATA

## ✅ Cosa è stato creato

### File Principali
1. **`telegram_bot.py`** - Bot principale con integrazione RAG
2. **`config.py`** - Configurazione con token e parametri
3. **`requirements.txt`** - Dipendenze Python
4. **`START_TELEGRAM_BOT.bat`** - Script di avvio Windows

### Documentazione
- **`README.md`** - Documentazione completa
- **`QUICK_START.md`** - Guida rapida setup
- **`config.template.py`** - Template configurazione sicura
- **`.gitignore`** - Protezione credenziali

## 🔑 TOKEN BOT

Il tuo token Telegram:
```
8209626692:AAFJ6g5oFEDSS5U5aN_5UOLMetFzLPCUUnE
```

**⚠️ IMPORTANTE:** Questo token è già configurato in `config.py`

## 🚀 COME AVVIARE

### Metodo 1: Batch File (Windows)
```bash
cd telegram_bot
START_TELEGRAM_BOT.bat
```

### Metodo 2: Manuale
```bash
cd telegram_bot
pip install -r requirements.txt
python telegram_bot.py
```

## ✅ Verifica Pre-requisiti

Prima di avviare, assicurati che:

1. **Ollama sia in esecuzione**
   ```bash
   ollama serve
   ```

2. **Modelli installati**
   ```bash
   ollama pull llama3.2:3b
   ollama pull nomic-embed-text:latest
   ```

3. **Sistema RAG caricato**
   Devono esistere:
   - `ai_system/Embedding/embeddings_cache.pkl`
   - `ai_system/Embedding/chunks_data.pkl`

## 🎯 Funzionalità Implementate

### Comandi Bot
- `/start` - Messaggio di benvenuto con menu interattivo
- `/help` - Guida completa utilizzo
- `/clear` - Cancella cronologia conversazione
- `/status` - Stato sistema AI (Ollama, RAG, embeddings)

### Menu Interattivo
1. **🔍 Catalogo Prodotti** - Panoramica completa gamma Teklab
2. **📊 Selezione Guidata** - Assistenza scelta prodotto
3. **🛠️ Supporto Tecnico** - Troubleshooting e installazione

### Sistema RAG
- Ricerca semantica nei documenti Teklab
- Top-3 chunks più rilevanti
- Threshold similarità: 0.28
- Context window: 4000 caratteri

### Gestione Utenti
- Cronologia individuale (max 10 scambi)
- Persistenza sessioni
- Reset manuale cronologia
- Supporto multilingua (IT/EN/ES/DE)

## 📱 COME USARE IL BOT

1. **Apri Telegram** sul tuo telefono/desktop

2. **Cerca il tuo bot** (nome configurato con @BotFather)

3. **Invia `/start`** per iniziare

4. **Fai domande tecniche**, esempi:
   - "Serve sensore livello olio per compressore 46 bar R404A"
   - "Differenza tra TK3+ e TK4?"
   - "Che sensore per serbatoio ammoniaca?"
   - "Come configurare MODBUS su TK4?"
   - "Specifiche ATEX per zona 1 gas"

## 🔧 Architettura Sistema

```
┌─────────────┐
│  TELEGRAM   │
│    USER     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  telegram_bot.py│
│  - Handlers     │
│  - Session Mgmt │
└────────┬────────┘
         │
         ├──► RAG System
         │    - embeddings_cache.pkl
         │    - chunks_data.pkl
         │    - nomic-embed-text
         │
         └──► Ollama LLM
              - llama3.2:3b
              - Response generation
```

## 📊 Prestazioni Attese

- **Latenza media:** 3-8 secondi per risposta
- **RAM utilizzata:** ~200MB (embeddings in memoria)
- **Utenti simultanei:** Illimitati (async handling)
- **Uptime:** Continuo (finché processo è attivo)

## 🔐 Sicurezza

### Per Sviluppo
✅ Token hardcoded in `config.py`
✅ File `.gitignore` protegge credenziali
✅ Template config per team sharing

### Per Produzione
⚠️ **Migliora la sicurezza:**

1. **Usa variabili ambiente:**
   ```python
   import os
   TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
   ```

2. **Setup systemd/supervisord** per restart automatico

3. **Logging su file:**
   ```python
   logging.basicConfig(
       filename='bot.log',
       level=logging.INFO
   )
   ```

4. **Monitoring** stato Ollama e errori

## 🐛 Troubleshooting Comuni

### Bot non risponde
1. Verifica bot sia in esecuzione (terminale deve rimanere aperto)
2. Controlla log per errori
3. Verifica connessione internet

### Errore "Ollama non disponibile"
```bash
# Avvia Ollama
ollama serve
```

### Errore "RAG System non caricato"
```bash
# Rigenera embeddings se mancano
python scripts/2_generate_embeddings.py
```

### Risposte lente
- Ollama su CPU è normale (3-8 sec)
- Per GPU: configura Ollama con CUDA
- Riduci `RAG_TOP_K` a 2 in `config.py`

## 📈 Prossimi Passi

### Ottimizzazioni Possibili
- [ ] Cache risposte frequenti
- [ ] Analytics utilizzo (domande comuni)
- [ ] Feedback utente (👍👎 su risposte)
- [ ] Notifiche proattive prodotti
- [ ] Integrazione CRM (lead capture)

### Funzionalità Avanzate
- [ ] Foto/documenti (OCR + analisi)
- [ ] Voice messages (speech-to-text)
- [ ] Preventivi automatici
- [ ] Tracking ordini
- [ ] Multi-agent (sales + support)

## 📞 Supporto

### Documenti di Riferimento
- `README.md` - Documentazione tecnica completa
- `QUICK_START.md` - Guida setup rapido
- File principale: `telegram_bot.py`

### Contatti Teklab
- Email: info@teklab.it
- Tel: +39 0376 663588
- Web: www.teklab.it

## ✅ CHECKLIST FINALE

Prima di considerare il bot "production-ready":

- [ ] Token in variabile ambiente
- [ ] Logging su file persistente
- [ ] Monitoring uptime configurato
- [ ] Backup configurazione
- [ ] Test con utenti reali
- [ ] Documentazione aggiornata
- [ ] Piano di incident response

## 🎉 IL BOT È PRONTO!

Esegui:
```bash
cd telegram_bot
python telegram_bot.py
```

E inizia a chattare su Telegram! 🚀