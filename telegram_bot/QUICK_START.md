# 🚀 SETUP RAPIDO BOT TELEGRAM TEKLAB

## Pre-requisiti
✅ Python 3.8+
✅ Ollama installato e in esecuzione
✅ Modelli Ollama: llama3.2:3b e nomic-embed-text
✅ Sistema RAG embeddings generati

## Installazione Rapida

### 1️⃣ Installa dipendenze
```bash
cd telegram_bot
pip install -r requirements.txt
```

### 2️⃣ Verifica Ollama
```bash
ollama list
# Deve mostrare:
# - llama3.2:3b
# - nomic-embed-text:latest
```

Se mancano:
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text:latest
```

### 3️⃣ Verifica RAG System
Assicurati che esistano:
- `ai_system/Embedding/embeddings_cache.pkl`
- `ai_system/Embedding/chunks_data.pkl`

### 4️⃣ Avvia il bot

**Windows:**
```bash
START_TELEGRAM_BOT.bat
```

**Manuale:**
```bash
python telegram_bot.py
```

### 5️⃣ Testa su Telegram
1. Apri Telegram
2. Cerca il tuo bot (nome definito con @BotFather)
3. Invia `/start`
4. Prova una domanda: "Che differenza c'è tra TK3+ e TK4?"

## ✅ Verifica Funzionamento

Il bot dovrebbe mostrare:
```
🤖 TEKLAB TELEGRAM BOT - Avvio in corso...
======================================
📚 Caricamento sistema RAG...
✅ Sistema RAG caricato con successo
✅ Embeddings caricati: XXX chunks
✅ Chunks data caricati: XXX entries
🚀 Bot Telegram avviato!
```

## ⚙️ Comandi Bot

- `/start` - Messaggio di benvenuto
- `/help` - Guida completa
- `/clear` - Cancella cronologia
- `/status` - Stato sistema

## 🐛 Troubleshooting

### Errore: Import "telegram" could not be resolved
```bash
pip install python-telegram-bot==20.7
```

### Errore: Ollama non disponibile
1. Verifica Ollama sia in esecuzione: `ollama list`
2. Se non parte: `ollama serve`

### Errore: RAG System non caricato
Verifica i file esistano:
```bash
dir ai_system\Embedding\embeddings_cache.pkl
dir ai_system\Embedding\chunks_data.pkl
```

Se mancano, rigenera embeddings:
```bash
python 2_generate_embeddings.py
```

### Il bot non risponde su Telegram
1. Verifica il token in `config.py`
2. Controlla che il bot sia avviato (deve rimanere in esecuzione)
3. Verifica connessione internet

## 📊 Performance

- **Tempo risposta:** 3-8 secondi
- **RAM utilizzata:** ~200MB (embeddings in memoria)
- **Utenti simultanei:** Illimitati (gestione asincrona)

## 🔐 Sicurezza

**⚠️ IMPORTANTE per produzione:**

1. **Sposta token in variabile ambiente:**
   ```python
   # In config.py
   import os
   TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
   ```

2. **Aggiungi a .gitignore:**
   ```
   telegram_bot/config.py
   *.log
   ```

3. **Setup logging persistente:**
   Modifica in `telegram_bot.py`:
   ```python
   logging.basicConfig(
       filename='telegram_bot.log',
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

## 📞 Supporto

Per problemi o domande:
- GitHub Issues
- Email: info@teklab.it
- Tel: +39 0376 663588