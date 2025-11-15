"""
Script per convertire i transcript di Mathias de Stefano in formato Markdown strutturato
Prepara i file per il chunking e gli embeddings del sistema RAG

Struttura Output:
- Metadati YAML frontmatter (per keywords extraction)
- Contenuto strutturato con headers markdown
- Sezioni tematiche identificate automaticamente
- Miglioramento AI del testo (punteggiatura e paragrafi via Ollama)
- Pronto per embedding generation

Author: Pietro
Date: 2025-11-14
Version: 2.1 (con Ollama AI enhancement)
"""

import re
import json
from pathlib import Path
from datetime import datetime
import time

# Import opzionale per Ollama
try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("[WARN] requests non disponibile. Installa con: pip install requests")

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
FONTI_DIR = PROJECT_ROOT / "Fonti" / "Autori"


class TranscriptProcessor:
    """
    Processa i transcript grezzi e li converte in markdown strutturato
    ottimizzato per RAG embeddings.
    Include AI enhancement via Ollama per migliorare punteggiatura e paragrafi.
    
    Supporta struttura multi-autore/multi-libro:
    - Input:  Fonti/Autori/[Autore]/Originali/[Libro]/file.txt
    - Output: Fonti/Autori/[Autore]/Processati/[Libro]/file.md
    """
    
    def __init__(self, use_ai: bool = True, ollama_model: str = "llama3.2:3b"):
        self.stats = {
            "processed": 0,
            "skipped": 0,
            "errors": 0
        }
        self.use_ai = use_ai and OLLAMA_AVAILABLE
        self.ollama_model = ollama_model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.fonti_dir = FONTI_DIR  # Directory base Fonti/Autori
        
        if self.use_ai:
            print(f"[AI] Inizializzazione Ollama (modello: {ollama_model})...")
            try:
                # Test connessione Ollama
                response = requests.post(
                    self.ollama_url,
                    json={"model": ollama_model, "prompt": "test", "stream": False},
                    timeout=20  # Aumentato timeout per primo caricamento modello
                )
                if response.status_code == 200:
                    print("[AI] Ollama connesso e pronto\n")
                else:
                    print(f"[WARN] Ollama risponde ma errore: {response.status_code}")
                    print("      Procedo senza AI enhancement\n")
                    self.use_ai = False
            except Exception as e:
                print(f"[WARN] Ollama non raggiungibile: {e}")
                print("      Assicurati che Ollama sia avviato: ollama serve")
                print("      Procedo senza AI enhancement\n")
                self.use_ai = False
    
    def find_all_transcripts(self):
        """
        Trova tutti i file transcript in tutte le cartelle autori.
        
        Struttura supportata:
        - Input:  Fonti/Autori/[Autore]/[Serie]/**/*.txt
        - Output: Fonti/Autori/[Autore]/Processati/[Serie]/**/*.md
        
        Returns:
            Lista di tuple (input_file_path, output_file_path, author, book_series)
        """
        transcripts = []
        
        if not self.fonti_dir.exists():
            print(f"[ERROR] Directory non trovata: {self.fonti_dir}")
            return transcripts
        
        # Cerca ricorsivamente: Fonti/Autori/**/*.txt
        # Escludi cartelle Processati e cartelle speciali
        for input_file in self.fonti_dir.rglob("*.txt"):
            # Salta se in cartella Processati o nascosta
            if "Processati" in input_file.parts or any(p.startswith('.') for p in input_file.parts):
                continue
            
            parts = input_file.parts
            
            try:
                # Trova indice "Autori"
                autori_idx = parts.index("Autori")
                
                # Struttura: .../ Autori / [Autore] / [Serie] / ... / file.txt
                # Author: cartella subito dopo "Autori"
                author = parts[autori_idx + 1]
                
                # Book series: cartelle tra author e file (può essere multi-livello)
                series_start_idx = autori_idx + 2
                series_end_idx = len(parts) - 1  # esclude filename
                
                if series_end_idx > series_start_idx:
                    book_path_parts = parts[series_start_idx:series_end_idx]
                    book_series = "/".join(book_path_parts)
                else:
                    book_series = "General"
                
                # Costruisci output path: inserisci "Processati" dopo author
                # Input:  Fonti/Autori/[Author]/[Series]/file.txt
                # Output: Fonti/Autori/[Author]/Processati/[Series]/file.md
                output_parts = list(parts[:autori_idx + 2]) + ["Processati"] + list(parts[autori_idx + 2:])
                output_file = Path(*output_parts)
                
                # Cambia estensione .txt -> .md
                output_file = output_file.with_suffix(".md")
                
                transcripts.append((input_file, output_file, author, book_series))
                
            except (ValueError, IndexError):
                print(f"[WARN] Ignorato file con struttura non valida: {input_file}")
                continue
        
        return transcripts
    
    def extract_day_number(self, filename: str) -> int:
        """Estrae il numero del giorno dal nome file (es: Day_1_Transcript.txt -> 1)"""
        match = re.search(r'Day_(\d+)_', filename)
        return int(match.group(1)) if match else 0
    
    def extract_title_from_content(self, content: str, day_number: int) -> str:
        """
        Genera un titolo conciso per il transcript basato sul contenuto principale.
        Restituisce SOLO il tema (senza "Day N -" che viene aggiunto dopo).
        
        Args:
            content: Testo del transcript
            day_number: Numero del giorno
            
        Returns:
            Tema principale (es: "Coherence and Alignment")
        """
        # Cerca patterns di temi spirituali nei primi 500 caratteri
        first_part = content[:500].lower()
        
        # Dizionario pattern -> tema
        themes = {
            'crown': 'Crown Chakra Work',
            'spiritual mind': 'Spiritual Mind Connection',
            'i can': 'I Can - Personal Power',
            'coherence': 'Coherence and Alignment',
            'consciousness': 'Consciousness Journey',
            'mantra': 'Mantra Practice',
            'meditation': 'Guided Meditation',
            'chakra': 'Chakra Activation',
            'portal': 'Portal Opening',
            'alignment': 'Energy Alignment'
        }
        
        # Trova primo tema che matcha
        for pattern, theme in themes.items():
            if pattern in first_part:
                return theme
        
        # Default
        return "Consciousness Work"
    
    def extract_keywords(self, content: str, day_num: int):
        """
        Estrae keywords automaticamente dal contenuto del transcript.
        Usa frequenza termini + termini chiave spirituali.
        """
        keywords = []
        
        # Keywords base sempre presenti
        keywords.extend([
            "Mathias de Stefano",
            "360 days",
            f"Day {day_num}",
            "consciousness",
            "spiritual practice",
            "meditation",
            "pyramid"
        ])
        
        content_lower = content.lower()
        
        # Termini spirituali comuni da cercare
        spiritual_terms = {
            "chakra": "chakras",
            "mantra": "mantras",
            "meditation": "meditation",
            "vibration": "vibrational practice",
            "alignment": "energetic alignment",
            "portal": "portals",
            "consciousness": "consciousness work",
            "crown": "crown chakra",
            "root": "root chakra",
            "heart": "heart chakra",
            "third eye": "third eye",
            "i am": "I AM presence",
            "i can": "I CAN affirmation",
            "breathe": "breathing exercises",
            "atlantean": "Atlantean teachings",
            "giza": "Giza pyramid",
            "sirius": "Sirius alignment",
            "constellation": "constellation work"
        }
        
        for term, keyword in spiritual_terms.items():
            if term in content_lower:
                keywords.append(keyword)
        
        # Estrai eventuali riferimenti ai mesi (hollac, holsu, etc.)
        atlantean_months = re.findall(r'hol\w+', content_lower)
        if atlantean_months:
            keywords.extend([f"month {month}" for month in set(atlantean_months)])
        
        # Limita a 15 keywords più rilevanti
        return list(dict.fromkeys(keywords))[:15]  # Rimuove duplicati preservando ordine
    
    def detect_sections(self, content: str):
        """
        Identifica automaticamente le sezioni tematiche nel transcript.
        Restituisce lista di (titolo_sezione, contenuto_sezione).
        """
        sections = []
        
        # Split per paragrafi
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        current_section = "Introduction"
        current_content = []
        
        for para in paragraphs:
            para_lower = para.lower()
            
            # Identifica cambio di sezione basato su keywords
            new_section = None
            
            if any(keyword in para_lower for keyword in ['we are going to work', 'let\'s understand', 'the structure of']):
                new_section = "Practice Structure"
            elif any(keyword in para_lower for keyword in ['the code of the day', 'code of today']):
                new_section = "Daily Code"
            elif any(keyword in para_lower for keyword in ['mantra', 'statement', 'vibration of the day']):
                new_section = "Daily Practice Elements"
            elif any(keyword in para_lower for keyword in ['meditation', 'close my eyes', 'breathe', 'visualize']):
                new_section = "Guided Meditation"
            elif any(keyword in para_lower for keyword in ['chakra', 'portal', 'crown', 'root']):
                if new_section != "Guided Meditation":
                    new_section = "Energy Work"
            elif any(keyword in para_lower for keyword in ['question', 'q&a', 'ask']):
                new_section = "Q&A"
            
            # Se cambia sezione, salva la precedente
            if new_section and new_section != current_section and current_content:
                sections.append((current_section, '\n\n'.join(current_content)))
                current_section = new_section
                current_content = [para]
            else:
                current_content.append(para)
        
        # Aggiungi ultima sezione
        if current_content:
            sections.append((current_section, '\n\n'.join(current_content)))
        
        return sections
    
    def clean_transcript_text(self, text: str) -> str:
        """
        Pulisce il testo del transcript:
        - Rimuove ripetizioni eccessive (um, uh)
        - Sistema la punteggiatura
        - Unisce righe spezzate in paragrafi coesi
        - Mantiene il tono naturale parlato
        """
        # Rimuovi marker audio [Music], [Applause], etc.
        text = re.sub(r'\[.*?\]', '', text)
        
        # FASE 1: Unisci TUTTE le righe in un flusso continuo
        # (i transcript hanno righe spezzate ovunque)
        text = ' '.join(line.strip() for line in text.split('\n') if line.strip())
        
        # FASE 2: Rimuovi filler words eccessivi
        text = re.sub(r'\b(um|uh)\s+', '', text, flags=re.IGNORECASE)  # Rimuovi tutti um/uh
        text = re.sub(r'\b(like)\s+(?:\1\s+)+', r'\1 ', text, flags=re.IGNORECASE)  # Rimuovi "like like like"
        
        # FASE 3: Sistema spazi multipli
        text = re.sub(r' +', ' ', text)
        
        # FASE 4: Sistema punteggiatura (spazio dopo virgole e punti)
        text = re.sub(r'([.,!?])([^\s\d])', r'\1 \2', text)
        
        # FASE 5: Crea paragrafi logici basati su pause naturali
        # Spezza in paragrafi quando ci sono frasi complete (terminano con .)
        # e la frase successiva inizia con maiuscola o keyword
        sentences = re.split(r'([.!?]+\s+)', text)
        paragraphs = []
        current_para = []
        
        for i in range(0, len(sentences), 2):
            if i >= len(sentences):
                break
            
            sentence = sentences[i]
            separator = sentences[i+1] if i+1 < len(sentences) else ''
            
            current_para.append(sentence + separator)
            
            # Crea nuovo paragrafo ogni 3-5 frasi O se la prossima inizia con keyword
            next_sentence = sentences[i+2] if i+2 < len(sentences) else ''
            is_new_topic = any(next_sentence.lower().startswith(kw) for kw in [
                'the reason', 'another thing', 'remember', 'okay', 
                'so', 'now', 'let\'s', 'today', 'we are going'
            ])
            
            if len(current_para) >= 4 or is_new_topic:
                paragraphs.append(''.join(current_para).strip())
                current_para = []
        
        if current_para:
            paragraphs.append(''.join(current_para).strip())
        
        # FASE 6: Ricomponi con doppi newline tra paragrafi
        text = '\n\n'.join(p for p in paragraphs if p)
        
        # FASE 7: Capitalizza inizio frasi
        text = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
        
        return text.strip()
    
    def enhance_text_with_ai(self, text: str, section_name: str = "") -> str:
        """
        Usa Ollama per strutturare il testo in markdown con sezioni logiche.
        Aggiunge logging dettagliato e timing.
        
        Args:
            text: Testo da strutturare
            section_name: Nome della sezione per contesto
        
        Returns:
            Testo strutturato in markdown con sezioni e paragrafi
        """
        if not self.use_ai or len(text) < 100:
            return text
        
        print(f"\n   [AI-PROC] Inizio elaborazione con Ollama...")
        print(f"   [AI-INFO] Lunghezza testo: {len(text)} caratteri")
        print(f"   [AI-INFO] Sezione: {section_name if section_name else 'Intero transcript'}")
        
        start_time = time.time()
        
        # Prompt ultra-semplificato per massima velocità
        prompt = f"""Add punctuation to this text. Keep ALL words.

{text}

Add periods, commas, paragraphs. Start now:"""
        
        try:
            print("   [AI-CALL] Invio richiesta a Ollama API...")
            call_start = time.time()
            
            # Chiamata Ollama API con timeout esteso per precisione
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Bassa per massima fedeltà
                        "num_predict": 10000,  # Molto alto per testi completi
                        "top_p": 0.95,
                        "top_k": 50,
                        "repeat_penalty": 1.05
                    }
                },
                timeout=1800  # 30 minuti timeout - priorità alla precisione
            )
            
            call_duration = time.time() - call_start
            print(f"   [AI-RESP] Risposta ricevuta in {call_duration:.2f}s")
            
            if response.status_code != 200:
                print(f"   [AI-ERROR] HTTP {response.status_code}, uso testo originale")
                return text
            
            result = response.json()
            improved_text = result.get('response', '').strip()
            
            # Rimuovi eventuali preamble di Ollama
            improved_text = re.sub(r'^(Here is|Here\'s).*?:\s*', '', improved_text, flags=re.IGNORECASE)
            improved_text = improved_text.strip()
            
            # Statistiche output
            print(f"   [AI-STATS] Tokens generati: {result.get('eval_count', 'N/A')}")
            print(f"   [AI-STATS] Tempo generazione: {result.get('eval_duration', 0) / 1e9:.2f}s")
            print(f"   [AI-STATS] Output: {len(improved_text)} caratteri")
            
            # Verifica qualità
            if not improved_text or len(improved_text) < len(text) * 0.4:
                print("   [AI-WARN] Output troppo corto, uso testo originale")
                return text
            
            total_duration = time.time() - start_time
            print(f"   [AI-OK] Completato in {total_duration:.2f}s totali\n")
            
            return improved_text
            
        except requests.Timeout:
            duration = time.time() - start_time
            print(f"   [AI-ERROR] Timeout dopo {duration:.1f}s, uso testo originale")
            return text
        except Exception as e:
            duration = time.time() - start_time
            print(f"   [AI-ERROR] Errore dopo {duration:.1f}s: {e}")
            return text
    
    def structure_content_with_ai(self, text: str, day_num: int, title: str) -> str:
        """
        Usa Ollama per RIORGANIZZARE il contenuto in struttura markdown a 6 sezioni.
        
        IMPORTANTE: NON è un riassunto - mantiene 100% delle informazioni,
        rimuove solo filler words e riorganizza in modo logico.
        
        Args:
            text: Testo pulito da riorganizzare
            day_num: Numero giorno
            title: Titolo del giorno
        
        Returns:
            Contenuto completo riorganizzato in 6 sezioni universali
        """
        if not self.use_ai or len(text) < 100:
            return text
        
        print("\n   [AI-REORGANIZE] Riorganizzazione contenuto (100% info preserved)...")
        print(f"   [AI-INFO] Lunghezza testo originale: {len(text)} caratteri")
        
        start_time = time.time()
        
        prompt = f"""REORGANIZE this Day {day_num} spiritual teaching transcript into well-structured markdown.

TITLE: {title}

ORIGINAL TRANSCRIPT:
{text}

YOUR TASK: Clean up and organize - NOT summarize!

CRITICAL RULES:
1. **PRESERVE 100% OF ALL INFORMATION** - Keep every concept, detail, instruction, name, term
2. ONLY REMOVE: filler words (um, uh, like), [Music] tags, fragmented/incomplete sentences
3. ADD: proper punctuation, paragraph breaks, clear structure
4. REORGANIZE into these 6 universal sections (keep ALL content from original):

## Overview
[Include: context of the day, connection to cycle/series, main goals, structural explanation (12 months, 3 weeks, etc.), alignment details (Sirius/Pyramids), complete introduction - PRESERVE ALL DETAILS]

## Core Teaching
[Include: ALL concepts explained, theories, philosophies, terminology (keep names like Hollac, MA, etc.), chakra explanations, portal system, code of the day, tools, working with temples/plants - ORGANIZE in subsections with ### but KEEP EVERYTHING]

### [Subsection Title]
[Content]

### [Subsection Title]  
[Content]

## Practice
[Include: COMPLETE step-by-step meditation/exercise - EVERY SINGLE STEP from preparation to closing, body scan details, visualization steps, all instructions - THIS MUST BE THE LONGEST SECTION]

### Preparation
[All preparation steps]

### [Practice Phase]
[All steps]

### Closing
[All closing steps]

## Key Insights
[Extract 7-10 most impactful direct quotes as bullet points with **bold** - actual phrases from the text]

## Integration
[Include: how to apply daily, practical suggestions, next steps, connection to ongoing practice - ALL recommendations from the original]

OUTPUT REQUIREMENTS:
- Target length: 90-100% of original character count
- Keep all specific names, terms, numbers, sequences
- Practice section should be comprehensive and detailed
- Use clear markdown: headers ##, subheaders ###, bullet points, **bold** for emphasis
- Maintain spiritual teaching tone

Output the reorganized content in markdown:"""
        
        try:
            print("   [AI-CALL] Riorganizzazione in corso...")
            call_start = time.time()
            
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 12000,
                        "top_p": 0.9,
                        "repeat_penalty": 1.05
                    }
                },
                timeout=1800
            )
            
            call_duration = time.time() - call_start
            print(f"   [AI-RESP] Risposta ricevuta in {call_duration:.2f}s")
            
            if response.status_code != 200:
                print(f"   [AI-ERROR] HTTP {response.status_code}, uso testo originale")
                return text
            
            result = response.json()
            reorganized = result.get('response', '').strip()
            
            # Rimuovi eventuali preamble
            reorganized = re.sub(r'^(Here is|Here\'s|This is|I have|I\'ve).*?:\s*\n*', '', reorganized, flags=re.IGNORECASE | re.MULTILINE)
            reorganized = reorganized.strip()
            
            print(f"   [AI-STATS] Tokens generati: {result.get('eval_count', 'N/A')}")
            print(f"   [AI-STATS] Output: {len(reorganized)} caratteri (originale: {len(text)})")
            
            if len(reorganized) > 0:
                retention = len(reorganized) / len(text) * 100
                print(f"   [AI-STATS] Retention rate: {retention:.1f}%")
                
                if retention < 70:
                    print(f"   [AI-WARN] Retention troppo bassa ({retention:.1f}%) - possibile perdita info")
            
            print(f"   [AI-OK] Completato in {time.time() - start_time:.2f}s totali\n")
            
            if not reorganized:
                print("   [AI-WARN] Output vuoto, uso testo originale")
                return text
            
            return reorganized
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"   [AI-ERROR] Errore dopo {duration:.1f}s: {e}")
            return text
    
    def generate_faq_with_ai(self, content: str, day_num: int, title: str, practice_elements: dict) -> str:
        """
        Genera sezione Q&A basata sul contenuto.
        
        Args:
            content: Contenuto completo (o riassunto) del giorno
            day_num: Numero giorno
            title: Titolo del giorno
            practice_elements: Elementi pratica (mantra, vibration, etc.)
        
        Returns:
            Sezione Q&A in formato markdown
        """
        if not self.use_ai:
            return ""
        
        print("\n   [AI-QA] Generazione sezione Q&A...")
        
        # Prepara summary practice elements
        practice_summary = ""
        if practice_elements:
            practice_summary = "\n".join([f"- {k.title()}: {v}" for k, v in practice_elements.items()])
        
        # Usa solo primi 1500 caratteri del contenuto per FAQ
        content_sample = content[:1500] if len(content) > 1500 else content
        
        prompt = f"""Generate Q&A section for Day {day_num}: {title}

PRACTICE ELEMENTS:
{practice_summary if practice_summary else "None"}

CONTENT SAMPLE:
{content_sample}...

INSTRUCTIONS:
Create 4-6 practical Q&A pairs following this format:

### Q: [Practical question about the practice/teaching]?

[Concise answer based ONLY on the content - 2-3 sentences max]

FOCUS ON:
- How to do the practice
- Common doubts/concerns
- Practical application
- Technical details (chakra, mantra, etc.)

CRITICAL RULES:
1. Base answers ONLY on information in the content
2. DO NOT invent information
3. Keep answers practical and concise
4. Use markdown format: ### Q: ... followed by answer paragraph

Output ONLY the Q&A section:"""
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                        "num_predict": 1500,
                        "top_p": 0.9
                    }
                },
                timeout=300
            )
            
            if response.status_code != 200:
                return ""
            
            result = response.json()
            qa = result.get('response', '').strip()
            
            # Pulisci preamble
            qa = re.sub(r'^(Here (is|are)|Q&A|Questions).*?:\s*', '', qa, flags=re.IGNORECASE | re.MULTILINE)
            
            print(f"   [AI-QA] Generata sezione Q&A: {len(qa)} caratteri")
            
            return qa if qa else ""
            
        except Exception as e:
            print(f"   [AI-QA-ERROR] {e}")
            return ""
    
    def extract_practice_elements(self, content: str):
        """
        Estrae elementi specifici della pratica quotidiana:
        - Mantra
        - Vibration
        - Statement
        - Chakra
        """
        elements = {}
        
        content_lower = content.lower()
        
        # Estrai mantra (cerca pattern più specifici)
        # Pattern 1: "the mantra is X" o "mantra of the month is X"
        mantra_patterns = [
            r'mantra\s+(?:of[^.]*)?is\s+([\w\s]{2,30})(?:\s+for|\.|\n)',
            r'the\s+mantra\s+is\s+([\w\s]{2,30})(?:\s+for|\.|\n)',
            r'mantra:\s*["\']?([\w\s]{2,30})["\']?'
        ]
        
        for pattern in mantra_patterns:
            mantra_match = re.search(pattern, content_lower)
            if mantra_match:
                mantra_text = mantra_match.group(1).strip()
                # Pulisci il mantra da parole di contorno
                mantra_text = re.sub(r'^(a|an|the)\s+', '', mantra_text)
                if len(mantra_text) <= 30 and len(mantra_text.split()) <= 5:
                    elements['mantra'] = mantra_text.upper()
                    break
        
        # Estrai vibrazione (suoni brevi come MA, RA, etc.)
        vibration_patterns = [
            r'vibration\s+of\s+the\s+day\s+(?:today\s+)?is\s+([a-z]{1,4})(?:\s|\.|\n)',
            r'the\s+vibration\s+is\s+([a-z]{1,4})(?:\s|\.|\n)',
            r'vibration:\s*([a-z]{1,4})(?:\s|\.|\n)'
        ]
        
        for pattern in vibration_patterns:
            vibration_match = re.search(pattern, content_lower)
            if vibration_match:
                elements['vibration'] = vibration_match.group(1).strip().upper()
                break
        
        # Estrai statement (frasi tipo "I am...")
        statement_patterns = [
            r'the\s+statement\s+(?:of\s+today\s+)?is\s+([^.\n]{10,100})',
            r'statement:\s*["\']?([^.\n"\']{10,100})["\']?',
            r'statement\s+is\s+([^.\n]{10,100})'
        ]
        
        for pattern in statement_patterns:
            statement_match = re.search(pattern, content_lower)
            if statement_match:
                statement_text = statement_match.group(1).strip()
                # Capitalizza correttamente
                statement_text = statement_text[0].upper() + statement_text[1:] if statement_text else ''
                if len(statement_text) >= 10:
                    elements['statement'] = statement_text
                    break
        
        # Estrai chakra
        chakras = ['crown', 'third eye', 'throat', 'heart', 'solar plexus', 'sacral', 'root']
        for chakra in chakras:
            if chakra in content_lower:
                elements['chakra'] = chakra.title()
                break
        
        return elements
    
    def convert_to_markdown(self, input_file: Path, author: str = None, book_series: str = None) -> str:
        """
        Converte un singolo transcript in markdown strutturato.
        
        Args:
            input_file: Path del file transcript
            author: Nome dell'autore (estratto dalla struttura cartelle)
            book_series: Nome del libro/serie (estratto dalla struttura cartelle)
        
        Returns:
            Contenuto markdown completo
        """
        # Leggi contenuto
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Estrai informazioni DAL CONTENUTO GREZZO (prima della pulizia)
        day_num = self.extract_day_number(input_file.name)
        keywords = self.extract_keywords(content, day_num)
        practice_elements = self.extract_practice_elements(content)
        
        # PULISCI IL CONTENUTO (unisci righe, rimuovi filler, crea paragrafi)
        content_cleaned = self.clean_transcript_text(content)
        
        # Estrai titolo DAL CONTENUTO PULITO
        title = self.extract_title_from_content(content_cleaned, day_num)
        
        # ELABORA CON AI: Riorganizza in 6 sezioni mantenendo 100% info
        if self.use_ai:
            print("   [AI] Riorganizzazione contenuto (preserva tutte le info)...")
            content_structured = self.structure_content_with_ai(content_cleaned, day_num, title)
        else:
            # Fallback senza AI: usa contenuto pulito
            content_structured = content_cleaned
        
        # Usa metadati dinamici o fallback
        author_name = author or "Unknown Author"
        series_name = book_series or "General Collection"
        
        # ========================================================================
        # Costruisci Markdown con YAML Frontmatter
        # ========================================================================
        
        markdown = []
        
        # YAML Frontmatter
        markdown.append("---")
        markdown.append(f"title: \"Day {day_num} - {title}\"")
        markdown.append(f"author: {author_name}")
        markdown.append(f"series: \"{series_name}\"")
        markdown.append(f"day_number: {day_num}")
        markdown.append(f"source: \"{book_series or 'General'}\"")
        markdown.append(f"date_processed: {datetime.now().strftime('%Y-%m-%d')}")
        markdown.append("document_type: \"transcript\"")
        markdown.append("language: \"en\"")
        markdown.append("")
        markdown.append("keywords:")
        for kw in keywords:
            markdown.append(f"  - {kw}")
        markdown.append("")
        
        # Practice Elements
        if practice_elements:
            markdown.append("practice_elements:")
            for key, value in practice_elements.items():
                markdown.append(f"  {key}: \"{value}\"")
            markdown.append("")
        
        markdown.append("---")
        markdown.append("")
        
        # Header principale (usa metadati dinamici)
        markdown.append(f"# Day {day_num} - {title}")
        markdown.append("")
        markdown.append(f"**Author:** {author_name}  ")
        markdown.append(f"**Series:** {series_name}  ")
        markdown.append(f"**Source:** {book_series or 'General'}  ")
        markdown.append("")
        
        # Practice Elements Box (se presenti)
        if practice_elements:
            markdown.append("## Daily Practice Elements")
            markdown.append("")
            for key, value in practice_elements.items():
                markdown.append(f"- **{key.replace('_', ' ').title()}:** `{value}`")
            markdown.append("")
        
        # Contenuto principale strutturato (riassunto con 6 sezioni universali)
        markdown.append(content_structured)
        markdown.append("")
        
        # Sezione Q&A generata automaticamente dall'AI
        if self.use_ai:
            print("   [AI] Generazione Q&A...")
            qa_content = self.generate_faq_with_ai(content_structured, day_num, title, practice_elements)
            if qa_content:
                markdown.append("## Q&A")
                markdown.append("")
                markdown.append(qa_content)
                markdown.append("")
        
        # Footer
        markdown.append("---")
        markdown.append("")
        markdown.append("*Transcript processed for RAG embeddings*")
        markdown.append(f"*Processing date: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        
        return '\n'.join(markdown)
    
    def process_all_transcripts(self, overwrite: bool = False, author_filter: str = None, book_filter: str = None):
        """
        Processa tutti i transcript trovati ricorsivamente in tutte le cartelle autori.
        Crea automaticamente la struttura Processati/ replicando quella di Originali/.
        
        Args:
            overwrite: Se True, sovrascrive i file esistenti
            author_filter: Se specificato, processa solo questo autore
            book_filter: Se specificato, processa solo questo libro/serie
        """
        print("=" * 80)
        print("CONVERSIONE TRANSCRIPT -> MARKDOWN STRUTTURATO (Multi-Autore)")
        print("=" * 80)
        print(f"\nDirectory base: {self.fonti_dir}")
        print(f"Ricerca ricorsiva: Autori/**/Originali/**/*.txt\n")
        
        # Trova tutti i transcript con metadati
        all_transcripts = self.find_all_transcripts()
        
        if not all_transcripts:
            print("[ERROR] Nessun file transcript trovato!")
            print(f"   Verifica struttura: Fonti/Autori/[Nome]/Originali/[Libro]/*.txt")
            return
        
        # Applica filtri opzionali
        if author_filter:
            all_transcripts = [t for t in all_transcripts if author_filter.lower() in t[2].lower()]
            print(f"[FILTER] Autore: {author_filter}")
        
        if book_filter:
            all_transcripts = [t for t in all_transcripts if book_filter.lower() in t[3].lower()]
            print(f"[FILTER] Libro: {book_filter}")
        
        if not all_transcripts:
            print("[WARN] Nessun file trovato con i filtri applicati")
            return
        
        print(f"[OK] Trovati {len(all_transcripts)} transcript da processare\n")
        
        # Raggruppa per autore/libro per logging
        by_author = {}
        for input_file, output_file, author, book in all_transcripts:
            key = f"{author}/{book}"
            by_author.setdefault(key, []).append((input_file, output_file))
        
        print("Struttura da processare:")
        for key, files in by_author.items():
            print(f"  {key}: {len(files)} file")
        print()
        
        # Processa ogni file
        for i, (input_file, output_file, author, book_series) in enumerate(all_transcripts, 1):
            # Crea directory output se non esiste (riproduce struttura)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Skip se esiste e non vogliamo sovrascrivere
            if output_file.exists() and not overwrite:
                print(f"[SKIP] [{i}/{len(all_transcripts)}] {author}/{book_series}/{input_file.name}")
                self.stats["skipped"] += 1
                continue
            
            try:
                print(f"[PROC] [{i}/{len(all_transcripts)}] {author}/{book_series}/{input_file.name}...", end=" ")
                
                # Converti con metadati dinamici
                markdown_content = self.convert_to_markdown(input_file, author, book_series)
                
                # Salva
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                print("OK")
                self.stats["processed"] += 1
                
            except Exception as e:
                print("ERROR")
                print(f"   Errore: {e}")
                self.stats["errors"] += 1
        
        # Statistiche finali
        print("\n" + "=" * 80)
        print("STATISTICHE CONVERSIONE")
        print("=" * 80)
        print(f"[OK] Processati:  {self.stats['processed']}")
        print(f"[SKIP] Skippati:  {self.stats['skipped']}")
        print(f"[ERR] Errori:     {self.stats['errors']}")
        print(f"[TOT] Totale:     {len(all_transcripts)}")
        print("=" * 80)
        
        if self.stats["processed"] > 0:
            # Mostra cartelle processate
            processed_dirs = set()
            for _, output_file, author, book in all_transcripts:
                processed_dirs.add(output_file.parent)
            
            print("\n[OK] File markdown salvati nelle seguenti cartelle:")
            for dir_path in sorted(processed_dirs):
                print(f"   [DIR] {dir_path}")
            
            print("\nProssimi passi:")
            print("   1. Verifica i file markdown generati")
            print("   2. Esegui lo script di generazione embeddings")
            print("   3. Testa il retrieval RAG con query di esempio")
    
    def process_single_file(self, file_path: str, author: str = None, book_series: str = None):
        """
        Riprocessa un singolo file specifico.
        
        Args:
            file_path: Path del file da processare (relativo o assoluto)
            author: Nome autore (opzionale, auto-estratto se None)
            book_series: Nome libro/serie (opzionale, auto-estratto se None)
        
        Returns:
            True se processato con successo, False altrimenti
        """
        input_file = Path(file_path)
        
        if not input_file.exists():
            print(f"[ERROR] File non trovato: {input_file}")
            return False
        
        # Auto-estrai metadati dalla struttura se non forniti
        if not author or not book_series:
            parts = input_file.parts
            try:
                # Trova indice "Autori"
                autori_idx = parts.index("Autori")
                
                # Author: cartella subito dopo "Autori"
                if not author:
                    author = parts[autori_idx + 1]
                
                # Book series: cartelle tra author e file
                if not book_series:
                    series_start_idx = autori_idx + 2
                    series_end_idx = len(parts) - 1
                    
                    if series_end_idx > series_start_idx:
                        book_path_parts = parts[series_start_idx:series_end_idx]
                        book_series = "/".join(book_path_parts)
                    else:
                        book_series = "General"
                        
            except (ValueError, IndexError):
                print("[WARN] Impossibile estrarre metadati dalla struttura cartelle")
                author = author or "Unknown Author"
                book_series = book_series or "General"
        
        # Costruisci output path: inserisci "Processati" dopo author
        # Input:  Fonti/Autori/[Author]/[Series]/file.txt
        # Output: Fonti/Autori/[Author]/Processati/[Series]/file.md
        parts = list(input_file.parts)
        try:
            autori_idx = parts.index("Autori")
            output_parts = parts[:autori_idx + 2] + ["Processati"] + parts[autori_idx + 2:]
            output_file = Path(*output_parts).with_suffix(".md")
        except ValueError:
            # Fallback: salva nella stessa directory con .md
            output_file = input_file.with_suffix(".md")
        
        # Crea directory se necessario
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[PROC] Processamento: {input_file.name}")
        print(f"       Autore: {author}")
        print(f"       Serie: {book_series}")
        
        try:
            markdown_content = self.convert_to_markdown(input_file, author, book_series)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print("[OK] File processato con successo!")
            print(f"[OUT] Output: {output_file}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Errore durante il processamento: {e}")
            import traceback
            traceback.print_exc()
            return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Entry point dello script con supporto multi-autore/multi-libro"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Converti transcript in markdown con AI enhancement e supporto multi-autore',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  # Processa tutti i transcript di tutti gli autori
  python convert_transcripts_to_markdown.py
  
  # Processa solo transcript di Mathias de Stefano
  python convert_transcripts_to_markdown.py --author "Mathias de Stefano"
  
  # Processa solo libro Pyramid.mathias
  python convert_transcripts_to_markdown.py --book "Pyramid.mathias"
  
  # Processa singolo file
  python convert_transcripts_to_markdown.py --file "path/to/Day_1_Transcript.txt"
  
  # Riprocessa tutto con AI enhancement
  python convert_transcripts_to_markdown.py --overwrite
  
  # Processa senza AI (veloce)
  python convert_transcripts_to_markdown.py --no-ai
        """
    )
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disabilita AI enhancement (più veloce ma senza miglioramento testo)'
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Riprocessa anche i file già esistenti'
    )
    parser.add_argument(
        '--author',
        type=str,
        help='Filtra per autore specifico (es: "Mathias de Stefano")'
    )
    parser.add_argument(
        '--book',
        type=str,
        help='Filtra per libro/serie specifico (es: "Pyramid.mathias")'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Processa solo un file specifico (path completo)'
    )
    
    args = parser.parse_args()
    
    # Crea processor con/senza AI
    use_ai = not args.no_ai
    processor = TranscriptProcessor(use_ai=use_ai)
    
    if args.file:
        # Processa singolo file specifico
        processor.process_single_file(args.file)
    else:
        # Processa tutti con filtri opzionali
        processor.process_all_transcripts(
            overwrite=args.overwrite,
            author_filter=args.author,
            book_filter=args.book
        )


if __name__ == "__main__":
    main()
