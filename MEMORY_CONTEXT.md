# 🧠 Spirituality AI - Sistema di Memoria e Contesto

## 📊 Configurazione Attuale del Progetto

### Database di Conoscenza Spirituale
- **Serie**: "365 Days - The Path of I Am" di Matías De Stefano
- **Giorni totali**: 365 lezioni trascritte
- **Progresso elaborazione**: 53/365 giorni completati (14.5%)
- **Struttura**: 12 costellazioni zodiacali × ~30 giorni ciascuna
- **Formato sorgente**: TXT transcripts → MD processed files

### Memoria della Conversazione
- **Scambi memorizzati**: Ultimi **10 turni** di conversazione (user + assistant)
- **Configurazione**: `MAX_HISTORY_TURNS = 10` in `app_chatgpt.py`
- **Persistenza**: Per tutta la sessione utente (fino a chiusura browser)

### Utilizzo del Contesto

#### 1️⃣ **RAG Search (Ricerca Insegnamenti Spirituali)**
Quando l'utente cerca informazioni sugli insegnamenti:
- **Trigger words**: `chakra`, `vibration`, `grid`, `I Am`, `approfondisci`, `spiega`, `cos'è`, `come funziona`, `tell me more`, ecc.
- **Contesto usato**: Ultimi **2-3 messaggi utente** precedenti
- **Esempio**:
  ```
  User 1: "Qual è la differenza tra apprendere e apprehend?"
  User 2: "Spiegami di più su questo concetto della vibrazione"
  
  → RAG riceve: "Qual è la differenza tra apprendere e apprehend? Spiegami di più su questo concetto della vibrazione"
  ```

#### 2️⃣ **ChatGPT Generation (Risposta AI)**
- **Contesto usato**: Ultimi **5 turni completi** (10 messaggi: 5 user + 5 assistant)
- **Motivo**: Balance tra contesto ricco e limite token (~2000 token di prompt)
- **Benefit**: ChatGPT capisce il flusso della conversazione spirituale e mantiene coerenza tematica

## 🔄 Flusso Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User invia domanda sugli insegnamenti spirituali         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Sistema carica cronologia (max 10 scambi)                │
│    📚 Log: "Cronologia: X scambi memorizzati (max 10)"      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. RAG Search con contesto                                   │
│    • Analizza query per concetti spirituali                  │
│    • Cerca nei 365 giorni processati (MD files)             │
│    • Se termini vaghi: aggiunge ultimi 2-3 messaggi user    │
│    🔗 Log: "Query arricchita con contesto"                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ChatGPT Generation                                        │
│    • System prompt (spiritual teaching context)              │
│    • Ultimi 5 turni conversazione (10 messaggi)             │
│    • Insegnamenti RAG (da MD files processati)              │
│    • Query corrente                                          │
│    💬 Log: "Contesto conversazione: X turni precedenti"     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Risposta salvata in cronologia                           │
│    💾 Log: "Saved conversation turn (total: X turns)"       │
│    • Se X > 10: rimuove i più vecchi automaticamente        │
└─────────────────────────────────────────────────────────────┘
```

## 💡 Perché 10 scambi?

### ✅ Vantaggi
1. **Contesto ricco** per conversazioni multi-turno
2. **Balance token**: Non eccede limit di gpt-4o-mini
3. **Memoria sufficiente** per follow-up complessi
4. **Performance**: Non rallenta il sistema

### ⚖️ Trade-off
- **5 scambi**: Troppo poco per conversazioni lunghe
- **10 scambi**: ✅ **OTTIMALE** (5-10 minuti di conversazione continua)
- **20 scambi**: Rischio di superare token limit, costi più alti

## 📈 Statistiche Token Stimate

| Componente | Token Stimati |
|-----------|---------------|
| System Prompt (spiritual context) | ~2000 |
| Cronologia (5 turni) | ~800-1200 |
| RAG Context (insegnamenti MD) | ~500-800 |
| Query corrente | ~20-100 |
| **TOTALE INPUT** | **~3500-4100** |
| Risposta (max) | ~1500 |
| **TOTALE PER REQUEST** | **~5000-5600** |

**Costo per query**: ~$0.0004-0.0008 (~$0.50-1.00 al mese per 100 query/giorno)

## 🔧 Modifica Configurazione

Per cambiare il numero di scambi memorizzati, modifica in `app_chatgpt.py`:

```python
MAX_HISTORY_TURNS = 10  # Cambia questo valore (5-20 consigliato)
```

**Nota**: Aumentare oltre 15 può causare:
- ⚠️ Superamento token limit
- ⚠️ Costi più alti
- ⚠️ Risposte più lente

## 🧪 Test Scenario - Conversazione Spirituale

**Conversazione esempio (10 turni)**:
1. "Cosa significa meditare?"
2. "Qual è la differenza tra spiritualità e religione?"
3. "Come funziona la Legge della Vibrazione?"
4. "Perché il cuore pulsa più forte durante la meditazione?"
5. "Cosa sono i chakra nel corpo fisico?"
6. "Come si fa ad essere più coscienti?"
7. "Spiegami di più sulla griglia energetica" ← **Usa contesto turni 1-6**
8. "Quali sono i 7 pricipi dell'universo"
9. "Come si integra la spiritualità nella vita quotidiana?"
10. "Cosa succede dopo la morte?"
11. "Quali sono gli esercizi pratici da fare ogni giorno?" ← **Rimuove turno 1, mantiene 2-11**

## 📊 Logs di Debug

Quando il sistema usa il contesto, vedrai nei log:

```
🟢 Processing spiritual query for session 5e03d849
📚 Cronologia: 3 scambi memorizzati (max 10)
⏱️  Timer avviato: 16:30:13

🔍 Avvio RAG Search (365 Days teachings)...
   🔗 Query arricchita con contesto (ultimi 2 messaggi)
   📝 'Qual è la Legge della Vibrazione? Spiegami di più su...'
   📄 Trovati: Day_53 (Apprehend), Day_52 (Context), Day_51 (Be Born)
⏱️  RAG Search completata: 3.8s

🤖 CHATGPT GENERATION START
   💬 Contesto conversazione: 3 turni precedenti
   📖 Insegnamenti caricati: 3 giorni rilevanti
```

---

## 🎯 Struttura del Progetto

### Cartelle Principali
- **`Fonti/Autori/Mathias de Stefano/365 Days The Path Of I Am/`** - TXT transcripts originali
- **`Fonti/Autori/Mathias de Stefano/Processati/MD/`** - MD files processati (53/365 completi)
- **`ai_system/Embedding/`** - Vector embeddings per RAG search
- **`Prompt/`** - System prompts per ChatGPT
- **`backend_api/`** - API Flask per gestione conversazioni

### Pipeline di Elaborazione
1. **TXT → MD**: Conversione transcripts seguendo `TRANSCRIPTION_INSTRUCTIONS.md`
2. **MD → Embeddings**: Generazione vettori per semantic search
3. **RAG + ChatGPT**: Query → Search embeddings → Generate response con contesto
4. **UI**: Interface web per conversazioni (`UI_experience_chatgpt/`)

---

**Sistema ottimizzato per insegnamenti spirituali e conversazioni contestuali!** 🎯✨
