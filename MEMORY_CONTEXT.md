# 🧠 Sistema di Memoria e Contesto Conversazionale

## 📊 Configurazione Attuale

### Memoria della Conversazione
- **Scambi memorizzati**: Ultimi **10 turni** di conversazione (user + assistant)
- **Configurazione**: `MAX_HISTORY_TURNS = 10` in `app_chatgpt.py`
- **Persistenza**: Per tutta la sessione utente (fino a chiusura browser)

### Utilizzo del Contesto

#### 1️⃣ **RAG Search (Ricerca Documenti)**
Quando l'utente usa termini vaghi o di approfondimento:
- **Trigger words**: `questi`, `quelli`, `di più`, `approfondisci`, `come`, `perché`, `cosa`, `more about`, `tell me more`, ecc.
- **Contesto usato**: Ultimi **2-3 messaggi utente** precedenti
- **Esempio**:
  ```
  User 1: "Qual'è la differenza tra TK1 e TK3?"
  User 2: "Mi racconti di più sulla tecnologia di questi apparecchi?"
  
  → RAG riceve: "Qual'è la differenza tra TK1 e TK3? Mi racconti di più sulla tecnologia di questi apparecchi?"
  ```

#### 2️⃣ **ChatGPT Generation (Risposta AI)**
- **Contesto usato**: Ultimi **5 turni completi** (10 messaggi: 5 user + 5 assistant)
- **Motivo**: Balance tra contesto ricco e limite token (~2000 token di prompt)
- **Benefit**: ChatGPT capisce il flusso della conversazione

## 🔄 Flusso Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User invia messaggio                                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Sistema carica cronologia (max 10 scambi)                │
│    📚 Log: "Cronologia: X scambi memorizzati (max 10)"      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. RAG Search con contesto                                   │
│    • Analizza query per termini vaghi                        │
│    • Se trovati: aggiunge ultimi 2-3 messaggi user          │
│    🔗 Log: "Query arricchita con contesto"                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ChatGPT Generation                                        │
│    • System prompt (8000 chars)                              │
│    • Ultimi 5 turni conversazione (10 messaggi)             │
│    • Documentazione RAG (se trovata)                         │
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
| System Prompt | ~2000 |
| Cronologia (5 turni) | ~800-1200 |
| RAG Context | ~500-800 |
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

## 🧪 Test Scenario

**Conversazione esempio (10 turni)**:
1. "Quali tipi di TK3 esistono?"
2. "Qual è la differenza tra TK3 e TK4?"
3. "Il TK4 costa di più?"
4. "Quanto costa circa?"
5. "E per CO2 transcritico?"
6. "Quali sono le certificazioni?"
7. "Mi racconti di più sulla tecnologia?" ← **Usa contesto turni 1-6**
8. "Come si installa?"
9. "Serve un tecnico specializzato?"
10. "Quali sono i tempi di consegna?"
11. "Avete distributori in Italia?" ← **Rimuove turno 1, mantiene 2-11**

## 📊 Logs di Debug

Quando il sistema usa il contesto, vedrai nei log:

```
🟢 Processing message for session 5e03d849
📚 Cronologia: 3 scambi memorizzati (max 10)
⏱️  Timer avviato: 16:30:13

🔍 Avvio RAG Search...
   🔗 Query arricchita con contesto (ultimi 2 messaggi)
   📝 'Qual'è la differenza tra TK1 e TK3? Mi racconti di più sulla...'
⏱️  RAG Search completata: 3.8s

🤖 CHATGPT GENERATION START
   💬 Contesto conversazione: 3 turni precedenti
```

---

**Sistema ottimizzato per conversazioni naturali e contestuali!** 🎯
