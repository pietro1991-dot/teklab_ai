"""
Backend API Flask per Teklab B2B AI Chatbot
Usa Ollama + RAG per generare risposte tecniche
MULTI-USER SUPPORT: Queue system per gestire richieste concorrenti
"""

from flask import Flask, request, jsonify, Response, stream_with_context, session
from flask_cors import CORS
import json
import sys
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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

# Import configurazione prompt Teklab
try:
    from prompts_config import SYSTEM_PROMPT, build_rag_prompt, build_simple_prompt
    logger.info("✅ Configurazione Teklab caricata (SYSTEM_PROMPT + RAG templates)")
except ImportError as e:
    logger.warning(f"⚠️  prompts_config non trovato: {e}")
    SYSTEM_PROMPT = """You are a technical sales assistant for Teklab industrial sensors.
Provide accurate, professional information about:
- TK series oil level controllers (TK1+, TK3+, TK4)
- LC series level switches (LC-PS, LC-XP, LC-XT)
- ATEX explosion-proof sensors
- Pressure ratings and refrigerant compatibility
- MODBUS communication and installation

Be concise and technical. Use the provided context to answer accurately."""
    
    # Fallback se import fallisce
    def build_rag_prompt(rag_context, user_message):
        return f"Context:\n{rag_context}\n\nQuestion: {user_message}\n\nAnswer:"
    
    def build_simple_prompt(user_message):
        return f"Question: {user_message}\n\nAnswer:"

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
        """Restituisce prossima richiesta da processare (FIFO)"""
        with self.lock:
            if self.queue and self.can_process():
                return self.queue[0]
        return None

# Istanza globale della coda
request_queue = RequestQueue(max_concurrent=1)

# Session storage per conversation history
_conversation_sessions = {}  # session_id -> conversation_history

