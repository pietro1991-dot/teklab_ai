"""
Bot Telegram per Teklab AI Chatbot
USA LA STESSA LOGICA di scripts/6_chatbot_ollama.py
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import pickle
import json
import logging

# Import Telegram Bot API
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Setup paths (come 6_chatbot_ollama.py)
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

# Import configurazione Teklab
try:
    from prompts_config import SYSTEM_PROMPT, build_rag_prompt, build_simple_prompt
except ImportError as e:
    print(f"❌ Errore import prompts_config: {e}")
    SYSTEM_PROMPT = "You are a technical sales assistant for Teklab industrial sensors."
    
    def build_rag_prompt(context, query):
        return f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    
    def build_simple_prompt(query):
        return f"Question: {query}\n\nAnswer:"

# Ollama client
try:
    import requests
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configurazione
TELEGRAM_TOKEN = "8209626692:AAFJ6g5oFEDSS5U5aN_5UOLMetFzLPCUUnE"
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Storage conversazioni utenti
user_conversations: Dict[int, List[Dict]] = {}

# RAG System (caricato all'avvio come 6_chatbot_ollama.py)
chunk_embeddings = {}
qa_embeddings = {}
summary_embeddings = {}
chunks_data = {}
summaries_data = {}
embedding_model = None


def load_embeddings():
    """Carica embeddings RAG (IDENTICO a 6_chatbot_ollama.py)"""
    global chunk_embeddings, qa_embeddings, summary_embeddings, chunks_data, summaries_data, embedding_model
    
    embeddings_path = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl"
    
    if not embeddings_path.exists():
        # Prova con .backup
        embeddings_path = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl.backup"
    
    if not embeddings_path.exists():
        logger.warning(f"⚠️  Cache embeddings non trovata: {embeddings_path}")
        return False
    
    try:
        with open(embeddings_path, 'rb') as f:
            cache = pickle.load(f)
        
        chunk_embeddings = cache.get('chunk_embeddings', {})
        qa_embeddings = cache.get('qa_embeddings', {})
        summary_embeddings = cache.get('summary_embeddings', {})
        chunks_data = cache.get('chunks_data', {})
        summaries_data = cache.get('summaries_data', {})
        
        # Carica modello embeddings (FORZA CPU come 6_chatbot_ollama.py)
        from sentence_transformers import SentenceTransformer
        model_name = cache.get('model', 'all-MiniLM-L6-v2')
        logger.info(f"📚 Modello embeddings: {model_name} (CPU)")
        embedding_model = SentenceTransformer(model_name, device='cpu')
        
        total = len(chunk_embeddings) + len(qa_embeddings) + len(summary_embeddings)
        logger.info(f"✅ Caricati {total} embeddings RAG")
        logger.info(f"   • Chunks: {len(chunk_embeddings)}")
        logger.info(f"   • Q&A: {len(qa_embeddings)}")
        logger.info(f"   • Summaries: {len(summary_embeddings)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Errore caricamento embeddings: {e}")
        return False


def retrieve_context(query: str, top_k: int = 3, min_similarity: float = 0.28) -> tuple:
    """Recupera contesto RAG (IDENTICO a 6_chatbot_ollama.py)"""
    if not embedding_model or not chunk_embeddings:
        return "", []
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        
        query_emb = embedding_model.encode([query])[0]
        
        similarities = []
        for chunk_id, chunk_emb in chunk_embeddings.items():
            sim = cosine_similarity([query_emb], [chunk_emb])[0][0]
            similarities.append((chunk_id, sim, 'chunk'))
        
        # DEBUG
        logger.info(f"🔍 RAG Search: '{query[:50]}'")
        similarities_sorted = sorted(similarities, key=lambda x: x[1], reverse=True)
        logger.info(f"   Top 5 similarities:")
        for i, (cid, sim, _) in enumerate(similarities_sorted[:5], 1):
            ok = "✅" if sim >= min_similarity else "❌"
            logger.info(f"      {ok} [{i}] sim={sim:.4f} - {cid[:50]}")
        
        if summary_embeddings:
            for summary_id, summary_emb in summary_embeddings.items():
                sim = cosine_similarity([query_emb], [summary_emb])[0][0]
                similarities.append((summary_id, sim, 'summary'))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filtra per similarity threshold
        filtered = [(item_id, score, item_type) for item_id, score, item_type in similarities if score >= min_similarity]
        top_items = filtered[:top_k]
        
        if not top_items:
            logger.warning(f"⚠️  Nessun chunk rilevante (tutti <{min_similarity:.2f} similarity)")
            return "", []
        
        context_parts = []
        retrieved_metadata = []
        
        for item_id, score, item_type in top_items:
            if item_type == 'chunk':
                chunk_data = chunks_data.get(item_id, {})
                
                # ARCHITETTURA TEKLAB: usa messages[2] (assistant formatted)
                chunk_text = ''
                if 'messages' in chunk_data:
                    if len(chunk_data['messages']) > 2:
                        chunk_text = chunk_data['messages'][2].get('content', '')
                    elif len(chunk_data['messages']) > 1:
                        chunk_text = chunk_data['messages'][1].get('content', '')
                
                if not chunk_text:
                    chunk_text = chunk_data.get('original_text', chunk_data.get('testo', ''))
                
                if chunk_text:
                    metadata = chunk_data.get('metadata', {})
                    product_model = metadata.get('product_model', 'Unknown')
                    category = chunk_data.get('category', 'unknown')
                    
                    context_parts.append(f"[Product: {product_model}]\n{chunk_text}\n")
                    
                    retrieved_metadata.append({
                        "chunk_id": item_id,
                        "similarity_score": round(float(score), 4),
                        "product": product_model,
                        "category": category
                    })
        
        context_text = "\n---\n".join(context_parts) if context_parts else ""
        return context_text, retrieved_metadata
        
    except Exception as e:
        logger.error(f"⚠️  Errore retrieve RAG: {e}")
        return "", []


def chat_with_ollama(user_message: str, conversation_history: List[Dict]) -> Dict:
    """Genera risposta con Ollama (IDENTICO a 6_chatbot_ollama.py)"""
    
    import time
    
    start_total = time.time()
    
    # Retrieve RAG context - ALLINEATO a backend_api/app.py
    start_retrieval = time.time()
    rag_context, retrieved_chunks = retrieve_context(user_message, top_k=3, min_similarity=0.28)  # ⚡ STESSO THRESHOLD di app.py
    retrieval_time = time.time() - start_retrieval
    
    # DEBUG: Log chunks
    logger.info(f"   Chunks trovati: {len(retrieved_chunks)}")
    for i, chunk_meta in enumerate(retrieved_chunks[:3]):
        product = chunk_meta.get('product', 'Unknown')
        category = chunk_meta.get('category', 'unknown')
        sim = chunk_meta.get('similarity_score', 0)
        logger.info(f"   [{i+1}] {product:25s} | {category:12s} | sim={sim:.3f}")
    
    # Costruisci prompt con cronologia RIDOTTA (Telegram: conciso)
    history_context = ""
    if conversation_history:
        recent_history = conversation_history[-2:]  # 🎯 Solo ULTIMI 2 turni (era 10 - troppo!)
        context_parts = []
        for turn in recent_history:
            # Tronca risposte lunghe nella cronologia
            user_msg = turn['user'][:150]
            assistant_msg = turn['assistant'][:200]
            context_parts.append(f"User: {user_msg}")
            context_parts.append(f"Assistant: {assistant_msg}")
        history_context = "\n".join(context_parts)
    
    if rag_context:
        # Tronca context se troppo lungo
        max_context_length = 2500  # ⚡ ALLINEATO a app.py
        if len(rag_context) > max_context_length:
            rag_context = rag_context[:max_context_length] + "\n\n[... Additional technical details available on request ...]"
        
        # 🎯 USA TEMPLATE CENTRALIZZATO da prompts_config.py (STESSO di app.py!)
        full_prompt = build_rag_prompt(rag_context, user_message)
        
        if history_context:
            full_prompt = full_prompt.replace("TEKLAB ASSISTANT RESPONSE:", f"{history_context}\n\nTEKLAB ASSISTANT RESPONSE:")
    else:
        # ⚠️ NESSUN CHUNK RILEVANTE - Rispondi onestamente
        logger.warning("⚠️  Nessun chunk rilevante trovato - risposta fallback")
        return {
            'response': "Mi dispiace, non ho informazioni sufficienti nella documentazione per rispondere accuratamente alla tua domanda. Per dettagli tecnici specifici, contatta il supporto Teklab: support@teklab.eu",
            'rag_context': "",
            'retrieved_chunks': [],
            'timing': {'retrieval_time': round(retrieval_time, 3), 'generation_time': 0, 'total_time': round(retrieval_time, 3)},
            'generation_mode': 'no_context_fallback',
            'num_predict': 0,
            'done_reason': 'no_context',
            'error': False
        }
    
    # Genera risposta con Ollama - SINGOLO LIVELLO (come UI quando completa naturalmente)
    try:
        logger.info("⏳ Generazione Ollama...")
        start_generation = time.time()
        
        # 🎯 TELEGRAM: Usa SOLO primo livello (400 token) come fa UI nella maggior parte dei casi
        # PROBLEMA: stream=False non ritorna done_reason='stop' correttamente → sempre 'length'
        # SOLUZIONE: Generazione singola da 400 token (sufficiente per "150-250 words" del prompt)
        num_predict = 400  # Stesso primo livello di app.py
        
        logger.info(f"📡 Calling Ollama API (model: {OLLAMA_MODEL}, num_predict={num_predict})...")
        
        # Chiama Ollama
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,  # Telegram non fa streaming
            "options": {
                "temperature": 0.6,
                "num_predict": num_predict,
                "top_p": 0.85,
                "num_ctx": 4096,
                "repeat_penalty": 1.1,
                "stop": ["\n\n\n", "CUSTOMER:", "QUESTION:", "---"]
            }
        }
        
        timeout = 180
        response = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result.get('response', '').strip()
        done_reason = result.get('done_reason', 'stop')
        
        logger.info(f"   Ollama done_reason: '{done_reason}' | Response length: {len(assistant_message)} chars")
        
        generation_time = time.time() - start_generation
        total_time = time.time() - start_total
        
        return {
            'response': assistant_message,
            'rag_context': rag_context,
            'retrieved_chunks': retrieved_chunks,
            'timing': {
                'retrieval_time': round(retrieval_time, 3),
                'generation_time': round(generation_time, 3),
                'total_time': round(total_time, 3)
            },
            'generation_info': {
                'num_predict': num_predict,
                'done_reason': done_reason,
                'mode': 'single_level'  # Telegram: singolo livello 400 token (come UI quando completa)
            },
            'error': False
        }
        
    except Exception as e:
        logger.error(f"❌ Errore Ollama: {e}")
        return {
            'response': f"❌ Errore generazione risposta: {str(e)}",
            'error': True
        }


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler /start"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Cliente"
    
    user_conversations[user_id] = []
    
    welcome_message = f"""🔧 Benvenuto in Teklab AI Assistant, {user_name}!

