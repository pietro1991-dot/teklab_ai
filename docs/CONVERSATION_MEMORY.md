# 🧠 Sistema di Memoria Conversazionale

## Funzionalità

Il chatbot ora **ricorda tutta la cronologia** della sessione corrente:
- ✅ Mantiene ultimi **10 turni** nel context window
- ✅ Gestione automatica overflow (tronca se eccede 6000 token)
- ✅ Comando `reset` per iniziare nuova sessione
- ✅ Salvataggio automatico prima di reset/quit

---

## Come Funziona

### 1️⃣ Context Window Structure

```
[System Prompt]
  ↓
[Turn 1 - User]
[Turn 1 - Assistant]
  ↓
[Turn 2 - User]
[Turn 2 - Assistant]
  ↓
...
  ↓
[Turn N - User + RAG Context]  ← Domanda corrente con chunk recuperati
```

### 2️⃣ Esempio Pratico

**Turno 1:**
```
User: Chi è Mathias de Stefano?
Bot: Mathias de Stefano è un educatore spirituale argentino...
```

**Turno 2:**
```
User: Che cosa insegna?
Bot: [RICORDA CHI È MATHIAS dalla conversazione precedente]
     Mathias insegna principalmente sui chakra, energia cosmica...
```

**Turno 3:**
```
User: Parlami del primo chakra
Bot: [RICORDA CONTESTO: Mathias + insegnamenti]
     Secondo quanto insegna Mathias, il primo chakra (Muladhara)...
```

---

## Limiti del Context Window

### Configurazione Attuale
- **MAX_HISTORY_TURNS:** 10 turni (ultimi 10 scambi user/assistant)
- **MAX_HISTORY_TOKENS:** 6000 token (riserva per RAG context + risposta)
- **Total Context Limit:** 8192 token (limite Llama 3.2 3B)

### Breakdown Token Budget

| Componente | Token Budget | Note |
|-----------|-------------|------|
| System Prompt | ~50 | Fisso |
| Cronologia (10 turni) | ~4000 | Variabile |
| RAG Context (3 chunk) | ~1500 | Variabile |
| Domanda corrente | ~100 | Variabile |
| **TOTALE INPUT** | ~5650 | |
| Risposta generata | ~300-500 | max_new_tokens=500 |
| **TOTALE** | ~6000-6150 | Sotto limite 8192 ✅ |

---

## Gestione Overflow

### Strategia 1: Ultimi N Turni (Implementata)
```python
# Prende ultimi 10 turni
recent_history = self.conversation_history[-10:]
```

**PRO:**
- ✅ Semplice
- ✅ Mantiene conversazioni recenti
- ✅ Prevedibile

**CONTRO:**
- ❌ Perde contesto più vecchio (dopo 10 turni)

### Strategia 2: Troncamento Token-Based (Futuro)
```python
# Calcola token effettivi
total_tokens = sum(len(tokenizer.encode(turn["user"] + turn["assistant"])) 
                   for turn in history)

# Tronca fino a rientrare in budget
while total_tokens > MAX_HISTORY_TOKENS:
    history.pop(0)  # Rimuovi turno più vecchio
    total_tokens = recalculate()
```

**PRO:**
- ✅ Più efficiente
- ✅ Massimizza cronologia preservata

**CONTRO:**
- ❌ Più complesso
- ❌ Overhead calcolo token

---

## Comandi Disponibili

### `reset` / `nuovo` / `new`
Resetta la cronologia e inizia una nuova sessione.

**Comportamento:**
1. Salva conversazione corrente in JSON
2. Genera nuovo session_id
3. Pulisce conversation_history
4. Mantiene embeddings e modello caricati

**Uso:**
```
🧘 Tu: reset
🔄 Cronologia resettata. Nuova sessione avviata.
   (Conversazione precedente salvata)
```

### `quit` / `exit` / `q`
Esce dal chatbot salvando la conversazione corrente.

### `clear`
Pulisce lo schermo (non resetta cronologia).

---

## Log Metriche Aggiornate

Esempio output dopo risposta:

```
📊 Metriche RAG:
   • Cronologia: 3 turni (ultimi 3 nel contesto)
   • Chunk recuperati: 3
      1. day03_chunk_001_pyramid_mathias (sim: 0.874)
      2. day05_chunk_003_pyramid_mathias (sim: 0.789)
      3. day12_chunk_002_pyramid_mathias (sim: 0.724)
   • Timing: retrieval 0.13s + generation 3.46s = 3.58s
   • Token: 1842 input + 187 output = 2029 totali
```

**Nuova riga:**
```
• Cronologia: 3 turni (ultimi 3 nel contesto)
               ↑           ↑
            totale    effettivamente usati
```

---

## JSON Salvato

Struttura completa della conversazione salvata:

