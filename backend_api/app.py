"""
Backend API Flask per Spirituality AI Chatbot
Funziona in LOCALE per sviluppo, pronto per deploy online
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "ai_system" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "Prompt"))

try:
    from models.llama_rag_wrapper import LlamaRAGWrapper
    from config.model_config import get_config
    from prompts_config import SYSTEM_PROMPT
except ImportError as e:
    logger.error(f"❌ Errore import: {e}")
    logger.error("Assicurati di:")
    logger.error("  1. Aver installato le dipendenze: pip install -r BOT/requirements.txt")
    logger.error("  2. Aver scaricato il modello: python scripts/1_download_llama.py")
    sys.exit(1)

# Inizializza Flask
app = Flask(__name__)
CORS(app)  # Permetti richieste da file HTML locali e da domini esterni

# Cache modello (lazy loading)
_model_cache = None
_conversation_history = []


def get_model():
    """Carica modello solo al primo utilizzo"""
    global _model_cache
    if _model_cache is None:
        logger.info("🦙 Caricamento Llama RAG...")
        try:
            config = get_config("llama-qlora")
            _model_cache = LlamaRAGWrapper(
                model_name_or_path=None,  # Auto-detect
                config=config,
                auto_find_checkpoint=True
            )
            logger.info("✅ Llama pronto!")
        except Exception as e:
            logger.error(f"❌ Errore caricamento modello: {e}")
            raise
    return _model_cache


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'spirituality-ai',
        'model': 'llama-2-7b-chat-hf',
        'model_loaded': _model_cache is not None,
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
        
        # Genera risposta
        model = get_model()
        
        # Usa il metodo chat con RAG
        response = model.chat(
            user_input=user_message,
            system_prompt=SYSTEM_PROMPT,
            top_k=5  # Numero chunk RAG
        )
        
        # Salva in history
        _conversation_history.append({
            'user': user_message,
            'bot': response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Limita history a ultimi 10 scambi
        if len(_conversation_history) > 10:
            _conversation_history = _conversation_history[-10:]
        
        logger.info(f"✅ Risposta generata ({len(response)} chars)")
        
        return jsonify({
            'response': response,
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
        'model_loaded': _model_cache is not None,
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
    print("🌟 SPIRITUALITY AI - Backend API")
    print("="*70)
    print("\n📡 Server in avvio su http://localhost:5000")
    print("💡 Apri UI_experience/index.html nel browser")
    print("\n✨ Endpoints disponibili:")
    print("   - POST   /chat      → Invia messaggio")
    print("   - GET    /health    → Health check")
    print("   - GET    /history   → Cronologia chat")
    print("   - POST   /clear     → Cancella storia")
    print("   - GET    /stats     → Statistiche")
    print("\n" + "="*70 + "\n")
    
    # Avvia server
    app.run(
        host='0.0.0.0',  # Accessibile da qualsiasi interfaccia
        port=5000,
        debug=True  # Debug mode per sviluppo locale
    )
