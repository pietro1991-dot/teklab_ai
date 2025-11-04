"""
Creazione Automatica Chunks RAG con Llama Fine-Tunato
======================================================

Legge trascrizioni originali e genera chunk strutturati JSON con:
- Messages (system/user/assistant)
- Metadata completa
- Keywords, quotes, formulas
- Q&A pairs

Usa automaticamente:
- Ultimo modello fine-tunato se disponibile
- Modello Llama pre-addestrato base altrimenti
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Aggiungi path per import moduli
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))

# Import modello Llama - USA LLAMA 3.2 3B DIRETTAMENTE
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  transformers non disponibile - installa con: pip install transformers")

# Configurazioni Path Base
FONTI_BASE = PROJECT_ROOT / "Fonti" / "Autori"

# Funzioni per gestione dinamica struttura
def get_available_authors() -> List[str]:
    """Restituisce lista autori disponibili"""
    if not FONTI_BASE.exists():
        return []
    return [d.name for d in FONTI_BASE.iterdir() if d.is_dir()]

def get_available_works(author: str) -> List[Dict[str, Path]]:
    """Restituisce lista opere per autore con path originali e processati
    
    Returns:
        List[Dict] con keys: 'name', 'originali_path', 'processati_path'
    """
    author_path = FONTI_BASE / author
    originali_path = author_path / "Originali"
    
    if not originali_path.exists():
        return []
    
    works = []
    for work_dir in originali_path.iterdir():
        if work_dir.is_dir():
            works.append({
                'name': work_dir.name,
                'originali_path': work_dir,
                'processati_path': author_path / "Processati" / work_dir.name
            })
    
    return works

def select_work_interactive() -> Optional[Dict[str, Path]]:
    """Selezione interattiva autore e opera"""
    authors = get_available_authors()
    
    if not authors:
        print("❌ Nessun autore trovato in Fonti/Autori/")
        return None
    
    print("\n📚 Autori disponibili:")
    for i, author in enumerate(authors, 1):
        print(f"   {i}. {author}")
    
    if len(authors) == 1:
        selected_author = authors[0]
        print(f"\n✅ Autore selezionato: {selected_author}")
    else:
        choice = input("\nSeleziona autore (1-{}): ".format(len(authors)))
        try:
            selected_author = authors[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Selezione non valida")
            return None
    
    works = get_available_works(selected_author)
    
    if not works:
        print(f"❌ Nessuna opera trovata per {selected_author}")
        return None
    
    print(f"\n📖 Opere disponibili per {selected_author}:")
    for i, work in enumerate(works, 1):
        print(f"   {i}. {work['name']}")
    
    if len(works) == 1:
        selected_work = works[0]
        print(f"\n✅ Opera selezionata: {selected_work['name']}")
    else:
        choice = input("\nSeleziona opera (1-{}): ".format(len(works)))
        try:
            selected_work = works[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Selezione non valida")
            return None
    
    return selected_work

# Carica system prompt dal prompt_config
try:
    sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))
    from prompts_config import SYSTEM_PROMPT
    from chunk_prompts_config import (
        get_chunk_prompt, 
        CHUNK_SYSTEM_PROMPT,
        SEMANTIC_CHUNKING_SYSTEM_PROMPT,
        SEMANTIC_CHUNKING_PROMPT,
        get_available_variants,
        get_variant_description
    )
except ImportError as e:
    print(f"⚠️  Errore import prompt config: {e}")
    # Fallback se non disponibile
    SYSTEM_PROMPT = """Sei una GUIDA SPIRITUALE esperta con conoscenze approfondite in crescita personale, filosofie spirituali e pratiche di consapevolezza.

