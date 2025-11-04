# 📊 RAG Logging System - Documentazione

## Overview

Il sistema RAG ora traccia **tutte le metriche** per ogni conversazione:
- ✅ Chunk recuperati (IDs + similarity scores)
- ✅ Tempi di esecuzione (retrieval + generation)
- ✅ Token usage (input + output)

---

## Esempio di Log JSON

```json
{
  "session_id": "abc123-def456",
  "timestamp": "2025-01-31T14:30:00",
  "total_turns": 3,
  "turns": [
    {
      "timestamp": "2025-01-31T14:30:15",
      "user": "Cosa sono i chakra secondo Mathias de Stefano?",
      "assistant": "I chakra sono centri energetici del corpo umano...",
      "rag_context": "[Source: day03_chunk_001]\nTesto completo del chunk...",
      
      "retrieved_chunks": [
        {
          "chunk_id": "day03_chunk_001_pyramid_mathias",
          "similarity_score": 0.8743,
          "source": "day03"
        },
        {
          "chunk_id": "day05_chunk_003_pyramid_mathias",
          "similarity_score": 0.7891,
          "source": "day05"
        },
        {
          "chunk_id": "day12_chunk_002_pyramid_mathias",
          "similarity_score": 0.7245,
          "source": "day12"
        }
      ],
      
      "timing_metrics": {
        "retrieval_time": 0.127,
        "generation_time": 3.456,
        "total_time": 3.583
      },
      
      "token_usage": {
        "input_tokens": 1842,
        "output_tokens": 187,
        "total_tokens": 2029
      }
    }
  ]
}
```

---

## Visualizzazione Console

Dopo ogni risposta, viene stampato:

```
📊 Metriche RAG:
   • Chunk recuperati: 3
      1. day03_chunk_001_pyramid_mathias (sim: 0.874)
      2. day05_chunk_003_pyramid_mathias (sim: 0.789)
      3. day12_chunk_002_pyramid_mathias (sim: 0.724)
   • Timing: retrieval 0.13s + generation 3.46s = 3.58s
   • Token: 1842 input + 187 output = 2029 totali
```

---

## Vantaggi

### 1️⃣ Trasparenza Completa
- Sai **esattamente** quali chunk hanno influenzato ogni risposta
- Puoi verificare la **rilevanza** tramite similarity scores

### 2️⃣ Performance Monitoring
- **Retrieval time**: Quanto tempo per trovare chunk rilevanti
- **Generation time**: Quanto tempo per generare risposta
- **Total time**: Tempo totale end-to-end

### 3️⃣ Token Management
- **Input tokens**: Prompt system + context RAG + domanda utente
- **Output tokens**: Risposta generata da Llama
- **Total tokens**: Somma (utile per calcolare costi se usassi API a pagamento)

### 4️⃣ Debugging & Ottimizzazione
- Se una risposta è errata → controlli i chunk recuperati
- Se similarity è bassa (<0.6) → problema embeddings o query formulation
- Se generation time > 10s → possibile ottimizzazione necessaria

---

## Training Dataset

I log vengono salvati in:
```
ai_system/training_data/conversations/YYYY-MM-DD/{session_id}.json
```

Utilizzabili per:
- **Fine-tuning futuro**: Script `4_create_training_dataset.py`
- **Analisi qualità**: Quali chunk portano a risposte migliori?
- **A/B testing**: Confrontare diverse strategie di retrieval

---

## Esempio Pratico

**Domanda Utente:**
> "Come funziona il primo chakra?"

**Chunk Recuperati:**
1. `day03_chunk_001` (sim: 0.912) → Lezione su Muladhara
2. `day15_chunk_007` (sim: 0.834) → Connessione terra-radici
3. `day08_chunk_004` (sim: 0.798) → Pratiche di grounding

**Analisi:**
- ✅ Top chunk molto rilevante (0.912)
- ✅ Altri chunk complementari
- ⚠️ Se similarity <0.7 → possibile risposta generica (fallback su conoscenza pre-training)

**Timing:**
- Retrieval: 0.08s (OK, embeddings caricati in RAM)
- Generation: 2.34s (OK per risposta ~150 token)
- Total: 2.42s (esperienza utente fluida)

**Token:**
- Input: 1450 (system 50 + context 1200 + query 200)
- Output: 145
- Total: 1595 (sotto limite 4096 di Llama 3.2 3B)

---

## Ottimizzazioni Possibili

### Se retrieval troppo lento (>1s):
```python
# Opzione 1: Ridurre top_k
rag_context, chunks = self.retrieve_context(query, top_k=2)  # invece di 3

# Opzione 2: FAISS index (ultra-fast)
import faiss
index = faiss.IndexFlatIP(384)  # sentence-transformers dimensionality
index.add(chunk_embeddings_matrix)
D, I = index.search(query_emb, k=3)  # <10ms su 10k chunk
```

### Se generation troppo lento (>5s):
```python
# Opzione 1: Ridurre max_new_tokens
max_new_tokens=300  # invece di 500

# Opzione 2: Aumentare temperature (più creativa, meno precisa)
temperature=0.9  # invece di 0.7

# Opzione 3: 4-bit quantization (già fatto)
```

### Se input tokens troppi (>3000):
```python
# Opzione 1: Riassumi chunk invece di testo completo
chunk_summary = chunk_data.get('metadata', {}).get('summary', '')

# Opzione 2: Limita lunghezza chunk
chunk_text = original_text[:500] + "..." if len(original_text) > 500 else original_text
```

---

## Conclusione

Il sistema ora offre **full observability** del pipeline RAG:
1. **Cosa** viene recuperato (chunk IDs)
2. **Quanto** è rilevante (similarity scores)
3. **Quanto tempo** ci vuole (timing breakdown)
4. **Quante risorse** usa (token count)

Questo permette di:
- ✅ Debuggare risposte errate
- ✅ Ottimizzare performance
- ✅ Monitorare qualità nel tempo
- ✅ Preparare dataset training di alta qualità