def get_session_id():
    """Ottieni o crea session ID per utente"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

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
            model_name = _embeddings_cache.get('model', 'BAAI/bge-base-en-v1.5')
            
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
    except:
        return False

def search_relevant_chunks(query, top_k=3):  # ⚡ Allineato a 3 chunks
    """Ricerca semantica nei chunks usando embeddings - OTTIMIZZATA"""
    if not load_embeddings():
        return []
    
    # Check se modello embeddings è disponibile
    if _model_embeddings is None:
        logger.warning("⚠️  Modello embeddings non disponibile - skip RAG search")
        return []
    
    # Genera embedding della query
    query_embedding = _model_embeddings.encode([query])[0]
    
    # Cerca nei chunks
    chunk_embeddings = _embeddings_cache.get('chunk_embeddings', {})
    chunks_data = _embeddings_cache.get('chunks_data', {})

    # Cerca nelle Q&A
    qa_embeddings = _embeddings_cache.get('qa_embeddings', {})

    # ⚡ OTTIMIZZAZIONE: usa sklearn cosine_similarity (più veloce di NumPy loop)
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    similarities = []
    
    # Cerca nei chunk
    if chunk_embeddings:
        chunk_ids = list(chunk_embeddings.keys())
        chunk_embs = np.array([chunk_embeddings[cid] for cid in chunk_ids])
        chunk_sims = cosine_similarity([query_embedding], chunk_embs)[0]
        for cid, sim in zip(chunk_ids, chunk_sims):
            similarities.append({'id': cid, 'sim': sim, 'type': 'chunk'})

    # Cerca nelle Q&A
    if qa_embeddings:
        qa_ids = list(qa_embeddings.keys())
        qa_embs = np.array([qa_embeddings[qid] for qid in qa_ids])
        qa_sims = cosine_similarity([query_embedding], qa_embs)[0]
        for qid, sim in zip(qa_ids, qa_sims):
            similarities.append({'id': qid, 'sim': sim, 'type': 'qa'})

    # Ordina per similarità e filtra
    similarities.sort(key=lambda x: x['sim'], reverse=True)
    
    # Filtra per threshold AUMENTATO (0.28 invece di 0.25 - più selettivo = meno noise)
    filtered_results = [res for res in similarities if res['sim'] >= 0.28]
    
    # Prendi top_k risultati
    results = []
    for res in filtered_results[:top_k]:
        item_id = res['id']
        sim = res['sim']
        item_type = res['type']

        if item_type == 'chunk':
            chunk_data = chunks_data.get(item_id, {})
            content = chunk_data.get('original_text', '')
            metadata = chunk_data.get('metadata', {})
            
            results.append({
                'content': content,
                'similarity': float(sim),
                'product_category': metadata.get('product_category', ''),
                'chunk_title': metadata.get('chunk_title', '')
            })
        elif item_type == 'qa':
            chunk_id, qa_idx_str = item_id.split('|qa_')
            qa_idx = int(qa_idx_str)
            chunk_data = chunks_data.get(chunk_id, {})
            qa_pair = chunk_data.get('metadata', {}).get('qa_pairs', [])[qa_idx]
            
            if qa_pair:
                question = qa_pair.get('question', '')
                answer = qa_pair.get('answer', '')
                content = f"Question: {question}\nAnswer: {answer}"
                metadata = chunk_data.get('metadata', {})

                results.append({
                    'content': content,
                    'similarity': float(sim),
                    'product_category': metadata.get('product_category', 'Q&A'),
                    'chunk_title': question
                })
    
    return results


# Inizializza Flask
app = Flask(__name__)
app.secret_key = 'teklab-b2b-ai-secret-key-change-in-production'  # Per session management
CORS(app, supports_credentials=True)  # Permetti cookies per session

# ==================== MULTI-USER QUEUE SYSTEM ====================

class RequestQueue:
    """
    Sistema di coda per gestire richieste concorrenti a Ollama
    CRITICAL per B2B: Ollama single-threaded, max 1 request alla volta
    """
    def __init__(self, max_concurrent=1):
        self.queue = deque()
        self.active_requests = {}  # session_id -> request_info
        self.lock = threading.Lock()
        self.max_concurrent = max_concurrent
        self.request_counter = 0
        
    def enqueue(self, session_id, request_data):
        """Aggiunge richiesta alla coda"""
        with self.lock:
            self.request_counter += 1
            request_info = {
                'session_id': session_id,
                'data': request_data,
                'request_id': self.request_counter,
                'enqueued_at': datetime.now(),
                'status': 'queued'
            }
            self.queue.append(request_info)
            logger.info(f"📥 Request #{self.request_counter} enqueued - Queue size: {len(self.queue)}")
            return self.request_counter
    
    def get_position(self, request_id):
        """Ottiene posizione in coda"""
        with self.lock:
            for i, req in enumerate(self.queue):
                if req['request_id'] == request_id:
                    return i + 1  # 1-indexed
            return None
    
    def get_queue_status(self):
        """Statistiche coda"""
        with self.lock:
            return {
                'queue_length': len(self.queue),
                'active_requests': len(self.active_requests),
                'total_processed': self.request_counter
            }
    
    def start_processing(self, request_id):
        """Marca richiesta come in processing"""
        with self.lock:
            for req in self.queue:
                if req['request_id'] == request_id:
                    req['status'] = 'processing'
                    req['started_at'] = datetime.now()
                    self.active_requests[req['session_id']] = req
                    self.queue.remove(req)
                    logger.info(f"▶️  Processing request #{request_id}")
                    return req
            return None
    
    def finish_processing(self, session_id):
        """Rimuove richiesta completata"""
        with self.lock:
            if session_id in self.active_requests:
                req = self.active_requests.pop(session_id)
                logger.info(f"✅ Completed request #{req['request_id']}")
                return True
            return False
    
    def get_next_request(self):
        """Ottiene prossima richiesta (FIFO)"""
        with self.lock:
            if self.queue and len(self.active_requests) < self.max_concurrent:
                return self.queue[0]['request_id']
            return None

# Istanza globale coda
request_queue = RequestQueue(max_concurrent=1)  # Ollama single-threaded

# Session-specific conversation history
_conversation_sessions = {}  # session_id -> conversation_history

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

# ==================== END QUEUE SYSTEM ====================

# Cache conversazione (DEPRECATED - usa session-based storage)
_conversation_history = []


def generate_response_with_ollama(user_message):
    """
    Genera risposta usando Ollama + RAG
    """
    # Verifica Ollama
    if not check_ollama():
        return {
            'response': "⚠️ Ollama non disponibile. Avvia Ollama ed esegui: ollama run llama3.2:3b",
            'error': True
        }
    
    # Cerca chunks rilevanti (aumentato top_k per più contesto)
    relevant_chunks = search_relevant_chunks(user_message, top_k=3)
    
    # DEBUG: Stampa chunk recuperati
    logger.info(f"🔍 RAG Search: '{user_message[:50]}'")
    logger.info(f"   Risultati trovati: {len(relevant_chunks)}")
    for i, chunk in enumerate(relevant_chunks):
        logger.info(f"   [{i+1}] {chunk['product_category']} | {chunk['chunk_title'][:30]}... | sim={chunk['similarity']:.3f}")
    
    # Costruisci contesto RAG
    if relevant_chunks:
        context_parts = []
        for chunk in relevant_chunks:
            context_parts.append(f"[{chunk['product_category']}] {chunk['content']}")
        rag_context = "\n\n".join(context_parts)
    else:
        rag_context = ""
    
    # Costruisci prompt per Ollama
    if rag_context:
        # AUMENTATO LIMITE: I chunk Teklab sono tecnici e lunghi (3000-8000 chars)
        # Per assistenza clienti professionale, serve contesto completo
        max_context_length = 4000  # Supporta 1-2 chunk completi
        if len(rag_context) > max_context_length:
            rag_context = rag_context[:max_context_length] + "\n\n[... Additional technical details available on request ...]"
        
        # PROMPT OTTIMIZZATO per assistenza clienti B2B Teklab
        full_prompt = f"""You are a TEKLAB TECHNICAL SALES ASSISTANT. Use the product documentation below to answer the customer's question.