MISSION: Fornire insegnamenti profondi e pratici su spiritualità, crescita interiore, meditazione, consapevolezza e connessione con il Sé superiore."""
    CHUNK_SYSTEM_PROMPT = "You are an expert at analyzing spiritual teachings."
    SEMANTIC_CHUNKING_SYSTEM_PROMPT = "You are an expert at text analysis."
    SEMANTIC_CHUNKING_PROMPT = None
    get_chunk_prompt = None
    get_available_variants = lambda: ["default"]
    get_variant_description = lambda v: "Default variant"


class ChunkCreator:
    """Crea chunk strutturati da trascrizioni usando Llama"""
    
    def __init__(
        self, 
        model_config: str = "llama-qlora", 
        prompt_variant: str = "default",
        work_info: Optional[Dict[str, Path]] = None
    ):
        """
        Args:
            model_config: Configurazione modello (default: llama-qlora)
            prompt_variant: Variante prompt per metadata extraction:
                - "default": Balanced quality and speed
                - "concise": Quick extraction
                - "detailed": Maximum quality
                - "multilingual": Language-aware
            work_info: Dict con 'name', 'originali_path', 'processati_path'
                       Se None, usa selezione interattiva
        """
        print("🦙 Inizializzazione Chunk Creator con Llama...")
        print("=" * 70)
        
        # Gestione work info
        if work_info is None:
            work_info = select_work_interactive()
            if work_info is None:
                raise ValueError("Nessuna opera selezionata")
        
        self.work_name = work_info['name']
        self.originali_path = work_info['originali_path']
        self.processati_path = work_info['processati_path']
        
        print(f"\n📚 Opera: {self.work_name}")
        print(f"   Originali: {self.originali_path}")
        print(f"   Processati: {self.processati_path}")
        
        # Salva variante prompt
        self.prompt_variant = prompt_variant
        print(f"\n📝 Prompt variant: {prompt_variant}")
        if get_variant_description:
            print(f"   {get_variant_description(prompt_variant)}")
        
        # Setup checkpoint system
        self.checkpoint_dir = self.processati_path / ".checkpoints"
        self.checkpoint_dir.mkdir(exist_ok=True, parents=True)
        print(f"\n💾 Sistema checkpoint abilitato: {self.checkpoint_dir}")
        
        # Inizializza modello (auto-detect ultimo fine-tuning o base)
        self.model = self._init_model(model_config)
        
        print("=" * 70)
        print()
    
    def _init_model(self, config_name: str):
        """Inizializza Llama 3.2 3B per generazione chunk (MASSIMAMENTE OTTIMIZZATO)"""
        print("\n📦 Caricamento Llama 3.2 3B...")
        
        if not TRANSFORMERS_AVAILABLE:
            print("❌ transformers non disponibile!")
            sys.exit(1)
        
        # Path modello locale
        model_path = PROJECT_ROOT / "ai_system" / "models" / "Llama-3.2-3B-Instruct"
        
        if not model_path.exists():
            print(f"❌ Modello non trovato: {model_path}")
            print("   Esegui: python download_llama_3_2_3b.py")
            sys.exit(1)
        
        print(f"📂 Caricamento da: {model_path}")
        print("⚙️  OTTIMIZZAZIONI: BetterTransformer + torch.compile + SDPA + Gradient Checkpointing")
        
        # Carica tokenizer e modello
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_path))
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            device_map={"": "cuda:0"} if torch.cuda.is_available() else "cpu",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True,
            max_memory={0: "3.5GB"} if torch.cuda.is_available() else None,
            use_cache=True,  # KV-cache per velocità
            attn_implementation="sdpa",  # Scaled Dot Product Attention veloce
        )
        
        # OTTIMIZZAZIONE 1: Gradient Checkpointing (riduce VRAM)
        if torch.cuda.is_available():
            print("   💾 Abilitazione Gradient Checkpointing...")
            try:
                self.model.gradient_checkpointing_enable()
                print("   ✅ Gradient Checkpointing abilitato!")
            except Exception as e:
                print(f"   ⚠️  Gradient Checkpointing non disponibile: {e}")
        
        # OTTIMIZZAZIONE 2: BetterTransformer (15-20% più veloce)
        if torch.cuda.is_available():
            print("   � Applicazione BetterTransformer...")
            try:
                from optimum.bettertransformer import BetterTransformer
                self.model = BetterTransformer.transform(self.model)
                print("   ✅ BetterTransformer applicato (+15-20% velocità)!")
            except ImportError:
                print("   ⚠️  BetterTransformer non disponibile (installa: pip install optimum)")
            except Exception as e:
                print(f"   ⚠️  BetterTransformer non applicabile: {e}")
        
        # OTTIMIZZAZIONE 3: torch.compile (30-40% più veloce)
        if torch.cuda.is_available():
            print("   🚀 Compilazione modello...")
            try:
                self.model = torch.compile(self.model, mode="reduce-overhead")
                print("   ✅ Modello compilato (+30-40% velocità)!")
            except Exception as e:
                print(f"   ⚠️  Compilazione non disponibile: {e}")
        
        print("✅ Llama 3.2 3B caricato con TUTTE le ottimizzazioni!")
        print(f"   Device: {self.model.device}")
        print("   Speedup totale stimato: 2.5-4x rispetto a baseline")
        
        return self.model
    
    def find_transcripts(self, pattern: str = "Day_*_Transcript.txt") -> List[Path]:
        """Trova tutte le trascrizioni originali"""
        transcripts = sorted(self.originali_path.glob(pattern))
        return transcripts
    
    def extract_day_number(self, filename: str) -> Optional[int]:
        """Estrae numero unità (giorno/capitolo/sezione) da filename
        
        Supporta formati:
        - Day_X_Transcript.txt -> X
        - Chapter_X.txt -> X
        - Section_X.txt -> X
        - Part_X.txt -> X
        """
        patterns = [
            r'Day_(\d+)',
            r'Chapter_(\d+)',
            r'Section_(\d+)',
            r'Part_(\d+)',
            r'day(\d+)',
            r'chapter(\d+)',
            r'section(\d+)',
            r'part(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def detect_unit_type(self, filename: str) -> str:
        """Rileva tipo unità dal filename
        
        Returns:
            'day', 'chapter', 'section', 'part', o 'unit'
        """
        filename_lower = filename.lower()
        
        if 'day' in filename_lower:
            return 'day'
        elif 'chapter' in filename_lower or 'capitolo' in filename_lower:
            return 'chapter'
        elif 'section' in filename_lower or 'sezione' in filename_lower:
            return 'section'
        elif 'part' in filename_lower or 'parte' in filename_lower:
            return 'part'
        else:
            return 'unit'  # generico
    
    def load_transcript(self, transcript_path: Path) -> str:
        """Carica contenuto trascrizione"""
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Errore lettura {transcript_path.name}: {e}")
            return ""
    
    def identify_semantic_breakpoints(self, text: str) -> List[int]:
        """
        Usa Llama per identificare breakpoint semantici naturali nel testo
        
        Args:
            text: Testo completo
        
        Returns:
            Lista di posizioni carattere dove spezzare
        """
        total_words = len(text.split())
        
        # Se testo troppo corto, non serve chunking
        if total_words < 500:
            print("      ℹ️  Testo breve (<500 parole), chunk singolo")
            return []
        
        # Divide in "logical lines" più piccole (30-40 parole invece di 50)
        # Questo crea più unità per l'AI
        sentences = re.split(r'(?<=[.!?])\s+', text)
        logical_lines = []
        current_line = []
        current_words = 0
        
        for sent in sentences:
            sent_words = len(sent.split())
            # Limite più basso: 30-40 parole per linea
            if current_words + sent_words > 35 and current_line:
                logical_lines.append(' '.join(current_line))
                current_line = [sent]
                current_words = sent_words
            else:
                current_line.append(sent)
                current_words += sent_words
        if current_line:
            logical_lines.append(' '.join(current_line))
        
        # Se abbiamo meno di 3 linee logiche, il testo è troppo denso o senza punteggiatura
        # In quel caso splittiamo forzatamente ogni ~40 parole
        if len(logical_lines) < 3 and total_words > 500:
            print("      ⚠️  Testo senza punteggiatura adeguata, split forzato ogni 40 parole")
            words = text.split()
            logical_lines = []
            for i in range(0, len(words), 40):
                chunk = ' '.join(words[i:i+40])
                logical_lines.append(chunk)
        
        print(f"      🧠 Analisi semantica: {len(logical_lines)} logical lines, {total_words} parole totali")
        
        # Se ancora abbiamo troppo poche linee, non ha senso fare chunking semantico
        if len(logical_lines) < 3:
            print("      ℹ️  Troppo poche unità semantiche, chunk singolo")
            return []
        
        # Prepara testo con numerazione per l'AI (mostra prime 80 parole per linea)
        numbered_lines = []
        for i, line in enumerate(logical_lines):
            preview = ' '.join(line.split()[:80])
            if len(line.split()) > 80:
                preview += "..."
            numbered_lines.append(f"[Line {i}] {preview}")
        
        numbered_text = "\n\n".join(numbered_lines)
        
        # Limita a 4000 caratteri per context window
        if len(numbered_text) > 4000:
            numbered_text = numbered_text[:4000] + "\n\n[...text continues...]"
        
        # Usa prompt per semantic chunking
        if SEMANTIC_CHUNKING_PROMPT:
            prompt_text = SEMANTIC_CHUNKING_PROMPT.format(text=numbered_text)
            system_prompt = SEMANTIC_CHUNKING_SYSTEM_PROMPT
        else:
            # Fallback prompt
            prompt_text = f"""Analyze this text and identify natural breakpoints where topics/concepts change.
