"""
Backend API Flask per Teklab B2B AI Chatbot
Usa Ollama + RAG per generare risposte tecniche
MULTI-USER SUPPORT: Queue system per gestire richieste concorrenti
"""

from flask import Flask, request, jsonify, Response, stream_with_context, session
from flask_cors import CORS
import json
import sys
import os
import logging
import pickle
import numpy as np
import requests
from pathlib import Path
from datetime import datetime
import threading
import queue
import uuid
from collections import deque
from functools import wraps
import time
import re

# Shared keyword list to detect product-family queries (Italian + English synonyms)
FAMILY_QUERY_KEYWORDS = [
    # Italian
    'tipologie', 'tipologia', 'tipi', 'tipo', 'varianti', 'varianti?', 'modelli', 'versioni',
    'esistono', 'quante', 'catalogo', 'gamma',
    # English
    'types', 'type', 'variants', 'models', 'versions', 'how many', 'list', 'range'
]

# Setup logging
logging.basicConfig(
    level=logging.INFO,  # ← Torniamo a INFO, abbiamo log espliciti ora
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

# Import librerie ML solo se necessario (lazy loading)
# Questo velocizza avvio e riduce memory footprint iniziale
try:
    from sentence_transformers import util
    import torch
    logger.info("✅ Librerie ML (torch, sentence-transformers) importate.")
except ImportError:
    logger.warning("⚠️  Librerie ML non trovate. RAG search non funzionerà.")
    util = None
    torch = None

# Import configurazione prompt Teklab
def load_system_prompt():
    """Carica/ricarica SYSTEM_PROMPT da prompts_config.py"""
    try:
        # Force reload del modulo per vedere le modifiche
        import importlib
        import prompts_config
        importlib.reload(prompts_config)
        
        prompt = prompts_config.SYSTEM_PROMPT
        logger.info("✅ Configurazione Teklab caricata (SYSTEM_PROMPT)")
        logger.info(f"   Lunghezza prompt: {len(prompt)} chars (~{len(prompt)//4} token)")
        return prompt
    except ImportError as e:
        logger.warning(f"⚠️  prompts_config non trovato: {e}")
        fallback = """You are a technical assistant for Teklab industrial sensors.
Provide accurate, professional information about:
- TK series oil level controllers (TK1+, TK3+, TK4)
- LC series level switches (LC-PS, LC-XP, LC-XT)
- ATEX explosion-proof sensors
- Pressure ratings and refrigerant compatibility
- MODBUS communication and installation

Be concise and technical. Use the provided context to answer accurately."""
        logger.warning(f"   Uso prompt di fallback ({len(fallback)} chars)")
        return fallback

# Carica prompt iniziale
SYSTEM_PROMPT = load_system_prompt()

# ✅ PROMPT BUILDERS: Definiti qui (non importati da prompts_config)
def build_rag_prompt(rag_context, user_message):
    """Costruisce prompt con contesto RAG per risposta informata"""
    return f"""Technical documentation:

{rag_context}

---

Customer question: {user_message}

TEKLAB ASSISTANT RESPONSE:"""

def build_simple_prompt(user_message):
    """Costruisce prompt semplice senza RAG per domande generiche"""
    return f"""Customer question: {user_message}

TEKLAB ASSISTANT RESPONSE:"""


def sanitize_chunk_text(raw_text, exclusion_terms):
    """Remove lines that reference excluded product families to reduce LLM confusion."""
    if not raw_text:
        return raw_text
    if not exclusion_terms:
        return raw_text
    sanitized_lines = []
    for line in raw_text.splitlines():
        line_lower = line.lower()
        if any(term in line_lower for term in exclusion_terms):
            continue
        sanitized_lines.append(line)
    if any(line.strip().startswith('|') for line in sanitized_lines):
        sanitized_lines = convert_markdown_table_to_bullets(sanitized_lines)
    return "\n".join(sanitized_lines).strip()


def convert_markdown_table_to_bullets(lines):
    """Convert simple Markdown tables into bullet list statements."""
    converted = []
    i = 0
    total = len(lines)
    while i < total:
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            header_line = stripped
            headers = [cell.strip() for cell in header_line.strip('|').split('|')]
            if all(not h or set(h) <= {'-', ':'} for h in headers):
                i += 1
                continue
            i += 1
            # Skip separator row if present
            if i < total and set(lines[i].strip()) <= {'|', '-', ' ', ':'}:
                i += 1
            while i < total:
                content_line = lines[i].strip()
                if not content_line.startswith('|') or not content_line.endswith('|'):
                    break
                cells = [cell.strip() for cell in content_line.strip('|').split('|')]
                cells += [''] * (len(headers) - len(cells))
                bullet_parts = []
                for header, value in zip(headers, cells):
                    if header and value:
                        bullet_parts.append(f"{header}: {value}")
                if bullet_parts:
                    converted.append("- " + "; ".join(bullet_parts))
                i += 1
            continue
        converted.append(line)
        i += 1
    return converted


def detect_pressure_variant(chunk, variants=None):
    """Return first matching pressure variant (e.g., '46', '80', '130') from chunk metadata/text."""
    if variants is None:
        variants = ['46', '80', '130']

    title_lower = (chunk.get('chunk_title') or chunk.get('title', '')).lower()
    product_lower = chunk.get('product', '').lower()
    keywords_lower = ' '.join(chunk.get('keywords') or []).lower()
    body = chunk.get('sanitized_content') or chunk.get('chunk_text', chunk.get('content', '')) or ''
    body_lower = body.lower()

    for variant in variants:
        direct_patterns = [
            rf"\b{variant}\s*bar\b",
            rf"\b{variant}\s*bars\b",
            rf"\b{variant}\s*barre\b",
            rf"\btk\s*{variant}\b"
        ]
        if any(re.search(pat, title_lower) for pat in direct_patterns):
            return variant
        if any(re.search(pat, product_lower) for pat in direct_patterns):
            return variant

    for variant in variants:
        patterns = [
            rf"\b{variant}\s*bar\b",
            rf"\b{variant}\s*bars\b",
            rf"\b{variant}\s*barre\b",
            rf"\btk\s*{variant}\b"
        ]
        for pat in patterns:
            if re.search(pat, title_lower):
                return variant
            if re.search(pat, keywords_lower):
                return variant
            if re.search(pat, body_lower):
                return variant
    return None

# ============================================================================
# REQUEST QUEUE SYSTEM per Multi-User Support
# ============================================================================
class RequestQueue:
    """
    Gestisce coda FIFO di richieste per Ollama (single-threaded).
    Previene timeout con più utenti concorrenti.
    """
    def __init__(self, max_concurrent=1):
        self.queue = deque()
        self.active_requests = {}  # session_id -> request_info
        self.request_counter = 0
        self.max_concurrent = max_concurrent
        self.lock = threading.Lock()
        
    def enqueue(self, session_id, data):
        """Accoda nuova richiesta e restituisce request_id"""
        with self.lock:
            self.request_counter += 1
            request_id = self.request_counter
            
            self.queue.append({
                'session_id': session_id,
                'request_id': request_id,
                'data': data,
                'status': 'queued',
                'enqueued_at': datetime.now()
            })
            
            logger.info(f"🔵 Request #{request_id} enqueued for session {session_id[:8]}... (queue size: {len(self.queue)})")
            return request_id
    
    def get_position(self, request_id):
        """Restituisce posizione nella coda (1-indexed) o 0 se in processing"""
        with self.lock:
            # Check se in processing
            for sid, info in self.active_requests.items():
                if info.get('request_id') == request_id:
                    return 0  # In processing
            
            # Check posizione in coda
            for idx, req in enumerate(self.queue):
                if req['request_id'] == request_id:
                    return idx + 1
            
            return -1  # Non trovato (completato o errore)
    
    def can_process(self):
        """Verifica se si può processare una nuova richiesta"""
        with self.lock:
            return len(self.active_requests) < self.max_concurrent
    
    def start_processing(self, request_id):
        """Marca richiesta come in processing e la rimuove dalla coda"""
        with self.lock:
            for idx, req in enumerate(self.queue):
                if req['request_id'] == request_id:
                    req['status'] = 'processing'
                    req['started_at'] = datetime.now()
                    self.active_requests[req['session_id']] = req
                    self.queue.remove(req)
                    logger.info(f"🟢 Request #{request_id} started processing (queue: {len(self.queue)})")
                    return req
            return None
    
    def finish_processing(self, session_id):
        """Rimuove richiesta da processing"""
        with self.lock:
            if session_id in self.active_requests:
                req = self.active_requests.pop(session_id)
                logger.info(f"✅ Request #{req['request_id']} completed for session {session_id[:8]}...")
                return True
            return False
    
    def get_next_request(self):
        """Restituisce request_id della prossima richiesta da processare (FIFO)"""
        with self.lock:
            can_proc = self.can_process()
            queue_len = len(self.queue)
            active_len = len(self.active_requests)
            result = None
            if self.queue and can_proc:
                result = self.queue[0]['request_id']
            
            # DEBUG LOG - Sempre in INFO per vedere cosa succede
            if queue_len > 0:
                logger.info(f"🔍 get_next_request() → queue={queue_len}, can_process={can_proc}, active={active_len}, returning={result}")
            
            return result

# Istanza globale della coda
request_queue = RequestQueue(max_concurrent=1)

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral:7b-instruct"  # Excellent instruction following, best for technical content
OLLAMA_TRANSLATE_MODEL = "gemma2:2b"  # ⚡ FAST multilingual translation (5-10x faster than aya-expanse:8b)

# Carica embeddings cache - NUOVA STRUTTURA TEKLAB
EMBEDDINGS_CACHE = PROJECT_ROOT / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"
_embeddings_cache = None
_model_embeddings = None

def load_embeddings():
    """Carica cache embeddings una volta sola - NUOVA STRUTTURA"""
    global _embeddings_cache, _model_embeddings
    
    if _embeddings_cache is not None:
        return True
    
    try:
        logger.info("📚 Caricamento embeddings cache (TEKLAB chunks)...")
        with open(EMBEDDINGS_CACHE, 'rb') as f:
            _embeddings_cache = pickle.load(f)
        
        # Carica modello per query encoding (FORZA CPU)
        try:
            from sentence_transformers import SentenceTransformer
            model_name = _embeddings_cache.get('model', 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2')  # 🔥 TOP per RAG multilingua
            
            logger.info("   Device: CPU (GPU riservata per Llama)")
            logger.info("   ⏳ Caricamento modello embeddings da cache locale...")
            
            # FORZA OFFLINE MODE - usa solo cache locale (no download)
            os.environ['TRANSFORMERS_OFFLINE'] = '1'
            os.environ['HF_HUB_OFFLINE'] = '1'
            
            _model_embeddings = SentenceTransformer(
                model_name, 
                device='cpu'
            )
            
            # NUOVA STRUTTURA
            embeddings_count = len(_embeddings_cache.get('embeddings', {}))
            chunks_count = len(_embeddings_cache.get('chunks_data', {}))
            logger.info(f"✅ Embeddings caricati: {embeddings_count} vettori, {chunks_count} chunk unici")
            return True
            
        except (Exception, KeyboardInterrupt) as e:
            logger.warning(f"⚠️  Impossibile caricare modello embeddings: {type(e).__name__}")
            logger.warning("   Il chatbot funzionerà SENZA ricerca semantica RAG")
            logger.warning("   (Usa solo Ollama senza contesto documenti)")
            _model_embeddings = None
            return False
        
    except FileNotFoundError:
        logger.error(f"❌ Cache embeddings non trovata: {EMBEDDINGS_CACHE}")
        logger.error("   Esegui: python scripts/2_generate_embeddings.py")
        return False
    except Exception as e:
        logger.error(f"❌ Errore caricamento embeddings: {e}")
        return False

def check_ollama():
    """Verifica che Ollama sia attivo"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m.get('name', '') for m in models]
            if OLLAMA_MODEL in model_names:
                return True
            logger.warning(f"⚠️  Modello {OLLAMA_MODEL} non trovato in Ollama")
            logger.warning(f"   Modelli disponibili: {model_names}")
            return False
        return False
    except Exception as e:
        logger.error(f"❌ Errore check_ollama: {e}")
        return False


def translate_with_ollama(text, source_lang, target_lang, timeout=300):
    """
    Traduce testo usando Ollama (modello locale).
    
    Args:
        text: Testo da tradurre
        source_lang: Lingua sorgente ('Italian', 'English', etc.)
        target_lang: Lingua target ('Italian', 'English', etc.)
        timeout: Timeout in secondi (default 300s = 5min per debug - Aya-Expanse molto lento su CPU)
    
    Returns:
        str: Testo tradotto o testo originale se fallisce
    """
    if source_lang == target_lang:
        return text
    
    trans_start = time.time()
    logger.info(f"🔄 Starting translation {source_lang}→{target_lang}...")
    logger.info(f"   Original text: '{text[:100]}{'...' if len(text) > 100 else ''}'")
    
    try:
        # 📚 TECHNICAL GLOSSARY: Termini critici per traduzione accurata
        # Garantisce consistenza nella terminologia tecnica B2B per tutte le lingue
        technical_glossary = {
            'Italian': {
                'Modbus interface': 'interfaccia Modbus',
                'Modbus connectivity': 'connettività Modbus', 
                'Modbus RS485': 'Modbus RS485',
                'BMS/SCADA integration': 'integrazione BMS/SCADA',
                'NFC wireless configuration': 'configurazione wireless NFC',
                'smartphone app': 'app per smartphone',
                'remote monitoring': 'monitoraggio remoto',
                'data logging': 'registrazione dati',
                'real-time': 'in tempo reale',
                'field programmable': 'programmabile in campo',
                'setpoint': 'setpoint',
                'control point': 'punto di controllo',
                'solenoid valve': 'valvola solenoide',
                'oil level regulator': 'regolatore di livello olio',
                'level switch': 'interruttore di livello',
                'pressure variant': 'variante di pressione',
                'electro-optic detection': 'rilevamento elettro-ottico'
            },
            'French': {
                'Modbus interface': 'interface Modbus',
                'Modbus connectivity': 'connectivité Modbus',
                'Modbus RS485': 'Modbus RS485',
                'BMS/SCADA integration': 'intégration BMS/SCADA',
                'NFC wireless configuration': 'configuration NFC sans fil',
                'smartphone app': 'application smartphone',
                'remote monitoring': 'surveillance à distance',
                'data logging': 'enregistrement de données',
                'real-time': 'en temps réel',
                'field programmable': 'programmable sur site',
                'setpoint': 'point de consigne',
                'control point': 'point de contrôle',
                'solenoid valve': 'électrovanne',
                'oil level regulator': 'régulateur de niveau d\'huile',
                'level switch': 'interrupteur de niveau',
                'pressure variant': 'variante de pression',
                'electro-optic detection': 'détection électro-optique'
            },
            'Spanish': {
                'Modbus interface': 'interfaz Modbus',
                'Modbus connectivity': 'conectividad Modbus',
                'Modbus RS485': 'Modbus RS485',
                'BMS/SCADA integration': 'integración BMS/SCADA',
                'NFC wireless configuration': 'configuración inalámbrica NFC',
                'smartphone app': 'aplicación para smartphone',
                'remote monitoring': 'monitoreo remoto',
                'data logging': 'registro de datos',
                'real-time': 'en tiempo real',
                'field programmable': 'programable en campo',
                'setpoint': 'punto de ajuste',
                'control point': 'punto de control',
                'solenoid valve': 'válvula solenoide',
                'oil level regulator': 'regulador de nivel de aceite',
                'level switch': 'interruptor de nivel',
                'pressure variant': 'variante de presión',
                'electro-optic detection': 'detección electro-óptica'
            },
            'German': {
                'Modbus interface': 'Modbus-Schnittstelle',
                'Modbus connectivity': 'Modbus-Konnektivität',
                'Modbus RS485': 'Modbus RS485',
                'BMS/SCADA integration': 'BMS/SCADA-Integration',
                'NFC wireless configuration': 'NFC-Wireless-Konfiguration',
                'smartphone app': 'Smartphone-App',
                'remote monitoring': 'Fernüberwachung',
                'data logging': 'Datenprotokollierung',
                'real-time': 'Echtzeit',
                'field programmable': 'vor Ort programmierbar',
                'setpoint': 'Sollwert',
                'control point': 'Kontrollpunkt',
                'solenoid valve': 'Magnetventil',
                'oil level regulator': 'Ölstandsregler',
                'level switch': 'Füllstandschalter',
                'pressure variant': 'Druckvariante',
                'electro-optic detection': 'elektro-optische Erkennung'
            }
        }
        
        # Costruisci glossario per lingua target
        glossary_hint = ""
        if target_lang in technical_glossary:
            glossary_items = technical_glossary[target_lang]
            glossary_hint = "\n\nTechnical terms reference:\n" + "\n".join([f"- '{en}' → '{target}'" for en, target in list(glossary_items.items())[:8]])
        
        # Prompt ottimizzato per Aya-Expanse (specializzato in traduzioni multilingue)
        # Aya-Expanse eccelle in traduzioni accurate preservando terminologia tecnica
        prompt = f"""Translate the following text from {source_lang} to {target_lang}.

RULES:
1. Preserve ALL technical terms and product names (TK3, TK4, NFC, Modbus, BMS/SCADA, etc.)
2. Use natural grammar and correct gender agreement in {target_lang}
3. Maintain professional B2B tone
4. Output ONLY the translation, no explanations{glossary_hint}

TEXT TO TRANSLATE:
{text}"""
        
        logger.info(f"   Calling Ollama model: {OLLAMA_TRANSLATE_MODEL}")
        
        # Chiamata Ollama (non streaming per avere risposta completa)
        payload = {
            "model": OLLAMA_TRANSLATE_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,   # Bassa per traduzione consistente
                "num_predict": 500,   # ✅ Aumentato a 500 per risposte lunghe (era 300)
                "top_p": 0.9,
                "top_k": 40
                # ✅ REMOVED stop markers - causavano troncamento con "\n\n" nelle traduzioni lunghe
            }
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get('response', '').strip()
            
            # ✅ VALIDAZIONE MIGLIORATA: Controllo più intelligente per testi lunghi
            # - Se traduzione vuota → invalida
            # - Se testo corto (<100 chars) e traduzione <30% → invalida
            # - Se testo lungo (>100 chars) e traduzione <50 chars → invalida (troncamento)
            # - Altrimenti → valida (traduzione OK anche se più corta dell'originale)
            if not translated or len(translated) < 10:
                logger.warning(f"⚠️ Traduzione vuota o troppo corta: '{translated}'")
                logger.warning(f"   Returning original text")
                return text
            
            # Per testi corti, verifica che traduzione non sia troppo ridotta
            if len(text) < 100 and len(translated) < len(text) * 0.3:
                logger.warning(f"⚠️ Traduzione sospetta per testo corto: '{translated[:50]}...'")
                logger.warning(f"   Original: {len(text)} chars → Translated: {len(translated)} chars")
                logger.warning(f"   Returning original text")
                return text
            
            # Per testi lunghi, accetta anche se più corta (normale per IT→EN o viceversa)
            # Ma rifiuta se troppo troncata (<50 chars per testi >500 chars)
            if len(text) > 500 and len(translated) < 50:
                logger.warning(f"⚠️ Traduzione sospetta (troncata): '{translated[:50]}...'")
                logger.warning(f"   Original: {len(text)} chars → Translated: {len(translated)} chars")
                logger.warning(f"   Returning original text")
                return text
            
            elapsed = time.time() - trans_start
            logger.info(f"✅ Translation completed in {elapsed:.2f}s")
            logger.info(f"   Translated text: '{translated[:100]}{'...' if len(translated) > 100 else ''}'")
            return translated
        else:
            logger.error(f"❌ Ollama translation failed: {response.status_code}")
            logger.error(f"   Returning original text")
            return text
            
    except requests.exceptions.Timeout:
        logger.warning(f"⏱️ Timeout traduzione ({timeout}s), uso originale")
        return text
    except Exception as e:
        logger.error(f"❌ Errore traduzione: {e}")
        logger.error(f"   Returning original text")
        return text


def detect_query_language(query):
    """
    Rileva la lingua della query usando Aya-Expanse (specializzato multilingue).
    Supporta: Italiano, Inglese, Tedesco, Francese, Spagnolo.
    
    Returns:
        str: Codice lingua ('it', 'en', 'de', 'fr', 'es') o 'en' se incerto
    """
    detect_start = time.time()
    logger.info(f"🔍 Detecting language for query: '{query[:80]}{'...' if len(query) > 80 else ''}'")
    
    try:
        # Prompt ottimizzato per Aya-Expanse (eccellente nel riconoscimento multilingue)
        prompt = f'What is the language of this text? Reply with only the 2-letter ISO code (en, it, fr, de, es):\n\n"{query[:100]}"'
        
        logger.info(f"   Calling Ollama model: {OLLAMA_TRANSLATE_MODEL}")
        
        payload = {
            "model": OLLAMA_TRANSLATE_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_predict": 30  # Aumentato per vedere risposta completa
            }
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)  # ✅ Aumentato a 15s per evitare timeout
        
        if response.status_code == 200:
            result = response.json()
            detected_text = result.get('response', '').strip().lower()
            
            logger.info(f"   Raw response from model: '{detected_text}'")
            
            # Mappa nomi lingua completi → codici
            lang_map = {
                'italian': 'it', 'italiano': 'it',
                'english': 'en', 'inglese': 'en',
                'french': 'fr', 'francese': 'fr', 'français': 'fr',
                'german': 'de', 'tedesco': 'de', 'deutsch': 'de',
                'spanish': 'es', 'spagnolo': 'es', 'español': 'es'
            }
            
            # Cerca nome lingua o codice nella risposta
            for key, code in lang_map.items():
                if key in detected_text:
                    elapsed = time.time() - detect_start
                    logger.info(f"✅ Language detected in {elapsed:.2f}s: {code.upper()} (matched: '{key}')")
                    return code
            
            # Cerca codici ISO direttamente
            for code in ['it', 'en', 'de', 'fr', 'es']:
                if f' {code} ' in f' {detected_text} ' or detected_text.startswith(code):
                    elapsed = time.time() - detect_start
                    logger.info(f"✅ Language detected in {elapsed:.2f}s: {code.upper()}")
                    return code
        
        # Fallback a inglese
        logger.warning(f"⚠️ Language detection failed, defaulting to 'en'")
        return 'en'
        
    except Exception as e:
        logger.error(f"❌ Language detection error: {e}, defaulting to 'en'")
        return 'en'




def search_relevant_chunks(query, top_k=5, enable_detailed_logging=True):
    """
    Cerca i chunk più rilevanti usando un approccio RAG ibrido a 2 FASI per efficienza.
    🌍 INCLUDE TRADUZIONE AUTOMATICA: Se query non-inglese, traduce prima dell'embedding.
    1. PRE-FILTERING: Ricerca semantica veloce per trovare i top 100 candidati.
    2. RE-RANKING: Calcolo ibrido (semantic + keyword) solo sui top 100.
    3. FINAL SELECTION: Restituisce top_k risultati (ma invia solo i top 3 a Ollama).
    """
    import time
    start_time = time.time()
    
    if not load_embeddings() or not torch or not util:
        logger.error("Cache embeddings o librerie ML non disponibili. Skip RAG search.")
        return []

    # ✅ CARICA chunk_texts per retrieval preciso (1 Q&A = 1 chunk)
    chunk_texts = _embeddings_cache.get('chunk_texts', {})
    if not chunk_texts:
        logger.warning("⚠️  'chunk_texts' non trovato in cache - usando fallback su 'content'")

    if enable_detailed_logging:
        logger.info(f"\n{'='*80}")
        logger.info(f"🔍 RAG SEARCH 2-PHASE LOG (Wide Retrieval + Narrow Context)")
        logger.info(f"{'='*80}")
        logger.info(f"📝 Original Query: '{query}'")
        logger.info(f"⏱️  Timer avviato: {time.strftime('%H:%M:%S')}")

    # ==================== 🌍 TRADUZIONE QUERY (se necessaria) ====================
    if enable_detailed_logging:
        logger.info(f"\n{'='*80}")
        logger.info(f"🌍 PHASE 0: LANGUAGE DETECTION & TRANSLATION")
        logger.info(f"{'='*80}")
    
    translation_start = time.time()
    
    # Rileva lingua query usando Mistral
    query_lang = detect_query_language(query)
    original_query = query
    
    # Traduci query in inglese se necessario (chunk sono in inglese)
    if query_lang != 'en':
        lang_names = {'it': 'Italian', 'de': 'German', 'fr': 'French', 'es': 'Spanish'}
        source_lang_name = lang_names.get(query_lang, 'Italian')
        
        if enable_detailed_logging:
            logger.info(f"\n📝 Original query ({query_lang.upper()}): '{original_query}'")
            logger.info(f"🔄 Translation needed: {source_lang_name} → English")
        
        query = translate_with_ollama(query, source_lang_name, 'English', timeout=30)
        
        if enable_detailed_logging:
            if query != original_query:
                logger.info(f"✅ Query ready for RAG: '{query}'")
                logger.info(f"⏱️  Total translation time: {time.time() - translation_start:.2f}s")
            else:
                logger.info(f"⚠️  Translation failed or unchanged, using original")
                logger.info(f"⏱️  Translation attempt time: {time.time() - translation_start:.2f}s")
    else:
        if enable_detailed_logging:
            logger.info(f"\n✅ Query already in English - No translation needed")
            logger.info(f"📝 Query for RAG: '{query}'")
    
    if enable_detailed_logging:
        logger.info(f"{'='*80}\n")
    
    # ==================== 1. QUERY ENCODING ====================
    phase1_start = time.time()
    
    # Usa query tradotta per embedding
    query_variants = [query]
    
    if enable_detailed_logging:
        logger.info(f"⚡ Using translated query for embedding")
        logger.info(f"   → Semantic matching between English query and English chunks")
    
    query_embeddings = _model_embeddings.encode(query_variants, convert_to_tensor=True, device='cpu')
    
    if enable_detailed_logging:
        logger.info(f"🧠 Encoded 1 query vector (shape: {query_embeddings[0].shape})")
        logger.info(f"⏱️  Tempo query encoding: {time.time() - phase1_start:.2f}s")

    # ============================================================================
    # FASE 1: PRE-FILTERING VELOCE (TOP 100) - RICERCA AMPIA
    # ============================================================================
    phase1_filter_start = time.time()
    
    # ✅ FIX: Converti embeddings da dict a tensor se necessario
    embeddings_data = _embeddings_cache['embeddings']
    chunks_data = _embeddings_cache['chunks_data']
    
    if isinstance(embeddings_data, dict):
        # Se embeddings è un dict, probabilmente chunks_data usa le stesse chiavi
        # Ma per sicurezza usiamo l'ordine coerente
        chunk_ids_sorted = sorted(embeddings_data.keys())
        
        # Converti numpy arrays in tensors se necessario
        embeddings_list = []
        for chunk_id in chunk_ids_sorted:
            emb = embeddings_data[chunk_id]
            if isinstance(emb, np.ndarray):
                emb = torch.from_numpy(emb).float()
            embeddings_list.append(emb)
        embeddings_tensor = torch.stack(embeddings_list)
        
        # Crea mappatura indice → chunk_id (usa le chiavi effettive di embeddings)
        idx_to_chunk_id = {i: chunk_id for i, chunk_id in enumerate(chunk_ids_sorted)}
    else:
        # Se è già un tensor, potrebbe essere indicizzato numericamente
        embeddings_tensor = embeddings_data
        # Prova a usare embedding_to_chunk_id se esiste, altrimenti usa indici numerici
        if 'embedding_to_chunk_id' in _embeddings_cache:
            idx_to_chunk_id = _embeddings_cache['embedding_to_chunk_id']
        else:
            # Fallback: usa gli indici numerici se chunks_data ha chiavi numeriche
            idx_to_chunk_id = {i: i for i in range(len(embeddings_tensor))}
    
    all_similarities = util.pytorch_cos_sim(query_embeddings, embeddings_tensor)
    aggregated_similarities, _ = torch.max(all_similarities, dim=0)
    
    # ✅ OTTIMIZZATO: 30 candidati (era 100) - Bilanciamento velocità/precisione per LLM 3B
    # 30 è sufficiente per re-ranking accurato e 3x più veloce
    num_candidates = min(30, len(aggregated_similarities))
    top_candidate_scores, top_candidate_indices = torch.topk(aggregated_similarities, k=num_candidates)

    if enable_detailed_logging:
        logger.info(f"\n🚀 FASE 1: PRE-FILTERING SEMANTICO (OPTIMIZED RETRIEVAL)")
        logger.info(f"   ✅ Trovati {num_candidates} candidati iniziali su {len(aggregated_similarities)} chunk totali.")
        logger.info(f"⏱️  Tempo pre-filtering: {time.time() - phase1_filter_start:.2f}s")

    # ============================================================================
    # FASE 2: RE-RANKING IBRIDO (sui TOP 100) - CALCOLO DETTAGLIATO
    # ============================================================================
    phase2_start = time.time()
    if enable_detailed_logging:
        logger.info(f"\n🔥 FASE 2: RE-RANKING IBRIDO (sui Top {num_candidates})")
        logger.info(f"   📊 Inizio calcolo hybrid score per ogni candidato...")
        
    scored_results = []
    chunks_data_keys = list(_embeddings_cache['chunks_data'].keys())
    
    for i in range(num_candidates):
        idx = top_candidate_indices[i].item()
        similarity_score = top_candidate_scores[i].item()
        
        # ✅ FIX: Usa la mappatura creata sopra
        chunk_id = idx_to_chunk_id.get(idx, idx)
        
        # ✅ CRITICAL FIX: Rimuovi suffisso |qa_X o |chunk_X per lookup in chunks_data
        # embeddings usa chiavi granulari: "file_Q&A|qa_0", "file_Q&A|qa_1", "file|keywords" etc.
        # chunks_data usa chiavi per file: "file_Q&A" (senza suffisso)
        base_chunk_id = chunk_id
        if isinstance(chunk_id, str) and ('|qa_' in chunk_id or '|chunk_' in chunk_id or '|keywords' in chunk_id):
            base_chunk_id = chunk_id.split('|')[0]  # "file_Q&A|qa_0" → "file_Q&A", "file|keywords" → "file"
        
        # Lookup in chunks_data usando base_chunk_id (senza suffisso)
        chunk_data = None
        if base_chunk_id in _embeddings_cache['chunks_data']:
            chunk_data = _embeddings_cache['chunks_data'][base_chunk_id]
        elif idx in _embeddings_cache['chunks_data']:
            chunk_data = _embeddings_cache['chunks_data'][idx]
        elif isinstance(idx, int) and idx < len(chunks_data_keys):
            # Fallback: usa l'indice per accedere alla lista di chiavi
            actual_key = chunks_data_keys[idx]
            chunk_data = _embeddings_cache['chunks_data'][actual_key]
        
        if chunk_data is None:
            logger.warning(f"⚠️  Chunk ID {chunk_id} (idx={idx}) non trovato, skip...")
            continue
        
        # ✅ RECUPERA chunk text per retrieval preciso (Q&A separati)
        chunk_text = chunk_texts.get(chunk_id, chunk_data.get('content', ''))
        
        metadata = chunk_data.get('metadata', {})
        chunk_title = chunk_data.get('title', 'Unknown')
        chunk_category = chunk_data.get('category', 'N/A')
        chunk_category = chunk_data.get('category', 'N/A')

        # ✅ Q&A Boost - Prioritizza chunk Q&A (risposte dirette e precise)
        is_qa_chunk = '|qa_' in str(chunk_id)
        qa_boost = 0.15 if is_qa_chunk else 0.0  # +15% score per Q&A chunks

        # ✅ KEYWORDS Boost - Prioritizza chunk keywords (boost retrieval codici prodotto)
        is_keywords_chunk = '|keywords' in str(chunk_id)
        keywords_boost = 0.20 if is_keywords_chunk else 0.0  # +20% score per keywords chunks (più forte di Q&A)

        # ✅ HYBRID SCORE: Semantic (60%) + Q&A (15%) + Keywords (25%)
        # Keywords > Q&A perché codici prodotto e termini tecnici hanno massima priorità
        hybrid_score = (0.60 * similarity_score) + (0.15 * qa_boost) + (0.25 * keywords_boost)

        scored_results.append({
            'chunk_data': chunk_data,
            'chunk_id': chunk_id,
            'chunk_text': chunk_text,
            'similarity': similarity_score,
            'qa_boost': qa_boost,
            'keywords_boost': keywords_boost,
            'is_qa': is_qa_chunk,
            'is_keywords': is_keywords_chunk,
            'hybrid_score': hybrid_score
        })
        
        # Log dettagliato per i primi 10 candidati
        if enable_detailed_logging and i < 10:
            chunk_type = "[KEYWORDS]" if is_keywords_chunk else ("[Q&A]" if is_qa_chunk else "[DOC]")
            logger.info(f"   [{i+1:2}] {chunk_type} {chunk_category:20} | {chunk_title[:35]:35}")
            logger.info(f"       Semantic: {similarity_score:.4f} (weight: 0.60)")
            if is_keywords_chunk:
                logger.info(f"       Keywords Boost: {keywords_boost:.4f} (weight: 0.25) 🔑")
            if is_qa_chunk:
                logger.info(f"       Q&A Boost: {qa_boost:.4f} (weight: 0.15) ❓")
            logger.info(f"       → Hybrid: {hybrid_score:.4f}")

    if enable_detailed_logging:
        logger.info(f"\n   ✅ Completato re-ranking di {num_candidates} candidati")
        logger.info(f"   🔄 Ordinamento per hybrid score...")
        logger.info(f"⏱️  Tempo re-ranking: {time.time() - phase2_start:.2f}s")

    phase2_sort_start = time.time()
    scored_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
    
    if enable_detailed_logging:
        logger.info(f"   ✅ Ordinamento completato - Top 10 risultati dopo re-ranking:")
        logger.info(f"⏱️  Tempo ordinamento: {time.time() - phase2_sort_start:.3f}s")
        for i, r in enumerate(scored_results[:10], 1):
            logger.info(f"      [{i:2}] Score: {r['hybrid_score']:.4f} | {r['chunk_data'].get('category', 'N/A'):20} | {r['chunk_data'].get('title', 'Unknown')[:35]}")

    # ==================== 3. ADAPTIVE THRESHOLD & FINAL SELECTION ====================
    phase3_start = time.time()
    final_results = apply_adaptive_threshold(scored_results, enable_detailed_logging)
    logger.info(f"⏱️  Tempo threshold filtering: {time.time() - phase3_start:.3f}s")
    
    phase4_start = time.time()
    final_top_k = final_results[:top_k]

    if enable_detailed_logging:
        log_final_results(final_top_k, query, top_k)
        
    total_time = time.time() - start_time
    logger.info(f"⏱️  ⚡ TEMPO TOTALE RAG SEARCH: {total_time:.2f}s")
    logger.info(f"   └─ Query expansion: {phase1_start:.2f}s")
    logger.info(f"   └─ Pre-filtering: {time.time() - phase1_filter_start:.2f}s")
    logger.info(f"   └─ Re-ranking: {time.time() - phase2_start:.2f}s")
    logger.info(f"   └─ Threshold: {time.time() - phase3_start:.3f}s")
    logger.info(f"")

    # ✅ FIX: Ritorna chunk_data con metadati di scoring + chunk_text per retrieval preciso
    return [{
        **res['chunk_data'],  # Unpack del chunk_data originale
        'chunk_text': res['chunk_text'],  # Testo chunk originale (Q&A separati)
        'similarity': res['similarity'],
        'hybrid_score': res['hybrid_score']
    } for res in final_top_k]


def apply_adaptive_threshold(scored_results, enable_detailed_logging=True):
    """Filtra i risultati usando una soglia adattiva basata sul top score."""
    if not scored_results:
        if enable_detailed_logging:
            logger.info(f"\n🎯 ADAPTIVE THRESHOLD FILTERING")
            logger.info(f"   ⚠️  Nessun risultato da filtrare")
        return []
        
    top_score = scored_results[0]['hybrid_score']
    # ✅ SOGLIA RIPRISTINATA: 70% con traduzione query attiva
    # Query tradotta in inglese prima dell'embedding → matching migliore
    adaptive_threshold = max(0.30, min(0.40, top_score * 0.70))
    
    if enable_detailed_logging:
        logger.info(f"\n🎯 FASE 3: ADAPTIVE THRESHOLD FILTERING")
        logger.info(f"   📊 Analisi distribuzione score:")
        logger.info(f"      Top-1 score:  {top_score:.4f}")
        logger.info(f"      Threshold:    {adaptive_threshold:.4f} (70% of top-1, range: 0.30-0.40)")
        logger.info(f"   🔍 Filtraggio in corso...")
    
    filtered_results = []
    rejected_count = 0
    for r in scored_results:
        if r['hybrid_score'] >= adaptive_threshold:
            filtered_results.append(r)
        else:
            rejected_count += 1
    
    if enable_detailed_logging:
        logger.info(f"   ✅ Risultati sopra threshold: {len(filtered_results)}")
        logger.info(f"   ❌ Risultati sotto threshold: {rejected_count}")
        logger.info(f"   📈 Score range dei filtrati: [{filtered_results[-1]['hybrid_score']:.4f} - {filtered_results[0]['hybrid_score']:.4f}]" if filtered_results else "   (nessun risultato)")
        
    return filtered_results


def log_final_results(final_results, query, top_k):
    """Logga i risultati finali della ricerca RAG con dettagli completi."""
    logger.info(f"\n{'='*80}")
    logger.info(f"✅ FASE 4: FINAL SELECTION & RESULTS")
    logger.info(f"{'='*80}")
    logger.info(f"📊 Selezione finale: TOP {top_k} chunk da {len(final_results)} candidati")
    logger.info(f"")
    
    if not final_results:
        logger.info(f"⚠️  NESSUN CHUNK TROVATO per la query: '{query}'")
        logger.info(f"{'='*80}\n")
        return
    
    logger.info(f"📋 RISULTATI FINALI ({len(final_results)} chunk):")
    logger.info(f"{'─'*80}")
    
    for i, r in enumerate(final_results, 1):
        chunk_title = r['chunk_data'].get('title', 'Unknown')
        category = r['chunk_data'].get('category', 'N/A')
        source_file = r['chunk_data'].get('source_file', 'N/A')
        content_preview = r['chunk_data'].get('content', '')[:100].replace('\n', ' ')
        
        hybrid = r['hybrid_score']
        semantic = r['similarity']
        
        logger.info(f"")
        logger.info(f"   [{i:2}] 📄 {category}")
        logger.info(f"        Titolo:  {chunk_title}")
        logger.info(f"        File:    {source_file}")
        logger.info(f"        Scores:  Hybrid={hybrid:.4f} (Semantic={semantic:.4f})")
        logger.info(f"        Preview: {content_preview}...")
                
    logger.info(f"")
    logger.info(f"{'='*80}\n")
    logger.info(f"✅ RAG Search completata - {len(final_results)} chunk pronti per Ollama\n")

# Inizializza Flask
app = Flask(__name__)
app.secret_key = 'teklab-b2b-ai-secret-key-change-in-production'  # Per session management
CORS(app, supports_credentials=True)  # Permetti cookies per session

# ==================== SESSION-BASED CONVERSATION HISTORY ====================
# UNIFIED SYSTEM: Usa solo _conversation_sessions per tutte le conversazioni
_conversation_sessions = {}  # session_id -> conversation_history

# Configuration constants
MAX_HISTORY_TURNS = 10  # Numero massimo turni da mantenere per sessione

def get_conversation_context(session_id, max_turns=2, current_user_message=""):
    """
    Costruisce contesto dalla cronologia conversazione.
    Limita a ultimi N turni per evitare prompt troppo lunghi.
    
    Args:
        session_id: ID sessione utente
        max_turns: Numero massimo turni da includere (default: 2)
        current_user_message: Messaggio corrente per rilevare lingua (default: "")
    
    Returns:
        str: Contesto formattato con cronologia recente nella lingua corretta
    """
    history = get_conversation_history(session_id)
    if not history or len(history) == 0:
        return ""
    
    # 🌍 RILEVA LINGUA dal messaggio corrente usando Mistral
    query_lang = detect_query_language(current_user_message)
    lang_names = {'it': 'Italian', 'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish'}
    detected_lang = lang_names.get(query_lang, 'English')
    
    # 🌍 ETICHETTE MULTILINGUA per cronologia
    lang_labels = {
        'Italian': {
            'header': 'CRONOLOGIA CONVERSAZIONE (contesto recente):',
            'q_prefix': 'Domanda precedente:',
            'a_prefix': 'Risposta precedente:'
        },
        'English': {
            'header': 'CONVERSATION HISTORY (recent context):',
            'q_prefix': 'Previous Q:',
            'a_prefix': 'Previous A:'
        }
    }
    
    labels = lang_labels.get(detected_lang, lang_labels['English'])
    
    # Prendi ultimi N turni
    recent_turns = history[-max_turns:] if len(history) > max_turns else history
    
    context_parts = []
    for turn in recent_turns:
        user_msg = turn.get('user', '')
        bot_msg = turn.get('assistant', '')
        if user_msg and bot_msg:
            # ⚡ AUMENTATO: Contesto più completo per follow-up questions
            context_parts.append(f"{labels['q_prefix']} {user_msg[:500]}")  # ⚡ 200→500 chars
            context_parts.append(f"{labels['a_prefix']} {bot_msg[:800]}")   # ⚡ 300→800 chars
    
    if context_parts:
        return labels['header'] + "\n" + "\n".join(context_parts) + "\n\n---\n\n"
    return ""


def get_session_id():
    """Ottiene o crea session ID per utente"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_conversation_history(session_id):
    """Ottiene cronologia conversazione per session"""
    if session_id not in _conversation_sessions:
        _conversation_sessions[session_id] = []
    return _conversation_sessions[session_id]

def set_conversation_history(session_id, history):
    """Imposta cronologia conversazione per session"""
    _conversation_sessions[session_id] = history

def clear_conversation_history(session_id):
    """Cancella cronologia conversazione per session"""
    if session_id in _conversation_sessions:
        _conversation_sessions[session_id] = []

def get_all_sessions():
    """Ottiene lista di tutte le sessioni attive"""
    return list(_conversation_sessions.keys())

# ==================== END QUEUE SYSTEM ====================


def generate_response_with_ollama(user_message):
    """
    Genera risposta usando Ollama + RAG
    🌍 INCLUDE TRADUZIONE BIDIREZIONALE:
    1. Query italiana → traduce in inglese per RAG search
    2. LLM genera risposta in inglese  
    3. Risposta inglese → traduce in italiano per utente
    """
    # 🌍 Rileva lingua originale query per traduzione risposta finale
    query_lang = detect_query_language(user_message)
    lang_names = {'it': 'Italian', 'en': 'English', 'de': 'German', 'fr': 'French', 'es': 'Spanish'}
    original_lang_name = lang_names.get(query_lang, 'English')
    
    # Verifica Ollama
    if not check_ollama():
        return {
            'response': "⚠️ Ollama non disponibile. Avvia Ollama ed esegui: ollama run llama3.2:3b",
            'error': True
        }
    
    # ✅ PRODUCT FAMILY DETECTION: Se query chiede "tipologie/varianti/modelli", aumenta top_k
    # per garantire retrieval completo di tutta la famiglia prodotti
    query_lower = user_message.lower()
    is_family_query = any(keyword in query_lower for keyword in FAMILY_QUERY_KEYWORDS)
    
    # ✅ OTTIMIZZATO per Llama 3.2 3B: Sempre 3 chunk per massima precisione
    # Query famiglia = stesso top_k (non serve più contesto, serve Q&A precise)
    top_k = 8 if is_family_query else 3  # Più ampia copertura per famiglie
    
    # Cerca chunks rilevanti
    relevant_chunks = search_relevant_chunks(user_message, top_k=top_k)
    
    # ✅ SMART Q&A SELECTION: Se primo chunk è Q&A con score >0.85, usa SOLO quello
    # Q&A contiene già risposta completa e diretta, altri chunk confondono l'LLM
    if relevant_chunks and len(relevant_chunks) > 0:
        first_chunk = relevant_chunks[0]
        is_first_qa = '|qa_' in first_chunk.get('chunk_id', '')
        first_score = first_chunk.get('hybrid_score', 0.0)
        
        if is_first_qa and first_score >= 0.85:
            # 🎯 CASO OTTIMALE: Q&A con score altissimo = risposta diretta
            logger.info(f"🎯 SMART Q&A MODE: Primo chunk è Q&A con score {first_score:.3f} >= 0.85")
            logger.info(f"   → Uso SOLO questo chunk (risposta diretta e completa)")
            relevant_chunks = [first_chunk]  # Usa solo il primo Q&A
        else:
            # Standard: usa top 3 chunk con Q&A boost già applicato nel re-ranking
            pass
    
    # DEBUG: Stampa chunk recuperati
    logger.info(f"🔍 RAG Search: '{user_message[:50]}'")
    logger.info(f"   Query type: {'PRODUCT FAMILY' if is_family_query else 'SPECIFIC'} (top_k={len(relevant_chunks)})")
    logger.info(f"   Risultati trovati: {len(relevant_chunks)}")
    for i, chunk in enumerate(relevant_chunks):
        chunk_type = "Q&A" if '|qa_' in chunk.get('chunk_id', '') else "DOC"
        hybrid_score = chunk.get('hybrid_score', chunk.get('similarity', 0.0))
        logger.info(f"   [{i+1}] [{chunk_type}] {chunk['product_category']} | {chunk['chunk_title'][:30]}... | hybrid={hybrid_score:.3f}")
    
    # Costruisci contesto RAG
    if relevant_chunks:
        context_parts = []
        for chunk in relevant_chunks:
            chunk_body = chunk.get('sanitized_content') or chunk.get('chunk_text', chunk.get('content', ''))
            context_parts.append(f"[{chunk['product_category']}] {chunk_body}")
        rag_context = "\n\n".join(context_parts)
    else:
        rag_context = ""
    
    # Costruisci prompt per Ollama - USA SOLO SYSTEM_PROMPT (no inline instructions)
    if rag_context:
        # ✅ OTTIMIZZATO per Llama 3.2 3B (8k context = ~32k chars)
        # TOKEN BUDGET (target: 5500 token utilizzati, 2500 reserve):
        # - SYSTEM_PROMPT: ~600 token
        # - RAG context: ~700 token (3 chunk × ~900 chars = 2700 chars)
        # - Conversation history: ~400 token (2 turni)
        # - User query: ~50 token
        # - Response: ~3750 token generati
        max_context_length = 2700  # ~700 token max (3 chunk × 900 chars, più margin)
        if len(rag_context) > max_context_length:
            # Tronca intelligentemente: mantieni chunk completi invece che tagliare a metà
            chunks_list = rag_context.split('\n\n')
            truncated_chunks = []
            current_length = 0
            for chunk in chunks_list:
                if current_length + len(chunk) <= max_context_length:
                    truncated_chunks.append(chunk)
                    current_length += len(chunk) + 2  # +2 per \n\n
                else:
                    break
            rag_context = '\n\n'.join(truncated_chunks)
            if len(chunks_list) > len(truncated_chunks):
                rag_context += "\n\n[... Additional context available - ask for more specific details ...]"
        
        # ✅ PROMPT PULITO: Solo contesto + domanda (SYSTEM_PROMPT gestisce tutto)
        full_prompt = f"""Technical documentation:

{rag_context}

---

{user_message}"""
    else:
        # ✅ PROMPT PULITO: Solo domanda (SYSTEM_PROMPT gestisce tutto)
        full_prompt = user_message
    
    # Chiama Ollama
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.1,  # ✅ ULTRA-RIDOTTO: 0.5→0.3 per massima aderenza a documentazione (Q&A mode)
                "num_predict": 1024,  # ✅ Aumentato per risposte complete (no troncamento)
                "top_p": 0.6,  # ✅ ULTRA-RIDOTTO: 0.85→0.75 per eliminare token creativi (solo fatti)
                "top_k": 5,  # ✅ ULTRA-RIDOTTO: 10→5 per usare SOLO token più probabili (anti-allucinazione)
                "repeat_penalty": 1.15,  # ⚡ AGGIUNTO: Evita ripetizioni
                "presence_penalty": 0.5,  # ⚡ AGGIUNTO: Penalizza token già usati (più varietà)
                "frequency_penalty": 0.5  # ⚡ AGGIUNTO: Penalizza ripetizioni frequenti
            }
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result.get('response', '').strip()
        
        logger.info(f"\n{'='*80}")
        logger.info(f"📤 English response generated ({len(assistant_message)} chars)")
        logger.info(f"{'='*80}")
        logger.info(f"   Preview: {assistant_message[:200]}{'...' if len(assistant_message) > 200 else ''}")
        logger.info(f"{'='*80}")
        
        # 🌍 TRADUZIONE RISPOSTA: Se query non era inglese, traduci risposta
        if query_lang != 'en':
            logger.info(f"\n{'='*80}")
            logger.info(f"🌍 RESPONSE TRANSLATION: English → {original_lang_name}")
            logger.info(f"{'='*80}")
            
            translated_response = translate_with_ollama(
                assistant_message, 
                'English', 
                original_lang_name, 
                timeout=300  # ✅ 5 minuti per debug (verifica se è problema timeout)
            )
            
            if translated_response != assistant_message:
                logger.info(f"✅ Final response ready in {original_lang_name} ({len(translated_response)} chars)")
                logger.info(f"{'='*80}\n")
                assistant_message = translated_response
            else:
                logger.warning(f"⚠️  Translation failed, returning English response")
                logger.info(f"{'='*80}\n")
        else:
            logger.info(f"✅ Response already in English - No translation needed")
            logger.info(f"{'='*80}\n")
        
        return {
            'response': assistant_message,
            'sources': [
                {
                    'product': c.get('product_category', 'Unknown Product'),  # ✅ Frontend si aspetta 'product'
                    'similarity': c['similarity'],
                    'title': c.get('chunk_title', '')
                }
                for c in relevant_chunks
            ],
            'error': False
        }
        
    except requests.exceptions.Timeout:
        logger.error("Ollama timeout")
        return {
            'response': "⏱️ La richiesta ha impiegato troppo tempo. Prova con una domanda più specifica.",
            'error': True
        }
    except Exception as e:
        logger.error(f"Errore Ollama: {e}")
        return {
            'response': f"❌ Errore nella generazione della risposta. Verifica che Ollama sia attivo.",
            'error': True
        }


@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    Endpoint streaming con Server-Sent Events (SSE)
    ⚡ SIMPLIFIED: Direct processing senza queue system
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        reset_history = data.get('reset_history', False)
        
        if not user_message:
            return jsonify({'error': 'Messaggio vuoto'}), 400
        
        # ✅ INPUT VALIDATION
        if len(user_message) > 5000:
            return jsonify({
                'error': 'Messaggio troppo lungo (max 5000 caratteri)',
                'status': 'error'
            }), 400
        
        # Ottieni session ID utente
        session_id = get_session_id()
        
        if reset_history:
            clear_conversation_history(session_id)
            logger.info(f"🔄 Storia conversazione resettata per session {session_id[:8]}...")
        
        # Verifica Ollama
        if not check_ollama():
            return jsonify({
                'error': 'Ollama non disponibile. Avvia Ollama ed esegui: ollama run llama3.2:3b'
            }), 503
        
        logger.info(f"👤 User {session_id[:8]}... - Message: '{user_message[:50]}...'")
        
        def generate():
            """Generator function per streaming SSE - DIRECT PROCESSING"""
            logger.info(f"🎬 Generator started for session {session_id[:8]}...")
            try:
                # ✅ Inizializza variabili timing per evitare NameError in except block
                rag_search_time = 0.0
                prompt_build_time = 0.0
                ollama_total_time = 0.0
                
                # Invia evento init
                init_data = {
                    'type': 'init',
                    'session_id': session_id[:8],
                    'message': 'Connessione stabilita'
                }
                yield f"data: {json.dumps(init_data)}\n\n"
                logger.info(f"✅ SSE connection established for session {session_id[:8]}")
                
                # Ora processare DIRETTAMENTE (no queue)
                processing_start_time = time.time()
                
                logger.info(f"\n{'='*80}")
                logger.info(f"🟢 Processing message for session {session_id[:8]}")
                logger.info(f"⏱️  Timer Processing avviato: {time.strftime('%H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
                # ✅ PRODUCT FAMILY DETECTION: Determina tipo query per context selection
                query_lower = user_message.lower()
                is_family_query = any(keyword in query_lower for keyword in FAMILY_QUERY_KEYWORDS)
                
                # ✅ RICERCA SEMPRE AMPIA: cerca 10 chunk per massima copertura
                # La selezione finale (3-5 chunk) avverrà dopo, in base al tipo di query
                rag_search_start = time.time()
                logger.info(f"🔍 Avvio RAG Search...")
                relevant_chunks = search_relevant_chunks(user_message, top_k=10)
                rag_search_time = time.time() - rag_search_start
                
                logger.info(f"\n{'='*80}")
                logger.info(f"🔍 RAG Search completata: '{user_message[:50]}'")
                logger.info(f"   Query type: {'PRODUCT FAMILY' if is_family_query else 'SPECIFIC'}")
                logger.info(f"   Risultati trovati: {len(relevant_chunks)}")
                logger.info(f"⏱️  Tempo RAG Search: {rag_search_time:.2f}s")
                logger.info(f"⏱️  Tempo totale finora: {time.time() - processing_start_time:.2f}s")
                logger.info(f"{'='*80}\n")
                
                # ============================================================================
                # 🎯 PRODUCT FAMILY FILTERING: Se query menziona prodotto specifico,
                # FILTRA chunk per includere SOLO quel prodotto
                # Esempio: "quali tipologie di tk3 ci sono?" → SOLO chunk TK3+ (no TK4, no LC-*)
                # ============================================================================
                detected_product = None
                product_specific_guidance = None

                if relevant_chunks:
                    query_lower = user_message.lower()
                    product_filters = {
                        'tk4 mb': ['tk4 mb', 'tk4mb'],  # ⚠️ CHECK FIRST (più specifico)
                        'tk4': ['tk4'],  # ⚠️ CHECK BEFORE tk3 (evita false positive)
                        'tk3': ['tk3+', 'tk3'],  # TK3+ family only
                        'tk1': ['tk1+', 'tk1'],  # TK1+ family only
                        'lc-ps': ['lc-ps', 'lc ps'],  # LC-PS only
                        'lc-ph': ['lc-ph', 'lc ph'],  # LC-PH only
                        'lc-xt': ['lc-xt', 'lc xt'],  # LC-XT only
                        'lc-xp': ['lc-xp', 'lc xp'],  # LC-XP only
                    }
                    
                    for product_key, patterns in product_filters.items():
                        if any(pattern in query_lower for pattern in patterns):
                            detected_product = product_key
                            break
                    
                    if detected_product:
                        logger.info(f"\n🎯 PRODUCT FAMILY FILTER ACTIVATED")
                        logger.info(f"   Prodotto rilevato nella query: '{detected_product}'")
                        logger.info(f"   Filtraggio chunk per includere SOLO '{detected_product}' family...")
                        
                        # Filter patterns da cercare nel title/content del chunk
                        filter_patterns = product_filters[detected_product]
                        
                        # ✅ EXCLUSION LIST: Prodotti da ESCLUDERE esplicitamente
                        exclusion_patterns = []
                        if detected_product == 'tk3':
                            # Se cerco TK3, ESCLUDI TK4 e TK4 MB
                            exclusion_patterns = ['tk4 mb', 'tk4mb', 'tk4']
                        elif detected_product == 'tk4':
                            # Se cerco TK4, ESCLUDI TK4 MB e TK3
                            exclusion_patterns = ['tk4 mb', 'tk4mb', 'tk3+', 'tk3']
                        
                        filtered_chunks = []
                        rejected_chunks = []
                        
                        for chunk in relevant_chunks:
                            chunk_title_lower = chunk.get('title', '').lower()
                            keywords = chunk.get('keywords') or []
                            chunk_metadata = (chunk.get('category', '') + ' ' + ' '.join(keywords)).lower()
                            
                            # ✅ CHECK ESCLUSIONI SOLO IN TITLE/METADATA (non body)
                            # Reason: Evita false positive tipo "TK3+ vs TK4" che menziona TK4 ma è chunk TK3+
                            is_excluded = any(excl in chunk_title_lower or excl in chunk_metadata
                                            for excl in exclusion_patterns)
                            
                            if is_excluded:
                                rejected_chunks.append(chunk)
                                continue
                            
                            # Check se chunk TITLE contiene il prodotto richiesto (più affidabile del body)
                            is_match = any(pattern in chunk_title_lower for pattern in filter_patterns)
                            
                            if is_match:
                                chunk_text = chunk.get('chunk_text', chunk.get('content', ''))
                                sanitized = sanitize_chunk_text(chunk_text, exclusion_patterns)
                                if sanitized:
                                    chunk['sanitized_content'] = sanitized
                                filtered_chunks.append(chunk)
                            else:
                                rejected_chunks.append(chunk)
                        
                        logger.info(f"   ✅ Chunk filtrati (match): {len(filtered_chunks)}")
                        logger.info(f"   ❌ Chunk respinti (no match): {len(rejected_chunks)}")
                        
                        if rejected_chunks and len(rejected_chunks) <= 5:
                            for chunk in rejected_chunks[:5]:
                                reject_reason = ""
                                chunk_title = chunk.get('title', 'Unknown')[:40]
                                chunk_category = chunk.get('category', 'N/A')
                                
                                # Check perché respinto (usa stessa logica del filtro)
                                chunk_title_lower = chunk.get('title', '').lower()
                                keywords = chunk.get('keywords') or []
                                chunk_metadata = (chunk.get('category', '') + ' ' + ' '.join(keywords)).lower()
                                
                                if any(excl in chunk_title_lower or excl in chunk_metadata for excl in exclusion_patterns):
                                    reject_reason = f"[EXCLUDED: {', '.join([e for e in exclusion_patterns if e in chunk_title_lower or e in chunk_metadata])}]"
                                else:
                                    reject_reason = "[NO MATCH: title]"
                                
                                logger.info(f"      - {reject_reason} {chunk_category} | {chunk_title}")
                        
                        # Use filtered chunks if we found matches, otherwise keep original
                        if filtered_chunks:
                            relevant_chunks = filtered_chunks
                            logger.info(f"   🎯 FILTER APPLIED: {len(relevant_chunks)} chunk rimasti (solo '{detected_product}' family)")
                        else:
                            logger.info(f"   ⚠️  NESSUN MATCH trovato - mantiengo tutti i chunk originali")
                        
                        logger.info(f"")
                
                # Costruisci contesto RAG
                if relevant_chunks:
                    # ============================================================================
                    # ✅ SMART CONTEXT SELECTION: Ottimizza in base al tipo di query
                    # Ricerca AMPIA (sempre 10 chunk) ma contesto OTTIMIZZATO per Ollama:
                    # - Query FAMILY (tipologie/varianti): TOP 5 chunk (contesto ricco)
                    # - Query SPECIFIC: TOP 3 chunk (contesto mirato)
                    # Vantaggi:
                    # - Context window rispettato (~15-30k token invece di 70k+)
                    # - Velocità ottimizzata (Ollama elabora meno token)
                    # - Qualità superiore (solo chunk più rilevanti, no rumore)
                    # ============================================================================
                    
                    logger.info(f"\n{'='*80}")
                    logger.info(f"📦 FASE 5: SMART CONTEXT SELECTION FOR OLLAMA")
                    logger.info(f"{'='*80}")
                    logger.info(f"📊 Chunk trovati dalla ricerca RAG: {len(relevant_chunks)}")
                    
                    # ⚡ OTTIMIZZATO: 1 chunk per query specifiche, 6 per query famiglia
                    # Query famiglia: serve copertura completa varianti (46/80/130 bar)
                    # Query specifica: 1 chunk ultra-mirato (~6500 chars = ~1600 tokens)
                    context_limit = 1 if not is_family_query else 6
                    
                    if is_family_query:
                        logger.info(f"🎯 Query FAMILY detected → Selezione TOP 6 chunk (garantisce tutte varianti)")
                    else:
                        logger.info(f"🎯 Query SPECIFIC detected → Selezione TOP 1 chunk (contesto ultra-mirato)")
                    
                    logger.info(f"")
                    context_chunks = []
                    # Use RAG chunks directly - prioritize variants if family query
                    if is_family_query and detected_product == 'tk3':
                        variant_order = ['46', '80', '130']
                        variant_chunks = {}
                        for chunk in relevant_chunks:
                            variant = detect_pressure_variant(chunk, variant_order)
                            if variant and variant not in variant_chunks:
                                variant_chunks[variant] = chunk
                        
                        # Build prioritized list: variants first (46→80→130), then others
                        prioritized_chunks = [variant_chunks[v] for v in variant_order if v in variant_chunks]
                        for chunk in relevant_chunks:
                            if len(prioritized_chunks) >= context_limit:
                                break
                            if chunk not in prioritized_chunks:
                                prioritized_chunks.append(chunk)
                        context_chunks = prioritized_chunks[:context_limit]
                    else:
                        context_chunks = relevant_chunks[:context_limit]
                    
                    for i, chunk in enumerate(context_chunks, 1):
                        chunk_title = chunk.get('title', 'Unknown')
                        chunk_category = chunk.get('category', 'N/A')
                        chunk_body = chunk.get('sanitized_content') or chunk.get('chunk_text', chunk.get('content', ''))
                        chunk_length = len(chunk_body)
                        if detected_product == 'tk3' and not chunk.get('title', '').lower().endswith('summary'):
                            variant = detect_pressure_variant(chunk)
                            variant_info = f" | variant={variant} bar" if variant else ""
                        elif chunk.get('title', '').lower().endswith('summary'):
                            variant_info = " | summary"
                        else:
                            variant_info = ""
                        logger.info(f"   ✅ Chunk {i}/{context_limit}: {chunk_category} - {chunk_title}")
                        logger.info(f"      Lunghezza: {chunk_length} chars (~{chunk_length//4} tokens){variant_info}")
                    
                    logger.info(f"")
                    excluded_count = max(len(relevant_chunks) - len(context_chunks), 0)
                    if excluded_count > 0:
                        logger.info(f"❌ Chunk esclusi (score più basso): {excluded_count}")
                    
                    context_parts = []
                    total_context_chars = 0
                    for chunk in context_chunks:
                        chunk_category = chunk.get('category', 'General')
                        chunk_body = chunk.get('sanitized_content') or chunk.get('chunk_text', chunk.get('content', ''))
                        content = f"[{chunk_category}] {chunk_body}"
                        context_parts.append(content)
                        total_context_chars += len(content)
                    
                    rag_context = "\n\n".join(context_parts)
                    
                    logger.info(f"")
                    logger.info(f"📏 Contesto RAG totale costruito:")
                    logger.info(f"   Caratteri: {len(rag_context)}")
                    logger.info(f"   Token stimati: ~{len(rag_context)//4}")
                    logger.info(f"   Chunk inclusi: {len(context_chunks)}/{len(relevant_chunks)}")
                    logger.info(f"{'='*80}\n")
                else:
                    rag_context = ""
                    logger.info(f"\n⚠️  NESSUN CONTESTO RAG: Il chatbot risponderà senza documenti di supporto\n")
                
                # ⚡ SMART CONTEXT OPTIMIZATION
                # Query FAMILY: TOP 5 chunk (~15-25k chars = ~3750-6250 token)
                # Query SPECIFIC: TOP 3 chunk (~9-15k chars = ~2250-3750 token)
                # Context window llama3.2:3b: 8192 token
                # Budget INPUT: SYSTEM(800) + HISTORY(varia) + RAG(3k-6k) + GUIDELINES(600) = ~5-8k token
                # Budget OUTPUT: 800 token per livello × 4 livelli max = 3200 token
                # Totale: ~8-11k token → Fit perfetto dentro 8192 context window!
                # Con 50 chunk possiamo avere 100k-500k chars di contesto
                # max_context_length rimosso per permettere contesto completo
                
                # 🧠 CRONOLOGIA CONVERSAZIONE: Recupera contesto recente (con lingua rilevata)
                # ⚡ AUMENTATO: 10 turni (20 messaggi) per conversazioni tecniche lunghe
                # 🌍 PASSA user_message per rilevare lingua e formattare cronologia correttamente
                history_context = get_conversation_context(session_id, max_turns=10, current_user_message=user_message)
                
                # ==================== CONVERSATION CONTEXT LOGGING ====================
                conversation_history = get_conversation_history(session_id)
                if conversation_history and len(conversation_history) > 0:
                    logger.info(f"\n{'='*80}")
                    logger.info(f"💬 CONVERSATION CONTEXT INJECTION")
                    logger.info(f"{'='*80}")
                    logger.info(f"   Session ID: {session_id[:16]}...")
                    logger.info(f"   Total turns in history: {len(conversation_history)}")
                    logger.info(f"   Injecting last 10 turns into prompt")
                    logger.info(f"   Context length: {len(history_context)} chars (~{len(history_context)//4} tokens)")
                    logger.info(f"   Preview: {history_context[:200]}...")
                    logger.info(f"{'='*80}\n")
                else:
                    logger.info(f"\n💬 CONVERSATION: New session (no history)\n")
                
                # 🎯 USA TEMPLATE CENTRALIZZATO da prompts_config.py
                prompt_build_start = time.time()
                if rag_context:
                    full_prompt = build_rag_prompt(rag_context, user_message)
                    # Aggiungi cronologia se presente
                    if history_context:
                        full_prompt = full_prompt.replace("TEKLAB ASSISTANT RESPONSE:", 
                                                          f"{history_context}TEKLAB ASSISTANT RESPONSE:")
                else:
                    full_prompt = build_simple_prompt(user_message)
                    if history_context:
                        full_prompt = f"{history_context}{full_prompt}"
                
                if product_specific_guidance:
                    full_prompt = f"{full_prompt}\n\nSPECIAL INSTRUCTIONS:\n{product_specific_guidance}"

                prompt_build_time = time.time() - prompt_build_start
                
                # ==================== PROMPT ASSEMBLY LOGGING ====================
                logger.info(f"\n{'='*80}")
                logger.info(f"🎯 FINAL PROMPT ASSEMBLY")
                logger.info(f"{'='*80}")
                logger.info(f"   RAG context: {len(rag_context)} chars (~{len(rag_context)//4} tokens)" if rag_context else "   RAG context: None (no relevant chunks)")
                logger.info(f"   History context: {len(history_context)} chars (~{len(history_context)//4} tokens)" if history_context else "   History context: None")
                logger.info(f"   User message: {len(user_message)} chars (~{len(user_message)//4} tokens)")
                logger.info(f"   Total prompt length: {len(full_prompt)} chars (~{len(full_prompt)//4} tokens)")
                logger.info(f"   Prompt preview (first 300 chars):")
                logger.info(f"   {full_prompt[:300]}...")
                logger.info(f"⏱️  Tempo costruzione prompt: {prompt_build_time:.3f}s")
                logger.info(f"⏱️  Tempo totale finora: {time.time() - processing_start_time:.2f}s")
                logger.info(f"{'='*80}\n")
                
                # ✅ FIX: Invia sources SOLO dei chunk effettivamente usati per la risposta
                # Prima: inviava tutti relevant_chunks (10)
                # Ora: invia solo context_chunks (3 o 5, quelli realmente usati da Ollama)
                actual_sources = context_chunks if relevant_chunks else []
                logger.info(f"📤 Sending sources to client ({len(actual_sources)} chunks actually used)...")
                sources_data = {
                    'type': 'sources',
                    'sources': [
                        {
                            'product': c.get('category', 'Unknown Product'),  # ✅ Usa 'category' da chunk_data
                            'similarity': c.get('similarity', c.get('hybrid_score', 0.0)),  # ✅ Fallback a hybrid_score
                            'title': c.get('title', '')  # ✅ Usa 'title' da chunk_data
                        } 
                        for c in actual_sources  # ✅ FIXED: Usa solo chunk effettivamente nel prompt
                    ]
                }
                yield f"data: {json.dumps(sources_data)}\n\n"
                logger.info(f"✅ Sources sent via SSE ({len(actual_sources)} chunks match prompt context)")
                
                # ==================== LANGUAGE DETECTION ====================
                # Rileva lingua query per enforcement nel system prompt
                detected_language = detect_query_language(user_message)
                
                # 🔥 LANGUAGE ENFORCEMENT: Inietta lingua universale nel system prompt
                language_names = {
                    'it': 'Italian',
                    'en': 'English', 
                    'de': 'German',
                    'fr': 'French',
                    'es': 'Spanish'
                }
                detected_lang_name = language_names.get(detected_language, 'English')
                
                # ✅ NO language enforcement - SYSTEM_PROMPT già gestisce multilingual
                enforced_system_prompt = SYSTEM_PROMPT
                
                logger.info(f"🌍 Lingua rilevata: {detected_language.upper()} → Enforcement: {detected_lang_name}")
                
                # 🔄 SISTEMA ADATTIVO a 3 LIVELLI: 800 → 1300 → 2000 (no troncamenti)
                # CONTINUE MODE: ogni retry CONTINUA da dove si era fermato (no re-generazione)
                # ⚡ OTTIMIZZATO: Livello base 800 token per risposte SEMPRE complete (no stop prematuro)
                num_predict_levels = [800, 500, 700]  # Tot max: 2000 token (risposte complete garantite)
                current_level = 0
                full_response = ""
                ollama_start_time = time.time()
                
                logger.info(f"\n{'='*80}")
                logger.info(f"🤖 OLLAMA GENERATION START")
                logger.info(f"⏱️  Timer Ollama avviato: {time.strftime('%H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
                while current_level < len(num_predict_levels):
                    level_start_time = time.time()
                    num_predict = num_predict_levels[current_level]
                    
                    if current_level > 0:
                        # CONTINUE MODE: Non mostrare "[continua...]" - streaming già in corso
                        logger.info(f"\n🔄 Livello {current_level + 1}/3: Continue generation (+{num_predict} token)")
                        logger.info(f"⏱️  Timer livello {current_level + 1} avviato: {time.strftime('%H:%M:%S')}")
                    else:
                        logger.info(f"\n📡 Livello 1/3: Calling Ollama API")
                        logger.info(f"   Model: {OLLAMA_MODEL}")
                        logger.info(f"   Num predict: {num_predict} token")
                        logger.info(f"⏱️  Timer livello 1 avviato: {time.strftime('%H:%M:%S')}")
                    
                    # CONTINUE MODE: CRITICAL FIX
                    # Per far CONTINUARE (non ri-generare), costruiamo il prompt
                    # come se l'assistente avesse già iniziato a rispondere
                    if current_level > 0 and full_response:
                        # Formato: mostra la risposta parziale come già scritta,
                        # poi Ollama automaticamente continua da lì
                        continue_prompt = f"""{full_prompt}

TEKLAB ASSISTANT RESPONSE:
{full_response}"""
                        # Il modello vede la risposta parziale e continua naturalmente
                    else:
                        continue_prompt = full_prompt
                    
                    # Chiama Ollama con streaming
                    payload = {
                        "model": OLLAMA_MODEL,
                        "prompt": continue_prompt,
                        "system": enforced_system_prompt,
                        "stream": True,
                        "options": {
                            "temperature": 0.0,
                            "num_predict": num_predict,
                            "top_p": 0.5,
                            "top_k": 5,
                            "num_ctx": 8192,
                            "repeat_penalty": 1.50,
                            "presence_penalty": 0.1,
                            "frequency_penalty": 0.2,
                            "stop": ["\n\n\n", "CUSTOMER:", "QUESTION:", "---", "USER:"]
                        }
                    }
                    
                    response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=180)
                    response.raise_for_status()
                    
                    # Stream chunks progressivi (NO PREFILL - solo output Ollama diretto)
                    chunk_response = ""
                    for line in response.iter_lines():
                        if line:
                            chunk_data = json.loads(line)
                            
                            if 'response' in chunk_data:
                                token = chunk_data['response']
                                chunk_response += token
                                
                                # ⚠️ NON inviamo token durante generazione Mistral
                                # → Invieremo la risposta TRADOTTA dopo (anche en→en)
                                # Questo permette di mostrare SEMPRE la risposta nella lingua corretta
                                pass  # Buffer silenzioso
                            
                            # Se Ollama ha finito
                            if chunk_data.get('done', False):
                                done_reason = chunk_data.get('done_reason', 'stop')
                                
                                # APPEND alla risposta completa
                                full_response += chunk_response
                                
                                level_time = time.time() - level_start_time
                                
                                if done_reason == 'length' and current_level < len(num_predict_levels) - 1:
                                    # Troncato! CONTINUA al livello successivo
                                    logger.info(f"⚠️  Livello {current_level + 1} troncato (done_reason=length)")
                                    logger.info(f"⏱️  Tempo livello {current_level + 1}: {level_time:.2f}s")
                                    logger.info(f"⏱️  Tempo Ollama totale finora: {time.time() - ollama_start_time:.2f}s")
                                    logger.info(f"⏱️  Tempo totale finora: {time.time() - processing_start_time:.2f}s")
                                    current_level += 1
                                    break
                                else:
                                    # Completato o ultimo livello raggiunto
                                    total_tokens_used = sum(num_predict_levels[:current_level + 1])
                                    
                                    logger.info(f"\n{'='*80}")
                                    logger.info(f"✅ OLLAMA GENERATION COMPLETED")
                                    logger.info(f"{'='*80}")
                                    logger.info(f"   Livello finale: {current_level + 1}/4")
                                    logger.info(f"   Motivo completamento: {done_reason}")
                                    logger.info(f"   Token totali usati: {total_tokens_used}")
                                    logger.info(f"   Lunghezza risposta: {len(full_response)} chars (~{len(full_response)//4} tokens)")
                                    logger.info(f"⏱️  Tempo livello {current_level + 1}: {level_time:.2f}s")
                                    
                                    ollama_total_time = time.time() - ollama_start_time
                                    logger.info(f"⏱️  ⚡ TEMPO TOTALE OLLAMA: {ollama_total_time:.2f}s")
                                    
                                    # Breakdown per livello
                                    logger.info(f"   Breakdown livelli:")
                                    for i in range(current_level + 1):
                                        logger.info(f"      └─ Livello {i+1}: ~{num_predict_levels[i]} token")
                                    logger.info(f"{'='*80}\n")
                                    
                                    # ⚠️ NON inviare 'done' qui - lo faremo DOPO la traduzione
                                    # done_data = {
                                    #     'type': 'done',
                                    #     'timestamp': datetime.now().isoformat(),
                                    #     'num_predict_used': total_tokens_used,
                                    #     'retries': current_level
                                    # }
                                    # yield f"data: {json.dumps(done_data)}\n\n"
                                    break
                    
                    # Se completato (done_reason != 'length'), esci
                    if chunk_data.get('done_reason', 'stop') != 'length':
                        break
                
                # ==================== ENGLISH RESPONSE PREVIEW ====================
                logger.info(f"\n{'='*80}")
                logger.info(f"📤 ENGLISH RESPONSE GENERATED ({len(full_response)} chars)")
                logger.info(f"{'='*80}")
                logger.info(f"   Preview: {full_response[:300]}{'...' if len(full_response) > 300 else ''}")
                logger.info(f"{'='*80}\n")
                
                # ==================== RESPONSE TRANSLATION (ALWAYS) ====================
                # 🌍 TRADUZIONE RISPOSTA: SEMPRE traduci (anche en→en per consistenza)
                # Questo permette di streammare SOLO la risposta tradotta, mai l'originale inglese
                translation_time = 0.0
                if full_response.strip():
                    translation_start = time.time()
                    
                    # Determina lingua target (se inglese, traduce en→en che ritorna lo stesso testo)
                    target_lang = detected_lang_name if detected_language != 'en' else 'English'
                    
                    logger.info(f"\n{'='*80}")
                    logger.info(f"🌍 RESPONSE TRANSLATION (ALWAYS): English → {target_lang}")
                    logger.info(f"{'='*80}")
                    
                    translated_response = translate_with_ollama(
                        full_response.strip(), 
                        'English', 
                        target_lang, 
                        timeout=300  # 5 minuti per gestire Aya-Expanse lento
                    )
                    
                    translation_time = time.time() - translation_start
                    
                    logger.info(f"✅ Translation completed in {translation_time:.2f}s")
                    logger.info(f"   Translated response ({len(translated_response)} chars)")
                    logger.info(f"   Preview: {translated_response[:200]}{'...' if len(translated_response) > 200 else ''}")
                    logger.info(f"{'='*80}\n")
                    
                    # 📤 Invia risposta tradotta al client con streaming word-by-word
                    logger.info(f"📤 Streaming translated response to client...")
                    
                    # Prima invia evento speciale per segnalare inizio risposta tradotta
                    start_translation_event = {
                        'type': 'translation_start',
                        'language': detected_language,
                        'translation_time': translation_time
                    }
                    yield f"data: {json.dumps(start_translation_event)}\n\n"
                    
                    # Poi stream word-by-word della risposta tradotta
                    words = translated_response.split(' ')
                    for i, word in enumerate(words):
                        # Aggiungi spazio tra parole (tranne prima parola)
                        token_to_send = word if i == 0 else ' ' + word
                        token_data = {'type': 'token', 'token': token_to_send}
                        yield f"data: {json.dumps(token_data)}\n\n"
                    
                    logger.info(f"✅ Translated response streamed successfully ({len(words)} words)")
                else:
                    logger.warning(f"⚠️  Empty response, skipping translation")
                
                # ==================== SEND 'DONE' EVENT AFTER TRANSLATION ====================
                # ✅ Ora inviamo 'done' DOPO che la traduzione è completa (o subito se non serve)
                done_data = {
                    'type': 'done',
                    'timestamp': datetime.now().isoformat(),
                    'num_predict_used': total_tokens_used,
                    'retries': current_level
                }
                yield f"data: {json.dumps(done_data)}\n\n"
                
                # 💾 SALVA CONVERSAZIONE in cronologia sessione (FUORI dal try per avere full_response)
                if full_response and full_response.strip():
                    history = get_conversation_history(session_id)
                    history.append({
                        'user': user_message,
                        'assistant': full_response.strip(),
                        'timestamp': datetime.now().isoformat()
                    })
                    # Limita cronologia a ultimi 10 turni
                    if len(history) > 10:
                        _conversation_sessions[session_id] = history[-10:]
                    
                    logger.info(f"💾 Saved conversation turn (total: {len(history)} turns)")
                
                # ==================== FINAL TIMING SUMMARY ====================
                total_end_to_end_time = time.time() - processing_start_time
                
                logger.info(f"\n{'='*80}")
                logger.info(f"⏱️  ⚡⚡⚡ TIMING SUMMARY - SESSION {session_id[:8]} ⚡⚡⚡")
                logger.info(f"{'='*80}")
                logger.info(f"   🔍 RAG Search: {rag_search_time:.2f}s")
                logger.info(f"   🎯 Prompt Assembly: {prompt_build_time:.3f}s")
                logger.info(f"   🤖 Ollama Generation: {ollama_total_time:.2f}s")
                if translation_time > 0:
                    logger.info(f"   🌍 Response Translation: {translation_time:.2f}s")
                    logger.info(f"   📦 Overhead (queue, context, logging): {(total_end_to_end_time - rag_search_time - prompt_build_time - ollama_total_time - translation_time):.2f}s")
                else:
                    logger.info(f"   📦 Overhead (queue, context, logging): {(total_end_to_end_time - rag_search_time - prompt_build_time - ollama_total_time):.2f}s")
                logger.info(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logger.info(f"   ⚡ TOTAL END-TO-END: {total_end_to_end_time:.2f}s")
                logger.info(f"   ⏰ Timestamp completamento: {time.strftime('%H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
            except requests.exceptions.Timeout:
                error_data = {
                    'type': 'error',
                    'error': 'Timeout: la richiesta ha impiegato troppo tempo'
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                
            except Exception as e:
                logger.error(f"Errore streaming: {e}", exc_info=True)
                error_data = {
                    'type': 'error',
                    'error': f'Errore generazione: {str(e)}'
                }
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )
        
    except Exception as e:
        logger.error(f"Errore chat stream: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    # Calcola totale turni conversazione da tutte le sessioni
    total_turns = sum(len(hist) for hist in _conversation_sessions.values())
    
    return jsonify({
        'status': 'healthy',
        'service': 'teklab-ai',
        'model': 'mockup (RAG coming soon)',
        'model_loaded': True,
        'timestamp': datetime.now().isoformat(),
        'conversation_turns': total_turns,
        'active_sessions': len(_conversation_sessions)
    })


@app.route('/queue/status', methods=['GET'])
def queue_status():
    """
    Restituisce stato attuale della coda
    Utile per monitoring e debug
    """
    with request_queue.lock:
        return jsonify({
            'queue_length': len(request_queue.queue),
            'active_requests': len(request_queue.active_requests),
            'max_concurrent': request_queue.max_concurrent,
            'total_processed': request_queue.request_counter,
            'queue_items': [
                {
                    'request_id': req['request_id'],
                    'position': idx + 1,
                    'enqueued_at': req['enqueued_at'].isoformat(),
                    'status': req['status']
                }
                for idx, req in enumerate(request_queue.queue)
            ]
        })


@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint principale per chat (non-streaming)
    
    Request body:
    {
        "message": "Domanda utente",
        "reset_history": false (optional)
    }
    
    Response:
    {
        "response": "Risposta bot",
        "status": "success",
        "timestamp": "2025-10-31T..."
    }
    """
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Campo "message" mancante',
                'status': 'error'
            }), 400
        
        user_message = data['message'].strip()
        reset_history = data.get('reset_history', False)
        
        if not user_message:
            return jsonify({
                'error': 'Messaggio vuoto',
                'status': 'error'
            }), 400
        
        # ✅ INPUT VALIDATION
        if len(user_message) > 5000:
            return jsonify({
                'error': 'Messaggio troppo lungo (max 5000 caratteri)',
                'status': 'error'
            }), 400
        
        # Ottieni session ID
        session_id = get_session_id()
        
        # Reset storia se richiesto
        if reset_history:
            clear_conversation_history(session_id)
            logger.info(f"🔄 Storia conversazione resettata per session {session_id[:8]}...")
        
        logger.info(f"📩 Richiesta: {user_message[:100]}...")
        
        # Genera risposta con Ollama + RAG
        result = generate_response_with_ollama(user_message)
        response_text = result['response']
        has_error = result.get('error', False)
        
        # Salva in history solo se non errore
        if not has_error:
            history = get_conversation_history(session_id)
            history.append({
                'user': user_message,
                'assistant': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            # Limita history a MAX_HISTORY_TURNS scambi
            if len(history) > MAX_HISTORY_TURNS:
                history = history[-MAX_HISTORY_TURNS:]
                set_conversation_history(session_id, history)
        
        logger.info(f"✅ Risposta generata ({len(response_text)} chars)")
        
        return jsonify({
            'response': response_text,
            'sources': result.get('sources', []),
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"❌ Errore: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Errore interno del server',
            'status': 'error'
        }), 500


@app.route('/history', methods=['GET'])
def get_history():
    """Restituisce cronologia conversazione per la sessione corrente"""
    try:
        session_id = get_session_id()
        history = get_conversation_history(session_id)
        return jsonify({
            'history': history,
            'count': len(history),
            'session_id': session_id[:8] + "..."  # Mostra solo prime 8 char per privacy
        })
    except Exception as e:
        logger.error(f"❌ Errore get_history: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Errore recupero cronologia',
            'status': 'error'
        }), 500


@app.route('/clear', methods=['POST'])
def clear_history():
    """Cancella cronologia conversazione per la sessione corrente"""
    try:
        session_id = get_session_id()
        clear_conversation_history(session_id)
        return jsonify({
            'status': 'success',
            'message': 'Storia cancellata',
            'session_id': session_id[:8] + "..."
        })
    except Exception as e:
        logger.error(f"❌ Errore clear_history: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Errore cancellazione cronologia',
            'status': 'error'
        }), 500


@app.route('/reload_prompt', methods=['POST'])
def reload_prompt():
    """🔥 HOT RELOAD: Ricarica SYSTEM_PROMPT senza riavviare server"""
    global SYSTEM_PROMPT
    try:
        logger.info("🔄 Hot reload SYSTEM_PROMPT richiesto...")
        old_length = len(SYSTEM_PROMPT)
        
        SYSTEM_PROMPT = load_system_prompt()
        new_length = len(SYSTEM_PROMPT)
        
        return jsonify({
            'status': 'success',
            'message': 'SYSTEM_PROMPT ricaricato con successo',
            'old_length': old_length,
            'new_length': new_length,
            'changed': old_length != new_length,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"❌ Errore reload_prompt: {str(e)}", exc_info=True)
        return jsonify({
            'error': f'Errore ricaricamento prompt: {str(e)}',
            'status': 'error'
        }), 500


@app.route('/stats', methods=['GET'])
def stats():
    """Statistiche API"""
    # Calcola totale turni conversazione da tutte le sessioni
    total_turns = sum(len(hist) for hist in _conversation_sessions.values())
    
    return jsonify({
        'model_loaded': True,
        'conversation_turns': total_turns,
        'active_sessions': len(_conversation_sessions),
        'system_prompt_length': len(SYSTEM_PROMPT),
        'endpoints': {
            'health': 'GET /health',
            'chat': 'POST /chat',
            'chat_stream': 'POST /chat/stream',
            'history': 'GET /history',
            'clear': 'POST /clear',
            'reload_prompt': 'POST /reload_prompt',
            'stats': 'GET /stats',
            'queue_status': 'GET /queue/status'
        }
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("TEKLAB B2B AI - Backend API (Ollama + RAG)")
    print("="*70)
    
    # Verifica Ollama
    ollama_status = "Active" if check_ollama() else "Not available"
    # EMBEDDINGS: caricati LAZY (solo quando serve, non all'avvio)
    
    print("\nSystem status:")
    print(f"   - Ollama {OLLAMA_MODEL}: {ollama_status}")
    print("   - Embeddings RAG: Lazy loading (loaded on first use)")
    
    print("\nServer starting on http://localhost:5000")
    print("Open UI_experience/index.html in browser")
    print("\nEndpoints:")
    print("   - POST   /chat         -> Chat with Ollama + RAG")
    print("   - POST   /chat/stream  -> Chat streaming (SSE)")
    print("   - GET    /health       -> Health check")
    print("   - GET    /history      -> Chat history")
    print("   - POST   /clear        -> Clear history")
    print("   - POST   /reload_prompt -> 🔥 Hot reload SYSTEM_PROMPT")
    print("   - GET    /stats        -> Statistics")
    print("\n" + "="*70 + "\n")
    
    # Avvia server
    try:
        app.run(
            host='0.0.0.0',  # Accessibile da qualsiasi interfaccia
            port=5000,
            debug=False,  # NO DEBUG per evitare crash reloader
            threaded=True  # Supporto multi-threading per queue
        )
    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
