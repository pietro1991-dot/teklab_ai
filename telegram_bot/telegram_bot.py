"""
Bot Telegram per Teklab AI Chatbot
Utilizza lo stesso sistema RAG del backend Flask
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import pickle
import numpy as np
import requests

# Import Telegram Bot API
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import configurazione
try:
    from config import (
        TELEGRAM_TOKEN, BACKEND_URL, OLLAMA_URL, OLLAMA_MODEL,
        RAG_THRESHOLD, RAG_TOP_K, RAG_MAX_CONTEXT, 
        MAX_CONVERSATION_HISTORY, TELEGRAM_MESSAGE_LIMIT,
        WELCOME_MESSAGE, ERROR_MESSAGE, SYSTEM_OFFLINE_MESSAGE
    )
except ImportError:
    logger.warning("Config file not found, using defaults")
    # Fallback configuration
    TELEGRAM_TOKEN = "8209626692:AAFJ6g5oFEDSS5U5aN_5UOLMetFzLPCUUnE"
    BACKEND_URL = "http://localhost:5000"
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "llama3.2:3b"
    RAG_THRESHOLD = 0.28
    RAG_TOP_K = 3
    RAG_MAX_CONTEXT = 4000
    MAX_CONVERSATION_HISTORY = 10
    TELEGRAM_MESSAGE_LIMIT = 4096
    WELCOME_MESSAGE = "🔧 Benvenuto in Teklab AI Assistant!"
    ERROR_MESSAGE = "❌ Errore nel sistema."
    SYSTEM_OFFLINE_MESSAGE = "⚠️ Sistema non disponibile."

# Setup paths per RAG system
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

# Import prompt configuration
try:
    from prompts_config import SYSTEM_PROMPT
    logger.info("✅ Configurazione Teklab caricata")
except ImportError as e:
    logger.warning(f"⚠️  prompts_config non trovato: {e}")
    SYSTEM_PROMPT = """You are a technical sales assistant for Teklab industrial sensors.
Provide accurate, professional information about Teklab products."""

# Storage per conversazioni degli utenti
user_conversations: Dict[int, List[Dict]] = {}

# RAG System Cache
embeddings_cache = None
chunks_data = None

def load_rag_system():
    """Carica il sistema RAG (embeddings e chunks)"""
    global embeddings_cache, chunks_data
    
    try:
        # Carica embeddings
        embeddings_path = PROJECT_ROOT / "ai_system" / "Embedding" / "embeddings_cache.pkl"
        with open(embeddings_path, 'rb') as f:
            embeddings_cache = pickle.load(f)
        logger.info(f"✅ Embeddings caricati: {len(embeddings_cache)} chunks")
        
        # Carica chunks data
        chunks_path = PROJECT_ROOT / "ai_system" / "Embedding" / "chunks_data.pkl"
        with open(chunks_path, 'rb') as f:
            chunks_data = pickle.load(f)
        logger.info(f"✅ Chunks data caricati: {len(chunks_data)} entries")
        
        return True
    except Exception as e:
        logger.error(f"❌ Errore caricamento RAG: {e}")
        return False

def cosine_similarity(a, b):
    """Calcola similarità coseno tra due vettori"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_relevant_chunks(query: str, top_k: int = 3) -> List[Dict]:
    """Cerca chunks rilevanti usando il sistema RAG"""
    if not embeddings_cache or not chunks_data:
        return []
    
    try:
        # Genera embedding per la query
        query_payload = {
            "model": "nomic-embed-text:latest",
            "prompt": query
        }
        response = requests.post("http://localhost:11434/api/embeddings", json=query_payload, timeout=30)
        response.raise_for_status()
        query_embedding = response.json()['embedding']
        
        # Calcola similarità con tutti i chunks
        similarities = []
        chunk_ids = list(embeddings_cache.keys())
        chunk_embs = [embeddings_cache[chunk_id] for chunk_id in chunk_ids]
        
        sims = [cosine_similarity(query_embedding, emb) for emb in chunk_embs]
        
        # Filtra per threshold
        for i, (chunk_id, sim) in enumerate(zip(chunk_ids, sims)):
            if sim >= RAG_THRESHOLD:
                similarities.append((chunk_id, sim))
        
        # Ordina per similarità
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Prendi top_k risultati
        results = []
        for chunk_id, sim in similarities[:top_k]:
            chunk_data = chunks_data.get(chunk_id, {})
            
            # Usa il messaggio assistant (formatted response)
            messages = chunk_data.get('messages', [])
            content = ""
            
            if len(messages) > 2:
                content = messages[2].get('content', '')
            elif len(messages) > 1:
                content = messages[1].get('content', '')
            
            metadata = chunk_data.get('metadata', {})
            
            results.append({
                'content': content,
                'similarity': float(sim),
                'product': metadata.get('product_model', ''),
                'category': chunk_data.get('category', '')
            })
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Errore ricerca RAG: {e}")
        return []