Text has {len(logical_lines)} logical lines. Suggest 2-5 breakpoints for semantic chunking.
Respond with JSON: {{"breakpoints": [3, 8, 15], "reasoning": ["why", "why", "why"]}}

TEXT:
{numbered_text[:3000]}"""
            system_prompt = "You are an expert at text structure analysis."
        
        try:
            # Genera con Llama
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text}
            ]
            
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=300,  # RIDOTTO: 300 token per breakpoint (era 500)
                    temperature=0.2,
                    do_sample=True,
                    top_p=0.9,
                    top_k=50,  # Limita scelte per velocità
                    pad_token_id=self.tokenizer.pad_token_id,
                    num_beams=1,  # Greedy decoding veloce
                )
            
            # Decodifica
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Estrai risposta
            response_marker = "<|start_header_id|>assistant<|end_header_id|>"
            if response_marker in full_output:
                response = full_output.split(response_marker)[-1].strip()
            else:
                response = full_output.split("assistant")[-1].strip()
            
            # Pulisci markdown
            response = response.replace("```json", "").replace("```", "").strip()
            
            # Parse JSON
            try:
                result = json.loads(response)
                breakpoints = result.get("breakpoints", [])
                reasoning = result.get("reasoning", [])
                
                if not breakpoints:
                    print("      ℹ️  AI suggerisce nessun breakpoint (testo coerente)")
                    return []
                
                print(f"      ✅ Breakpoint identificati: {len(breakpoints)}")
                for i, (bp, reason) in enumerate(zip(breakpoints, reasoning)):
                    print(f"         {i+1}. Line {bp}: {reason[:60]}...")
                
                # Valida breakpoints
                valid_breakpoints = [bp for bp in breakpoints if 0 <= bp < len(logical_lines)]
                
                # Converti line index in posizioni carattere nel testo originale
                char_positions = []
                current_pos = 0
                for i, line in enumerate(logical_lines):
                    if i in valid_breakpoints:
                        char_positions.append(current_pos)
                    current_pos += len(line) + 1  # +1 per spazio
                
                return char_positions
                
            except json.JSONDecodeError:
                print("      ⚠️  Risposta non JSON valido, uso chunking tradizionale")
                print(f"         Risposta AI: {response[:200]}")
                return []
            
        except Exception as e:
            print(f"      ⚠️  Errore semantic chunking: {e}")
            return []
    
    def split_into_sections(self, text: str, max_words: int = 800) -> List[str]:
        """
        Divide trascrizione in sezioni semantiche (LEGACY - ora usa identify_semantic_breakpoints)
        
        Args:
            text: Testo completo
            max_words: Massimo parole per sezione
        
        Returns:
            Lista di sezioni
        """
        # Divide per paragrafi
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        sections = []
        current_section = []
        current_words = 0
        
        for para in paragraphs:
            para_words = len(para.split())
            
            # Se paragrafo troppo lungo, aggiungilo come sezione separata
            if para_words > max_words:
                if current_section:
                    sections.append('\n\n'.join(current_section))
                    current_section = []
                    current_words = 0
                sections.append(para)
                continue
            
            # Se aggiungere paragrafo supera limite, salva sezione corrente
            if current_words + para_words > max_words and current_section:
                sections.append('\n\n'.join(current_section))
                current_section = [para]
                current_words = para_words
            else:
                current_section.append(para)
                current_words += para_words
        
        # Aggiungi ultima sezione
        if current_section:
            sections.append('\n\n'.join(current_section))
        
        return sections
    
    def split_by_semantic_breakpoints(self, text: str, breakpoints: List[int]) -> List[str]:
        """
        Divide testo usando breakpoint semantici (posizioni carattere)
        
        Args:
            text: Testo completo
            breakpoints: Lista di posizioni carattere dove spezzare
        
        Returns:
            Lista di sezioni
        """
        if not breakpoints:
            return [text]
        
        sections = []
        start_pos = 0
        
        for bp in sorted(breakpoints):
            if bp > start_pos and bp <= len(text):
                section = text[start_pos:bp].strip()
                if section:  # Evita sezioni vuote
                    sections.append(section)
                start_pos = bp
        
        # Aggiungi ultima sezione
        if start_pos < len(text):
            section = text[start_pos:].strip()
            if section:
                sections.append(section)
        
        return sections if sections else [text]
    
    def generate_chunk_metadata(self, section_text: str, day_num: int, chunk_num: int) -> Dict:
        """
        Genera metadata completa per chunk usando Llama
        
        Args:
            section_text: Testo della sezione
            day_num: Numero giorno
            chunk_num: Numero chunk
        
        Returns:
            Dict con metadata strutturata
        """
        # Calcola dinamicamente quante Q&A servono in base alla complessità
        word_count = len(section_text.split())
        sentence_count = len(re.split(r'[.!?]+', section_text))
        
        # Formula: Q&A basate su lunghezza e densità
        if word_count < 200:
            num_qa_needed = 2
        elif word_count < 400:
            num_qa_needed = 3
        elif word_count < 600:
            num_qa_needed = 4
        elif word_count < 1000:
            num_qa_needed = 5
        else:
            num_qa_needed = max(6, min(10, word_count // 200))  # 1 Q&A ogni 200 parole, max 10
        
        print(f"         📊 Chunk: {word_count} parole → richiedendo {num_qa_needed} Q&A pairs")
        
        # Usa prompt configurabile dal nuovo sistema
        if get_chunk_prompt:
            # Limita testo per context window (max 2000 caratteri)
            text_for_analysis = section_text[:2000]
            
            # Ottieni prompt dalla configurazione
            extraction_prompt = get_chunk_prompt(
                text=text_for_analysis,
                variant=self.prompt_variant,
                source_language="English"
            )
            
            # INIETTA numero Q&A richieste nel prompt
            extraction_prompt = extraction_prompt.replace(
                "Generate VARIABLE number of Q&A pairs",
                f"Generate EXACTLY {num_qa_needed} Q&A pairs"
            )
            
            # System prompt dedicato per chunk creation
            system_prompt = CHUNK_SYSTEM_PROMPT
        else:
            # Fallback a prompt hardcoded se import fallisce
            text_for_analysis = section_text[:2000]
            extraction_prompt = f"""Analyze this spiritual teaching transcript and extract structured metadata.