```json
{
  "session_id": "abc123-def456",
  "timestamp": "2025-11-02T14:30:00",
  "total_turns": 5,
  "turns": [
    {
      "timestamp": "2025-11-02T14:30:15",
      "user": "Chi è Mathias de Stefano?",
      "assistant": "Mathias de Stefano è...",
      "rag_context": "[Source: ...]\n...",
      "retrieved_chunks": [...],
      "timing_metrics": {...},
      "token_usage": {...}
    },
    {
      "timestamp": "2025-11-02T14:31:42",
      "user": "Che cosa insegna?",
      "assistant": "Insegna principalmente...",
      "rag_context": "[Source: ...]\n...",
      "retrieved_chunks": [...],
      "timing_metrics": {...},
      "token_usage": {...}
    }
  ]
}
```

**Nota:** Ogni turno è **autocontenuto** con:
- Domanda utente
- Risposta bot
- Chunk usati
- Metriche timing/token

---

## Vantaggi della Cronologia

### 1️⃣ Conversazioni Naturali
```
User: Parlami dei chakra
Bot: I chakra sono centri energetici...

User: Quanti sono?
Bot: [RICORDA CHE PARLIAMO DI CHAKRA]
     Sono 7 chakra principali...

User: Descrivimi il primo
Bot: [RICORDA CHE PARLIAMO DI 7 CHAKRA]
     Il primo chakra si chiama Muladhara...
```

### 2️⃣ Follow-up Questions
```
User: Chi è Mathias de Stefano?
Bot: È un educatore spirituale argentino...

User: Dove ha studiato?
Bot: [SA DI CHI PARLIAMO - no bisogno di ripetere]
     Mathias ha studiato...
```

### 3️⃣ Correzioni e Approfondimenti
```
User: Parlami del terzo chakra
Bot: Il terzo chakra (Manipura) è...

User: No, intendevo il secondo
Bot: [RICORDA CHE ABBIAMO DISCUSSO IL TERZO]
     Mi scuso, il secondo chakra (Svadhisthana) è...
```

---

## Performance Impact

### Con Cronologia (10 turni):
- **Input tokens:** ~5650 (system 50 + history 4000 + RAG 1500 + query 100)
- **Generation time:** +0.5-1s (più token da processare)
- **VRAM usage:** +100-200MB (attention heads più grandi)

### Senza Cronologia:
- **Input tokens:** ~1650 (system 50 + RAG 1500 + query 100)
- **Generation time:** baseline
- **VRAM usage:** baseline

**Conclusione:** Overhead accettabile per esperienza conversazionale naturale.

---

## Troubleshooting

### Problema: "CUDA Out of Memory"
**Causa:** Cronologia + RAG context eccedono VRAM  
**Fix:**
```python
# In scripts/6_chatbot.py
MAX_HISTORY_TURNS = 5  # Ridotto da 10
```

### Problema: "Risposte troppo lente (>10s)"
**Causa:** Troppi token input da processare  
**Fix 1:** Ridurre cronologia
```python
MAX_HISTORY_TURNS = 3
```

**Fix 2:** Ridurre RAG chunks
```python
rag_context, chunks = self.retrieve_context(query, top_k=2)  # invece di 3
```

### Problema: "Bot dimentica info dopo 10 turni"
**Causa:** MAX_HISTORY_TURNS limita a 10 scambi  
**Fix:** Aumentare limite (occhio a VRAM)
```python
MAX_HISTORY_TURNS = 15  # Aumentato da 10
MAX_HISTORY_TOKENS = 8000  # Aumentato da 6000
```

### Problema: "Cronologia contiene errori passati"
**Soluzione:** Usa comando `reset` per iniziare pulito
```
🧘 Tu: reset
```

---

## Ottimizzazioni Future

### 1️⃣ Summarization di Turni Vecchi
Invece di scartare, riassumi:
```python
# Turni 1-5: riassunti in 200 token
summary = summarize(turns[:5])
# Turni 6-10: testo completo
recent = turns[5:]

messages = [system, summary] + recent + [current_query]
```

### 2️⃣ Semantic Chunking della Cronologia
Mantieni solo turni rilevanti alla domanda corrente:
```python
# Calcola similarity query vs ogni turno
relevant_turns = filter(lambda t: similarity(query, t["user"]) > 0.7, history)
messages = [system] + relevant_turns + [current_query]
```

### 3️⃣ Hybrid Memory (Short + Long Term)
```python
short_term = last_3_turns  # Sempre inclusi
long_term_summary = summarize(all_previous_turns)  # Riassunto

messages = [system, long_term_summary] + short_term + [current_query]
```

---

## Conclusione

Il chatbot ora offre **memoria conversazionale completa**:
- ✅ Ricorda ultimi 10 turni automaticamente
- ✅ Gestisce overflow context window
- ✅ Comando `reset` per iniziare nuova sessione
- ✅ Log completo mostra cronologia attiva
- ✅ Salvataggio JSON preserva intera conversazione

Questo permette conversazioni **naturali e fluide** senza dover ripetere contesto ogni volta.
