# 🎯 Sistema di Prompt Configurabili per Chunk Creation

## ✅ COMPLETATO - Modifiche Implementate

### 📁 Files Creati/Modificati

1. **✅ NUOVO: `Prompt/chunk_prompts_config.py`** (421 righe)
   - Sistema completo di prompt configurabili per Llama
   - 5 varianti disponibili
   - Helper functions per gestione prompt
   
2. **✅ MODIFICATO: `scripts/3_create_chunks_with_llama.py`**
   - Integrazione sistema prompt configurabile
   - Nuovo parametro `--prompt-variant`
   - Import automatico con fallback
   
3. **✅ NUOVO: `scripts/test_chunk_prompts.py`** (176 righe)
   - Test suite completa
   - Verifica import, varianti, generazione prompt
   - Test integrazione workflow

---

## 📦 Prompt/chunk_prompts_config.py

### Prompt Variants Disponibili

#### 1. **DEFAULT** - Bilanciato (1555 caratteri)
```python
variant = "default"  # Qualità/velocità equilibrata
```
**Quando usarlo:**
- Uso standard per la maggior parte dei chunk
- Dataset di dimensioni medie (10-100 giorni)
- Qualità buona con tempi ragionevoli

**Output:**
- 5-7 key concepts
- 5-8 primary keywords
- 2-4 iconic quotes
- 3-5 natural questions
- Summary conciso (2-3 frasi)

---

#### 2. **CONCISE** - Veloce (661 caratteri)
```python
variant = "concise"  # Estrazione rapida
```
**Quando usarlo:**
- Dataset molto grandi (100+ giorni)
- Prima passata per overview
- Risorse computazionali limitate

**Output:**
- 3 key concepts
- 3 primary keywords
- 1 iconic quote
- 2 natural questions
- Summary essenziale (1 frase)

---

#### 3. **DETAILED** - Massima Qualità (3590 caratteri)
```python
variant = "detailed"  # Massima profondità
```
**Quando usarlo:**
- Chunk di altissima qualità
- Training dataset finale
- Contenuti premium/flagship

**Output:**
- 7-10 key concepts (con descrizioni dettagliate)
- 6-10 primary keywords
- 3-5 synonyms per keyword
- Keywords relations (connessioni semantiche)
- 3-5 iconic quotes
- 3-5 key formulas/principles
- 5-7 natural questions (diverse types)
- Themes, difficulty_level, tone
- Prerequisites, natural_followup
- Summary comprensivo (3-5 frasi)

---

#### 4. **MULTILINGUAL** - Multilingua (1600 caratteri)
```python
variant = "multilingual"  # Language-aware
```
**Quando usarlo:**
- Sorgenti in lingue diverse dall'inglese
- Preservare contesto culturale
- Termini non traducibili

**Output:**
- Metadata in ENGLISH (consistenza database)
- `keywords_original_language` per termini significativi
- `cultural_notes` per contesto culturale/linguistico
- Tutti gli altri field standard

---

#### 5. **VALIDATION** - Quality Check
```python
from chunk_prompts_config import get_validation_prompt
validation_prompt = get_validation_prompt(generated_chunk)
```
**Quando usarlo:**
- Validare chunk generati prima di salvarli
- Quality assurance automatica
- Identificare chunk problematici

**Output:**
- `is_valid`: true/false
- Score per categoria (completeness, accuracy, clarity, relevance, quality)
- `overall_score`: 0-100
- `issues`: lista problemi
- `suggestions`: miglioramenti suggeriti

---

## 🚀 Come Usare

### Uso Base (Default Variant)
```bash
python scripts/3_create_chunks_with_llama.py --days 1
```

### Uso con Variant Specifica
```bash
# Massima qualità
python scripts/3_create_chunks_with_llama.py --days 1 --prompt-variant detailed

# Estrazione veloce
python scripts/3_create_chunks_with_llama.py --days 1 2 3 --prompt-variant concise

# Multilingua
python scripts/3_create_chunks_with_llama.py --days 1 --prompt-variant multilingual
```

### Test Sistema
```bash
# Verifica configurazione
python scripts/test_chunk_prompts.py
```

### Help Completo
```bash
python scripts/3_create_chunks_with_llama.py --help
```

