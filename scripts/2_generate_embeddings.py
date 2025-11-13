"""
Generatore di Embeddings per RAG Chatbot - Teklab B2B AI
Genera embeddings di tutti i chunks (5 categorie: Oil_Level_Regulators, Level_Switches, Sensors, Support, General) e Q&A
Esegui quando aggiungi nuovi prodotti o contenuti tecnici
"""

import re
import pickle
from pathlib import Path

# Lazy import per velocizzare startup
SentenceTransformer = None

def import_sentence_transformers():
    """Import lazy di SentenceTransformer per velocizzare startup"""
    global SentenceTransformer
    if SentenceTransformer is None:
        try:
            print("🔄 Caricamento librerie (prima volta può richiedere 10-30 secondi)...")
            from sentence_transformers import SentenceTransformer as ST
            SentenceTransformer = ST
            print("✅ Librerie caricate\n")
            return True
        except ImportError:
            print("❌ Installare prima: pip install sentence-transformers scikit-learn")
            return False
    return True

# Configurazione (deve stare dopo gli import)
SCRIPT_DIR = Path(__file__).parent  # scripts/
PROJECT_ROOT = SCRIPT_DIR.parent  # Root del progetto (teklab_ai/)
FONTI_BASE_PATH = PROJECT_ROOT / "Fonti"  # ✅ NUOVA STRUTTURA: File unificati COMPLETE.md direttamente in Fonti/
EMBEDDINGS_CACHE_PATH = PROJECT_ROOT / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"  # ✅ TEKLAB cache

# Modello embeddings - Ottimizzato per tecnico IT+EN
EMBEDDING_MODEL = 'intfloat/multilingual-e5-base'  # ✅ PROVATO: miglior trade-off qualità/velocità
# Alternative testate:
# 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'  # ❌ Score troppo bassi
# 'all-MiniLM-L6-v2'  # Solo inglese, più veloce
# 'all-mpnet-base-v2'  # Buon tuttofare, ma meno specializzato
# 'all-MiniLM-L6-v2'  # Più veloce ma meno preciso (384-dim)

# ============================================================================
# 🛠️ FIX: Normalizza chunk IDs per eliminare typo e caratteri duplicati
# ============================================================================
def normalize_chunk_id(text):
    """
    Normalizza chunk IDs per prevenire typo e caratteri duplicati.
    
    Fix comuni:
    - Rimuove caratteri duplicati (||, __, etc.)
    - Corregge typo comuni nei nomi file
    - Normalizza spacing
    
    Args:
        text: Testo da normalizzare (chunk_id)
    
    Returns:
        Testo normalizzato senza typo
    """
    import re
    
    # 1. Rimuovi estensione .md se presente
    text = text.replace('.md', '')
    
    # 2. Fix caratteri duplicati
    text = re.sub(r'_+', '_', text)   # ___ → _
    text = re.sub(r'\|+', '|', text)  # || → |
    text = re.sub(r'\s+', ' ', text)  # spazi multipli → spazio singolo
    
    # 3. Fix typo comuni (AGGIUNGI QUI ALTRI TYPO CHE TROVI)
    typo_map = {
        'Dimensionns': 'Dimensions',
        'Dimenssions': 'Dimensions',
        'Dimensiions': 'Dimensions',
        'Keywordds': 'Keywords',
        'Keyworrds': 'Keywords',
        'Specifiications': 'Specifications',
        'Specificaations': 'Specifications',
        'Speciffiications': 'Specifications',
        'Featurees': 'Features',
        'Featurres': 'Features',
        'Orderinng': 'Ordering',
        'Orderiing': 'Ordering',
        'chunkk': 'chunk',
        'chhunk': 'chunk',
        'chuunk': 'chunk',
        'chunk__': 'chunk_',   # Doppio underscore
        'chunnk': 'chunk',
        'idxx': 'idx',
        'iidx': 'idx'
    }
    
    for typo, correct in typo_map.items():
        text = text.replace(typo, correct)
    
    # 4. Strip whitespace finale
    text = text.strip()
    
    return text