TEKLAB PRODUCT DOCUMENTATION:
{rag_context}

---

CUSTOMER QUESTION: {user_message}

RESPONSE GUIDELINES:
1. LANGUAGE: Respond in the SAME language as the customer's question (Italian/English/Spanish/German)
2. ACCURACY: Use ONLY information from the documentation above - cite specific models, specs, pressure ratings
3. PRACTICAL: Focus on the customer's application - recommend the RIGHT product with technical justification
4. COMPLETE: Include key specs (pressure, temp range, refrigerants, outputs, certifications)
5. PROFESSIONAL: Be consultative but concise (aim for 150-250 words)
6. HONEST: If documentation doesn't cover the question fully, say "I recommend contacting Teklab support for detailed specs on..."

TEKLAB ASSISTANT RESPONSE:"""
    else:
        full_prompt = f"""CUSTOMER QUESTION: {user_message}

You are a Teklab technical assistant. The customer is asking about industrial sensors.
Available products: TK series (TK1+, TK3+, TK4), LC series (LC-PS, LC-XP, LC-XT), ATEX sensors.

Provide a brief, professional answer. If you need specific technical details, ask the customer to clarify their application.

ANSWER:"""
    
    # Chiama Ollama
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 1024,  # ✅ Aumentato per risposte complete (no troncamento)
                "top_p": 0.9
            }
        }
        
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result.get('response', '').strip()
        
        return {
            'response': assistant_message,
            'sources': [{'product_category': c['product_category'], 'chunk_title': c['chunk_title'], 'similarity': c['similarity']} for c in relevant_chunks],
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
    MULTI-USER: Queue system per gestire richieste concorrenti
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        reset_history = data.get('reset_history', False)
        
        if not user_message:
            return jsonify({'error': 'Messaggio vuoto'}), 400
        
        # Ottieni session ID utente
        session_id = get_session_id()
        
        if reset_history:
            if session_id in _conversation_sessions:
                _conversation_sessions[session_id].clear()
        
        # Verifica Ollama
        if not check_ollama():
            return jsonify({
                'error': 'Ollama non disponibile. Avvia Ollama ed esegui: ollama run llama3.2:3b'
            }), 503
        
        # 🔥 ENQUEUE REQUEST (CRITICAL per multi-user)
        request_id = request_queue.enqueue(session_id, {
            'message': user_message,
            'session_id': session_id
        })
        
        logger.info(f"👤 User {session_id[:8]}... - Request #{request_id} - Queue: {len(request_queue.queue)}")
        
        def generate():
            """Generator function per streaming SSE con queue management"""
            try:
                # ⏳ WAIT IN QUEUE fino a quando diventa il nostro turno
                position = request_queue.get_position(request_id)
                if position and position > 1:
                    # Invia queue status se non siamo primi
                    queue_data = {
                        'type': 'queue',
                        'position': position,
                        'message': f'In coda: posizione {position}'
                    }
                    yield f"data: {json.dumps(queue_data)}\n\n"
                
                # Polling: attendi il nostro turno (ogni 500ms check)
                while True:
                    next_request = request_queue.get_next_request()
                    if next_request == request_id:
                        # È il nostro turno!
                        request_queue.start_processing(request_id)
                        break
                    
                    # Aggiorna posizione in coda
                    position = request_queue.get_position(request_id)
                    if position and position > 1:
                        queue_data = {
                            'type': 'queue',
                            'position': position,
                            'message': f'In coda: posizione {position}'
                        }
                        yield f"data: {json.dumps(queue_data)}\n\n"
                    
                    time.sleep(0.5)  # Check ogni 500ms
                
                # Ora possiamo processare (abbiamo il lock su Ollama)
                logger.info(f"🟢 Processing request #{request_id} - searching RAG chunks...")
                
                # Cerca chunks rilevanti
                relevant_chunks = search_relevant_chunks(user_message, top_k=3)  # ⚡ Ridotto da 5 a 3
                
                logger.info(f"🔍 RAG Search (stream): '{user_message[:50]}'")
                logger.info(f"   Risultati trovati: {len(relevant_chunks)}")
                
                # Costruisci contesto RAG
                if relevant_chunks:
                    context_parts = []
                    for chunk in relevant_chunks:
                        context_parts.append(f"[{chunk['product_category']}] {chunk['content']}")
                    rag_context = "\n\n".join(context_parts)
                else:
                    rag_context = ""
                
                # ⚡ OTTIMIZZAZIONE: Tronca context se troppo lungo
                max_context_length = 2500  # Supporta ~3 chunks completi
                if rag_context and len(rag_context) > max_context_length:
                    rag_context = rag_context[:max_context_length] + "\n\n[... Additional technical details available on request ...]"
                
                # 🎯 USA TEMPLATE CENTRALIZZATO da prompts_config.py
                if rag_context:
                    full_prompt = build_rag_prompt(rag_context, user_message)
                else:
                    full_prompt = build_simple_prompt(user_message)
                
                # Invia sources prima della risposta
                logger.info(f"📤 Sending sources to client ({len(relevant_chunks)} chunks)...")
                sources_data = {
                    'type': 'sources',
                    'sources': [{'product_category': c['product_category'], 'chunk_title': c['chunk_title'], 'similarity': c['similarity']} for c in relevant_chunks]
                }
                yield f"data: {json.dumps(sources_data)}\n\n"
                logger.info(f"✅ Sources sent via SSE")
                
                # 🔄 SISTEMA ADATTIVO a 4 LIVELLI: 400 → 800 → 1200 → 1600
                # CONTINUE MODE: ogni retry CONTINUA da dove si era fermato (no re-generazione)
                num_predict_levels = [400, 400, 400, 400]  # Ogni livello aggiunge 400 token
                current_level = 0
                full_response = ""
                
                while current_level < len(num_predict_levels):
                    num_predict = num_predict_levels[current_level]
                    
                    if current_level > 0:
                        # CONTINUE MODE: Non mostrare "[continua...]" - streaming già in corso
                        logger.info(f"🔄 Continue generation (level {current_level + 1}/4, +{num_predict} token)")
                    else:
                        logger.info(f"📡 Calling Ollama API (model: {OLLAMA_MODEL}, num_predict={num_predict})...")
                    
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
                        "system": SYSTEM_PROMPT,
                        "stream": True,  # ✅ STREAMING ENABLED
                        "options": {
                            "temperature": 0.6,
                            "num_predict": num_predict,  # 🔄 ADATTIVO: sempre 400 per livello
                            "top_p": 0.85,
                            "num_ctx": 4096,  # ⚡ AUMENTATO da 2048 - supporta RAG context più lunghi
                            "repeat_penalty": 1.1,
                            "stop": ["\n\n\n", "CUSTOMER:", "QUESTION:", "---"]
                        }
                    }
                    
                    response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=180)
                    response.raise_for_status()
                    
                    # Stream chunks progressivi
                    chunk_response = ""
                    for line in response.iter_lines():
                        if line:
                            chunk_data = json.loads(line)
                            
                            if 'response' in chunk_data:
                                token = chunk_data['response']
                                chunk_response += token
                                
                                # Invia SEMPRE token al frontend (streaming continuo)
                                token_data = {'type': 'token', 'token': token}
                                yield f"data: {json.dumps(token_data)}\n\n"
                            
                            # Se Ollama ha finito
                            if chunk_data.get('done', False):
                                done_reason = chunk_data.get('done_reason', 'stop')
                                
                                # APPEND alla risposta completa
                                full_response += chunk_response
                                
                                if done_reason == 'length' and current_level < len(num_predict_levels) - 1:
                                    # Troncato! CONTINUA al livello successivo
                                    current_level += 1
                                    break
                                else:
                                    # Completato o ultimo livello raggiunto
                                    total_tokens_used = sum(num_predict_levels[:current_level + 1])
                                    
                                    done_data = {
                                        'type': 'done',
                                        'timestamp': datetime.now().isoformat(),
                                        'num_predict_used': total_tokens_used,
                                        'retries': current_level
                                    }
                                    yield f"data: {json.dumps(done_data)}\n\n"
                                    break
                    
                    # Se completato (done_reason != 'length'), esci
                    if chunk_data.get('done_reason', 'stop') != 'length':
                        break
                
            except requests.exceptions.Timeout:
                error_data = {
                    'type': 'error',
                    'error': 'Timeout: la richiesta ha impiegato troppo tempo'
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                
            except Exception as e:
                logger.error(f"Errore streaming: {e}")
                error_data = {
                    'type': 'error',
                    'error': f'Errore generazione: {str(e)}'
                }
                yield f"data: {json.dumps(error_data)}\n\n"
            
            finally:
                # ✅ RELEASE QUEUE LOCK quando finito (success o error)
                request_queue.finish_processing(session_id)
                logger.info(f"🔓 Session {session_id[:8]}... released Ollama lock")
        
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
    return jsonify({
        'status': 'healthy',
        'service': 'teklab-ai',
        'model': 'mockup (RAG coming soon)',
        'model_loaded': True,
        'timestamp': datetime.now().isoformat(),
        'conversation_turns': len(_conversation_history)
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
    Endpoint principale per chat
    
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
        
        # Reset storia se richiesto
        if reset_history:
            global _conversation_history
            _conversation_history = []
            logger.info("🔄 Storia conversazione resettata")
        
        logger.info(f"📩 Richiesta: {user_message[:100]}...")
        
        # Genera risposta con Ollama + RAG
        result = generate_response_with_ollama(user_message)
        response_text = result['response']
        has_error = result.get('error', False)
        
        # Salva in history solo se non errore
        if not has_error:
            _conversation_history.append({
                'user': user_message,
                'bot': response_text,
                'timestamp': datetime.now().isoformat()
            })
        
        # Limita history a ultimi 10 scambi
        if len(_conversation_history) > 10:
            _conversation_history = _conversation_history[-10:]
        
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
            'details': str(e),
            'status': 'error'
        }), 500


@app.route('/history', methods=['GET'])
def get_history():
    """Restituisce cronologia conversazione"""
    return jsonify({
        'history': _conversation_history,
        'count': len(_conversation_history)
    })


@app.route('/clear', methods=['POST'])
def clear_history():
    """Cancella cronologia conversazione"""
    global _conversation_history
    _conversation_history = []
    return jsonify({
        'status': 'success',
        'message': 'Storia cancellata'
    })


@app.route('/stats', methods=['GET'])
def stats():
    """Statistiche API"""
    return jsonify({
        'model_loaded': True,
        'conversation_turns': len(_conversation_history),
        'endpoints': {
            'health': 'GET /health',
            'chat': 'POST /chat',
            'history': 'GET /history',
            'clear': 'POST /clear',
            'stats': 'GET /stats'
        }
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🔧 TEKLAB B2B AI - Backend API (Ollama + RAG)")
    print("="*70)
    
    # Verifica Ollama
    ollama_status = "✅ Attivo" if check_ollama() else "❌ Non disponibile"
    # EMBEDDINGS: caricati LAZY (solo quando serve, non all'avvio)
    
    print(f"\n🔍 Stato sistema:")
    print(f"   • Ollama {OLLAMA_MODEL}: {ollama_status}")
    print(f"   • Embeddings RAG: Lazy loading (caricati al primo utilizzo)")
    
    print("\n📡 Server in avvio su http://localhost:5000")
    print("💡 Apri UI_experience/index.html nel browser")
    print("\n✨ Endpoints disponibili:")
    print("   - POST   /chat      → Chat con Ollama + RAG")
    print("   - GET    /health    → Health check")
    print("   - GET    /history   → Cronologia chat")
    print("   - POST   /clear     → Cancella storia")
    print("   - GET    /stats     → Statistiche")
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
        print(f"\n❌ Errore avvio server: {e}")
        import traceback
        traceback.print_exc()
