"""
Creazione Automatica Chunks RAG con Ollama - TEKLAB AI
====================================================================

Legge documentazione tecnica Teklab e genera chunk strutturati JSON con:
- Messages (system/user/assistant)
- Metadata tecnica (prodotti, specifiche, applicazioni)
- Keywords tecniche, quotes importanti
- Q&A pairs per assistenza tecnica

Usa Ollama + llama3.2:3b per generazione veloce di metadata
Ottimizzato per documentazione industriale B2B (sensori livello liquido)
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
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))  # Per chunk_prompts_config

# Import Ollama client
try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  requests non disponibile - installa con: pip install requests")

# Configurazioni Path Base - TEKLAB
FONTI_BASE = PROJECT_ROOT / "Fonti" / "Autori" / "Teklab"  # Path diretto a Teklab

# Ollama settings
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Funzioni per gestione documentazione Teklab
def get_teklab_files() -> List[Path]:
    """Restituisce tutti i file di documentazione Teklab (.txt, .html)
    
    Cerca in:
    - Fonti/Autori/Teklab/*.txt|.html (root)
    - Fonti/Autori/Teklab/Dal Catalogo/TXT/*.txt
    - Fonti/Autori/Teklab/Dal Sito/**/*.html
    """
    if not FONTI_BASE.exists():
        print(f"❌ Cartella Teklab non trovata: {FONTI_BASE}")
        return []
    
    files = []
    
    # 1. File nella root Teklab
    for ext in ['*.txt', '*.html', '*.htm']:
        files.extend(FONTI_BASE.glob(ext))
    
    # 2. File in Dal Catalogo/TXT/
    catalogo_txt = FONTI_BASE / "Dal Catalogo" / "TXT"
    if catalogo_txt.exists():
        files.extend(catalogo_txt.glob("*.txt"))
    
    # 3. File in Dal Sito/ (ricorsivo)
    dal_sito = FONTI_BASE / "Dal Sito"
    if dal_sito.exists():
        for ext in ['*.html', '*.htm']:
            files.extend(dal_sito.rglob(ext))  # rglob = ricorsivo
    
    return sorted(set(files))  # Rimuovi duplicati e ordina

def get_teklab_categories() -> Dict[str, List[Path]]:
    """Raggruppa file Teklab per categoria prodotto
    
    Returns:
        Dict con categories: 'Oil_Level_Regulators', 'Level_Switches', 'Sensors', 'Support', 'General'
    """
    files = get_teklab_files()
    categories = {
        'Oil_Level_Regulators': [],  # TK3+, TK4, TK4MB
        'Level_Switches': [],         # TK1+, LC-XT, LC-XP, LC-PH, LC-PS, Rotalock
        'Sensors': [],                # K25, K11, ATEX
        'Support': [],                # Adapters, Communication, Guides
        'General': []                 # Company info, other docs
    }
    
    for file in files:
        filename = file.name.lower()
        parent = file.parent.name.lower()
        
        # Oil Level Regulators: TK3+, TK4, TK4MB (tutti con 46/80/130 bar)
        if any(x in filename for x in ['tk3+', 'tk3 ', 'tk4 ', 'tk4mb']):
            categories['Oil_Level_Regulators'].append(file)
        
        # Level Switches: TK1+, LC series, Rotalock
        elif any(x in filename for x in ['tk1+', 'tk1 ', 'lc-ps', 'lc-ph', 'lc-xp', 'lc-xt', 'lc ps', 'lc ph', 'lc xp', 'lc xt', 'rotalock']):
            categories['Level_Switches'].append(file)
        
        # Sensors: K25, K11, ATEX
        elif any(x in filename for x in ['k25', 'k11', 'atex']):
            categories['Sensors'].append(file)
        
        # Support: Adapters, Communication, Guides
        elif any(x in filename for x in ['adapter', 'communication', 'innovative', 'guide', 'faq', 'troubleshooting']):
            categories['Support'].append(file)
        
        # General: Company presentation, catalogs, other
        elif any(x in filename for x in ['presentazione', 'catalogue', 'catalog', 'company', 'compressor']):
            categories['General'].append(file)
        
        # Fallback: se dal sito web, probabilmente general
        elif 'dal sito' in str(file.parent).lower():
            categories['General'].append(file)
        
        else:
            categories['General'].append(file)
    
    return categories
    
    return categories

def select_work_interactive() -> Optional[Dict[str, Path]]:
    """Selezione interattiva categoria Teklab"""
    categories = get_teklab_categories()
    
    # Rimuovi categorie vuote
    categories = {k: v for k, v in categories.items() if v}
    
    if not categories:
        print("❌ Nessun file trovato in Fonti/Autori/Teklab/")
        return None
    
    print("\n📚 Categorie prodotti Teklab disponibili:")
    cat_list = list(categories.keys())
    for i, cat in enumerate(cat_list, 1):
        count = len(categories[cat])
        print(f"   {i}. {cat} ({count} file)")
    
    if len(cat_list) == 1:
        selected_cat = cat_list[0]
        print(f"\n✅ Categoria selezionata: {selected_cat}")
    else:
        choice = input(f"\nSeleziona categoria (1-{len(cat_list)}) o 'all' per tutte: ")
        
        if choice.lower() == 'all':
            # Processa tutte le categorie
            return {
                'name': 'All_Categories',
                'originali_path': FONTI_BASE,
                'processati_path': FONTI_BASE / "Processati",
                'files': [f for files in categories.values() for f in files],
                'category': 'all'
            }
        
        try:
            selected_cat = cat_list[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Selezione non valida")
            return None
    
    # Ritorna info categoria selezionata
    return {
        'name': selected_cat,
        'originali_path': FONTI_BASE,
        'processati_path': FONTI_BASE / "Processati" / selected_cat.lower(),
        'files': categories[selected_cat],
        'category': selected_cat.lower()
    }

# Carica system prompt dal prompt_config (REQUIRED - no fallback)
try:
    from prompts_config import SYSTEM_PROMPT
    from chunk_prompts_config import (
        get_chunk_prompt, 
        CHUNK_SYSTEM_PROMPT,
        SEMANTIC_CHUNKING_SYSTEM_PROMPT,
        SEMANTIC_CHUNKING_PROMPT,
        get_available_variants,
        get_variant_description
    )
    print("✅ Prompt Teklab caricati correttamente\n")
except ImportError as e:
    print(f"\n❌ ERRORE CRITICO: Impossibile caricare prompt Teklab!")
    print(f"   Dettaglio: {e}")
    print(f"   Verifica che esistano:")
    print(f"   - Prompt/prompts_config.py")
    print(f"   - Prompt/chunk_prompts_config.py")
    print(f"\n   Impossibile procedere senza prompt Teklab.\n")
    sys.exit(1)


class ChunkCreatorOllama:
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
                raise ValueError("Nessuna categoria selezionata")
        
        self.work_name = work_info['name']
        self.originali_path = work_info['originali_path']
        self.processati_path = work_info['processati_path']
        self.category = work_info.get('category', 'general')
        
        # Salva lista file se fornita (per Teklab)
        self.files_list = work_info.get('files', [])
        
        print(f"\n📚 Categoria: {self.work_name}")
        print(f"   Originali: {self.originali_path}")
        print(f"   Processati: {self.processati_path}")
        if self.files_list:
            print(f"   File da processare: {len(self.files_list)}")
        
        # Salva variante prompt
        self.prompt_variant = prompt_variant
        print(f"\n📝 Prompt variant: {prompt_variant}")
        if get_variant_description:
            print(f"   {get_variant_description(prompt_variant)}")
        
        # Setup checkpoint system
        self.checkpoint_dir = self.processati_path / ".checkpoints"
        self.checkpoint_dir.mkdir(exist_ok=True, parents=True)
        print(f"\n💾 Sistema checkpoint abilitato: {self.checkpoint_dir}")
        
        # Verifica Ollama
        self._check_ollama()
        
        print("=" * 70)
        print()
    
    def _check_ollama(self):
        """Verifica che Ollama sia attivo e il modello disponibile"""
        print("\n🔍 Verifica Ollama...")
        
        if not OLLAMA_AVAILABLE:
            print("❌ requests non disponibile!")
            print("   Installa con: pip install requests")
            sys.exit(1)
        
        try:
            # Test connessione
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            response.raise_for_status()
            
            # Verifica modello
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            
            if not any(OLLAMA_MODEL in name for name in model_names):
                print(f"❌ Modello {OLLAMA_MODEL} non trovato!")
                print(f"   Modelli disponibili: {', '.join(model_names)}")
                print(f"\n   Scarica con: ollama pull {OLLAMA_MODEL}")
                sys.exit(1)
            
            print(f"✅ Ollama attivo con modello {OLLAMA_MODEL}")
            
        except requests.exceptions.ConnectionError:
            print("❌ Ollama non è in esecuzione!")
            print("   Avvia con: ollama serve")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Errore verifica Ollama: {e}")
            sys.exit(1)
    
    def _generate_with_ollama(self, prompt: str, system_prompt: str, max_tokens: int = 1500, temperature: float = 0.3) -> str:
        """Helper function per generazione con Ollama
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            max_tokens: Massimo token da generare
            temperature: Temperature sampling
            
        Returns:
            Risposta generata dal modello
        """
        # Retry logic per timeout
        max_retries = 2
        timeout = 600  # 10 minuti per chunk grandi
        
        for attempt in range(max_retries):
            try:
                payload = {
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.9,
                        "top_k": 50,
                        "num_predict": max_tokens,
                        "repeat_penalty": 1.1
                    }
                }
                
                response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
                response.raise_for_status()
                
                result = response.json()
                return result.get('response', '').strip()
                
            except requests.exceptions.ReadTimeout:
                if attempt < max_retries - 1:
                    print(f"      ⚠️  Timeout (tentativo {attempt + 1}/{max_retries}), riprovo...")
                    continue
                else:
                    print(f"      ❌ Timeout dopo {max_retries} tentativi")
                    return ""
            except Exception as e:
                print(f"      ❌ Errore generazione Ollama: {e}")
                return ""
        
        return ""
    
    def find_transcripts(self, pattern: str = "*.txt") -> List[Path]:
        """Trova tutti i file di documentazione Teklab
        
        Args:
            pattern: Pattern glob per ricerca file (default: "*.txt")
                    Supporta "*.html", "*.htm", "*.pdf"
        
        Returns:
            Lista ordinata di file Path
        """
        if hasattr(self, 'files_list') and self.files_list:
            # Usa lista file fornita dalla selezione interattiva
            return sorted(self.files_list)
        else:
            # Fallback: cerca pattern nella cartella originali
            files = sorted(self.originali_path.glob(pattern))
            # Aggiungi anche HTML se cercavi txt
            if pattern == "*.txt":
                files.extend(sorted(self.originali_path.glob("*.html")))
                files.extend(sorted(self.originali_path.glob("*.htm")))
            return sorted(set(files))  # Rimuovi duplicati e ordina
    
    def extract_file_index(self, filename: str) -> Optional[int]:
        """Estrae indice numerico da filename (se presente)
        
        Supporta formati:
        - TK3_46bar_Manual.txt -> None (usa indice lista)
        - 001_Product_Guide.txt -> 1
        - Product_v2.txt -> 2
        
        Returns:
            Numero estratto o None (verrà usato indice lista)
        """
        # Pattern per numeri espliciti all'inizio
        match = re.search(r'^(\d+)', filename)
        if match:
            return int(match.group(1))
        
        # Pattern per versioni
        match = re.search(r'_v(\d+)', filename, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        return None
    
    def detect_product_family(self, filename: str) -> str:
        """Rileva famiglia prodotto dal filename
        
        Returns:
            'TK_Series', 'LC_Series', 'K25', 'Rotalock', 'ATEX', 'Support', 'General'
        """
        filename_lower = filename.lower()
        
        if any(x in filename_lower for x in ['tk1', 'tk3', 'tk4']):
            return 'TK_Series'
        elif any(x in filename_lower for x in ['lc-ps', 'lc-ph', 'lc-xp', 'lc-xt']):
            return 'LC_Series'
        elif 'k25' in filename_lower:
            return 'K25'
        elif 'rotalock' in filename_lower or 'rlk' in filename_lower:
            return 'Rotalock'
        elif 'atex' in filename_lower:
            return 'ATEX'
        elif any(x in filename_lower for x in ['adapter', 'accessory', 'guide', 'faq', 'support']):
            return 'Support'
        else:
            return 'General'
    
    def load_transcript(self, transcript_path: Path) -> str:
        """Carica contenuto file documentazione (txt o html)"""
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
            # Genera con Ollama (SOSTITUITO)
            response = self._generate_with_ollama(
                prompt=prompt_text,
                system_prompt=system_prompt,
                max_tokens=300,
                temperature=0.2
            )
            
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

        # Genera con Ollama (SOSTITUITO)
        try:
            print("         Generazione metadata con Ollama (30-90 sec)...")
            content = self._generate_with_ollama(
                prompt=extraction_prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.3
            )
            
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
        
        # Genera almeno 2 Q&A pairs di base
        word_count = len(text.split())
        num_qa = max(2, min(5, word_count // 300))
        
        fallback_qa = []
        for i in range(num_qa):
            fallback_qa.append({
                "question": f"What is discussed in this section? (Part {i+1})",
                "answer": text[:300] if i == 0 else f"This section continues exploring the themes introduced earlier. {text[i*300:(i+1)*300]}",
                "difficulty": "beginner",
                "intent": ["understanding_concept"]
            })
        
        return {
            "chunk_title": title or f"teaching_{chunk_num}",
            "key_concepts": ["content analysis", "main topics", "key ideas"],
            "keywords_primary": ["general", "content", "analysis"],
            "iconic_quotes": [],
            "qa_pairs": fallback_qa,
            "natural_questions": ["What is this content about?", "What are the main teachings here?"],
            "summary": text[:300],  # Primi 300 char come summary
            "domain_metadata": {}  # Vuoto di default
        }
    
    def create_chunk_json(
        self, 
        section_text: str, 
        file_index: int, 
        chunk_num: int,
        metadata: Dict
    ) -> Dict:
        """
        Crea struttura JSON completa del chunk per documentazione Teklab
        
        Args:
            section_text: Testo della sezione
            file_index: Indice file (non più day_num)
            chunk_num: Numero chunk
            metadata: Metadata generata da Llama
        
        Returns:
            Dict in formato chunk completo
        """
        # ID chunk con nome file più descrittivo
        safe_title = metadata['chunk_title'].replace(' ', '_').replace('/', '_')[:50]
        chunk_id = f"teklab_chunk_{file_index:03d}_{chunk_num:03d}_{safe_title}"
        
        # Usa la prima domanda naturale o fallback tecnico
        natural_questions = metadata.get('natural_questions', [])
        if natural_questions and len(natural_questions) > 0:
            main_question = natural_questions[0]
        else:
            # Fallback: cerca nelle Q&A pairs
            qa_pairs = metadata.get('qa_pairs', [])
            if qa_pairs and len(qa_pairs) > 0:
                main_question = qa_pairs[0].get('question', 'What are the technical specifications?')
            else:
                main_question = 'What are the technical specifications of this product?'
        
        # Context per user message - TECNICO, non spirituale
        product_family = metadata.get('domain_metadata', {}).get('product_family', 'General')
        # Gestisci se product_family è una lista (Ollama può restituire array)
        if isinstance(product_family, list):
            product_family = product_family[0] if product_family else 'General'
        context_text = f"""Technical documentation context (Teklab industrial products):