TEXT:
{text_for_analysis}

Generate EXACTLY {num_qa_needed} comprehensive Q&A pairs (200-400 words each answer).

Generate a JSON response with these fields:
{{
  "chunk_title": "short descriptive title (5-8 words)",
  "key_concepts": ["concept 1", "concept 2", "concept 3"],
  "keywords_primary": ["keyword1", "keyword2", "keyword3"],
  "iconic_quotes": ["quote 1", "quote 2"],
  "qa_pairs": [/* {num_qa_needed} Q&A pairs here */],
  "natural_questions": ["question 1", "question 2"],
  "summary": "2-3 sentence summary of main ideas",
  "domain_metadata": {{}}
}}

IMPORTANT for domain_metadata:
- Analyze the content type and extract ONLY relevant domain-specific metadata
- For spiritual/esoteric: chakra, mantra, element, color, practices
- For philosophy: philosophical_school, key_thinkers, concepts
- For history: time_period, locations, events
- For science: scientific_field, theories, researchers
- Use empty object {{}} if no specific domain metadata applies
- NEVER force metadata that isn't clearly in the text

Respond ONLY with valid JSON - no markdown, no extra text."""
            system_prompt = "You are an expert at analyzing diverse content types and extracting relevant structured metadata. Adapt your analysis to the actual content. Output valid JSON only."

        # Genera con Llama 3.2 3B
        try:
            # Crea messages per Llama
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": extraction_prompt}
            ]
            
            # Apply chat template
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            
            # Generate - OTTIMIZZATO per velocità
            print("         Generazione metadata (1-2 min con ottimizzazioni)...")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1500,  # RIDOTTO da 4000 a 1500 (metadata più concise)
                    temperature=0.3,  # Bassa per consistenza
                    do_sample=True,
                    top_p=0.9,
                    top_k=50,  # Limita scelte per velocità
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    num_beams=1,  # Greedy decoding veloce
                )
            
            # Decode - solo la risposta generata
            input_length = inputs['input_ids'].shape[1]
            generated_tokens = outputs[0][input_length:]
            content = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            
            # Prova a estrarre JSON - sia con regex che con fallback parsing
            try:
                # Prova parsing diretto prima
                metadata_raw = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: cerca pattern JSON con regex
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    try:
                        metadata_raw = json.loads(json_str)
                    except json.JSONDecodeError:
                        # Ultimo tentativo: estrai campi individualmente con regex
                        metadata_raw = self._extract_json_fields_from_text(content)
                else:
                    print("⚠️  Risposta non contiene JSON valido")
                    print(f"   Contenuto generato:\n{content[:500]}")
                    return self._get_fallback_metadata(section_text, day_num, chunk_num)
            
            # Estrai solo i campi che servono
            metadata = {
                "chunk_title": metadata_raw.get("chunk_title", f"teaching_{chunk_num}"),
                "key_concepts": metadata_raw.get("key_concepts", [])[:7],
                "keywords_primary": metadata_raw.get("keywords_primary", [])[:8],
                "iconic_quotes": metadata_raw.get("iconic_quotes", [])[:4],
                "qa_pairs": metadata_raw.get("qa_pairs", []),  # TUTTE le Q&A generate (no limit)
                "natural_questions": metadata_raw.get("natural_questions", [])[:5],
                "summary": metadata_raw.get("summary", ""),
                "domain_metadata": metadata_raw.get("domain_metadata", {})  # Flessibile: accetta qualsiasi struttura o {}
            }
            
            # Log dettagliato con numero Q&A e info qualità
            num_qa = len(metadata.get('qa_pairs', []))
            qa_info = f", {num_qa} Q&A pairs"
            
            # Calcola lunghezza media risposte
            if num_qa > 0:
                avg_answer_length = sum(len(qa.get('answer', '').split()) for qa in metadata['qa_pairs']) / num_qa
                qa_info += f" (~{int(avg_answer_length)} parole/risposta)"
            
            domain_info = ""
            dm = metadata.get('domain_metadata', {})
            if dm:
                # Mostra i campi presenti (es: chakra, philosophical_school, time_period, etc)
                present_fields = [k for k, v in dm.items() if v and (isinstance(v, (list, dict)) and len(v) > 0 or v)]
                if present_fields:
                    domain_info = f", domain: {', '.join(present_fields[:3])}"  # Primi 3 campi
            
            print(f"      ✅ Metadata estratti: {len(metadata.get('key_concepts', []))} concetti, {len(metadata.get('keywords_primary', []))} keywords{domain_info}{qa_info}")
            return metadata
                
        except Exception as e:
            print(f"⚠️  Errore generazione metadata: {e}")
            print(f"   Tipo errore: {type(e).__name__}")
            return self._get_fallback_metadata(section_text, day_num, chunk_num)
    
    def _extract_json_fields_from_text(self, text: str) -> Dict:
        """Estrae campi JSON usando regex quando il parsing fallisce"""
        metadata = {}
        
        # chunk_title
        title_match = re.search(r'"chunk_title"\s*:\s*"([^"]+)"', text)
        if title_match:
            metadata["chunk_title"] = title_match.group(1)
        
        # key_concepts (array)
        concepts_match = re.search(r'"key_concepts"\s*:\s*\[(.*?)\]', text, re.DOTALL)
        if concepts_match:
            concepts_str = concepts_match.group(1)
            metadata["key_concepts"] = [c.strip(' "') for c in re.findall(r'"([^"]+)"', concepts_str)]
        
        # keywords_primary (array)
        keywords_match = re.search(r'"keywords_primary"\s*:\s*\[(.*?)\]', text, re.DOTALL)
        if keywords_match:
            keywords_str = keywords_match.group(1)
            metadata["keywords_primary"] = [k.strip(' "') for k in re.findall(r'"([^"]+)"', keywords_str)]
        
        # iconic_quotes (array)
        quotes_match = re.search(r'"iconic_quotes"\s*:\s*\[(.*?)\]', text, re.DOTALL)
        if quotes_match:
            quotes_str = quotes_match.group(1)
            metadata["iconic_quotes"] = [q.strip(' "') for q in re.findall(r'"([^"]+)"', quotes_str)]
        
        # natural_questions (array)
        questions_match = re.search(r'"natural_questions"\s*:\s*\[(.*?)\]', text, re.DOTALL)
        if questions_match:
            questions_str = questions_match.group(1)
            metadata["natural_questions"] = [q.strip(' "') for q in re.findall(r'"([^"]+)"', questions_str)]
        
        # summary
        summary_match = re.search(r'"summary"\s*:\s*"([^"]+)"', text, re.DOTALL)
        if summary_match:
            metadata["summary"] = summary_match.group(1)
        
        # domain_metadata (cerca oggetto completo, estrae tutto ciò che trova)
        domain_match = re.search(r'"domain_metadata"\s*:\s*(\{.*?\})', text, re.DOTALL)
        if domain_match:
            try:
                # Prova a parsare l'oggetto domain_metadata
                domain_str = domain_match.group(1)
                domain_metadata = json.loads(domain_str)
                # Filtra solo valori non-null e non-empty
                filtered_dm = {k: v for k, v in domain_metadata.items() 
                              if v and (not isinstance(v, (list, dict)) or len(v) > 0)}
                if filtered_dm:
                    metadata["domain_metadata"] = filtered_dm
            except json.JSONDecodeError:
                # Se non parsabile, lascia vuoto
                pass
        
        return metadata
    
    def _get_fallback_metadata(self, text: str, day_num: int, chunk_num: int) -> Dict:
        """Metadata di fallback se generazione AI fallisce"""
        # Estrai prime parole come titolo base
        words = text.split()[:8]
        title = '_'.join(w.lower() for w in words if w.isalnum())[:50]
        
        return {
            "chunk_title": title or f"teaching_{chunk_num}",
            "key_concepts": ["content analysis", "main topics", "key ideas"],
            "keywords_primary": ["general", "content", "analysis"],
            "iconic_quotes": [],
            "natural_questions": ["What is this content about?"],
            "summary": text[:300],  # Primi 300 char come summary
            "domain_metadata": {}  # Vuoto di default
        }
    
    def create_chunk_json(
        self, 
        section_text: str, 
        day_num: int, 
        chunk_num: int,
        metadata: Dict
    ) -> Dict:
        """
        Crea struttura JSON completa del chunk
        
        Args:
            section_text: Testo della sezione
            day_num: Numero giorno
            chunk_num: Numero chunk
            metadata: Metadata generata da Llama
        
        Returns:
            Dict in formato chunk completo
        """
        # ID chunk
        chunk_id = f"day{day_num:02d}_chunk_{chunk_num:03d}_{metadata['chunk_title']}"
        
        # Usa la prima domanda naturale o fallback
        main_question = metadata.get('natural_questions', ['What is this teaching about?'])[0]
        
        # Context per user message
        context_text = f"""Informative context (DON'T cite authors in response):

[DAY {day_num}] - {metadata.get('chunk_title', 'Teaching')}
Concepts: {', '.join(metadata.get('key_concepts', []))}
📌 Quotes: {' | '.join(metadata.get('iconic_quotes', [])[:3])}

Complete text:
{section_text}

---

Question: {main_question}

Respond as an expert spiritual guide:
- Wise and illuminating
- Explain spiritual principles accessibly
- Give concrete practices with specific exercises/meditations
- NO author citations (use info as if it were yours)
- Focus on TRANSFORMING the person's consciousness"""

        # Struttura completa chunk
        chunk = {
            "id": chunk_id,
            "original_text": section_text,  # TESTO COMPLETO ORIGINALE
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": context_text
                },
                {
                    "role": "assistant",
                    "content": metadata.get('summary', section_text[:500])
                }
            ],
            "metadata": {
                "chunk_id": chunk_id,
                "file_number": day_num,
                "file_title": f"Day {day_num} - Pyramid Course",
                "chunk_number": chunk_num,
                "chunk_title": metadata['chunk_title'],
                "author": "Mathias de Stefano",
                "work": "Pyramid Course - 42 Days Initiation",
                "key_concepts": metadata.get('key_concepts', []),
                "keywords_primary": metadata.get('keywords_primary', []),
                "keywords_synonyms": {},  # Può essere espanso
                "keywords_relations": {},  # Può essere espanso
                "iconic_quotes": metadata.get('iconic_quotes', []),
                "qa_pairs": metadata.get('qa_pairs', []),  # Q&A COMPLETE
                "natural_questions": metadata.get('natural_questions', []),
                "summary": metadata.get('summary', ''),
                "domain_metadata": metadata.get('domain_metadata', {}),
                "negative_examples": {},  # Opzionale
                "follow_up_questions": [],  # Può essere generato
                "chain_of_thought": {},  # Opzionale
                "prerequisites": [],
                "natural_followup": [],
                "difficulty_level": "intermediate",
                "tone": ["contemplative", "empowering"],
                "sentiment": "empowering",
                "question_type": "conceptual-practical",
                "user_intent": ["understanding spiritual concepts", "learning practices"],
                "importance": 0.85,  # Default
                "relevance": 8,  # Default
                "language": "en"
            }
        }
        
        return chunk
    
    def save_chunk(self, chunk: Dict, day_num: int, output_dir: Optional[Path] = None):
        """
        Salva chunk in file JSON
        
        Args:
            chunk: Dizionario chunk completo
            day_num: Numero giorno
            output_dir: Directory output (default: Processati/{work_name}/chunks/dayXX)
        """
        if output_dir is None:
            # Crea path dinamico: Processati/{work_name}/chunks/dayXX
            output_dir = self.processati_path / "chunks" / f"day{day_num:02d}"
        
        # Crea directory se non esiste
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Nome file
        chunk_id = chunk['id']
        filename = f"{chunk_id}.json"
        filepath = output_dir / filename
        
        # Salva JSON
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(chunk, f, indent=4, ensure_ascii=False)
            print(f"   ✅ {filename}")
        except Exception as e:
            print(f"   ❌ Errore salvataggio {filename}: {e}")
    
    def generate_unit_summary(
        self,
        unit_num: int,
        unit_type: str,
        chunks: List[Dict],
        output_dir: Optional[Path] = None
    ):
        """
        Genera summary aggregato per unità (giorno/capitolo/sezione)
        
        Args:
            unit_num: Numero unità
            unit_type: Tipo unità ('day', 'chapter', 'section', 'part')
            chunks: Lista chunk dell'unità
            output_dir: Directory output (default: processati_path/summaries/)
        """
        if not chunks:
            return
        
        # Directory output
        if output_dir is None:
            output_dir = self.processati_path / "summaries"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Aggrega metadata da tutti i chunk
        all_keywords = []
        all_concepts = []
        all_quotes = []
        all_questions = []
        chunk_ids = []
        
        for chunk in chunks:
            metadata = chunk.get('metadata', {})
            chunk_ids.append(chunk.get('id', ''))
            
            # Keywords
            all_keywords.extend(metadata.get('keywords_primary', []))
            
            # Concepts
            all_concepts.extend(metadata.get('key_concepts', []))
            
            # Quotes
            all_quotes.extend(metadata.get('iconic_quotes', []))
            
            # Questions
            all_questions.extend(metadata.get('natural_questions', []))
        
        # Rimuovi duplicati mantenendo ordine
        all_keywords = list(dict.fromkeys(all_keywords))
        all_concepts = list(dict.fromkeys(all_concepts))
        all_quotes = list(dict.fromkeys(all_quotes))
        all_questions = list(dict.fromkeys(all_questions))
        
        # Crea summary
        unit_label = {
            'day': f'Day {unit_num}',
            'chapter': f'Chapter {unit_num}',
            'section': f'Section {unit_num}',
            'part': f'Part {unit_num}',
            'unit': f'Unit {unit_num}'
        }.get(unit_type, f'Unit {unit_num}')
        
        summary = {
            "unit_number": unit_num,
            "unit_type": unit_type,
            "unit_label": unit_label,
            "work_name": self.work_name,
            "total_chunks": len(chunks),
            "chunk_ids": chunk_ids,
            
            "aggregated_metadata": {
                "all_keywords": all_keywords,
                "all_concepts": all_concepts,
                "iconic_quotes": all_quotes,
                "natural_questions": all_questions
            },
            
            # Metadata primo chunk (per info generali)
            "unit_metadata": chunks[0].get('metadata', {}) if chunks else {},
            
            "chunk_files": [
                f"chunks/{unit_type}{unit_num:02d}/{chunk.get('id', '')}.json"
                for chunk in chunks
            ]
        }
        
        # Salva summary
        filename = f"{unit_type}{unit_num:02d}_summary.json"
        filepath = output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=4, ensure_ascii=False)
            print(f"   📊 Summary: {filename}")
        except Exception as e:
            print(f"   ❌ Errore salvataggio summary: {e}")
    
    def process_transcript(
        self, 
        transcript_path: Path,
        max_chunks: Optional[int] = None,
        save: bool = True
    ) -> List[Dict]:
        """
        Processa una trascrizione completa con sistema checkpoint
        
        Args:
            transcript_path: Path al file trascrizione
            max_chunks: Massimo numero chunk da creare (None = tutti)
            save: Se True, salva chunk su file
        
        Returns:
            Lista di chunk creati
        """
        # Estrai numero e tipo unità
        unit_num = self.extract_day_number(transcript_path.name)
        if unit_num is None:
            print(f"❌ Impossibile estrarre numero unità da {transcript_path.name}")
            return []
        
        # Verifica checkpoint esistente
        checkpoint_file = self.checkpoint_dir / f"unit_{unit_num}_checkpoint.json"
        if checkpoint_file.exists():
            print(f"\n💾 Trovato checkpoint per Unit {unit_num}")
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint_data = json.load(f)
                print(f"   ✅ Ripristinati {len(checkpoint_data['chunks'])} chunk già processati")
                print("   ⏩ Salto questa unità (già completata)")
                return checkpoint_data['chunks']
            except Exception as e:
                print(f"   ⚠️  Errore lettura checkpoint: {e}")
                print("   🔄 Riprocesso unità da zero...")
        
        unit_type = self.detect_unit_type(transcript_path.name)
        unit_label = {
            'day': f'Day {unit_num}',
            'chapter': f'Chapter {unit_num}',
            'section': f'Section {unit_num}',
            'part': f'Part {unit_num}',
            'unit': f'Unit {unit_num}'
        }.get(unit_type, f'Unit {unit_num}')
        
        print(f"\n📄 Processamento: {unit_label}")
        print("-" * 70)
        
        # Carica testo
        print("   📖 Caricamento trascrizione...")
        text = self.load_transcript(transcript_path)
        if not text:
            return []
        
        print(f"   📏 Lunghezza: {len(text.split())} parole")
        
        # Divide in sezioni usando AI semantic chunking
        print("   ✂️  Divisione semantica...")
        print("   🧠 Fase 1: Identificazione breakpoint con Llama...")
        breakpoints = self.identify_semantic_breakpoints(text)
        
        if breakpoints and len(breakpoints) > 0:
            sections = self.split_by_semantic_breakpoints(text, breakpoints)
            # Verifica che il chunking abbia funzionato
            if sections and len(sections) > 1:
                print(f"   ✅ Chunk semantici creati: {len(sections)}")
            else:
                print("   ⚠️  Semantic chunking non ha prodotto risultati, uso chunking tradizionale")
                sections = self.split_into_sections(text, max_words=600)  # 600 parole invece di 800 per chunk più gestibili
                print(f"   📦 Sezioni create: {len(sections)}")
        else:
            # Fallback a chunking tradizionale con limite più basso per chunk migliori
            print("   ⚠️  Nessun breakpoint semantico, uso chunking tradizionale (600 parole)")
            sections = self.split_into_sections(text, max_words=600)
            print(f"   📦 Sezioni create: {len(sections)}")
        
        # Mostra dimensioni chunk
        for i, section in enumerate(sections, 1):
            words = len(section.split())
            print(f"      Chunk {i}: {words} parole")
        
        # Limita se richiesto
        if max_chunks:
            sections = sections[:max_chunks]
            print(f"   ⚠️  Limitato a {max_chunks} chunk")
        
        # Genera chunk
        print("\n   🤖 Fase 2: Generazione metadata con Llama...")
        chunks = []
        
        for i, section in enumerate(sections, 1):
            print(f"\n   [{i}/{len(sections)}] Chunk {i}...")
            
            # Genera metadata con AI
            print("      🧠 Estrazione metadata...")
            metadata = self.generate_chunk_metadata(section, unit_num, i)
            
            # Crea struttura chunk
            print("      📦 Creazione struttura JSON...")
            chunk = self.create_chunk_json(section, unit_num, i, metadata)
            chunks.append(chunk)
            
            # Salva singolo chunk
            if save:
                print("      💾 Salvataggio chunk...")
                self.save_chunk(chunk, unit_num)
            
            # CHECKPOINT: Salva progresso dopo ogni chunk
            if save and i % 3 == 0:  # Checkpoint ogni 3 chunk
                print(f"      💾 Checkpoint progresso ({i}/{len(sections)} chunk)...")
                try:
                    checkpoint_data = {
                        'unit_num': unit_num,
                        'unit_label': unit_label,
                        'total_chunks': len(sections),
                        'processed_chunks': i,
                        'chunks': chunks
                    }
                    with open(checkpoint_file, 'w', encoding='utf-8') as f:
                        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"      ⚠️  Errore salvataggio checkpoint: {e}")
        
        # CHECKPOINT FINALE: Salva stato completo
        if save:
            print(f"\n   💾 Checkpoint finale...")
            try:
                checkpoint_data = {
                    'unit_num': unit_num,
                    'unit_label': unit_label,
                    'total_chunks': len(sections),
                    'processed_chunks': len(chunks),
                    'chunks': chunks,
                    'completed': True
                }
                with open(checkpoint_file, 'w', encoding='utf-8') as f:
                    json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
                print(f"   ✅ Checkpoint salvato: {checkpoint_file.name}")
            except Exception as e:
                print(f"   ⚠️  Errore salvataggio checkpoint finale: {e}")
        
        print(f"\n✅ {unit_label} completato: {len(chunks)} chunk creati")
        
        # Genera summary aggregato
        if save and chunks:
            self.generate_unit_summary(unit_num, unit_type, chunks)
        
        return chunks
    
    def process_multiple_days(
        self, 
        day_numbers: List[int],
        max_chunks_per_day: Optional[int] = None
    ):
        """
        Processa più unità in sequenza (giorni/capitoli/sezioni)
        
        Args:
            day_numbers: Lista numeri unità da processare
            max_chunks_per_day: Max chunk per unità (None = tutti)
        """
        print("\n" + "=" * 70)
        print("🚀 CREAZIONE CHUNK AUTOMATICA CON LLAMA")
        print("=" * 70)
        
        total_chunks = 0
        processed_units = 0
        
        for unit_num in day_numbers:
            # Trova trascrizione con pattern flessibili
            patterns = [
                f"Day_{unit_num}_*.txt",
                f"Day{unit_num}_*.txt",
                f"Chapter_{unit_num}_*.txt",
                f"Chapter{unit_num}_*.txt",
                f"Section_{unit_num}_*.txt",
                f"Part_{unit_num}_*.txt",
                f"day_{unit_num}_*.txt",
                f"chapter_{unit_num}_*.txt",
            ]
            
            transcripts = []
            for pattern in patterns:
                transcripts = list(self.originali_path.glob(pattern))
                if transcripts:
                    break
            
            if not transcripts:
                print(f"\n⚠️  Unit {unit_num}: trascrizione non trovata")
                continue
            
            # Processa
            chunks = self.process_transcript(
                transcripts[0],
                max_chunks=max_chunks_per_day,
                save=True
            )
            total_chunks += len(chunks)
            processed_units += 1
        
        print("\n" + "=" * 70)
        print("✅ COMPLETATO!")
        print(f"   Unità processate: {processed_units}")
        print(f"   Chunk totali creati: {total_chunks}")
        print("=" * 70)


