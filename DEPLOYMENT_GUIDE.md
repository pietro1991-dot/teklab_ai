# 🚀 Guida Deployment Teklab Chatbot

## 📋 Panoramica

Sistema chatbot multi-utente con RAG per assistenza tecnica Teklab, deployato **GRATIS** usando:
- **Frontend**: GitHub Pages (hosting statico, CDN globale)
- **Backend**: PC locale + Cloudflare Tunnel (espone Flask pubblicamente)

---

## ✅ Prerequisiti (GIÀ INSTALLATI)

- [x] Python 3.10+
- [x] Ollama con llama3.2:3b
- [x] Cloudflared (in `%USERPROFILE%\cloudflared.exe`)
- [x] Repository GitHub: `pietro1991-dot/teklab_ai`

---

## 🎯 DEPLOYMENT IN 4 PASSAGGI

### **PASSAGGIO 1: Avvia Backend + Tunnel**

Doppio click su `START_PRODUCTION.bat` per avviare automaticamente:
1. Flask backend (porta 5000)
2. Cloudflare Tunnel (espone pubblicamente)

Oppure manuale:

```powershell
# Terminale 1: Backend
cd D:\GitHub_puba\teklab_ai\backend_api
python app.py

# Terminale 2: Cloudflare Tunnel
& "$env:USERPROFILE\cloudflared.exe" tunnel --url http://localhost:5000
```

**Output Cloudflare Tunnel:**
```
2025-11-05 | https://teklab-abc-xyz-123.trycloudflare.com
```

📋 **COPIA QUESTO URL** → Lo userai nel prossimo step.

---

### **PASSAGGIO 2: Aggiorna Configurazione Frontend**

Apri `UI_experience/config.js` e sostituisci l'URL Cloudflare:

```javascript
const CONFIG = {
    // Auto-detect: Cloudflare se su GitHub Pages, localhost se locale
    API_URL: window.location.hostname.includes('github.io')
        ? 'https://teklab-abc-xyz-123.trycloudflare.com'  // ← INCOLLA QUI URL CLOUDFLARE
        : 'http://localhost:5000',
    
    BOT_NAME: 'Teklab Assistant',
    // ... resto config
}
```

**⚠️ IMPORTANTE:**
- Sostituisci `teklab-abc-xyz-123` con il TUO URL Cloudflare copiato prima
- L'URL cambia ogni volta che riavvii il tunnel (modalità free)
- Se vuoi URL fisso → crea tunnel permanente (vedi sotto)

---

### **PASSAGGIO 3: Commit e Push su GitHub**

```powershell
cd D:\GitHub_puba\teklab_ai

# Commit modifiche config
git add UI_experience/config.js
git commit -m "Update: Cloudflare Tunnel URL per produzione"
git push origin main
```

---

### **PASSAGGIO 4: Attiva GitHub Pages**

1. Vai su: https://github.com/pietro1991-dot/teklab_ai/settings/pages
2. **Source**: Deploy from a branch
3. **Branch**: `main`
4. **Folder**: `/ (root)` 
5. Click **Save**

Attendi 1-2 minuti, poi vai su:
```
https://pietro1991-dot.github.io/teklab_ai/UI_experience/
```

🎉 **CHATBOT ONLINE!**

---

## 🧪 Test Completo

### **Test Locale (prima di deploy):**
1. Apri browser: `http://localhost:5000` → Vedi homepage Flask
2. Apri: `file:///D:/GitHub_puba/teklab_ai/UI_experience/index.html`
3. Invia messaggio: "Differenza tra TK3+ e TK4?"
4. Verifica:
   - ✅ "🧠 Sto pensando..." appare subito
   - ✅ "💡 X fonti trovate" dopo 1-2s
   - ✅ Risposta streaming (word-by-word)
   - ✅ Markdown formattato (bold, bullets, headings)
   - ✅ Timer: "Risposto in Xs | Token: Y (L1/4)"

### **Test Cloudflare Tunnel:**
1. Copia URL Cloudflare: `https://teklab-abc-xyz.trycloudflare.com`
2. Apri in browser incognito (per testare come cliente esterno)
3. Vai su: `https://teklab-abc-xyz.trycloudflare.com/` → Vedi homepage Flask
4. Ripeti test chat

### **Test GitHub Pages (produzione finale):**
1. Vai su: `https://pietro1991-dot.github.io/teklab_ai/UI_experience/`
2. Apri DevTools Console (F12)
3. Verifica: `fetch` va a URL Cloudflare (non localhost)
4. Invia query: "Cos'è Teklab TK4?"
5. Verifica funzionamento identico a test locale

---

## 🔧 Tunnel Permanente (URL Fisso)

**Problema attuale**: URL Cloudflare cambia ogni restart (es. `https://random-123.trycloudflare.com`)

**Soluzione**: Crea tunnel con nome fisso (account Cloudflare gratuito)

### **Setup una tantum:**

```powershell
# 1. Login (apre browser per autenticazione)
& "$env:USERPROFILE\cloudflared.exe" tunnel login

# 2. Crea tunnel permanente
& "$env:USERPROFILE\cloudflared.exe" tunnel create teklab-backend

# Output: Tunnel credentials written to C:\Users\USERNAME\.cloudflared\UUID.json
# Copia il tunnel ID (UUID lungo)

# 3. Crea file config
$configContent = @"
tunnel: TUNNEL_UUID_QUI
credentials-file: C:\Users\$env:USERNAME\.cloudflared\TUNNEL_UUID_QUI.json

ingress:
  - hostname: teklab-backend.TUODOMINIO.com
    service: http://localhost:5000
  - service: http_status:404
"@

$configContent | Out-File -Encoding UTF8 "$env:USERPROFILE\.cloudflared\config.yml"

# 4. Assegna DNS (opzionale - altrimenti usa URL .cfargotunnel.com)
& "$env:USERPROFILE\cloudflared.exe" tunnel route dns teklab-backend teklab-backend.TUODOMINIO.com

# 5. Avvia tunnel permanente
& "$env:USERPROFILE\cloudflared.exe" tunnel run teklab-backend
```