class EmbeddingsGenerator:
    """
    Generatore di Embeddings ottimizzato per RAG basato su domande.
    Crea vettori specifici per ogni domanda e coppia Q&A, mappandoli 
    al chunk di testo originale.
    """
    def __init__(self):
        self.model = None
        self.chunks_data = {}           # {chunk_id: chunk_data}
        self.embeddings = {}            # {embedding_id: vector}
        self.embedding_to_chunk_id = {} # {embedding_id: chunk_id}
    
    def _load_model(self):
        """Carica modello embeddings (lazy loading)"""
        if self.model is None:
            if not import_sentence_transformers():
                return False
            print("🧠 Inizializzazione modello embeddings...")
            print(f"   Modello: {EMBEDDING_MODEL}")
            print("   Device: CPU (GPU riservata per Llama)")
            self.model = SentenceTransformer(EMBEDDING_MODEL, device='cpu')
            print("✅ Modello caricato su CPU\n")
        return True
    
    def find_all_rag_folders(self):
        """
        Trova tutti i file markdown nella nuova struttura Fonti/ (file unificati COMPLETE.md):
        - TK3_SERIES_COMPLETE.md (Oil_Level_Regulators)
        - TK4_SERIES_COMPLETE.md (Oil_Level_Regulators)
        - TK4_MB_SERIES_COMPLETE.md (Oil_Level_Regulators)
        - LC_PH_COMPLETE.md, LC_PS_COMPLETE.md, LC_XT_XP_COMPLETE.md, TK1_COMPLETE.md, ROTALOCK_COMPLETE.md (Level_Switches)
        - K11_COMPLETE.md, K25_COMPLETE.md, ATEX_COMPLETE.md (Sensors)
        - ADAPTERS_COMPLETE.md (Adapters)
        """
        markdown_files = []
        
        if not FONTI_BASE_PATH.exists():
            print(f"❌ Cartella base non trovata: {FONTI_BASE_PATH}")
            return []
        
        # Mappa nome file → categoria (per classificazione automatica)
        file_to_category = {
            # Oil Level Regulators
            "TK3_SERIES_COMPLETE.md": ("Oil_Level_Regulators", "TK3_Series"),
            "TK4_SERIES_COMPLETE.md": ("Oil_Level_Regulators", "TK4_Series"),
            "TK4_MB_SERIES_COMPLETE.md": ("Oil_Level_Regulators", "TK4_MB_Series"),
            
            # Level Switches
            "LC_PH_COMPLETE.md": ("Level_Switches", "LC_PH"),
            "LC_PS_COMPLETE.md": ("Level_Switches", "LC_PS"),
            "LC_XT_XP_COMPLETE.md": ("Level_Switches", "LC_XT_XP"),
            "TK1_COMPLETE.md": ("Level_Switches", "TK1"),
            "ROTALOCK_COMPLETE.md": ("Level_Switches", "Rotalock"),
            
            # Sensors
            "K11_COMPLETE.md": ("Sensors", "K11"),
            "K25_COMPLETE.md": ("Sensors", "K25"),
            "ATEX_COMPLETE.md": ("Sensors", "ATEX"),
            
            # Adapters
            "ADAPTERS_COMPLETE.md": ("Adapters", "Adapters"),
        }
        
        # Scansiona tutti i file .md nella cartella Fonti/
        for md_file in FONTI_BASE_PATH.glob("*.md"):
            filename = md_file.name
            
            if filename in file_to_category:
                category, product = file_to_category[filename]
                markdown_files.append({
                    "path": md_file,
                    "category": category,
                    "product": product,
                    "doc_type": "unified_complete",
                    "source": "Teklab"
                })
            else:
                # File non riconosciuto → categoria generica
                print(f"   ⚠️  File non mappato: {filename} (categoria: General)")
                markdown_files.append({
                    "path": md_file,
                    "category": "General",
                    "product": md_file.stem.replace("_COMPLETE", ""),
                    "doc_type": "unified_complete",
                    "source": "Teklab"
                })
        
        return markdown_files
    
    def load_all_data(self):
        """
        Carica tutti i file markdown dalla nuova struttura Teklab.
        Estrae keywords, FAQ e contenuto per creare embeddings.
        """
        print("📚 Caricamento dati Teklab dalla nuova struttura...\n")
        
        markdown_files = self.find_all_rag_folders()
        
        if not markdown_files:
            print("❌ Nessun file markdown trovato!")
            print(f"   Verifica che esistano file .md in: {FONTI_BASE_PATH}")
            return False
        
        print(f"✅ Trovati {len(markdown_files)} file markdown:\n")
        
        total_documents = 0
        category_stats = {}
        
        for file_info in markdown_files:
            md_file = file_info["path"]
            category = file_info["category"]
            
            if category not in category_stats:
                category_stats[category] = 0
            
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # ✅ FIX: Normalizza il nome file per eliminare typo
                    normalized_filename = normalize_chunk_id(md_file.stem)
                    
                    # Crea un documento strutturato per ogni file markdown
                    chunk_id = f"{category}_{normalized_filename}"
                    
                    # Estrai sezioni dal markdown
                    doc_data = {
                        "id": chunk_id,
                        "source_file": str(md_file.relative_to(FONTI_BASE_PATH)),
                        "category": category,
                        "title": normalized_filename.replace("_", " "),  # ✅ Usa nome normalizzato
                        "content": content,
                        "metadata": self._extract_metadata_from_markdown(content)
                    }
                    
                    self.chunks_data[chunk_id] = doc_data
                    category_stats[category] += 1
                    total_documents += 1
                    
            except Exception as e:
                print(f"      ⚠️  Errore lettura {md_file.name}: {e}")
        
        print(f"\n{'='*60}")
        print("📊 DOCUMENTI CARICATI:")
        for cat, count in sorted(category_stats.items()):
            print(f"   • {cat}: {count} file")
        print(f"   • TOTALE: {total_documents} documenti")
        print(f"{'='*60}\n")
        
        return total_documents > 0
    
    def _extract_metadata_from_markdown(self, content):
        """
        Estrae metadati strutturati dal contenuto markdown:
        - Keywords da YAML frontmatter (PRIORITÀ) o sezioni markdown
        - FAQ sections (Q&A pairs)
        - Domande naturali (titoli delle FAQ)
        
        OTTIMIZZAZIONI BATCH 1:
        - ✅ Fix Regex ReDoS (pattern Q&A più veloce)
        - ✅ YAML frontmatter extraction (keyword boost +30-50%)
        """
        import re
        
        metadata = {
            "keywords": [],
            "qa_pairs": [],
            "natural_questions": []
        }
        
        # ========================================================================
        # 🔴 CRITICO: YAML FRONTMATTER EXTRACTION (Priorità 1)
        # ========================================================================
        # Estrai keywords da YAML frontmatter (presente in TUTTI i file Teklab)
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        yaml_match = re.search(yaml_pattern, content, re.DOTALL | re.MULTILINE)
        
        if yaml_match:
            try:
                yaml_content = yaml_match.group(1)
                
                # Parse manuale YAML keywords (evita dipendenza da pyyaml)
                # Supporta sia formato lista che stringa:
                # keywords:
                # - keyword1
                # - keyword2
                # keywords: keyword1, keyword2, keyword3
                
                # Trova sezione keywords
                kw_match = re.search(r'keywords:\s*\n((?:\s*-\s*.+\n)+)', yaml_content, re.MULTILINE)
                if kw_match:
                    # Formato lista (- keyword)
                    kw_list = re.findall(r'-\s*(.+)', kw_match.group(1))
                    metadata["keywords"].extend([k.strip() for k in kw_list if k.strip()])
                else:
                    # Formato stringa singola (keywords: kw1, kw2, kw3)
                    kw_match = re.search(r'keywords:\s*(.+)', yaml_content)
                    if kw_match:
                        keywords = [k.strip() for k in kw_match.group(1).split(',') if k.strip()]
                        metadata["keywords"].extend(keywords)
                        
            except Exception as e:
                # Fallback silenzioso a metodo markdown
                pass
        
        # ========================================================================
        # FALLBACK: Estrai keywords da sezioni markdown (se YAML vuoto)
        # ========================================================================
        if not metadata["keywords"]:
            keywords_pattern = r'\*\*(?:Primary|Secondary|Application|Technical|Compatibility|Competitive|Corporate|Selection) Keywords\*\*:?\s*([^\n]+(?:\n(?!\*\*)[^\n]+)*)'
            keywords_matches = re.findall(keywords_pattern, content, re.IGNORECASE | re.MULTILINE)
            
            for kw_text in keywords_matches:
                # Split per virgole e pulisci
                keywords = [k.strip() for k in kw_text.split(',') if k.strip()]
                metadata["keywords"].extend(keywords)
        
        # ========================================================================
        # 🔴 CRITICO: FIX REGEX ReDoS (Q&A Pattern Ottimizzato)
        # ========================================================================
        # PATTERN SUPPORTA DUE FORMATI:
        # 1. **Q1: Question?** (bold - usato da Tk3+ files)
        # 2. ## Q1: Question? (heading - usato dalla maggior parte dei file)
        #
        # Pattern 1: **Q\d+:** (bold)
        qa_pattern_bold = r'\*\*Q\d+:\s*([^\*]+?)\*\*\s*\n((?:(?!\*\*Q\d+:).)*?)(?=\*\*Q\d+:|\n##|$)'
        qa_matches_bold = re.findall(qa_pattern_bold, content, re.DOTALL)
        
        # Pattern 2: ## Q\d+: (heading)
        qa_pattern_heading = r'##\s+Q\d+:\s*([^\n]+)\n((?:(?!##\s+Q\d+:).)*?)(?=##\s+Q\d+:|##\s+[A-Z]|$)'
        qa_matches_heading = re.findall(qa_pattern_heading, content, re.DOTALL)
        
        # Combina entrambi i match
        qa_matches = qa_matches_bold + qa_matches_heading
        
        for question, answer in qa_matches:
            question = question.strip()
            answer = answer.strip()
            if question and answer:
                metadata["qa_pairs"].append({
                    "question": question,
                    "answer": answer
                })
                # Aggiungi anche come domanda naturale
                metadata["natural_questions"].append(question)
        
        # Estrai anche le domande dalla sezione FAQ più semplice (### Domanda?)
        # Pattern ottimizzato anche qui
        simple_qa_pattern = r'###\s+([^\n]+\?)\s*\n((?:(?!###).)*?)(?=###|\n##|$)'
        simple_qa_matches = re.findall(simple_qa_pattern, content, re.DOTALL)
        
        for question, answer in simple_qa_matches:
            question = question.strip()
            answer = answer.strip()
            if question and answer:
                # Evita duplicati
                if question not in metadata["natural_questions"]:
                    metadata["qa_pairs"].append({
                        "question": question,
                        "answer": answer
                    })
                    metadata["natural_questions"].append(question)
        
        return metadata
    
    def _semantic_chunk_text(self, text, max_chunk_tokens=384, overlap_sentences=3):
        """
        Chunking semantico intelligente usando embeddings per identificare punti di divisione naturali.
        Divide il testo in base a confini semantici (paragrafi, sezioni) invece che caratteri arbitrari.
        
        OPTIMIZED FOR LLAMA 3.2 3B (8k context window):
        - max_chunk_tokens=384 (~1500 chars) ensures 5 chunks fit comfortably in context
        - overlap_sentences=3 improves context continuity between chunks
        
        Args:
            text: Testo da dividere
            max_chunk_tokens: Tokens massimi per chunk (384 tokens = ~1500 caratteri, ottimizzato per Llama 3.2 3B)
            overlap_sentences: Numero frasi di overlap tra chunks per preservare contesto (3 frasi = migliore continuità)
        
        Returns:
            Lista di chunks semanticamente coerenti
        """
        import re
        
        # 1. Dividi per sezioni markdown (## Headers prioritari)
        section_pattern = r'\n##+ [^\n]+'
        sections = re.split(section_pattern, text)
        section_headers = re.findall(section_pattern, text)
        
        # Ricostruisci sezioni con i loro headers
        structured_sections = []
        if sections[0].strip():  # Contenuto prima del primo header
            structured_sections.append(sections[0])
        
        for i, header in enumerate(section_headers):
            if i + 1 < len(sections):
                structured_sections.append(header + sections[i + 1])
        
        # 2. Processa ogni sezione semanticamente
        chunks = []
        for section in structured_sections:
            section = section.strip()
            if not section:
                continue
            
            # Stima tokens (approssimazione: 1 token ≈ 4 caratteri per testi tecnici)
            estimated_tokens = len(section) // 4
            
            if estimated_tokens <= max_chunk_tokens:
                # Sezione piccola → chunk singolo
                chunks.append(section)
            else:
                # Sezione grande → dividi per paragrafi preservando struttura
                paragraphs = [p.strip() for p in section.split('\n\n') if p.strip()]
                
                current_chunk = []
                current_size = 0
                
                for para in paragraphs:
                    para_tokens = len(para) // 4
                    
                    # Se aggiungere questo paragrafo supera il limite
                    if current_size + para_tokens > max_chunk_tokens and current_chunk:
                        # Salva chunk corrente
                        chunks.append('\n\n'.join(current_chunk))
                        
                        # Inizia nuovo chunk con overlap (ultime N frasi del chunk precedente)
                        sentences = re.split(r'[.!?]+\s+', current_chunk[-1])
                        overlap_text = '. '.join(sentences[-overlap_sentences:]) if len(sentences) > overlap_sentences else ''
                        
                        current_chunk = [overlap_text, para] if overlap_text else [para]
                        current_size = len(overlap_text) // 4 + para_tokens
                    else:
                        # Aggiungi al chunk corrente
                        current_chunk.append(para)
                        current_size += para_tokens
                
                # Aggiungi ultimo chunk
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
        
        # 3. Post-processing: unisci chunks troppo piccoli
        # OTTIMIZZATO: con max_chunk_tokens=384, buffer max = 1536 chars (~384 token)
        final_chunks = []
        buffer_chunk = ""
        
        for chunk in chunks:
            # *4 converte token→chars (1 token ≈ 4 chars), quindi 384*4 = 1536 chars max
            if len(buffer_chunk) + len(chunk) <= max_chunk_tokens * 4:
                buffer_chunk += "\n\n" + chunk if buffer_chunk else chunk
            else:
                if buffer_chunk:
                    final_chunks.append(buffer_chunk.strip())
                buffer_chunk = chunk
        
        if buffer_chunk:
            final_chunks.append(buffer_chunk.strip())
        
        # 4. HARD LIMIT: Dividi chunks che superano ancora il limite (safety split)
        # Questo gestisce sezioni markdown molto lunghe che non hanno paragrafi chiari
        hard_limited_chunks = []
        HARD_LIMIT = max_chunk_tokens * 4  # 384*4 = 1536 chars max
        
        for chunk in final_chunks:
            if len(chunk) <= HARD_LIMIT:
                hard_limited_chunks.append(chunk)
            else:
                # Chunk troppo grande → split forzato per frasi
                sentences = re.split(r'(?<=[.!?])\s+', chunk)
                current_split = []
                current_size = 0
                
                for sentence in sentences:
                    sentence_size = len(sentence)
                    if current_size + sentence_size > HARD_LIMIT and current_split:
                        hard_limited_chunks.append(' '.join(current_split))
                        current_split = [sentence]
                        current_size = sentence_size
                    else:
                        current_split.append(sentence)
                        current_size += sentence_size
                
                if current_split:
                    hard_limited_chunks.append(' '.join(current_split))
        
        return hard_limited_chunks if hard_limited_chunks else [text]

    def generate_embeddings(self):
        """
        Genera embeddings per DOCUMENTI COMPLETI con chunking SEMANTICO intelligente.
        Usa embeddings del modello per dividere il testo in chunk semanticamente coerenti.
        """
        print("🔄 GENERAZIONE EMBEDDINGS CON CHUNKING SEMANTICO...\n")
        
        if not self._load_model():
            return False
        
        texts_to_encode = []
        embedding_ids = []
        chunk_texts = {}  # 🔴 CRITICO: Mappa embedding_id → testo originale chunk (per retrieval chatbot)
        
        print("📝 Preparazione documenti con chunking semantico intelligente...")
        print("   (Preserva sezioni markdown, paragrafi e contesto semantico)\n")
        
        total_chunks = 0
        chunk_stats = {"small": 0, "medium": 0, "large": 0}
        skipped_chunking = 0  # Track documenti mantenuti interi
        qa_chunks_count = 0  # Track Q&A chunks separati
        keywords_chunks_count = 0  # Track keywords embeddings generati
        
        for chunk_id, chunk_data in self.chunks_data.items():
            content = chunk_data.get("content", "")
            
            if not content:
                continue
            
            # ========================================================================
            # 🔴 CRITICO: CHUNKING SPECIALE PER FILE Q&A
            # ========================================================================
            # File Q&A devono essere chunkizzati UNA DOMANDA PER CHUNK
            # per migliorare il retrieval di risposte specifiche
            
            source_file = chunk_data.get("source_file", "")
            # FIX: Rilevamento robusto dei file Q&A (case-insensitive, multipli pattern)
            source_file_upper = str(source_file).upper()
            chunk_id_upper = str(chunk_id).upper()
            
            # 🔍 DEBUG BRUTALE: Stampa TUTTI i chunk_id per vedere pattern
            if "_Q" in chunk_id_upper or "Q&A" in chunk_id_upper:
                print(f"   🔍 CHUNK CON 'Q': chunk_id='{chunk_id}' | source='{source_file}'")
            
            is_qa_file = ("Q&A" in source_file_upper or 
                          "Q&A" in chunk_id_upper or 
                          "_QA_" in chunk_id_upper or
                          "/Q&A." in source_file_upper)
            
            if is_qa_file:
                # Estrai Q&A pairs dai metadati
                metadata = chunk_data.get("metadata", {})
                qa_pairs = metadata.get("qa_pairs", [])
                
                # 🔍 DEBUG: Stampa sempre per file Q&A (anche se vuoto)
                if qa_pairs:
                    print(f"   • {chunk_data['title']}: {len(qa_pairs)} Q&A chunks (1 domanda = 1 chunk)")
                else:
                    print(f"   ❌ {chunk_data['title']}: File Q&A ma nessun Q&A pair estratto dal regex!")
                    # Mostra preview contenuto per debug (prime 10 righe dopo frontmatter)
                    lines = content.split('\n')
                    
                    # Trova la prima riga con Q (dopo YAML frontmatter)
                    first_q_line = None
                    for i, line in enumerate(lines[10:50], start=10):  # Cerca tra riga 10-50
                        if 'Q1:' in line or 'Q2:' in line or '**Q' in line or 'q1:' in line.lower():
                            first_q_line = i
                            break
                    
                    if first_q_line:
                        preview = '\n'.join(lines[first_q_line:first_q_line+6])
                        print(f"      🔍 Prima domanda trovata alla riga {first_q_line}:")
                        for preview_line in lines[first_q_line:first_q_line+6]:
                            print(f"         | {preview_line[:120]}")
                    else:
                        print(f"      ⚠️  NESSUNA riga con 'Q1:', 'Q2:' o '**Q' trovata nel file!")
                        print(f"      📄 Mostra prime 10 righe dopo frontmatter (riga 12-22):")
                        for line_idx in range(12, min(22, len(lines))):
                            print(f"         [{line_idx:2}] {lines[line_idx][:120]}")
                
                if qa_pairs:
                    # Crea un chunk separato per ogni Q&A pair
                    for qa_idx, qa_pair in enumerate(qa_pairs):
                        question = qa_pair.get("question", "").strip()
                        answer = qa_pair.get("answer", "").strip()
                        
                        if question and answer:
                            # Formatta il chunk come "Q: ... A: ..."
                            qa_text = f"Q: {question}\n\nA: {answer}"
                            
                            # Crea embedding ID univoco per questo Q&A
                            embedding_id = normalize_chunk_id(f"{chunk_id}|qa_{qa_idx}")
                            
                            texts_to_encode.append(qa_text)
                            embedding_ids.append(embedding_id)
                            self.embedding_to_chunk_id[embedding_id] = chunk_id
                            chunk_texts[embedding_id] = qa_text  # 🔴 SALVA testo per retrieval
                            total_chunks += 1
                            qa_chunks_count += 1
                            
                            # Statistiche
                            chunk_len = len(qa_text)
                            if chunk_len < 1000:
                                chunk_stats["small"] += 1
                            elif chunk_len < 2500:
                                chunk_stats["medium"] += 1
                            else:
                                chunk_stats["large"] += 1
                    
                    # IMPORTANTE: Salta il chunking normale per questo file
                    continue
                else:
                    # Se non ci sono Q&A pairs estratti, processa come file normale
                    # (fallback per evitare di perdere contenuto)
                    print(f"      → Fallback a chunking normale per preservare contenuto")
            
            # ========================================================================
            # 🟠 ALTA PRIORITÀ: Skip Chunking per File Brevi (NON Q&A)
            # ========================================================================
            # File piccoli (<512 token = ~2048 chars) → mantieni intero
            # Vantaggi:
            # - Contesto completo (no split artificiale)
            # - -20% embeddings generati
            # - Retrieval più preciso
            content_tokens = len(content) // 4  # Approssimazione: 1 token ≈ 4 chars
            
            if content_tokens <= 512:
                # Documento breve → mantieni intero (contesto completo)
                document_chunks = [content]
                skipped_chunking += 1
            else:
                # Documento lungo → chunking semantico intelligente
                document_chunks = self._semantic_chunk_text(content, max_chunk_tokens=384, overlap_sentences=3)
            
            # Crea embedding per ogni chunk semantico
            for i, text_chunk in enumerate(document_chunks):
                if text_chunk.strip():
                    # ✅ FIX: Normalizza embedding_id per coerenza
                    raw_embedding_id = f"{chunk_id}|chunk_{i}"
                    embedding_id = normalize_chunk_id(raw_embedding_id)
                    
                    texts_to_encode.append(text_chunk)
                    embedding_ids.append(embedding_id)
                    self.embedding_to_chunk_id[embedding_id] = chunk_id
                    chunk_texts[embedding_id] = text_chunk  # 🔴 SALVA testo per retrieval
                    total_chunks += 1
                    
                    # Statistiche dimensioni chunks
                    chunk_len = len(text_chunk)
                    if chunk_len < 1000:
                        chunk_stats["small"] += 1
                    elif chunk_len < 2500:
                        chunk_stats["medium"] += 1
                    else:
                        chunk_stats["large"] += 1
            
            # ========================================================================
            # 🔴 CRITICO: KEYWORDS EMBEDDING BOOST (Migliora Retrieval)
            # ========================================================================
            # Crea embedding dedicati per le keywords del documento
            # 
            # DOPPIA STRATEGIA:
            # 1. Keywords nei metadati → filtraggio/classificazione nel RAG pipeline
            # 2. Keywords come embedding → boost similarità coseno per query tecniche
            #
            # Vantaggi embedding keywords:
            # - Retrieval più preciso per query tecniche (es. "TK4 46 bar", "Modbus RTU")
            # - Query brevi matchano meglio con keywords che con testo lungo
            # - Boost retrieval per nomi prodotto, codici, acronimi
            #
            # NOTA: Se file non ha keywords YAML, estrae automaticamente da titolo/metadati
            
            metadata = chunk_data.get("metadata", {})
            keywords = metadata.get("keywords", [])
            
            # Se non ci sono keywords YAML, estrai da titolo e contenuto
            if not keywords:
                # Strategia fallback: usa titolo prodotto come keyword principale
                title = chunk_data.get("title", "")
                category = chunk_data.get("category", "")
                
                # Estrai codici prodotto e termini tecnici dal titolo
                # Es. "TK3 SERIES COMPLETE" → ["TK3", "TK3 Series", "oil level regulator"]
                # Es. "K11 COMPLETE" → ["K11", "K11 sensor", "level switch"]
                
                fallback_keywords = []
                
                # Aggiungi titolo base
                if title:
                    # Rimuovi "COMPLETE" e normalizza
                    clean_title = title.replace("COMPLETE", "").replace("_", " ").strip()
                    fallback_keywords.append(clean_title)
                    
                    # Estrai codice prodotto (pattern: TK3, TK4, LC-PH, K11, etc.)
                    product_codes = re.findall(r'\b(?:TK\d+|LC[-_][A-Z]{2,4}|K\d+|ATEX|ROTALOCK|ADAPTER)\b', 
                                               clean_title, re.IGNORECASE)
                    fallback_keywords.extend(product_codes)
                
                # Aggiungi categoria come keyword contestuale
                if category:
                    category_keywords = {
                        "Oil_Level_Regulators": ["oil level regulator", "oil management"],
                        "Level_Switches": ["level switch", "level sensor"],
                        "Sensors": ["sensor", "detection"],
                        "Adapters": ["adapter", "mounting"]
                    }
                    fallback_keywords.extend(category_keywords.get(category, []))
                
                # Rimuovi duplicati e limita a 10 keywords
                keywords = list(dict.fromkeys([k for k in fallback_keywords if k]))[:10]
            
            if keywords:
                # Combina le keywords in un testo dedicato
                # Format: "Keywords: keyword1, keyword2, keyword3"
                # Questo aiuta il modello a capire che sono termini chiave
                keywords_text = "Keywords: " + ", ".join(keywords[:15])  # Limita a 15 keywords più rilevanti
                
                # Crea embedding dedicato per keywords
                # Fix: Rimuovi trailing pipe da chunk_id prima di aggiungere |keywords
                clean_chunk_id = chunk_id.rstrip('|')
                keywords_embedding_id = normalize_chunk_id(f"{clean_chunk_id}|keywords")
                
                texts_to_encode.append(keywords_text)
                embedding_ids.append(keywords_embedding_id)
                self.embedding_to_chunk_id[keywords_embedding_id] = chunk_id
                chunk_texts[keywords_embedding_id] = keywords_text
                total_chunks += 1
                chunk_stats["small"] += 1  # Keywords sono sempre piccoli
                keywords_chunks_count += 1  # Conta keywords embedding
            
            # Log progress per documenti grandi
            if len(document_chunks) > 1 and not is_qa_file:
                keywords_note = " + keywords" if keywords else ""
                print(f"   • {chunk_data['title']}: {len(document_chunks)} chunks semantici{keywords_note}")

        print(f"\n   ✅ Preparati {len(texts_to_encode)} chunks semantici da {len(self.chunks_data)} documenti")
        print(f"      📊 Distribuzione: {chunk_stats['small']} piccoli, {chunk_stats['medium']} medi, {chunk_stats['large']} grandi")
        print(f"      ⚡ Documenti mantenuti interi (no chunking): {skipped_chunking}")
        print(f"      ❓ Q&A chunks separati (1 domanda = 1 chunk): {qa_chunks_count}")
        print(f"      🔑 Keywords embeddings generati: {keywords_chunks_count}\n")
        
        if not texts_to_encode:
            print("❌ Nessun documento trovato per generare embeddings!")
            return False
        
        # Genera embeddings con progress bar
        print(f"🧠 Codifica di {len(texts_to_encode)} testi in corso...")
        print("   (Può richiedere 1-5 minuti a seconda della CPU e del numero di testi)\n")
        
        # Genera embeddings in batch ottimizzati per CPU (batch_size=16 più stabile su CPU)
        generated_embeddings = self.model.encode(
            texts_to_encode, 
            show_progress_bar=True,
            batch_size=16  # Ottimizzato per CPU (32 può causare slowdown su CPU)
        )
        
        # Popola il dizionario di embeddings
        self.embeddings = {eid: emb for eid, emb in zip(embedding_ids, generated_embeddings)}
        
        print(f"\n✅ Generati {len(self.embeddings)} vettori di embedding.")
        print(f"   • Content chunks: {len(self.embeddings) - qa_chunks_count - keywords_chunks_count}")
        print(f"   • Q&A embeddings: {qa_chunks_count} (ricerca precisa per domande)")
        print(f"   • Keywords embeddings: {keywords_chunks_count} (boost retrieval termini tecnici)")
        
        # Salva la cache aggiornata
        print(f"\n💾 Salvataggio nuova cache in {EMBEDDINGS_CACHE_PATH.name}...")
        try:
            EMBEDDINGS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            with open(EMBEDDINGS_CACHE_PATH, 'wb') as f:
                pickle.dump({
                    'embeddings': self.embeddings,
                    'embedding_to_chunk_id': self.embedding_to_chunk_id,
                    'chunks_data': self.chunks_data,
                    'chunk_texts': chunk_texts,  # 🔴 CRITICO: Salva testi originali chunk per retrieval
                    'model': EMBEDDING_MODEL
                }, f)
            
            size_mb = EMBEDDINGS_CACHE_PATH.stat().st_size / (1024 * 1024)
            print(f"   ✅ Cache salvata con successo ({size_mb:.1f} MB)\n")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Errore durante il salvataggio della cache: {e}\n")
            return False
    
    def verify_cache(self):
        """Verifica che la cache sia valida e mostri le nuove informazioni."""
        if not EMBEDDINGS_CACHE_PATH.exists():
            print("❌ La cache non esiste.")
            return False
        
        try:
            with open(EMBEDDINGS_CACHE_PATH, 'rb') as f:
                cache = pickle.load(f)
            
            embeddings = cache.get('embeddings', {})
            emb_to_chunk = cache.get('embedding_to_chunk_id', {})
            chunks = cache.get('chunks_data', {})
            model_used = cache.get('model', 'unknown')
            
            print("\n✅ CACHE VALIDA (Document-Based Embeddings):")
            print(f"   • Modello Utilizzato: {model_used}")
            print(f"   • Numero di Documenti Originali: {len(chunks)}")
            print(f"   • Numero di Chunks (Embeddings): {len(embeddings)}")
            print(f"   • Mapping Chunk->Documento: {len(emb_to_chunk)} voci")
            
            size_mb = EMBEDDINGS_CACHE_PATH.stat().st_size / (1024 * 1024)
            print(f"   • Dimensione Cache: {size_mb:.1f} MB\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Cache corrotta o in formato vecchio: {e}")
            return False