def main():
    """Script principale"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Crea chunk RAG automatici da trascrizioni usando Llama"
    )
    parser.add_argument(
        '--author',
        type=str,
        default=None,
        help='Nome autore (default: selezione interattiva)'
    )
    parser.add_argument(
        '--work',
        type=str,
        default=None,
        help='Nome opera (default: selezione interattiva)'
    )
    parser.add_argument(
        '--days',
        type=int,
        nargs='+',
        help='Numeri giorni da processare (es: --days 1 2 3)'
    )
    parser.add_argument(
        '--range',
        type=int,
        nargs=2,
        metavar=('START', 'END'),
        help='Range giorni da processare (es: --range 1 10)'
    )
    parser.add_argument(
        '--max-chunks',
        type=int,
        default=None,
        help='Massimo chunk per giorno (default: tutti)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='llama-qlora',
        choices=['llama-2-7b', 'llama-3-8b', 'llama-qlora'],
        help='Configurazione modello (default: llama-qlora)'
    )
    parser.add_argument(
        '--prompt-variant',
        type=str,
        default='default',
        choices=['default', 'concise', 'detailed', 'multilingual'],
        help='Variante prompt per metadata extraction (default: default)'
    )
    
    args = parser.parse_args()
    
    # Mostra info varianti prompt disponibili
    if get_available_variants:
        print("\n📝 Prompt Variants Available:")
        for variant in get_available_variants():
            desc = get_variant_description(variant) if get_variant_description else ""
            marker = "✓" if variant == args.prompt_variant else " "
            print(f"   [{marker}] {variant}: {desc}")
        print()
    
    # Selezione opera
    work_info = None
    if args.author and args.work:
        # Usa argomenti CLI
        works = get_available_works(args.author)
        work_info = next((w for w in works if w['name'] == args.work), None)
        if work_info is None:
            print(f"❌ Opera '{args.work}' non trovata per autore '{args.author}'")
            print(f"   Opere disponibili: {[w['name'] for w in works]}")
            return
    # else: usa selezione interattiva (gestita in ChunkCreator.__init__)
    
    # Determina giorni da processare
    if args.days:
        day_numbers = args.days
    elif args.range:
        day_numbers = list(range(args.range[0], args.range[1] + 1))
    else:
        # Default: chiedi interattivamente
        print("\n🦙 CHUNK CREATOR - LLAMA RAG")
        print("=" * 70)
        print("\nScegli giorni da processare:")
        print("  1. Singolo giorno")
        print("  2. Range giorni (es: 1-10)")
        print("  3. Tutti i giorni disponibili")
        
        choice = input("\nScelta [1/2/3]: ").strip()
        
        if choice == '1':
            day = int(input("Numero giorno: "))
            day_numbers = [day]
        elif choice == '2':
            start = int(input("Giorno iniziale: "))
            end = int(input("Giorno finale: "))
            day_numbers = list(range(start, end + 1))
        elif choice == '3':
            day_numbers = list(range(1, 366))  # Max range, script skipperà file mancanti
        else:
            print("❌ Scelta non valida")
            return
    
    # Inizializza creator con variante prompt e work info
    creator = ChunkCreator(
        model_config=args.config,
        prompt_variant=args.prompt_variant,
        work_info=work_info  # None = selezione interattiva
    )
    
    # Processa
    creator.process_multiple_days(
        day_numbers=day_numbers,
        max_chunks_per_day=args.max_chunks
    )


if __name__ == "__main__":
    main()
