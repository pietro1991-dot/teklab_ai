# 🚀 Guida Ottimizzazione Prestazioni

## Problema: Generazione lenta

Se il chatbot impiega molto tempo a rispondere, ecco le soluzioni:

### ✅ Soluzione 1: Ridurre lunghezza risposte
Nel file `chatbot_config.py`, modifica:
```python
MAX_NEW_TOKENS = 50  # Invece di 100-300
```
**Effetto**: Risposte più brevi ma molto più veloci (2-3x più veloce)

### ✅ Soluzione 2: Usare un modello più piccolo
Scarica TinyLlama 1.1B (molto più veloce):
```bash
python -c "from huggingface_hub import snapshot_download; snapshot_download('TinyLlama/TinyLlama-1.1B-Chat-v1.0', local_dir='ai_system/models/TinyLlama-1.1B-Chat')"
```

Poi modifica `chatbot_config.py`:
```python
MODEL_PATH = "ai_system/models/TinyLlama-1.1B-Chat"
```
**Effetto**: 5-10x più veloce, usa solo 1GB VRAM

### ✅ Soluzione 3: Ridurre chunk RAG
Nel file `chatbot_config.py`:
```python
RAG_TOP_K = 1  # Invece di 3
```
**Effetto**: Meno contesto ma prompt più piccolo = generazione più veloce

### 📊 Benchmark GTX 1050 Ti (4GB):

| Modello | VRAM | Velocità | Qualità |
|---------|------|----------|---------|
| Llama 3.2 3B | 2.7GB | ~5 token/sec | ⭐⭐⭐⭐⭐ |
| TinyLlama 1.1B | 0.9GB | ~15 token/sec | ⭐⭐⭐ |

### 🎯 Configurazione raccomandata per GTX 1050 Ti:

```python
# chatbot_config.py
MAX_NEW_TOKENS = 80  # Buon compromesso
TEMPERATURE = 0.8  # Più creativo
RAG_TOP_K = 2  # 2 chunk invece di 3
```

**Tempo medio risposta**: 15-30 secondi per 80 token

### 💡 Tips:
- Risposte di 50-100 token sono sufficienti per la maggior parte delle domande
- La prima generazione è più lenta (caricamento cache)
- Le generazioni successive sono più veloci
- Su GPU 4GB, 3B è il limite - evita modelli 7B+