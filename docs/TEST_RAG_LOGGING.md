# 🧪 Test RAG Logging System

## Test Scenario
**Data:** 2025-01-31  
**Obiettivo:** Verificare logging completo di chunk retrieval, timing, token usage

---

## Domanda Test
```
Cosa insegna Mathias de Stefano sui chakra?
```

---

## Aspettative

### 1️⃣ Retrieval
- Sistema deve cercare tra 242 embeddings
- Deve restituire top-3 chunk più simili
- Similarity score > 0.6 (buona rilevanza)

### 2️⃣ Context Injection
- Chunk recuperati iniettati nel prompt come "Informative context"
- Formato: `[Source: dayXX_chunk_YYY]\n{testo}`

### 3️⃣ Generation
- Llama 3.2 3B genera risposta basata su:
  - System prompt (carattere del chatbot)
  - RAG context (knowledge base)
  - User query

### 4️⃣ Logging
**Console output:**
```
📊 Metriche RAG:
   • Chunk recuperati: 3
      1. {chunk_id_1} (sim: X.XXX)
      2. {chunk_id_2} (sim: X.XXX)
      3. {chunk_id_3} (sim: X.XXX)
   • Timing: retrieval X.XXs + generation X.XXs = X.XXs
   • Token: XXX input + XX output = XXX totali
```

**JSON salvato:**
```json
{
  "timestamp": "...",
  "user": "Cosa insegna Mathias de Stefano sui chakra?",
  "assistant": "...",
  "rag_context": "[Source: ...]\n...",
  "retrieved_chunks": [
    {"chunk_id": "...", "similarity_score": 0.XXX, "source": "dayXX"}
  ],
  "timing_metrics": {
    "retrieval_time": X.XX,
    "generation_time": X.XX,
    "total_time": X.XX
  },
  "token_usage": {
    "input_tokens": XXX,
    "output_tokens": XX,
    "total_tokens": XXX
  }
}
```

---

## Esecuzione

Per testare manualmente:
```bash
cd D:\spirituality.ai
python scripts/6_chatbot.py

# Quando appare "🧘 Tu:", digita:
Cosa insegna Mathias de Stefano sui chakra?

# Osserva output console + verifica log salvato in:
# ai_system/training_data/conversations/{today}/{session_id}.json
```

---

## Validazione

### ✅ Success Criteria
1. Sistema recupera 3 chunk
2. Almeno 1 chunk con similarity > 0.8
3. Retrieval time < 1s
4. Generation time < 10s
5. Total tokens < 3000
6. JSON salvato contiene tutti i campi

### ❌ Failure Scenarios
- **Nessun chunk recuperato** → Embeddings non caricati correttamente
- **Similarity <0.5** → Query/chunk mismatch, problema embedding model
- **Retrieval time >5s** → Troppi chunk, serve FAISS index
- **Generation time >20s** → GPU overload, ridurre max_new_tokens
- **Token overflow** → Context troppo lungo, riassumere chunk

---

## Risultati Attesi

### Chunk Recuperati
Domanda parla di "chakra" + "Mathias de Stefano" → dovrebbero emergere:
- Day 3 (introduzione chakra)
- Day 5 (chakra e corpo energetico)
- Day 12 (applicazioni pratiche)

### Timing
- **Retrieval:** ~0.1-0.3s (embeddings già in RAM)
- **Generation:** ~2-5s (risposta ~100-200 token)
- **Total:** ~2-5s

### Token Usage
- **Input:** ~1500-2000 (system 50 + context 1200 + query 50)
- **Output:** ~100-200 (risposta media)
- **Total:** ~1600-2200

---

## Troubleshooting

### Problema: "No chunks retrieved"
**Causa:** Embeddings non caricati  
**Fix:**
```bash
python scripts/2_generate_embeddings.py
```

### Problema: "Similarity scores too low (<0.5)"
**Causa:** Query usa termini non presenti nei chunk  
**Fix:**
- Riformula domanda con termini più semplici
- Verifica chunk contengano davvero info su chakra

### Problema: "Generation too slow (>10s)"
**Causa:** GPU sovraccarica o max_new_tokens troppo alto  
**Fix:**
```python
# In scripts/6_chatbot.py
max_new_tokens=300  # ridotto da 500
```

### Problema: "CUDA out of memory"
**Causa:** VRAM insufficiente (GTX 1050 Ti = 4GB)  
**Fix:**
```python
# In scripts/6_chatbot.py
load_in_4bit=True  # già abilitato
torch.cuda.empty_cache()  # aggiungi prima di generate()
```

---

## Next Steps

Dopo aver verificato il logging:
1. ✅ Esegui 5-10 conversazioni test
2. ✅ Analizza log JSON salvati
3. ✅ Verifica pattern di chunk retrieval
4. ✅ Ottimizza top_k se necessario (2 o 4 invece di 3)
5. ✅ Genera dataset completo 42 giorni overnight
6. ✅ Fine-tuning con conversation history
