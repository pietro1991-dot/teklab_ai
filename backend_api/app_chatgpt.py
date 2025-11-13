"""
Backend API Flask per Teklab B2B AI Chatbot - ChatGPT Version
Usa OpenAI API + RAG per generare risposte tecniche
Compatibile con UI_experience/index.html esistente
"""

from flask import Flask, request, jsonify, Response, stream_with_context, session
from flask_cors import CORS
import json
import sys
import os
import logging
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
import uuid
import time
import re
from openai import OpenAI

# Setup logging
logging.basicConfig(
    level=logging.INFO,  # INFO per logging pulito
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Disattiva log DEBUG delle librerie esterne (urllib3, httpx, httpcore, sentence_transformers)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

# Import librerie ML per RAG
try:
    from sentence_transformers import util
    import torch
    # Disabilita progress bar di sentence-transformers
    import os
    os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
    logger.info("✅ Librerie ML (torch, sentence-transformers) importate.")
except ImportError:
    logger.warning("⚠️  Librerie ML non trovate. RAG search non funzionerà.")
    util = None
    torch = None

# OpenAI Configuration
# Legge la chiave API dal file config.txt
def load_api_key():
    """Carica la chiave API dal file config.txt"""
    config_path = Path(__file__).parent / "config.txt"
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Debug: stampa ogni riga letta
                if line and not line.startswith('#'):
                    logger.debug(f"Config line: {line[:50]}...")  # Primi 50 caratteri
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    logger.debug(f"API key found, length: {len(api_key)}")
                    if api_key and api_key != 'your_api_key_here':
                        logger.info(f"✅ API key loaded successfully (length: {len(api_key)})")
                        return api_key
        logger.error("❌ Chiave API non trovata in config.txt")
        return None
    except FileNotFoundError:
        logger.error("❌ File config.txt non trovato in backend_api/")
        return None
    except Exception as e:
        logger.error(f"❌ Errore durante la lettura di config.txt: {e}")
        return None

OPENAI_API_KEY = load_api_key()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
CHATGPT_MODEL = "gpt-4o-mini"  # Ottimo rapporto qualità/prezzo per uso tecnico

# Carica embeddings cache per RAG
EMBEDDINGS_CACHE = PROJECT_ROOT / "ai_system" / "Embedding" / "teklab_embeddings_cache.pkl"
_embeddings_cache = None
_model_embeddings = None

# Shared keyword list per product-family queries
FAMILY_QUERY_KEYWORDS = [
    'tipologie', 'tipologia', 'tipi', 'tipo', 'varianti', 'modelli', 'versioni',
    'esistono', 'quante', 'catalogo', 'gamma',
    'types', 'type', 'variants', 'models', 'versions', 'how many', 'list', 'range'
]

# Import configurazione prompt
def load_system_prompt():
    """Carica SYSTEM_PROMPT da prompts_config_chatgpt.py (versione ottimizzata per ChatGPT)"""
    try:
        import importlib
        import prompts_config_chatgpt
        importlib.reload(prompts_config_chatgpt)
        
        prompt = prompts_config_chatgpt.SYSTEM_PROMPT
        logger.info("✅ Configurazione Teklab caricata (SYSTEM_PROMPT - ChatGPT version)")
        logger.info(f"   Lunghezza prompt: {len(prompt)} chars (~{len(prompt)//4} token)")
        return prompt
    except ImportError as e:
        logger.warning(f"⚠️  prompts_config_chatgpt non trovato: {e}")
        logger.warning(f"   Tentativo fallback con prompts_config.py...")
        try:
            import prompts_config
            importlib.reload(prompts_config)
            prompt = prompts_config.SYSTEM_PROMPT
            logger.info("✅ Usato prompt standard (prompts_config.py)")
            return prompt
        except:
            fallback = """You are a technical assistant for Teklab industrial refrigeration products.

Provide accurate, professional information about Teklab products based on the provided documentation.
Be concise, technical, and precise. Answer ONLY based on the context provided.
Respond in the same language as the user's question."""
            logger.warning(f"   Uso prompt di fallback ({len(fallback)} chars)")
            return fallback

SYSTEM_PROMPT = load_system_prompt()

def load_embeddings():
    """Carica cache embeddings per RAG"""
    global _embeddings_cache, _model_embeddings
    
    if _embeddings_cache is not None:
        return True
    
    try:
        logger.info("📚 Caricamento embeddings cache (TEKLAB chunks)...")
        with open(EMBEDDINGS_CACHE, 'rb') as f:
            _embeddings_cache = pickle.load(f)
        
        from sentence_transformers import SentenceTransformer
        model_name = _embeddings_cache.get('model', 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        
        logger.info("   Device: CPU")
        logger.info("   ⏳ Caricamento modello embeddings da cache locale...")
        
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        os.environ['HF_HUB_OFFLINE'] = '1'
        
        _model_embeddings = SentenceTransformer(model_name, device='cpu')
        
        embeddings_count = len(_embeddings_cache.get('embeddings', {}))
        chunks_count = len(_embeddings_cache.get('chunks_data', {}))
        logger.info(f"✅ Embeddings caricati: {embeddings_count} vettori, {chunks_count} chunk unici")
        return True
        
    except FileNotFoundError:
        logger.error(f"❌ Cache embeddings non trovata: {EMBEDDINGS_CACHE}")
        return False
    except Exception as e:
        logger.error(f"❌ Errore caricamento embeddings: {e}")
        return False

def search_relevant_chunks(query, top_k=5):
    """Cerca chunks rilevanti usando RAG (stesso algoritmo di app.py)"""
    
    if not load_embeddings() or not torch or not util:
        logger.error("Cache embeddings o librerie ML non disponibili")
        return []
    
    chunk_texts = _embeddings_cache.get('chunk_texts', {})
    
    logger.info(f"\n{'='*80}")
    logger.info(f"🔍 RAG SEARCH")
    logger.info(f"📝 Query: '{query}'")
    logger.info(f"⏱️  Timer avviato: {time.strftime('%H:%M:%S')}")
    
    # Query encoding
    query_embeddings = _model_embeddings.encode([query], convert_to_tensor=True, device='cpu')
    
    # Converti embeddings da dict a tensor
    embeddings_data = _embeddings_cache['embeddings']
    chunks_data = _embeddings_cache['chunks_data']
    
    if isinstance(embeddings_data, dict):
        chunk_ids_sorted = sorted(embeddings_data.keys())
        embeddings_list = []
        for chunk_id in chunk_ids_sorted:
            emb = embeddings_data[chunk_id]
            if isinstance(emb, np.ndarray):
                emb = torch.from_numpy(emb)
            embeddings_list.append(emb)
        embeddings_tensor = torch.stack(embeddings_list)
        idx_to_chunk_id = {i: chunk_id for i, chunk_id in enumerate(chunk_ids_sorted)}
    else:
        embeddings_tensor = embeddings_data
        idx_to_chunk_id = {i: i for i in range(len(embeddings_tensor))}
    
    # Calcola similarità
    all_similarities = util.pytorch_cos_sim(query_embeddings, embeddings_tensor)
    aggregated_similarities, _ = torch.max(all_similarities, dim=0)
    
    # Pre-filtering: top 30 candidati
    num_candidates = min(30, len(aggregated_similarities))
    top_candidate_scores, top_candidate_indices = torch.topk(aggregated_similarities, k=num_candidates)
    
    logger.info(f"🚀 FASE 1: PRE-FILTERING")
    logger.info(f"   ✅ Trovati {num_candidates} candidati iniziali")
    
    # Re-ranking con boost Q&A e keywords
    scored_results = []
    chunks_data_keys = list(chunks_data.keys())
    
    for i in range(num_candidates):
        idx = top_candidate_indices[i].item()
        similarity_score = top_candidate_scores[i].item()
        
        chunk_id = idx_to_chunk_id.get(idx, idx)
        
        # Rimuovi suffisso per lookup
        base_chunk_id = chunk_id
        if isinstance(chunk_id, str) and ('|qa_' in chunk_id or '|chunk_' in chunk_id or '|keywords' in chunk_id):
            base_chunk_id = chunk_id.split('|')[0]
        
        chunk_data = None
        if base_chunk_id in chunks_data:
            chunk_data = chunks_data[base_chunk_id]
        elif idx in chunks_data:
            chunk_data = chunks_data[idx]
        elif isinstance(idx, int) and idx < len(chunks_data_keys):
            actual_key = chunks_data_keys[idx]
            chunk_data = chunks_data[actual_key]
        
        if chunk_data is None:
            continue
        
        chunk_text = chunk_texts.get(chunk_id, chunk_data.get('content', ''))
        
        # Q&A e Keywords boost
        is_qa_chunk = '|qa_' in str(chunk_id)
        is_keywords_chunk = '|keywords' in str(chunk_id)
        qa_boost = 0.15 if is_qa_chunk else 0.0
        keywords_boost = 0.20 if is_keywords_chunk else 0.0
        
        # Hybrid score
        hybrid_score = (0.60 * similarity_score) + (0.15 * qa_boost) + (0.25 * keywords_boost)
        
        scored_results.append({
            'chunk_data': chunk_data,
            'chunk_id': chunk_id,
            'chunk_text': chunk_text,
            'similarity': similarity_score,
            'hybrid_score': hybrid_score
        })
    
    logger.info(f"🔥 FASE 2: RE-RANKING")
    logger.info(f"   ✅ Completato re-ranking di {num_candidates} candidati")
    
    # Ordina per hybrid score
    scored_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
    
    # Adaptive threshold
    if scored_results:
        top_score = scored_results[0]['hybrid_score']
        adaptive_threshold = max(0.30, min(0.40, top_score * 0.70))
        
        filtered_results = [r for r in scored_results if r['hybrid_score'] >= adaptive_threshold]
        
        logger.info(f"🎯 FASE 3: THRESHOLD FILTERING")
        logger.info(f"   Threshold: {adaptive_threshold:.4f}")
        logger.info(f"   ✅ Risultati filtrati: {len(filtered_results)}")
    else:
        filtered_results = []
    
    # Restituisci top_k
    final_results = filtered_results[:top_k]
    
    logger.info(f"✅ RISULTATI FINALI: {len(final_results)} chunk")
    for i, r in enumerate(final_results, 1):
        logger.info(f"   [{i}] {r['chunk_data'].get('category', 'N/A')} | {r['chunk_data'].get('title', 'Unknown')[:40]} | score={r['hybrid_score']:.3f}")
    logger.info(f"{'='*80}\n")
    
    return [{
        **res['chunk_data'],
        'chunk_text': res['chunk_text'],
        'similarity': res['similarity'],
        'hybrid_score': res['hybrid_score']
    } for res in final_results]

# Inizializza Flask
app = Flask(__name__)
app.secret_key = 'teklab-chatgpt-secret-key-change-in-production'
CORS(app, supports_credentials=True)

# Session management
_conversation_sessions = {}
_token_usage_sessions = {}  # Track token usage per session
MAX_HISTORY_TURNS = 10  # Mantiene ultimi 10 scambi di conversazione per contesto

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        _token_usage_sessions[session['session_id']] = {
            'total_tokens': 0,
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'requests_count': 0,
            'started_at': datetime.now().isoformat()
        }
    return session['session_id']

def update_token_usage(session_id, prompt_tokens, completion_tokens):
    """Aggiorna statistiche token per la sessione"""
    if session_id not in _token_usage_sessions:
        _token_usage_sessions[session_id] = {
            'total_tokens': 0,
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'requests_count': 0,
            'started_at': datetime.now().isoformat()
        }
    
    _token_usage_sessions[session_id]['prompt_tokens'] += prompt_tokens
    _token_usage_sessions[session_id]['completion_tokens'] += completion_tokens
    _token_usage_sessions[session_id]['total_tokens'] += (prompt_tokens + completion_tokens)
    _token_usage_sessions[session_id]['requests_count'] += 1
    _token_usage_sessions[session_id]['last_request'] = datetime.now().isoformat()

def get_token_usage(session_id):
    """Ottiene statistiche token per la sessione"""
    return _token_usage_sessions.get(session_id, {
        'total_tokens': 0,
        'prompt_tokens': 0,
        'completion_tokens': 0,
        'requests_count': 0
    })

def get_conversation_history(session_id):
    if session_id not in _conversation_sessions:
        _conversation_sessions[session_id] = []
    return _conversation_sessions[session_id]

def clear_conversation_history(session_id):
    if session_id in _conversation_sessions:
        _conversation_sessions[session_id] = []

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    total_turns = sum(len(hist) for hist in _conversation_sessions.values())
    total_tokens = sum(usage['total_tokens'] for usage in _token_usage_sessions.values())
    total_requests = sum(usage['requests_count'] for usage in _token_usage_sessions.values())
    
    return jsonify({
        'status': 'healthy',
        'service': 'teklab-ai-chatgpt',
        'model': CHATGPT_MODEL,
        'model_loaded': True,
        'timestamp': datetime.now().isoformat(),
        'conversation_turns': total_turns,
        'active_sessions': len(_conversation_sessions),
        'total_tokens_used': total_tokens,
        'total_requests': total_requests,
        'estimated_cost_usd': (total_tokens / 1000000) * 0.15
    })

@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    Endpoint streaming con Server-Sent Events (SSE)
    Compatibile con UI_experience/index.html
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        reset_history = data.get('reset_history', False)
        
        if not user_message:
            return jsonify({'error': 'Messaggio vuoto'}), 400
        
        if len(user_message) > 5000:
            return jsonify({'error': 'Messaggio troppo lungo (max 5000 caratteri)'}), 400
        
        session_id = get_session_id()
        
        if reset_history:
            clear_conversation_history(session_id)
        
        # Verifica API key (caricata da config.txt)
        if not OPENAI_API_KEY or not client:
            return jsonify({
                'error': 'OpenAI API key non configurata. Controlla backend_api/config.txt'
            }), 500
        
        logger.info(f"👤 User {session_id[:8]}... - Message: '{user_message[:50]}...'")
        
        def generate():
            try:
                request_id = str(uuid.uuid4())
                processing_start_time = time.time()
                
                # Invia evento init
                yield f"data: {json.dumps({'type': 'init', 'request_id': request_id})}\n\n"
                
                # Ottieni cronologia per mostrare contesto disponibile
                history = get_conversation_history(session_id)
                
                logger.info(f"\n{'='*80}")
                logger.info(f"🟢 Processing message for session {session_id[:8]}")
                logger.info(f"📚 Cronologia: {len(history)} scambi memorizzati (max {MAX_HISTORY_TURNS})")
                logger.info(f"⏱️  Timer avviato: {time.strftime('%H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
                # RAG Search
                logger.info("🔍 Avvio RAG Search...")
                rag_start = time.time()
                
                # Arricchisci query con contesto conversazione per RAG (ultimi 10 scambi)
                history = get_conversation_history(session_id)
                enriched_query = user_message
                
                if history:
                    # Se la query contiene pronomi vaghi o richieste di approfondimento
                    vague_terms = ['questi', 'quelli', 'those', 'them', 'questo', 'quello', 
                                   'di più', 'more about', 'approfondisci', 'expand', 'tell me more',
                                   'come', 'perché', 'why', 'how', 'cosa', 'what']
                    
                    has_vague_term = any(word in user_message.lower() for word in vague_terms)
                    
                    if has_vague_term:
                        # Prendi ultimi 2-3 scambi per contesto ricco
                        recent_turns = history[-3:] if len(history) >= 3 else history
                        context_parts = []
                        for turn in recent_turns:
                            if turn.get('user'):
                                context_parts.append(turn['user'])
                        
                        # Combina contesto + query corrente
                        context_str = " ".join(context_parts[-2:])  # Ultimi 2 messaggi utente
                        enriched_query = f"{context_str} {user_message}"
                        logger.info(f"   🔗 Query arricchita con contesto (ultimi {len(context_parts)} messaggi)")
                        logger.info(f"   📝 '{enriched_query[:100]}...'")
                
                query_lower = user_message.lower()
                is_family_query = any(keyword in query_lower for keyword in FAMILY_QUERY_KEYWORDS)
                top_k = 8 if is_family_query else 3
                
                relevant_chunks = search_relevant_chunks(enriched_query, top_k=top_k)
                
                rag_time = time.time() - rag_start
                logger.info(f"⏱️  RAG Search completata: {rag_time:.2f}s")
                logger.info(f"   Query type: {'PRODUCT FAMILY' if is_family_query else 'SPECIFIC'}")
                logger.info(f"   Risultati trovati: {len(relevant_chunks)}\n")
                
                # Invia sources
                if relevant_chunks:
                    sources_data = {
                        'type': 'sources',
                        'sources': [
                            {
                                'product': c.get('category', 'Unknown'),
                                'similarity': float(c.get('similarity', 0)),
                                'title': c.get('title', c.get('filename', ''))
                            }
                            for c in relevant_chunks
                        ]
                    }
                    yield f"data: {json.dumps(sources_data)}\n\n"
                    logger.info(f"📤 Sources inviati al client ({len(relevant_chunks)} chunks)")
                
                # Costruisci contesto RAG
                if relevant_chunks:
                    context_parts = []
                    for chunk in relevant_chunks:
                        chunk_body = chunk.get('sanitized_content') or chunk.get('chunk_text', chunk.get('content', ''))
                        # Usa 'family' se esiste, altrimenti prova altre chiavi
                        category = chunk.get('family') or chunk.get('product_category', 'Unknown')
                        context_parts.append(f"[{category}] {chunk_body}")
                    rag_context = "\n\n".join(context_parts)
                    
                    # Limita lunghezza contesto
                    max_context_length = 3000
                    if len(rag_context) > max_context_length:
                        chunks_list = rag_context.split('\n\n')
                        truncated_chunks = []
                        current_length = 0
                        for chunk in chunks_list:
                            if current_length + len(chunk) <= max_context_length:
                                truncated_chunks.append(chunk)
                                current_length += len(chunk)
                            else:
                                break
                        rag_context = '\n\n'.join(truncated_chunks)
                else:
                    rag_context = ""
                
                # Costruisci messaggi per ChatGPT
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT}
                ]
                
                # Aggiungi cronologia conversazione (ultimi 5 turni = 10 messaggi)
                # Mantiene contesto ricco senza eccedere token limit
                history = get_conversation_history(session_id)
                recent_history = history[-5:] if len(history) > 5 else history
                
                for turn in recent_history:
                    messages.append({"role": "user", "content": turn.get('user', '')})
                    messages.append({"role": "assistant", "content": turn.get('assistant', '')})
                
                logger.info(f"   💬 Contesto conversazione: {len(recent_history)} turni precedenti")
                # Aggiungi messaggio corrente con contesto RAG
                if rag_context:
                    user_content = f"""Technical documentation:

{rag_context}

---

Customer question: {user_message}"""
                else:
                    user_content = user_message
                
                messages.append({"role": "user", "content": user_content})
                
                # Chiamata ChatGPT con streaming
                logger.info(f"\n{'='*80}")
                logger.info(f"🤖 CHATGPT GENERATION START")
                logger.info(f"   Model: {CHATGPT_MODEL}")
                logger.info(f"   Messages: {len(messages)}")
                logger.info(f"⏱️  Timer avviato: {time.strftime('%H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
                generation_start = time.time()
                full_response = ""
                prompt_tokens = 0
                completion_tokens = 0
                
                try:
                    stream = client.chat.completions.create(
                        model=CHATGPT_MODEL,
                        messages=messages,
                        stream=True,
                        temperature=0.3,
                        max_tokens=1500,
                        stream_options={"include_usage": True}  # Ottiene token usage anche con streaming
                    )
                    
                    for chunk in stream:
                        # Token content
                        if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                            token = chunk.choices[0].delta.content
                            full_response += token
                            
                            # Invia token al client
                            token_data = {'type': 'token', 'token': token}
                            yield f"data: {json.dumps(token_data)}\n\n"
                        
                        # Token usage (arriva nell'ultimo chunk)
                        if hasattr(chunk, 'usage') and chunk.usage:
                            prompt_tokens = chunk.usage.prompt_tokens
                            completion_tokens = chunk.usage.completion_tokens
                    
                    generation_time = time.time() - generation_start
                    
                    # Update token usage stats
                    if prompt_tokens > 0 or completion_tokens > 0:
                        update_token_usage(session_id, prompt_tokens, completion_tokens)
                        total_tokens = prompt_tokens + completion_tokens
                        session_usage = get_token_usage(session_id)
                        
                        logger.info(f"\n{'='*80}")
                        logger.info(f"✅ CHATGPT GENERATION COMPLETED")
                        logger.info(f"{'='*80}")
                        logger.info(f"   Response length: {len(full_response)} chars")
                        logger.info(f"⏱️  Generation time: {generation_time:.2f}s")
                        logger.info(f"💰 TOKEN USAGE:")
                        logger.info(f"   This request: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total")
                        logger.info(f"   Session total: {session_usage['total_tokens']} tokens ({session_usage['requests_count']} requests)")
                        logger.info(f"   Estimated cost: ${(total_tokens / 1000000) * 0.15:.6f} (this request)")
                        logger.info(f"   Session cost: ${(session_usage['total_tokens'] / 1000000) * 0.15:.6f} (cumulative)")
                        logger.info(f"{'='*80}\n")
                    else:
                        logger.info(f"\n{'='*80}")
                        logger.info(f"✅ CHATGPT GENERATION COMPLETED")
                        logger.info(f"{'='*80}")
                        logger.info(f"   Response length: {len(full_response)} chars")
                        logger.info(f"⏱️  Generation time: {generation_time:.2f}s")
                        logger.info(f"⚠️  Token usage not available (streaming without usage data)")
                        logger.info(f"{'='*80}\n")
                    
                except Exception as e:
                    logger.error(f"❌ ChatGPT API error: {e}")
                    error_data = {
                        'type': 'error',
                        'error': f'ChatGPT API error: {str(e)}'
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                    return
                
                # Salva in history
                if full_response and full_response.strip():
                    history = get_conversation_history(session_id)
                    history.append({
                        'user': user_message,
                        'assistant': full_response.strip(),
                        'timestamp': datetime.now().isoformat()
                    })
                    if len(history) > MAX_HISTORY_TURNS:
                        _conversation_sessions[session_id] = history[-MAX_HISTORY_TURNS:]
                    
                    logger.info(f"💾 Saved conversation turn (total: {len(history)} turns)")
                
                # Invia done event
                total_time = time.time() - processing_start_time
                
                done_data = {
                    'type': 'done',
                    'timestamp': datetime.now().isoformat(),
                    'total_time': total_time,
                    'rag_time': rag_time,
                    'generation_time': generation_time
                }
                yield f"data: {json.dumps(done_data)}\n\n"
                
                logger.info(f"\n{'='*80}")
                logger.info(f"⏱️  ⚡⚡⚡ TIMING SUMMARY ⚡⚡⚡")
                logger.info(f"{'='*80}")
                logger.info(f"   🔍 RAG Search: {rag_time:.2f}s")
                logger.info(f"   🤖 ChatGPT Generation: {generation_time:.2f}s")
                logger.info(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logger.info(f"   ⚡ TOTAL END-TO-END: {total_time:.2f}s")
                logger.info(f"   ⏰ Timestamp: {time.strftime('%H:%M:%S')}")
                logger.info(f"{'='*80}\n")
                
            except Exception as e:
                logger.error(f"❌ Error in generate: {e}", exc_info=True)
                error_data = {'type': 'error', 'error': str(e)}
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
        logger.error(f"❌ Error chat stream: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Restituisce cronologia conversazione con statistiche token"""
    try:
        session_id = get_session_id()
        history = get_conversation_history(session_id)
        token_stats = get_token_usage(session_id)
        
        return jsonify({
            'history': history,
            'count': len(history),
            'session_id': session_id[:8] + "...",
            'token_usage': token_stats,
            'estimated_cost_usd': (token_stats['total_tokens'] / 1000000) * 0.15
        })
    except Exception as e:
        logger.error(f"❌ Error get_history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_history():
    """Cancella cronologia conversazione"""
    try:
        session_id = get_session_id()
        clear_conversation_history(session_id)
        return jsonify({
            'status': 'success',
            'message': 'Storia cancellata',
            'session_id': session_id[:8] + "..."
        })
    except Exception as e:
        logger.error(f"❌ Error clear_history: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/reload_prompt', methods=['POST'])
def reload_prompt():
    """Hot reload SYSTEM_PROMPT from prompts_config_chatgpt.py"""
    global SYSTEM_PROMPT
    try:
        logger.info("🔄 Hot reload SYSTEM_PROMPT richiesto (ChatGPT version)...")
        old_length = len(SYSTEM_PROMPT)
        
        SYSTEM_PROMPT = load_system_prompt()
        new_length = len(SYSTEM_PROMPT)
        
        return jsonify({
            'status': 'success',
            'message': 'SYSTEM_PROMPT ricaricato da prompts_config_chatgpt.py',
            'old_length': old_length,
            'new_length': new_length,
            'changed': old_length != new_length
        })
    except Exception as e:
        logger.error(f"❌ Error reload_prompt: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Statistiche API con dettagli token"""
    total_turns = sum(len(hist) for hist in _conversation_sessions.values())
    total_tokens = sum(usage['total_tokens'] for usage in _token_usage_sessions.values())
    total_requests = sum(usage['requests_count'] for usage in _token_usage_sessions.values())
    
    return jsonify({
        'model': CHATGPT_MODEL,
        'model_loaded': True,
        'conversation_turns': total_turns,
        'active_sessions': len(_conversation_sessions),
        'system_prompt_length': len(SYSTEM_PROMPT),
        'token_usage': {
            'total_tokens': total_tokens,
            'total_requests': total_requests,
            'avg_tokens_per_request': round(total_tokens / total_requests, 2) if total_requests > 0 else 0,
            'estimated_cost_usd': (total_tokens / 1000000) * 0.15
        },
        'endpoints': {
            'health': 'GET /health',
            'chat_stream': 'POST /chat/stream',
            'history': 'GET /history',
            'clear': 'POST /clear',
            'reload_prompt': 'POST /reload_prompt',
            'stats': 'GET /stats'
        }
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("TEKLAB B2B AI - Backend API (ChatGPT + RAG)")
    print("="*70)
    
    # Verifica API key
    if not OPENAI_API_KEY or not client:
        print("\n❌ ERRORE: Chiave API OpenAI non configurata!")
        print("   Apri backend_api/config.txt e inserisci la tua API key:")
        print("   OPENAI_API_KEY=sk-proj-your_actual_key_here")
        print("\n   Ottieni la chiave su: https://platform.openai.com/api-keys")
        print("\n")
        import sys
        sys.exit(1)
    else:
        print(f"\n✅ OpenAI API key caricata da config.txt")
    
    print("\nSystem status:")
    print(f"   - ChatGPT Model: {CHATGPT_MODEL}")
    print("   - RAG Embeddings: Lazy loading")
    
    print("\n🌐 Server starting on http://localhost:5000")
    print("📱 Open UI_experience/index.html in browser")
    print("\nEndpoints:")
    print("   - POST   /chat/stream  -> Chat streaming (SSE)")
    print("   - GET    /health       -> Health check")
    print("   - GET    /history      -> Chat history")
    print("   - POST   /clear        -> Clear history")
    print("   - POST   /reload_prompt -> Hot reload SYSTEM_PROMPT")
    print("   - GET    /stats        -> Statistics")
    print("\n" + "="*70 + "\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