---

## 🔧 Helper Functions

### `get_chunk_prompt()`
```python
from Prompt.chunk_prompts_config import get_chunk_prompt

prompt = get_chunk_prompt(
    text="Your text here...",
    variant="detailed",          # default, concise, detailed, multilingual
    source_language="English"    # Solo per multilingual variant
)
```

### `get_validation_prompt()`
```python
from Prompt.chunk_prompts_config import get_validation_prompt

validation_prompt = get_validation_prompt(chunk_json_text)
```

### `get_available_variants()`
```python
from Prompt.chunk_prompts_config import get_available_variants

variants = get_available_variants()
# Returns: ["default", "concise", "detailed", "multilingual"]
```

### `get_variant_description()`
```python
from Prompt.chunk_prompts_config import get_variant_description

desc = get_variant_description("detailed")
# Returns: "Maximum quality - comprehensive metadata with depth"
```

---

## 📊 Confronto Varianti

| Caratteristica | Default | Concise | Detailed | Multilingual |
|---|---|---|---|---|
| **Lunghezza prompt** | 1555 char | 661 char | 3590 char | 1600 char |
| **Key concepts** | 5-7 | 3 | 7-10 | 5-7 |
| **Keywords** | 5-8 | 3 | 6-10 | 5-8 |
| **Synonyms** | Basic | No | Extensive | Yes |
| **Relations** | No | No | Yes | No |
| **Quotes** | 2-4 | 1 | 3-5 | 2-4 |
| **Formulas** | No | No | Yes | No |
| **Questions** | 3-5 | 2 | 5-7 | 3-5 |
| **Metadata extra** | No | No | Yes | Cultural notes |
| **Velocità** | ⚡⚡⚡ | ⚡⚡⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡ |
| **Qualità** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🎓 Workflow Consigliato

### Fase 1: Prima Passata (Concise)
```bash
# Genera overview rapida di tutto il dataset
python scripts/3_create_chunks_with_llama.py --range 1 42 --prompt-variant concise
```

### Fase 2: Verifica e Selezione
- Analizza chunk generati
- Identifica giorni/sezioni di alta qualità
- Seleziona chunk da rigenerare in detailed

### Fase 3: Rigenerazione Dettagliata
```bash
# Rigenera chunk selezionati con massima qualità
python scripts/3_create_chunks_with_llama.py --days 1 5 10 15 --prompt-variant detailed
```

### Fase 4: Validazione (Opzionale)
```python
# Script custom per validare chunk
from Prompt.chunk_prompts_config import get_validation_prompt

for chunk in chunks:
    validation_prompt = get_validation_prompt(chunk)
    score = llama.validate(validation_prompt)
    if score['overall_score'] < 80:
        print(f"⚠️ Chunk {chunk['id']} needs review: {score['issues']}")
```

---

## 🔍 System Prompt per Chunk Creation

```python
CHUNK_SYSTEM_PROMPT = """You are an expert AI assistant specialized in 
analyzing spiritual and philosophical texts. Your role is to extract 
structured metadata from text chunks to enable semantic search and 
RAG (Retrieval Augmented Generation).

Your responsibilities:
- Extract key concepts, themes, and ideas from the text
- Identify meaningful keywords for semantic search
- Select iconic quotes that capture the essence
- Generate natural questions users might ask about this content
- Provide clear, concise summaries
- Maintain spiritual and philosophical depth in your analysis

Output format: Always respond with valid JSON containing the 
requested metadata fields."""
```

**Differenze con SYSTEM_PROMPT del chatbot:**
- `CHUNK_SYSTEM_PROMPT`: Analitico, estrazione metadata, output JSON
- `SYSTEM_PROMPT` (chatbot): Guida spirituale, conversazionale, insegnamenti

---

## 📝 Note Tecniche

### Import nel Script 3
```python
try:
    from chunk_prompts_config import (
        get_chunk_prompt, 
        CHUNK_SYSTEM_PROMPT,
        get_available_variants,
        get_variant_description
    )
except ImportError:
    # Fallback a prompt hardcoded
    # Sistema continua a funzionare anche se import fallisce
```

