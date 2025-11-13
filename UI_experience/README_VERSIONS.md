# 🚀 Teklab AI - Guida Rapida

## Due Versioni Disponibili

### 🔧 Versione Locale (Ollama)
- **Backend**: `backend_api/app.py`
- **UI**: `UI_experience/index.html`
- **Modelli**: Mistral 7B + Gemma2 2B (locale)
- **Velocità**: ~89 secondi per risposta
- **Costo**: Gratuito
- **Requisiti**: Ollama installato

**Come avviare:**
```bash
# 1. Avvia il backend
python backend_api/app.py

# 2. Apri nel browser
UI_experience/index.html
```

---

### ⚡ Versione ChatGPT (OpenAI API)
- **Backend**: `backend_api/app_chatgpt.py`
- **UI**: `UI_experience/index_chatgpt.html`
- **Modello**: gpt-4o-mini (cloud)
- **Velocità**: ~5-10 secondi per risposta (9x più veloce!)
- **Costo**: ~$0.01 per query (~$1.65/mese per 100 query/giorno)
- **Requisiti**: Chiave API OpenAI

**Come avviare:**
```bash
# 1. Configura la chiave API
# Apri backend_api/config.txt e inserisci:
OPENAI_API_KEY=sk-proj-your_actual_key_here

# 2. Avvia il backend
python backend_api/app_chatgpt.py

# 3. Apri nel browser
UI_experience/index_chatgpt.html
```

---

## 📊 Confronto

| Feature | Ollama (app.py) | ChatGPT (app_chatgpt.py) |
|---------|----------------|--------------------------|
| Velocità | ~89s | ~5-10s (9x più veloce) |
| Costo | Gratuito | ~$1.65/mese |
| Offline | ✅ Sì | ❌ No (richiede internet) |
| Setup | Complesso (Ollama) | Semplice (solo API key) |
| Multilingual | ✅ Con traduzioni | ✅ Nativo |
| RAG | ✅ Identico | ✅ Identico |

---

## 🔑 Come Ottenere la Chiave API OpenAI

1. Vai su https://platform.openai.com/api-keys
2. Crea un account (o fai login)
3. Clicca "Create new secret key"
4. Copia la chiave (inizia con `sk-proj-...`)
5. Incollala in `backend_api/config.txt`

---

## 💡 Quale Usare?

**Usa la versione Ollama (app.py) se:**
- Vuoi zero costi
- Lavori offline
- Hai tempo per risposte più lente
- Privacy/dati sensibili

**Usa la versione ChatGPT (app_chatgpt.py) se:**
- Vuoi risposte velocissime (9x più rapide)
- Hai budget minimo (~$2/mese)
- Lavori online
- Demo/presentazioni

---

## 🛠️ Risoluzione Problemi

### Backend non si avvia
```bash
# Verifica che Flask sia installato
pip install flask flask-cors openai

# Per Ollama: verifica che Ollama sia attivo
ollama list
```

### UI non si connette al backend
1. Verifica che il backend sia avviato (deve stampare "Server starting on http://localhost:5000")
2. Controlla che la porta 5000 sia libera
3. Apri la console del browser (F12) per vedere errori

### ChatGPT: "API key non configurata"
1. Apri `backend_api/config.txt`
2. Verifica che la riga sia: `OPENAI_API_KEY=sk-proj-...` (senza spazi)
3. Controlla che la chiave sia valida su https://platform.openai.com/api-keys

---

## 📝 Note

- Entrambe le versioni usano lo stesso sistema RAG (embeddings + semantic search)
- Le conversazioni sono salvate in localStorage del browser
- Il file `config.txt` è protetto da `.gitignore` (non verrà caricato su Git)