def main():
    """Script principale"""
    print("\n" + "="*60)
    print("🚀 GENERATORE EMBEDDINGS - RAG CHATBOT")
    print("="*60 + "\n")
    
    # Check dipendenze prima di procedere
    print("🔍 Verifica dipendenze...")
    if not import_sentence_transformers():
        print("\n❌ Dipendenze mancanti! Installa con:")
        print("   pip install sentence-transformers scikit-learn torch\n")
        return
    print("✅ Dipendenze OK\n")
    
    # Verifica cache esistente
    if EMBEDDINGS_CACHE_PATH.exists():
        print("⚠️  Cache embeddings già presente!\n")
        print("Opzioni:")
        print("  [R] Rigenera (sovrascrive cache esistente)")
        print("  [V] Verifica cache (leggi info)")
        print("  [Q] Esci")
        
        choice = input("\nScegli [R/V/Q]: ").strip().upper()
        
        if choice == 'Q':
            print("\n👋 Uscita\n")
            return
        elif choice == 'V':
            generator = EmbeddingsGenerator()
            generator.verify_cache()
            return
        elif choice != 'R':
            print("❌ Scelta non valida")
            return
        
        print()
    
    # Inizializza generator
    generator = EmbeddingsGenerator()
    
    # Carica dati
    if not generator.load_all_data():
        print("❌ Errore caricamento dati")
        return
    
    # Conferma prima di generare
    print("⚠️  ATTENZIONE: La generazione può richiedere 1-3 minuti")
    confirm = input("Procedere? [S/n]: ").strip().upper()
    
    if confirm and confirm != 'S':
        print("\n❌ Operazione annullata\n")
        return
    
    print()
    
    # Genera embeddings
    if generator.generate_embeddings():
        print("="*60)
        print("✅ EMBEDDINGS GENERATI CON SUCCESSO!")
        print("="*60)
        print("\n💡 Ora puoi usare il chatbot con ricerca semantica:")
        print("   python test_rag_chatbot.py\n")
    else:
        print("❌ Errore durante la generazione")


if __name__ == "__main__":
    main()