### Compatibilità
- ✅ Backward compatible: Se import fallisce, usa prompt originale
- ✅ No breaking changes: Script funziona come prima se non usi `--prompt-variant`
- ✅ Testato: Tutti i test passano (test_chunk_prompts.py)

---

## 🎯 Prossimi Passi

1. **Testa Varianti su Chunk Reale**
   ```bash
   # Genera 1 chunk con ogni variante
   python scripts/3_create_chunks_with_llama.py --days 1 --max-chunks 1 --prompt-variant default
   python scripts/3_create_chunks_with_llama.py --days 1 --max-chunks 1 --prompt-variant concise
   python scripts/3_create_chunks_with_llama.py --days 1 --max-chunks 1 --prompt-variant detailed
   ```

2. **Confronta Output**
   - Apri chunk generati
   - Compara qualità metadata
   - Scegli variant ottimale per il tuo use case

3. **Genera Dataset Completo**
   ```bash
   # Usa variant scelta per tutto il dataset
   python scripts/3_create_chunks_with_llama.py --range 1 42 --prompt-variant [chosen]
   ```

4. **Validazione (Opzionale)**
   - Implementa script validazione automatica
   - Usa CHUNK_VALIDATION_PROMPT
   - Filtra chunk con score < 80

---

## ✅ Test Results

```
🧪 Testing Chunk Prompts Configuration System
======================================================================
✅ Import successful!

📝 Test 1: System Prompt
✅ System prompt loaded

📝 Test 2: Available Variants
✅ All variants available

📝 Test 3: Generate Prompts
✅ DEFAULT: 1555 characters - Text correctly embedded
✅ CONCISE: 661 characters - Text correctly embedded
✅ DETAILED: 3590 characters - Text correctly embedded
✅ MULTILINGUAL: 1600 characters - Text correctly embedded

📝 Test 4: Validation Prompt
✅ Validation prompt generated: 1107 characters

📝 Test 5: Error Handling
✅ Correctly raised ValueError for invalid variants

📝 Test 6: Prompt Templates Validation
✅ All templates have {text} placeholder
✅ Multilingual templates have {source_language} placeholder

📝 Test 7: Integration Test (Simulated Workflow)
✅ Integration test successful

======================================================================
🎉 ALL TESTS PASSED!
======================================================================
```

---

## 📚 File Differenze

### Prima (Hardcoded)
```python
# scripts/3_create_chunks_with_llama.py
extraction_prompt = f"""Analyze this spiritual teaching transcript...
TEXT:
{section_text[:2000]}
Generate a JSON response with: ...
"""
```

### Dopo (Configurabile)
```python
# scripts/3_create_chunks_with_llama.py
from chunk_prompts_config import get_chunk_prompt, CHUNK_SYSTEM_PROMPT

extraction_prompt = get_chunk_prompt(
    text=section_text[:2000],
    variant=self.prompt_variant,
    source_language="English"
)
```

---

## 🎉 Vantaggi

✅ **Flessibilità**: 4 varianti per casi d'uso diversi  
✅ **Manutenibilità**: Prompt centralizzati in un file  
✅ **Qualità**: Variant "detailed" per training data premium  
✅ **Velocità**: Variant "concise" per grandi dataset  
✅ **Validazione**: Sistema di quality check automatico  
✅ **Backward Compatible**: Funziona anche senza il nuovo sistema  
✅ **Testato**: Test suite completa che verifica tutto  

---

## 📞 Supporto

Per modificare i prompt:
1. Apri `Prompt/chunk_prompts_config.py`
2. Modifica le costanti `CHUNK_ANALYSIS_*`
3. Testa con `python scripts/test_chunk_prompts.py`
4. Usa nel script 3 con `--prompt-variant [variant]`

Per aggiungere nuove varianti:
1. Aggiungi costante `CHUNK_ANALYSIS_NUOVA` in `chunk_prompts_config.py`
2. Aggiungi a dizionario in `get_chunk_prompt()`
3. Aggiungi descrizione in `get_variant_description()`
4. Aggiungi a `get_available_variants()`
5. Aggiungi a choices in `scripts/3_create_chunks_with_llama.py` argparse

---

**Creato**: 2025-01-27  
**Versione**: 1.0.0  
**Status**: ✅ COMPLETATO E TESTATO