def generate_response_with_ollama(user_message: str) -> Dict:
    """Genera risposta usando Ollama + RAG"""
    try:
        # Cerca chunks rilevanti
        relevant_chunks = search_relevant_chunks(user_message, top_k=RAG_TOP_K)
        
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
            max_context_length = RAG_MAX_CONTEXT
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
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "system": SYSTEM_PROMPT,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 512,
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
        
    except Exception as e:
        logger.error(f"❌ Errore Ollama: {e}")
        return {
            'response': f"❌ Errore nel sistema AI: {str(e)}",
            'error': True
        }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per il comando /start"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Cliente"
    
    # Inizializza conversazione per l'utente
    user_conversations[user_id] = []
    
    welcome_message = f"""🔧 **Benvenuto in Teklab AI Assistant**, {user_name}!

Sono il tuo assistente tecnico per i sensori industriali Teklab. Posso aiutarti con:

🎯 **Selezione prodotti**
• TK series (TK1+, TK3+, TK4) - Controllori livello olio
• LC series (LC-PS, LC-XP, LC-XT) - Interruttori di livello
• Sensori ATEX antideflagranti

🔧 **Supporto tecnico**
• Specifiche pressione e temperatura
• Compatibilità refrigeranti
• Integrazione MODBUS/4-20mA
• Troubleshooting e installazione

💬 **Come utilizzarmi:**
Scrivi la tua domanda in italiano o inglese.
Esempio: "Serve sensore olio per compressore 40 bar CO2"

⚙️ **Comandi utili:**
/help - Mostra questo messaggio
/clear - Cancella cronologia conversazione
/status - Stato del sistema

Sono qui per fornire consulenza tecnica precisa sui prodotti Teklab! 🚀"""
    
    # Keyboard con opzioni rapide
    keyboard = [
        [InlineKeyboardButton("🔍 Catalogo Prodotti", callback_data="products")],
        [InlineKeyboardButton("📊 Selezione Guidata", callback_data="selection")],
        [InlineKeyboardButton("🛠️ Supporto Tecnico", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per il comando /help"""
    help_text = """🔧 **TEKLAB AI ASSISTANT - GUIDA**

**🎯 Cosa posso fare:**
• Consulenza tecnica sui sensori Teklab
• Selezione prodotto per la tua applicazione
• Specifiche tecniche e compatibilità
• Troubleshooting e installazione
• Confronto tra modelli diversi

**📝 Esempi di domande:**
• "Sensore livello olio per compressore 46 bar R404A"
• "Differenza tra TK3+ e TK4?"
• "Che sensore per serbatoio ammoniaca?"
• "Come configurare MODBUS su TK4?"
• "Specifiche ATEX per sensore antideflagrante"

**⚙️ Comandi:**
/start - Messaggio di benvenuto
/help - Questa guida
/clear - Cancella cronologia
/status - Stato sistema AI

**💡 Suggerimenti:**
• Fornisci dettagli sull'applicazione (pressione, refrigerante, temperatura)
• Specifica se serve integrazione PLC/SCADA
• Chiedi confronti tra prodotti se indeciso

Scrivi la tua domanda e ti fornirò consulenza tecnica precisa! 🚀"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per il comando /clear"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    
    await update.message.reply_text(
        "🔄 **Cronologia cancellata!**\n\nPuoi iniziare una nuova conversazione.",
        parse_mode='Markdown'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per il comando /status"""
    user_id = update.effective_user.id
    conversation_count = len(user_conversations.get(user_id, []))
    
    # Verifica stato Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        ollama_status = "🟢 Attivo" if response.status_code == 200 else "🔴 Errore"
    except Exception:
        ollama_status = "🔴 Non disponibile"
    
    # Verifica RAG system
    rag_status = "🟢 Caricato" if embeddings_cache and chunks_data else "🔴 Non caricato"
    
    status_text = f"""🔧 **STATO SISTEMA TEKLAB AI**

**🤖 Ollama LLM:** {ollama_status}
**📚 RAG System:** {rag_status}
**💬 Tue conversazioni:** {conversation_count}
**📦 Chunks disponibili:** {len(chunks_data) if chunks_data else 0}
**🧠 Embeddings cache:** {len(embeddings_cache) if embeddings_cache else 0}

**📋 Sistema operativo e pronto per consulenza tecnica!**"""
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per i callback dai bottoni inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "products":
        products_text = """🔧 **CATALOGO PRODOTTI TEKLAB**

**🛢️ TK SERIES - Controllori Livello Olio**
• TK1+ - Monitoraggio (solo allarme)
• TK3+ - Controllo automatico + riempimento
• TK4 - Versione avanzata + MODBUS
• Pressioni: 46, 80, 130 bar
• Compatibili: HFC, HCFC, CO2, Ammoniaca

**⚡ LC SERIES - Interruttori di Livello**
• LC-PS - Pressostato sicurezza
• LC-XP - Versione antideflagrante ATEX
• LC-XT - Alta temperatura
• Pressioni fino a 140 bar

**🔥 SENSORI ATEX**
• Certificazione antideflagrante
• Zone 1 e 2 (gas) / Zone 21 e 22 (polveri)
• Integrazione Ex-i (sicurezza intrinseca)

**💡 Scrivi la tua domanda per consulenza personalizzata!**"""
        
        await query.edit_message_text(products_text, parse_mode='Markdown')
    
    elif query.data == "selection":
        selection_text = """🎯 **SELEZIONE GUIDATA PRODOTTO**

**Per scegliere il sensore giusto, dimmi:**

🔧 **Applicazione:**
• Tipo di fluido (olio, refrigerante, acqua...)
• Pressione di lavoro (bar/psi)
• Temperatura di esercizio (°C)
• Refrigerante utilizzato (R404A, CO2, NH3...)

⚙️ **Funzionalità richieste:**
• Solo monitoraggio (allarme)
• Controllo automatico (riempimento)
• Integrazione PLC (MODBUS, 4-20mA)

🏭 **Ambiente:**
• Standard industriale
• Zona ATEX (antideflagrante)
• Applicazione marina/offshore

**Esempio:** "Serve sensore livello olio per compressore rack refrigerazione, 46 bar, R404A, con controllo automatico riempimento e uscita MODBUS"

**Scrivi i dettagli della tua applicazione!**"""
        
        await query.edit_message_text(selection_text, parse_mode='Markdown')
    
    elif query.data == "support":
        support_text = """🛠️ **SUPPORTO TECNICO TEKLAB**

**🔧 Assistenza disponibile per:**

📋 **Specifiche tecniche**
• Dimensioni e attacchi
• Curve caratteristiche
• Certificazioni e omologazioni

⚙️ **Installazione**
• Procedure di montaggio
• Cablaggio elettrico
• Configurazione parametri

🔄 **Integrazione sistemi**
• Setup MODBUS RTU/TCP
• Calibrazione 4-20mA
• Interfaccia PLC/SCADA

🚨 **Troubleshooting**
• Diagnostica problemi
• Codici errore
• Manutenzione preventiva

**📞 Per supporto avanzato:**
• Email: info@teklab.it
• Tel: +39 0376 663588
• Web: www.teklab.it

**Scrivi il tuo problema tecnico specifico!**"""
        
        await query.edit_message_text(support_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per i messaggi di testo"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Inizializza conversazione se non esiste
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    logger.info(f"📩 Messaggio da {user_id}: {user_message[:100]}...")
    
    # Invia indicatore "sta scrivendo"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Genera risposta usando RAG + Ollama
        result = generate_response_with_ollama(user_message)
        response_text = result['response']
        sources = result.get('sources', [])
        has_error = result.get('error', False)
        
        # Salva in cronologia se non errore
        if not has_error:
            user_conversations[user_id].append({
                'user': user_message,
                'bot': response_text,
                'timestamp': datetime.now().isoformat(),
                'sources': sources
            })
            
            # Limita cronologia a ultimi N scambi
            if len(user_conversations[user_id]) > MAX_CONVERSATION_HISTORY:
                user_conversations[user_id] = user_conversations[user_id][-MAX_CONVERSATION_HISTORY:]
        
        # Prepara messaggio di risposta
        if sources and not has_error:
            # Aggiungi info sui prodotti utilizzati
            source_info = "\n\n📚 *Fonti utilizzate:*"
            for source in sources[:2]:  # Max 2 fonti per non intasare
                if source['product']:
                    source_info += f"\n• {source['product']} ({source['similarity']:.2f})"
        else:
            source_info = ""
        
        final_response = response_text + source_info
        
        # Invia risposta (dividi se troppo lunga)
        if len(final_response) > TELEGRAM_MESSAGE_LIMIT:
            # Telegram ha limite caratteri per messaggio
            chunks = [final_response[i:i+TELEGRAM_MESSAGE_LIMIT] for i in range(0, len(final_response), TELEGRAM_MESSAGE_LIMIT)]
            for chunk in chunks:
                await update.message.reply_text(chunk, parse_mode='Markdown')
        else:
            await update.message.reply_text(final_response, parse_mode='Markdown')
        
        logger.info(f"✅ Risposta inviata a {user_id} ({len(response_text)} chars)")
        
    except Exception as e:
        logger.error(f"❌ Errore processing messaggio: {e}", exc_info=True)
        await update.message.reply_text(
            "❌ Si è verificato un errore nel processare la tua richiesta. Riprova tra qualche momento.",
            parse_mode='Markdown'
        )

def main() -> None:
    """Avvia il bot Telegram"""
    print("\n" + "="*70)
    print("🤖 TEKLAB TELEGRAM BOT - Avvio in corso...")
    print("="*70)
    
    # Carica sistema RAG
    print("📚 Caricamento sistema RAG...")
    if load_rag_system():
        print("✅ Sistema RAG caricato con successo")
    else:
        print("❌ Errore caricamento RAG - Bot funzionerà con limitazioni")
    
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
    print("📱 Cerca @TeklabAI_bot su Telegram per iniziare")
    print("⚙️  Premi Ctrl+C per fermare")
    print("="*70)
    
    # Avvia bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()