[{product_family}] - {metadata.get('chunk_title', 'Product Information')}
Key Specifications: {', '.join(metadata.get('key_concepts', [])[:5])}
📌 Important Details: {' | '.join(metadata.get('iconic_quotes', [])[:2])}

Complete technical text:
{section_text}

---

Question: {main_question}

Respond as an expert Teklab technical sales assistant:
- Provide accurate technical specifications
- Explain product features and applications clearly
- Give installation and configuration guidance
- Focus on PRACTICAL IMPLEMENTATION and compatibility
- Cite pressure ranges, temperatures, certifications when relevant"""

        # Struttura completa chunk - METADATA TEKLAB
        chunk = {
            "id": chunk_id,
            "original_text": section_text,  # TESTO COMPLETO ORIGINALE
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT  # Già modificato per Teklab
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
                "file_index": file_index,
                "file_source": self.work_name,  # Es: "General", "TK_Series"
                "chunk_number": chunk_num,
                "chunk_title": metadata['chunk_title'],
                "manufacturer": "Teklab S.r.l.",
                "document_type": "Technical Documentation",
                "product_category": product_family,
                "key_concepts": metadata.get('key_concepts', []),
                "keywords_primary": metadata.get('keywords_primary', []),
                "keywords_synonyms": {},  # Può essere espanso
                "keywords_relations": {},  # Può essere espanso
                "iconic_quotes": metadata.get('iconic_quotes', []),
                "qa_pairs": metadata.get('qa_pairs', []),  # Q&A COMPLETE
                "natural_questions": metadata.get('natural_questions', []),
                "summary": metadata.get('summary', ''),
                "domain_metadata": metadata.get('domain_metadata', {}),  # pressure_class, refrigerants, etc.
                "applications": [],  # Può essere popolato
                "compatibility": [],  # Compressor brands/models
                "certifications": metadata.get('domain_metadata', {}).get('certifications', []),
                "difficulty_level": "technical",  # beginner/intermediate/advanced
                "content_type": "product_specification",  # specification/installation/troubleshooting
                "target_audience": ["HVAC engineers", "refrigeration technicians", "system integrators"],
                "importance": 0.85,  # Default
                "relevance": 8,  # Default
                "language": "en"  # Detect from text if needed
            }
        }
        
        return chunk
    
    def save_chunk(self, chunk: Dict, file_index: int, output_dir: Optional[Path] = None):
        """
        Salva chunk in file JSON
        
        Args:
            chunk: Dizionario chunk completo
            file_index: Indice file (non più day_num)
            output_dir: Directory output (default: Processati/{category}/chunks/)
        """
        if output_dir is None:
            # Usa product_family se disponibile, altrimenti category
            product_family = chunk.get('metadata', {}).get('product_category', 'general')
            # Gestisci lista da Ollama
            if isinstance(product_family, list):
                product_family = product_family[0] if product_family else 'general'
            safe_family = str(product_family).lower().replace(' ', '_')
            output_dir = self.processati_path / "chunks" / safe_family
        
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
    
    def generate_file_summary(
        self,
        file_index: int,
        product_family: str,
        chunks: List[Dict],
        filename: str,
        output_dir: Optional[Path] = None
    ):
        """
        Genera summary aggregato per file documentazione Teklab
        
        Args:
            file_index: Indice file
            product_family: Famiglia prodotto ('TK_Series', 'LC_Series', etc.)
            chunks: Lista chunk del file
            filename: Nome file originale
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
            
            # Quotes (specifiche tecniche importanti)
            all_quotes.extend(metadata.get('iconic_quotes', []))
            
            # Questions
            all_questions.extend(metadata.get('natural_questions', []))
        
        # Rimuovi duplicati mantenendo ordine
        all_keywords = list(dict.fromkeys(all_keywords))
        all_concepts = list(dict.fromkeys(all_concepts))
        all_quotes = list(dict.fromkeys(all_quotes))
        all_questions = list(dict.fromkeys(all_questions))
        
        # Crea summary
        safe_filename = filename.replace(' ', '_').replace('.', '_')
        summary_label = f"{product_family}: {filename}"
        
        summary = {
            "file_index": file_index,
            "filename": filename,
            "product_family": product_family,
            "summary_label": summary_label,
            "category": self.category,
            "total_chunks": len(chunks),
            "chunk_ids": chunk_ids,
            
            "aggregated_metadata": {
                "all_keywords": all_keywords,
                "all_concepts": all_concepts,
                "technical_specs": all_quotes,  # Specs importanti estratte
                "natural_questions": all_questions
            },
            
            # Metadata primo chunk (per info generali)
            "file_metadata": chunks[0].get('metadata', {}) if chunks else {},
            
            "chunk_files": [
                f"chunks/{product_family.lower()}/{chunk.get('id', '')}.json"
                for chunk in chunks
            ]
        }
        
        # Salva summary
        summary_filename = f"{safe_filename}_summary.json"
        filepath = output_dir / summary_filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=4, ensure_ascii=False)
            print(f"   📊 Summary: {summary_filename}")
        except Exception as e:
            print(f"   ❌ Errore salvataggio summary: {e}")
    
    def process_transcript(
        self, 
        transcript_path: Path,
        file_index: Optional[int] = None,
        max_chunks: Optional[int] = None,
        save: bool = True
    ) -> List[Dict]:
        """
        Processa un file di documentazione Teklab con sistema checkpoint
        
        Args:
            transcript_path: Path al file documentazione (.txt, .html)
            file_index: Indice file nella lista (se None, usa extract_file_index)
            max_chunks: Massimo numero chunk da creare (None = tutti)
            save: Se True, salva chunk su file
        
        Returns:
            Lista di chunk creati
        """
        # Estrai indice file (per checkpoint e organizzazione)
        if file_index is None:
            file_index = self.extract_file_index(transcript_path.name)
            if file_index is None:
                # Usa stem del filename come ID se non c'è numero
                file_index = hash(transcript_path.stem) % 10000  # Hash ridotto a 4 cifre
        
        # Verifica checkpoint esistente
        safe_filename = transcript_path.stem.replace(' ', '_').replace('.', '_')
        checkpoint_file = self.checkpoint_dir / f"file_{safe_filename}_checkpoint.json"
        if checkpoint_file.exists():
            print(f"\n💾 Trovato checkpoint per {transcript_path.name}")
            try:
                with open(checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint_data = json.load(f)
                print(f"   ✅ Ripristinati {len(checkpoint_data['chunks'])} chunk già processati")
                print("   ⏩ Salto questo file (già completato)")
                return checkpoint_data['chunks']
            except Exception as e:
                print(f"   ⚠️  Errore lettura checkpoint: {e}")
                print("   🔄 Riprocesso file da zero...")
        
        # Rileva famiglia prodotto e genera label
        product_family = self.detect_product_family(transcript_path.name)
        file_label = f"{product_family}: {transcript_path.name}"
        
        print(f"\n📄 Processamento: {file_label}")
        print("-" * 70)
        
        # Carica testo
        print("   📖 Caricamento documentazione...")
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
            metadata = self.generate_chunk_metadata(section, file_index, i)
            
            # Crea struttura chunk
            print("      📦 Creazione struttura JSON...")
            chunk = self.create_chunk_json(section, file_index, i, metadata)
            chunks.append(chunk)
            
            # Salva singolo chunk
            if save:
                print("      💾 Salvataggio chunk...")
                self.save_chunk(chunk, file_index)
            
            # CHECKPOINT: Salva progresso dopo ogni chunk
            if save and i % 3 == 0:  # Checkpoint ogni 3 chunk
                print(f"      💾 Checkpoint progresso ({i}/{len(sections)} chunk)...")
                try:
                    checkpoint_data = {
                        'file_index': file_index,
                        'file_label': file_label,
                        'product_family': product_family,
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
            print("\n   💾 Checkpoint finale...")
            try:
                checkpoint_data = {
                    'file_index': file_index,
                    'file_label': file_label,
                    'product_family': product_family,
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
        
        print(f"\n✅ {file_label} completato: {len(chunks)} chunk creati")
        
        # Genera summary aggregato
        if save and chunks:
            self.generate_file_summary(file_index, product_family, chunks, transcript_path.name)
        
        return chunks
    
    def process_multiple_files(
        self, 
        file_indices: Optional[List[int]] = None,
        max_chunks_per_file: Optional[int] = None
    ):
        """
        Processa più file documentazione Teklab in sequenza
        
        Args:
            file_indices: Lista indici file da processare (None = tutti)
            max_chunks_per_file: Max chunk per file (None = tutti)
        """
        print("\n" + "=" * 70)
        print("🚀 CREAZIONE CHUNK TEKLAB CON LLAMA")
        print("=" * 70)
        
        total_chunks = 0
        processed_files = 0
        skipped_files = 0
        
        # Get file list
        files = self.find_transcripts()
        
        if not files:
            print("❌ Nessun file trovato!")
            return
        
        # Filter by indices if provided
        if file_indices:
            files = [f for i, f in enumerate(files, 1) if i in file_indices]
        
        # Verifica checkpoint esistenti
        print(f"\n📋 File da processare: {len(files)}")
        print("\n🔍 Verifica checkpoint esistenti...")
        
        already_done = []
        to_process = []
        
        for file_path in files:
            safe_filename = file_path.stem.replace(' ', '_').replace('.', '_')
            checkpoint_file = self.checkpoint_dir / f"file_{safe_filename}_checkpoint.json"
            
            if checkpoint_file.exists():
                try:
                    with open(checkpoint_file, 'r', encoding='utf-8') as f:
                        checkpoint_data = json.load(f)
                    if checkpoint_data.get('completed', False):
                        already_done.append((file_path, len(checkpoint_data.get('chunks', []))))
                    else:
                        to_process.append(file_path)
                except Exception:
                    to_process.append(file_path)
            else:
                to_process.append(file_path)
        
        if already_done:
            print(f"\n✅ File già completati ({len(already_done)}):")
            for fpath, num_chunks in already_done[:10]:  # Mostra max 10
                print(f"   ✓ {fpath.name} ({num_chunks} chunks)")
            if len(already_done) > 10:
                print(f"   ... e altri {len(already_done) - 10} file")
        
        if to_process:
            print(f"\n📝 File da processare ({len(to_process)}):")
            for fpath in to_process[:10]:  # Mostra max 10
                print(f"   → {fpath.name}")
            if len(to_process) > 10:
                print(f"   ... e altri {len(to_process) - 10} file")
        else:
            print(f"\n🎉 Tutti i {len(files)} file sono già stati processati!")
            print(f"   Totale chunks esistenti: {sum(n for _, n in already_done)}")
            return
        
        print(f"\n{'='*70}")
        
        # Process only files that need it
        for idx, file_path in enumerate(to_process, 1):
            print(f"\n{'='*70}")
            print(f"File {idx}/{len(to_process)}: {file_path.name}")
            print(f"{'='*70}")
            
            # Process file
            chunks = self.process_transcript(
                file_path,
                file_index=idx,
                max_chunks=max_chunks_per_file,
                save=True
            )
            
            if chunks:
                total_chunks += len(chunks)
                processed_files += 1
            else:
                skipped_files += 1
        
        print("\n" + "=" * 70)
        print("✅ ELABORAZIONE COMPLETATA!")
        print(f"   File già completati: {len(already_done)}")
        print(f"   File processati ora: {processed_files}")
        print(f"   File saltati (errori): {skipped_files}")
        print(f"   Totale file: {len(files)}")
        print(f"   Chunk creati ora: {total_chunks}")
        if processed_files > 0:
            print(f"   Media chunk per file: {total_chunks/processed_files:.1f}")
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
    
    # Selezione categoria Teklab
    work_info = None
    if args.author and args.work:
        # CLI mode non supportato - usa selezione interattiva
        print("⚠️  Modalità CLI non disponibile per Teklab")
        print("   Usa selezione interattiva (rimuovi --author e --work)")
        return
    # else: usa selezione interattiva (gestita in ChunkCreator.__init__)
    
    # Determina file da processare
    file_indices = None
    if args.days:
        file_indices = args.days  # Riusa come indici file
    elif args.range:
        file_indices = list(range(args.range[0], args.range[1] + 1))
    else:
        # Default: processa tutti i file (opzionale: chiedi interattivamente)
        print("\n🦙 CHUNK CREATOR TEKLAB - LLAMA RAG")
        print("=" * 70)
        print("\nProcessare tutti i file disponibili?")
        print("  1. Sì, processa tutto")
        print("  2. No, seleziona range file (es: 1-5)")
        
        choice = input("\nScelta [1/2]: ").strip()
        
        if choice == '2':
            start = int(input("File iniziale (indice): "))
            end = int(input("File finale (indice): "))
            file_indices = list(range(start, end + 1))
        # else: file_indices rimane None = processa tutti
    
    # Inizializza creator con variante prompt e work info (OLLAMA)
    creator = ChunkCreatorOllama(
        model_config=args.config,
        prompt_variant=args.prompt_variant,
        work_info=work_info  # None = selezione interattiva
    )
    
    # Processa file Teklab
    creator.process_multiple_files(
        file_indices=file_indices,
        max_chunks_per_file=args.max_chunks
    )


if __name__ == "__main__":
    main()
