"""
Bot Telegram per Teklab AI Chatbot
COPIA ESATTA della UI Experience - utilizza lo stesso backend Flask con streaming SSE
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import requests
import json
import logging

# Import Telegram Bot API
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent

# Import configurazione
try:
    from config import *
    logging.basicConfig(
        format=LOG_FORMAT,
        level=getattr(logging, LOG_LEVEL)
    )
    logger = logging.getLogger(__name__)
except ImportError:
    # Fallback configuration
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    TELEGRAM_TOKEN = "8209626692:AAFJ6g5oFEDSS5U5aN_5UOLMetFzLPCUUnE"
    BACKEND_URL = "http://localhost:5000"
    MAX_CONVERSATION_HISTORY = 10
    TELEGRAM_MESSAGE_LIMIT = 4096
    WELCOME_MESSAGE = "🔧 Benvenuto in Teklab AI Assistant!"
    ERROR_MESSAGE = "❌ Si è verificato un errore."
    SYSTEM_OFFLINE_MESSAGE = "⚠️ Sistema AI non disponibile."

# Storage per conversazioni degli utenti (come UI)
user_conversations: Dict[int, List[Dict]] = {}

def check_backend_health() -> bool:
    """Verifica se il backend Flask è online (come UI)"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def send_message_stream(user_message: str) -> Dict:
    """
    Invia messaggio al backend usando streaming SSE
    ESATTAMENTE come fa la UI in api.js
    """
    try:
        # POST a /chat/stream come fa la UI
        response = requests.post(
            f"{BACKEND_URL}/chat/stream",
            json={'message': user_message.strip(), 'reset_history': False},
            headers={'Content-Type': 'application/json'},
            stream=True,  # IMPORTANTE: streaming attivo
            timeout=180
        )
        
        if not response.ok:
            error_data = response.json() if response.content else {}
            raise Exception(error_data.get('error', f'HTTP {response.status_code}'))
        
        # Leggi stream SSE (Server-Sent Events)
        full_response = ""
        sources = []
        queue_position = None
        
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith('data: '):
                try:
                    json_str = line[6:]  # Rimuovi "data: "
                    data = json.loads(json_str)
                    
                    # Gestisci eventi SSE come fa la UI
                    event_type = data.get('type')
                    
                    if event_type == 'queue':
                        # Utente in coda
                        queue_position = data.get('position')
                        logger.info(f"🔄 In coda: posizione {queue_position}")
                    
                    elif event_type == 'sources':
                        # Fonti RAG utilizzate
                        sources = data.get('sources', [])
                        logger.info(f"📚 Fonti: {len(sources)} chunks")
                    
                    elif event_type == 'token':
                        # Token di risposta (streaming)
                        token = data.get('token', '')
                        full_response += token
                    
                    elif event_type == 'done':
                        # Completato
                        logger.info("✅ Risposta completata")
                        return {
                            'response': full_response,
                            'sources': sources,
                            'timestamp': data.get('timestamp'),
                            'error': False
                        }
                    
                    elif event_type == 'error':
                        # Errore dal backend
                        error_msg = data.get('error', 'Errore sconosciuto')
                        return {
                            'response': f"❌ {error_msg}",
                            'error': True
                        }
                
                except json.JSONDecodeError as e:
                    logger.error(f"Errore parsing SSE: {e}")
                    continue
        
        # Se arriviamo qui, lo stream è terminato
        if full_response:
            return {
                'response': full_response,
                'sources': sources,
                'error': False
            }
        else:
            return {
                'response': ERROR_MESSAGE,
                'error': True
            }
        
    except requests.exceptions.Timeout:
        logger.error("Timeout richiesta al backend")
        return {
            'response': "⏱️ La richiesta ha impiegato troppo tempo. Riprova.",
            'error': True
        }
    except Exception as e:
        logger.error(f"Errore comunicazione backend: {e}")
        
        if 'Failed to fetch' in str(e) or 'Connection' in str(e):
            return {
                'response': SYSTEM_OFFLINE_MESSAGE + f"\n\nAssicurati che il backend sia avviato su {BACKEND_URL}",
                'error': True
            }
        
        return {
            'response': f"{ERROR_MESSAGE}\n\nDettagli: {str(e)}",
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

**Esempi:**
• "Che differenza c'è tra TK3+ e TK4?"
• "Quale sensore per R410A?"
• "Come si configura il MODBUS su TK4?"
• "Specifiche ATEX per ammoniaca"

⚙️ **Comandi utili:**
/help - Mostra questa guida
/clear - Cancella cronologia conversazione
/status - Stato del sistema

Sono qui per fornire consulenza tecnica precisa sui prodotti Teklab! 🚀"""
    
    # Keyboard con opzioni rapide (come UI)
    keyboard = [
        [InlineKeyboardButton("TK3+ vs TK4 comparison", callback_data="prompt_tk3_vs_tk4")],
        [InlineKeyboardButton("R410A sensor selection", callback_data="prompt_r410a")],
        [InlineKeyboardButton("ATEX for ammonia", callback_data="prompt_atex_ammonia")],
        [InlineKeyboardButton("MODBUS setup", callback_data="prompt_modbus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
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
    
    await update.message.reply_text(help_text)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per il comando /clear"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    
    await update.message.reply_text(
        "🔄 Cronologia cancellata!\n\nPuoi iniziare una nuova conversazione."
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per il comando /status"""
    user_id = update.effective_user.id
    conversation_count = len(user_conversations.get(user_id, []))
    
    # Verifica stato backend (come fa la UI)
    backend_online = check_backend_health()
    backend_status = "🟢 Attivo" if backend_online else "🔴 Offline"
    
    status_text = f"""🔧 STATO SISTEMA TEKLAB AI

🌐 Backend Flask: {backend_status}
💬 Tue conversazioni: {conversation_count}
📍 Backend URL: {BACKEND_URL}

{"📋 Sistema operativo e pronto per consulenza tecnica!" if backend_online else "⚠️ Backend non raggiungibile. Avvia il server Flask."}"""
    
    await update.message.reply_text(status_text)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per i callback dai bottoni inline (suggestion cards come UI)"""
    query = update.callback_query
    await query.answer()
    
    # Mappa prompt predefiniti (come suggestion cards della UI)
    prompts = {
        'prompt_tk3_vs_tk4': "What's the difference between TK3+ and TK4?",
        'prompt_r410a': "Which sensor for R410A refrigerant?",
        'prompt_atex_ammonia': "What are ATEX requirements for ammonia?",
        'prompt_modbus': "How does MODBUS communication work?"
    }
    
    prompt = prompts.get(query.data, "")
    
    if prompt:
        # Simula invio messaggio
        await query.edit_message_text(f"📝 {prompt}")
        
        # Invia indicatore "sta scrivendo"
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Invia al backend
        result = send_message_stream(prompt)
        response_text = result['response']
        sources = result.get('sources', [])
        
        # Prepara messaggio con fonti (se presenti)
        if sources and not result.get('error', False):
            source_info = "\n\n📚 *Fonti utilizzate:*"
            for source in sources[:2]:
                if source.get('product'):
                    source_info += f"\n• {source['product']} (sim: {source.get('similarity', 0):.2f})"
        else:
            source_info = ""
        
        final_response = response_text + source_info
        
        # Invia risposta
        if len(final_response) > TELEGRAM_MESSAGE_LIMIT:
            chunks = [final_response[i:i+TELEGRAM_MESSAGE_LIMIT] for i in range(0, len(final_response), TELEGRAM_MESSAGE_LIMIT)]
            for chunk in chunks:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=chunk
                )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=final_response
            )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler per i messaggi di testo (come UI)"""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Inizializza conversazione se non esiste
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    
    logger.info(f"📩 Messaggio da {user_id}: {user_message[:100]}...")
    
    # Invia indicatore "sta scrivendo"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Genera risposta usando backend Flask (ESATTAMENTE come UI)
        result = send_message_stream(user_message)
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
        
        # Prepara messaggio di risposta con fonti
        if sources and not has_error:
            source_info = "\n\n📚 *Fonti utilizzate:*"
            for source in sources[:2]:  # Max 2 fonti
                if source.get('product'):
                    source_info += f"\n• {source['product']} (sim: {source.get('similarity', 0):.2f})"
        else:
            source_info = ""
        
        final_response = response_text + source_info
        
        # Invia risposta (dividi se troppo lunga)
        # NOTA: Rimuovo parse_mode='Markdown' perché Telegram è rigido e il backend genera testo che potrebbe avere Markdown malformato
        if len(final_response) > TELEGRAM_MESSAGE_LIMIT:
            chunks = [final_response[i:i+TELEGRAM_MESSAGE_LIMIT] for i in range(0, len(final_response), TELEGRAM_MESSAGE_LIMIT)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(final_response)
        
        logger.info(f"✅ Risposta inviata a {user_id} ({len(response_text)} chars)")
        
    except Exception as e:
        logger.error(f"❌ Errore processing messaggio: {e}", exc_info=True)
        await update.message.reply_text(
            ERROR_MESSAGE
        )

def main() -> None:
    """Avvia il bot Telegram"""
    print("\n" + "="*70)
    print("🤖 TEKLAB TELEGRAM BOT - Avvio in corso...")
    print("="*70)
    
    # Verifica backend Flask (come fa la UI)
    print("🔍 Verifica connessione backend Flask...")
    if check_backend_health():
        print(f"✅ Backend attivo su {BACKEND_URL}")
    else:
        print(f"❌ Backend NON raggiungibile su {BACKEND_URL}")
        print("⚠️  Il bot funzionerà ma non potrà rispondere alle domande.")
        print(f"   Avvia il backend Flask: cd backend_api && python app.py")
    
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
    print("📱 Cerca il tuo bot su Telegram per iniziare")
    print("⚙️  Premi Ctrl+C per fermare")
    print("="*70)
    
    # Avvia bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
