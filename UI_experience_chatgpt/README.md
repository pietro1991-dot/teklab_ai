# 🔧 Teklab AI - UI Experience

Interfaccia web ChatGPT-style per il chatbot Teklab AI.

## 🎯 Features

- ✅ **UI identica a ChatGPT** (sidebar, chat center, responsive)
- ✅ **Responsive design** (desktop, tablet, mobile)
- ✅ **Dark/Light theme** con toggle
- ✅ **Conversazioni salvate** (localStorage)
- ✅ **Typing animations** fluide
- ✅ **Markdown rendering** nelle risposte
- ✅ **Copy to clipboard** per messaggi
- ✅ **Mobile-friendly** (sidebar collassabile)
- ✅ **Suggestion cards** per quick start
- ✅ **Toast notifications** per errori/successi
- ✅ **Auto-save** conversazioni

## 🚀 Quick Start (Locale)

### 1. Installa dipendenze backend

```bash
cd backend_api
pip install -r requirements.txt
```

### 2. Avvia backend API

```bash
cd backend_api
python app.py
```

Output atteso:
```
🔧 TEKLAB AI - Backend API
📡 Server in avvio su http://localhost:5000
✨ Endpoints disponibili:
   - POST   /chat      → Invia messaggio
   - GET    /health    → Health check
   ...
```

### 3. Apri UI nel browser

**Doppio click su:**
```
UI_experience/index.html
```

Oppure da terminale:
```bash
# Windows
start UI_experience/index.html

# Mac/Linux
open UI_experience/index.html
```

L'interfaccia si aprirà nel browser predefinito e si connetterà automaticamente al backend locale.

## 📁 Struttura File

```
UI_experience/
├── index.html              # Pagina principale
├── config.js               # Configurazione API
├── assets/
│   ├── css/
│   │   ├── main.css       # Stili principali (ChatGPT-style)
│   │   └── responsive.css # Media queries mobile/tablet
│   ├── js/
│   │   ├── app.js         # Logica applicazione
│   │   ├── api.js         # Chiamate backend
│   │   └── utils.js       # Funzioni helper
│   └── images/
│       └── (logo, icons)
└── README.md              # Questo file
```

## ⚙️ Configurazione

### Cambio Backend URL

Modifica `config.js`:

```javascript
// LOCALE (sviluppo)
API_URL: 'http://localhost:5000'

// ONLINE (produzione)
API_URL: 'https://tuo-dominio.com/api'
```

### Personalizzazione UI

**Colori (in `assets/css/main.css`):**
```css
:root {
    --accent-primary: #10a37f;  /* Verde ChatGPT */
    --bg-primary: #ffffff;      /* Sfondo chiaro */
    /* ... */
}
```

**Tema default (in `config.js`):**
```javascript
DEFAULT_THEME: 'light'  // o 'dark'
```

## 🎨 Temi

- **Light Theme** (default): Design pulito bianco/grigio
- **Dark Theme**: Sfondo scuro per uso notturno

Toggle con pulsante in basso a sinistra della sidebar.

## 📱 Responsive Breakpoints

- **Desktop**: > 1024px (sidebar visibile, layout 2 colonne)
- **Tablet**: 768px - 1024px (sidebar collassabile)
- **Mobile**: < 768px (sidebar overlay, header top)

## 🔧 Troubleshooting

### ❌ "Backend non raggiungibile"

**Problema:** Il frontend non riesce a connettersi al backend.

**Soluzione:**
1. Verifica che backend sia avviato: `python backend_api/app.py`
2. Controlla che sia su porta 5000: http://localhost:5000/health
3. Verifica firewall non blocchi porta 5000
4. Verifica embeddings cache: `ai_system/Embedding/teklab_embeddings_cache.pkl`

### ❌ "Failed to fetch"

**Problema:** CORS error o backend offline.

**Soluzione:**
1. Assicurati di avere `flask-cors` installato
2. Backend deve avere `CORS(app)` abilitato (già presente)
3. Riavvia backend dopo modifiche

### ❌ "Module not found"

**Problema:** Backend non trova moduli o embeddings.

**Soluzione:**
1. Verifica percorso progetto in `backend_api/app.py`
2. Esegui da root: `cd teklab_ai && python backend_api/app.py`
3. Controlla che `ai_system/Embedding/teklab_embeddings_cache.pkl` esista
4. Se manca, genera embeddings: `python scripts/2_generate_embeddings.py`

### 💾 "Troppi dati in localStorage"

Se noti lentezza:
1. Apri DevTools (F12)
2. Vai su Console
3. Esegui: `localStorage.clear()`
4. Ricarica pagina

## 🌐 Deploy Online (Futuro)

### Frontend (Vercel/Netlify)

```bash
# 1. Push su GitHub
git add UI_experience/
git commit -m "Add UI"
git push

# 2. Connetti repo su Vercel
# 3. Root directory: UI_experience/
# 4. Deploy automatico
```

### Backend (Railway/Render)

```bash
# 1. Crea Dockerfile (vedi guida principale)
# 2. Deploy su Railway/Render
# 3. Ottieni URL pubblico
# 4. Aggiorna config.js con nuovo URL
```

## 🐛 Debug Mode

Abilita debug in `config.js`:
```javascript
DEBUG: true
```

Apri Console browser (F12) per vedere:
- Chiamate API
- Errori JavaScript
- Timing responses

## 📊 Statistiche Storage

Apri Console (F12) e esegui:
```javascript
Utils.getStorageSize()  // KB usati
```

Per vedere conversazioni salvate:
```javascript
Utils.loadFromStorage('conversations')
```

## 🎯 Keyboard Shortcuts

- **Enter**: Invia messaggio
- **Shift+Enter**: Newline nel textarea
- **Esc**: Chiudi sidebar (mobile)

## 🎨 Customization Ideas

### Cambia Avatar Bot

In `index.html` e `app.js`, sostituisci `🔧` con:
- `🏭` Industria
- `⚙️` Meccanica
- `📊` Dati
- `�` Tecnico

### Aggiungi Suggestions

In `index.html`, sezione `suggestions`:
```html
<button class="suggestion-card" data-prompt="Tua domanda">
    <div class="suggestion-icon">🔮</div>
    <div class="suggestion-text">Tua domanda</div>
</button>
```

### Cambia Font

In `index.html`, tag `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
```

In `main.css`:
```css
--font-family: 'Poppins', sans-serif;
```

## 📝 License

Part of Teklab AI project.

## 🤝 Contributing

Per miglioramenti UI:
1. Modifica file in `UI_experience/`
2. Testa in locale
3. Commit & push

## 📧 Support

Per problemi tecnici, controlla:
1. Console browser (F12)
2. Terminal backend (output Python)
3. File README principale del progetto
4. Documentazione completa in `/docs/`

---

**Made with 🔧 by Teklab AI Team**

**Made with 🌟 by Spirituality AI Team**
