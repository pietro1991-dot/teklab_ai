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
    from prompts_config import SYSTEM_PROMPT
    logger.info("✅ Configurazione Teklab caricata")
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

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

# Carica embeddings cache
EMBEDDINGS_CACHE = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl"
_embeddings_cache = None
_model_embeddings = None

def load_embeddings():
    """Carica cache embeddings una volta sola"""
    global _embeddings_cache, _model_embeddings
    
    if _embeddings_cache is not None:
        return True
    
    try:
        logger.info("📚 Caricamento embeddings cache...")
        with open(EMBEDDINGS_CACHE, 'rb') as f:
            _embeddings_cache = pickle.load(f)
        
        # Carica modello per query encoding (FORZA CPU)
        from sentence_transformers import SentenceTransformer
        logger.info("   Device: CPU (GPU riservata per Llama)")
        _model_embeddings = SentenceTransformer('sentence-transformers/all-mpnet-base-v2', device='cpu')
        
        chunk_count = len(_embeddings_cache.get('chunk_embeddings', {}))
        qa_count = len(_embeddings_cache.get('qa_embeddings', {}))
        logger.info(f"✅ Embeddings caricati: {chunk_count} chunks, {qa_count} Q&A")
        return True
        
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

def search_relevant_chunks(query, top_k=2):
    """Ricerca semantica nei chunks usando embeddings - OTTIMIZZATA"""
    if not load_embeddings():
        return []
    
    # Genera embedding della query
    query_embedding = _model_embeddings.encode([query])[0]
    
    # Cerca nei chunks
    chunk_embeddings = _embeddings_cache.get('chunk_embeddings', {})
    chunks_data = _embeddings_cache.get('chunks_data', {})
    
    similarities = []
    for chunk_id, chunk_emb in chunk_embeddings.items():
            # Cosine similarity
            sim = np.dot(query_embedding, chunk_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(chunk_emb)
            )
            if sim >= 0.25:  # Abbassato threshold da 0.3 a 0.25 (query italiane vs chunk inglesi)
                similarities.append((chunk_id, sim))    # Ordina per similarità
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Prendi top_k risultati
    results = []
    for chunk_id, sim in similarities[:top_k]:
        chunk_data = chunks_data.get(chunk_id, {})
        
        # ARCHITETTURA TEKLAB OTTIMIZZATA: usa messages[2] (assistant formatted)
        # messages[0] = system prompt template
        # messages[1] = user prompt (SEMANTIC CONCEPT)
        # messages[2] = assistant (FORMATTED RESPONSE) ← QUESTO è il contenuto da usare
        messages = chunk_data.get('messages', [])
        content = ""
        
        # Priorità: assistant message (formatted response)
        if len(messages) > 2:
            content = messages[2].get('content', '')
        # Fallback: user content (raw prompt) se manca assistant
        elif len(messages) > 1:
            content = messages[1].get('content', '')
        
        # PER BACKEND API: NON troncare - frontend può gestire display
        # (rimuovere troncamento permette risposte complete)
        # if len(content) > 500:
        #     content = content[:500] + "..."
        
        metadata = chunk_data.get('metadata', {})
        
        results.append({
            'content': content,
            'similarity': float(sim),
            'product': metadata.get('product_model', ''),
            'category': chunk_data.get('category', '')
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
    logger.info(f"   Chunks trovati: {len(relevant_chunks)}")
    for i, chunk in enumerate(relevant_chunks):
        logger.info(f"   [{i+1}] {chunk['product']} | {chunk['category']} | sim={chunk['similarity']:.3f}")
    
    # Costruisci contesto RAG
    if relevant_chunks:
        context_parts = []
        for chunk in relevant_chunks:
            context_parts.append(f"[{chunk['category']}] {chunk['content']}")
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
            'sources': [{'product': c['product'], 'category': c['category'], 'similarity': c['similarity']} for c in relevant_chunks],
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
                
                # Cerca chunks rilevanti
                relevant_chunks = search_relevant_chunks(user_message, top_k=5)
                
                logger.info(f"🔍 RAG Search (stream): '{user_message[:50]}'")
                logger.info(f"   Chunks trovati: {len(relevant_chunks)}")
                
                # Costruisci contesto RAG
                if relevant_chunks:
                    context_parts = []
                    for chunk in relevant_chunks:
                        context_parts.append(f"[{chunk['category']}] {chunk['content']}")
                    rag_context = "\n\n".join(context_parts)
                else:
                    rag_context = ""
                
                # Costruisci prompt
                if rag_context:
                    max_context_length = 4000
                    if len(rag_context) > max_context_length:
                        rag_context = rag_context[:max_context_length] + "\n\n[... Additional technical details available on request ...]"
                    
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
5. PROFESSIONAL: Be consultative but concise (aim for 150-300 words)
6. HONEST: If documentation doesn't cover the question fully, say "I recommend contacting Teklab support for detailed specs on..."

TEKLAB ASSISTANT RESPONSE:"""
4. COMPLETE: Include key specs (pressure, temp range, refrigerants, outputs, certifications)
5. PROFESSIONAL: Be consultative but concise (aim for 150-300 words)
6. HONEST: If documentation doesn't cover the question fully, say "I recommend contacting Teklab support for detailed specs on..."

TEKLAB ASSISTANT RESPONSE:"""
        else:
            full_prompt = f"""CUSTOMER QUESTION: {user_message}

You are a Teklab technical assistant. The customer is asking about industrial sensors.
Available products: TK series (TK1+, TK3+, TK4), LC series (LC-PS, LC-XP, LC-XT), ATEX sensors.

Provide a brief, professional answer. If you need specific technical details, ask the customer to clarify their application.

ANSWER:"""
        
        def generate():
            """Generator function per streaming SSE"""
            try:
                # Invia sources prima della risposta
                sources_data = {
                    'type': 'sources',
                    'sources': [{'product': c['product'], 'category': c['category'], 'similarity': c['similarity']} for c in relevant_chunks]
                }
                yield f"data: {json.dumps(sources_data)}\n\n"
                
                # Chiama Ollama con streaming
                payload = {
                    "model": OLLAMA_MODEL,
                    "prompt": full_prompt,
                    "system": SYSTEM_PROMPT,
                    "stream": True,  # ✅ STREAMING ENABLED
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 1024,  # ✅ Aumentato per risposte complete (no troncamento)
                        "top_p": 0.9
                    }
                }
                
                response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
                response.raise_for_status()
                
                # Stream chunks progressivi
                for line in response.iter_lines():
                    if line:
                        chunk_data = json.loads(line)
                        
                        if 'response' in chunk_data:
                            token = chunk_data['response']
                            
                            # Invia token al frontend
                            token_data = {
                                'type': 'token',
                                'token': token
                            }
                            yield f"data: {json.dumps(token_data)}\n\n"
                        
                        # Se Ollama ha finito
                        if chunk_data.get('done', False):
                            done_data = {
                                'type': 'done',
                                'timestamp': datetime.now().isoformat()
                            }
                            yield f"data: {json.dumps(done_data)}\n\n"
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
    embeddings_status = "✅ Caricati" if load_embeddings() else "❌ Non trovati"
    
    print(f"\n� Stato sistema:")
    print(f"   • Ollama {OLLAMA_MODEL}: {ollama_status}")
    print(f"   • Embeddings RAG: {embeddings_status}")
    
    print("\n�📡 Server in avvio su http://localhost:5000")
    print("💡 Apri UI_experience/index.html nel browser")
    print("\n✨ Endpoints disponibili:")
    print("   - POST   /chat      → Chat con Ollama + RAG")
    print("   - GET    /health    → Health check")
    print("   - GET    /history   → Cronologia chat")
    print("   - POST   /clear     → Cancella storia")
    print("   - GET    /stats     → Statistiche")
    print("\n" + "="*70 + "\n")
    
    # Avvia server
    app.run(
        host='0.0.0.0',  # Accessibile da qualsiasi interfaccia
        port=5000,
        debug=False  # NO DEBUG per evitare crash reloader
    )
