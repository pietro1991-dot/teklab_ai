# 🚀 QUICK START - Spirituality AI UI

## ✅ SETUP COMPLETATO!

Hai creato un'interfaccia ChatGPT-style completa per il tuo chatbot.

---

## 📁 FILE CREATI

```
UI_experience/
├── index.html                      ✅ Interfaccia principale
├── config.js                       ✅ Configurazione
├── assets/
│   ├── css/
│   │   ├── main.css               ✅ Stili ChatGPT-style
│   │   └── responsive.css         ✅ Mobile/tablet
│   └── js/
│       ├── app.js                 ✅ Logica applicazione
│       ├── api.js                 ✅ Comunicazione backend
│       └── utils.js               ✅ Helper functions

backend_api/
├── app.py                         ✅ Flask API server
├── requirements.txt               ✅ Dipendenze
└── test_api.py                    ✅ Test automatici

START_CHATBOT.bat                  ✅ Avvio rapido Windows
```

---

## 🎯 COME USARE (3 STEP)

### **STEP 1: Installa Dipendenze Backend**

```bash
pip install flask flask-cors
```

O installa tutto:
```bash
pip install -r backend_api/requirements.txt
```

---

### **STEP 2: Avvia Backend**

**Opzione A - Doppio click:**
```
START_CHATBOT.bat
```

**Opzione B - Manuale:**
```bash
python backend_api/app.py
```

**Output atteso:**
```
🌟 SPIRITUALITY AI - Backend API
📡 Server in avvio su http://localhost:5000
✨ Endpoints disponibili:
   - POST   /chat      → Invia messaggio
   - GET    /health    → Health check
```

---

### **STEP 3: Apri UI nel Browser**

**Doppio click su:**
```
UI_experience/index.html
```

**Oppure trascina il file nel browser.**

L'interfaccia si aprirà e si connetterà automaticamente al backend!

---

## 🎨 INTERFACCIA

### **Desktop:**
```
┌────────────────────────────────────────────────┐
│  Sidebar       │    Chat Center                │
│  • New chat    │    🌟 Welcome Screen          │
│  • Conversaz.  │    💬 Messaggi                │
│  • Settings    │    📝 Input                   │
└────────────────────────────────────────────────┘
```

### **Mobile:**
```
┌─────────────────────┐
│  [☰] Spirituality   │  ← Header
├─────────────────────┤
│  💬 Chat            │
│  📝 Input           │
└─────────────────────┘
```

---

## ✨ FEATURES

- ✅ **Interfaccia ChatGPT-style** (identica)
- ✅ **Sidebar conversazioni** salvate
- ✅ **Responsive** (desktop/tablet/mobile)
- ✅ **Dark/Light theme** toggle
- ✅ **Typing animations** fluide
- ✅ **Auto-save** conversazioni (localStorage)
- ✅ **Copy to clipboard** per risposte
- ✅ **Suggestion cards** per quick start
- ✅ **Toast notifications** per feedback
- ✅ **Keyboard shortcuts** (Enter, Shift+Enter)

---

## 🧪 TEST BACKEND

Per verificare che tutto funzioni:

```bash
python backend_api/test_api.py
```

Output:
```
🧪 SPIRITUALITY AI - Backend API Test
🔍 Testing health endpoint...
✅ Health check OK
💬 Testing chat endpoint...
✅ Chat response OK
```

---

## ⚙️ CONFIGURAZIONE

### **Cambia URL Backend (per deploy futuro)**

Modifica `UI_experience/config.js`:

```javascript
API_URL: 'http://localhost:5000'          // Locale
↓
API_URL: 'https://tuo-dominio.com/api'    // Online
```

### **Cambia Theme Default**

```javascript
DEFAULT_THEME: 'light'  // o 'dark'
```

### **Cambia Timeout Richieste**

```javascript
REQUEST_TIMEOUT: 120000  // ms (2 minuti)
```

---

## 🐛 TROUBLESHOOTING

### ❌ "Backend non raggiungibile"

1. Verifica backend avviato: `python backend_api/app.py`
2. Apri http://localhost:5000/health nel browser
3. Dovrebbe rispondere: `{"status": "healthy", ...}`

### ❌ "Module not found" nel backend

1. Esegui da root progetto: `cd spirituality.ai`
2. Poi: `python backend_api/app.py`
3. Verifica percorsi in `app.py` siano corretti

### ❌ "CORS error" nel browser

1. Verifica `flask-cors` installato: `pip install flask-cors`
2. Backend deve avere `CORS(app)` (già presente)
3. Riavvia backend dopo modifiche

### 💾 UI lenta / localStorage pieno

1. Apri DevTools (F12) → Console
2. Esegui: `localStorage.clear()`
3. Ricarica pagina

---

## 🌐 DEPLOY ONLINE (Futuro)

### **Frontend → Vercel/Netlify (Gratis)**

1. Push `UI_experience/` su GitHub
2. Connetti repo su Vercel
3. Deploy automatico (URL: `https://tuo-nome.vercel.app`)

### **Backend → Railway/Render (Gratis)**

1. Crea `Dockerfile` per backend
2. Deploy su Railway/Render
3. Ottieni URL pubblico
4. Aggiorna `config.js` con nuovo URL

Guida completa in `README_DEPLOY.md` (se necessario).

---

## 📱 MOBILE TESTING

Per testare su mobile nella stessa rete WiFi:

1. Trova IP del tuo PC:
   ```bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   ```

2. Modifica `config.js`:
   ```javascript
   API_URL: 'http://192.168.1.XXX:5000'  # Tuo IP
   ```

3. Apri `UI_experience/index.html` su mobile

---

## 🎯 PROSSIMI PASSI

1. ✅ **Test locale**: Avvia backend + apri UI
2. ✅ **Personalizza**: Colori, avatar, suggestions
3. ✅ **Scarica Llama**: `python scripts/1_download_llama.py`
4. ✅ **Genera embeddings**: `python scripts/2_generate_embeddings.py`
5. ✅ **Testa chat completo**: Domande al bot
6. 🚀 **Deploy online**: Quando pronto

---

## 📚 RISORSE

- **README UI**: `UI_experience/README.md` (dettagli tecnici)
- **README Progetto**: `README.md` (overview completo)
- **Quick Start**: `QUICK_START.md` (workflow generale)

---

## 🤝 SUPPORT

**Problemi comuni risolti in:**
- `UI_experience/README.md` → Sezione Troubleshooting
- Console browser (F12) → Errori JavaScript
- Terminal backend → Errori Python

**Per debug:**
1. Abilita `DEBUG: true` in `config.js`
2. Apri Console browser (F12)
3. Osserva chiamate API e errori

---

## 🎉 RISULTATO FINALE

### **Interfaccia funzionante con:**
- Chat in tempo reale
- Conversazioni salvate
- Responsive mobile
- Theme dark/light
- Pronta per deploy online

### **Backend locale con:**
- Flask API REST
- Llama RAG integration
- Auto-detection modelli
- Logging completo

---

**🌟 Enjoy your Spirituality AI Chatbot!**

Per avviare tutto:
```bash
# 1. Backend
python backend_api/app.py

# 2. UI (doppio click)
UI_experience/index.html
```

---

_Made with 💜 by Spirituality AI Team_