**URL Finale**: `https://teklab-backend-uuid.cfargotunnel.com` (sempre lo stesso)

Aggiorna `config.js` con questo URL fisso, commit, e non dovrai più modificarlo.

---

## 🔥 Startup Automatico PC

Se il PC deve essere sempre server, aggiungi all'avvio automatico:

### **Metodo 1: Task Scheduler (Windows)**

```powershell
# Crea task che avvia START_PRODUCTION.bat all'accesso
$action = New-ScheduledTaskAction -Execute "D:\GitHub_puba\teklab_ai\START_PRODUCTION.bat"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
Register-ScheduledTask -TaskName "Teklab Chatbot Production" -Action $action -Trigger $trigger -Principal $principal
```

### **Metodo 2: Startup Folder (semplice)**

```powershell
# Crea collegamento in cartella Avvio
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Teklab_Backend.lnk")
$Shortcut.TargetPath = "D:\GitHub_puba\teklab_ai\START_PRODUCTION.bat"
$Shortcut.Save()
```

---

## 📊 Monitoring Produzione

### **Backend Logs:**
Flask mostra in console:
- Richieste ricevute (IP, user agent)
- Query RAG (fonti trovate, similarity scores)
- Token generati (adaptive levels)
- CONTINUE mode (se attivato)

### **Frontend DevTools:**
```javascript
// Apri Console (F12) per vedere:
[API] Invio query: "Differenza TK3+ vs TK4?"
[SSE] queue: position=1, total=1
[SSE] sources: 3 documenti trovati
[SSE] token: "La differenza principale..."
[SSE] done: 387 tokens in 92s (L1/4)
```

### **Metriche Chiave:**
- **Queue Wait**: Tempo attesa in coda (0s se solo 1 utente)
- **Processing Time**: Tempo generazione risposta
- **Adaptive Level**: L1/L2/L3/L4 (90% dovrebbe essere L1 ≈ 90s)
- **CONTINUE Count**: Quante volte ha dovuto continuare (ideale = 0)

---

## ⚠️ Troubleshooting

### **Problema: "Failed to fetch" in GitHub Pages**

**Causa**: CORS bloccato o URL Cloudflare sbagliato

**Soluzione**:
1. Verifica `config.js` abbia URL corretto
2. Controlla Console (F12): deve chiamare Cloudflare, non localhost
3. Verifica backend Flask abbia CORS abilitato:
   ```python
   # In app.py (già presente):
   CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})
   ```

### **Problema: Tunnel disconnesso**

**Causa**: PC spento o cloudflared crashato

**Soluzione**:
- Riavvia `START_PRODUCTION.bat`
- Se URL cambia → aggiorna `config.js` e commit

### **Problema: Risposta lenta (>120s)**

**Verifica**:
1. Ollama attivo? → `ollama list` deve mostrare `llama3.2:3b`
2. Embeddings cache? → Controlla `backend_api/embeddings_cache.json` esiste
3. RAG efficiente? → Console deve dire "sklearn batch" non "numpy loop"

**Ottimizzazioni già applicate**:
- ✅ Adaptive tokens (400/800/1200/1600)
- ✅ sklearn cosine_similarity (batch)
- ✅ top_k=3, threshold=0.28
- ✅ CONTINUE mode (no retry from scratch)

### **Problema: Markdown non formattato**

**Verifica**:
1. DevTools Console: `marked` deve essere definito
2. Controlla `index.html` include CDN:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/marked@11.1.0/marked.min.js"></script>
   ```
3. CSS caricato correttamente (`main.css`)

---

## 📈 Prossimi Step (Opzionali)

### **1. Analytics**
- Google Analytics su GitHub Pages
- Track: query count, avg response time, bounce rate

### **2. Authentication**
- Aggiungi login clienti (Firebase Auth)
- Rate limiting per utente

### **3. GPU Acceleration**
- Se PC ha NVIDIA GPU → Ollama usa automaticamente
- Speedup: 5x (da 90s → 18s per L1)

### **4. VPS Migration (se serve 24/7)**
- Hetzner Cloud: €5/mese (CPU)
- Contabo: €8/mese (GPU disponibile)
- AWS EC2 t3.medium: €30/mese

---

## 🎯 Checklist Pre-Launch

- [ ] `START_PRODUCTION.bat` avviato → Backend + Tunnel online
- [ ] URL Cloudflare copiato e aggiornato in `config.js`
- [ ] Commit + push su GitHub
- [ ] GitHub Pages attivato
- [ ] Test locale funzionante (http://localhost)
- [ ] Test Cloudflare Tunnel funzionante (https://tunnel-url)
- [ ] Test GitHub Pages finale (https://github.io)
- [ ] Markdown rendering corretto (bold, bullets, headings)
- [ ] Timer mostrato (Xs | Y tokens)
- [ ] "Sto pensando..." animazione visibile
- [ ] Multi-user queue testato (2+ tab browser)

---

## 📞 Supporto

**Repository**: https://github.com/pietro1991-dot/teklab_ai
**Docs**: `docs/` folder
**Logs**: Console backend + DevTools frontend

**Performance Target**:
- 90% query: <100s (Level 1)
- 8% query: <180s (Level 2)
- 1.5% query: <270s (Level 3)
- 0.5% query: <360s (Level 4)

🚀 **Sistema pronto per produzione B2B!**