Sono il tuo assistente tecnico per i sensori industriali Teklab.

🎯 Selezione prodotti:
• TK series (TK1+, TK3+, TK4) - Controllori livello olio
• LC series (LC-PS, LC-XP, LC-XT) - Interruttori di livello
• Sensori ATEX antideflagranti

🔧 Supporto tecnico:
• Specifiche pressione e temperatura
• Compatibilità refrigeranti
• Integrazione MODBUS/4-20mA
• Troubleshooting

💬 Esempi di domande:
• "Che differenza c'è tra TK3+ e TK4?"
• "Quale sensore per R410A?"
• "Come si configura MODBUS?"

⚙️ Comandi:
/help - Guida
/clear - Cancella cronologia
/status - Stato sistema

Scrivi la tua domanda! 🚀"""
    
    keyboard = [
        [InlineKeyboardButton("TK3+ vs TK4", callback_data="prompt_tk3_vs_tk4")],
        [InlineKeyboardButton("R410A sensor", callback_data="prompt_r410a")],
        [InlineKeyboardButton("ATEX ammonia", callback_data="prompt_atex_ammonia")],
        [InlineKeyboardButton("MODBUS setup", callback_data="prompt_modbus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler /help"""
    help_text = """🔧 TEKLAB AI ASSISTANT

Sono un assistente tecnico specializzato sui sensori industriali Teklab.

📝 Esempi domande:
• "Sensore livello olio per compressore 46 bar R404A"
• "Differenza tra TK3+ e TK4?"
• "Sensore per serbatoio ammoniaca"
• "Configurare MODBUS su TK4"

⚙️ Comandi:
/start - Benvenuto
/help - Questa guida
/clear - Cancella cronologia
/status - Stato sistema"""
    
    await update.message.reply_text(help_text)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler /clear"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    await update.message.reply_text("🔄 Cronologia cancellata!")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler /status"""
    user_id = update.effective_user.id
    conversation_count = len(user_conversations.get(user_id, []))
    
    # Verifica Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "🟢 Attivo" if response.status_code == 200 else "🔴 Errore"
    except Exception:
        ollama_status = "🔴 Offline"
    
    rag_status = "🟢 Caricato" if embedding_model else "🔴 Non caricato"
    
    status_text = f"""🔧 STATO SISTEMA TEKLAB AI

🤖 Ollama: {ollama_status}
📚 RAG System: {rag_status}
💬 Tue conversazioni: {conversation_count}
📦 Chunks disponibili: {len(chunks_data)}
🧠 Embeddings: {len(chunk_embeddings)}"""
    
    await update.message.reply_text(status_text)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler callback buttons"""
    query = update.callback_query
    await query.answer()
    
    prompts = {
        'prompt_tk3_vs_tk4': "What's the difference between TK3+ and TK4?",
        'prompt_r410a': "Which sensor for R410A refrigerant?",
        'prompt_atex_ammonia': "What are ATEX requirements for ammonia?",
        'prompt_modbus': "How does MODBUS communication work?"
    }
    
    prompt = prompts.get(query.data, "")
    
    if prompt:
        await query.edit_message_text(f"📝 {prompt}")
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        user_id = update.effective_chat.id
        if user_id not in user_conversations:
            user_conversations[user_id] = []
        
        result = chat_with_ollama(prompt, user_conversations[user_id])
        response_text = result['response']
        
        if not result.get('error', False):
            user_conversations[user_id].append({
                'user': prompt,
                'assistant': response_text,
                'timestamp': datetime.now().isoformat()
            })
        
        # Aggiungi info fonti
        chunks = result.get('retrieved_chunks', [])
        if chunks:
            source_info = "\n\n📚 Fonti utilizzate:"
            for chunk in chunks[:2]:
                source_info += f"\n• {chunk.get('product', 'Unknown')} (sim: {chunk.get('similarity_score', 0):.2f})"
            response_text += source_info
        
        # Invia risposta
        if len(response_text) > 4096:
            chunks_text = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk_text in chunks_text:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=chunk_text)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler messaggi"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    logger.info(f"📩 Messaggio da {user_id}: {user_message[:100]}...")
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Genera risposta usando STESSA LOGICA di 6_chatbot_ollama.py
        result = chat_with_ollama(user_message, user_conversations[user_id])
        response_text = result['response']
        has_error = result.get('error', False)
        
        # Salva in cronologia
        if not has_error:
            user_conversations[user_id].append({
                'user': user_message,
                'assistant': response_text,
                'timestamp': datetime.now().isoformat(),
                'retrieved_chunks': result.get('retrieved_chunks', [])
            })
            
            # Limita cronologia
            if len(user_conversations[user_id]) > 10:
                user_conversations[user_id] = user_conversations[user_id][-10:]
        
        # Aggiungi fonti
        chunks = result.get('retrieved_chunks', [])
        if chunks and not has_error:
            source_info = "\n\n📚 Fonti utilizzate:"
            for chunk in chunks[:2]:
                source_info += f"\n• {chunk.get('product', 'Unknown')} (sim: {chunk.get('similarity_score', 0):.2f})"
            response_text += source_info
        
        # Invia risposta (senza Markdown per evitare errori parsing)
        if len(response_text) > 4096:
            chunks_text = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
            for chunk_text in chunks_text:
                await update.message.reply_text(chunk_text)
        else:
            await update.message.reply_text(response_text)
        
        logger.info(f"✅ Risposta inviata a {user_id} ({len(response_text)} chars)")
        
    except Exception as e:
        logger.error(f"❌ Errore: {e}", exc_info=True)
        await update.message.reply_text("❌ Si è verificato un errore. Riprova.")


def main() -> None:
    """Avvia bot"""
    print("\n" + "="*70)
    print("🤖 TEKLAB TELEGRAM BOT - Avvio...")
    print("="*70)
    
    # Verifica Ollama
    print("🔍 Verifica Ollama...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✅ Ollama attivo")
        else:
            print("❌ Ollama non risponde")
            return
    except Exception:
        print("❌ Ollama non raggiungibile")
        print("   Avvia Ollama: ollama serve")
        return
    
    # Carica RAG
    print("📚 Caricamento RAG System...")
    if load_embeddings():
        print("✅ RAG System pronto")
    else:
        print("⚠️  RAG System non disponibile - bot funzionerà senza contesto")
    
    # Crea application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Aggiungi handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot Telegram avviato!")
    print("📱 Cerca @teklab_ai_b2b_assistant_bot su Telegram")
    print("⚙️  Premi Ctrl+C per fermare")
    print("="*70)
    
    # Avvia bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
