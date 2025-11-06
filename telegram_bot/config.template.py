# Template di configurazione Bot Telegram Teklab
# Copia questo file in config.py e inserisci le tue credenziali

# Token Bot Telegram (ottenuto da @BotFather)
TELEGRAM_TOKEN = "IL_TUO_TOKEN_QUI"

# URL Backend (modifica se serve)
BACKEND_URL = "http://localhost:5000"

# URL Ollama (modifica se su server diverso)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_EMBEDDINGS_URL = "http://localhost:11434/api/embeddings"

# Modello Ollama
OLLAMA_MODEL = "llama3.2:3b"
EMBEDDINGS_MODEL = "nomic-embed-text:latest"

# Configurazione RAG
RAG_THRESHOLD = 0.28        # Soglia similarità (0.0-1.0)
RAG_TOP_K = 3              # Numero chunks da utilizzare
RAG_MAX_CONTEXT = 4000     # Lunghezza massima contesto

# Configurazione Ollama
OLLAMA_TEMPERATURE = 0.7   # Creatività risposta (0.0-1.0)
OLLAMA_NUM_PREDICT = 512   # Numero token massimo
OLLAMA_TOP_P = 0.9         # Diversità vocabolario
OLLAMA_TIMEOUT = 60        # Timeout secondi

# Configurazione utenti
MAX_CONVERSATION_HISTORY = 10  # Messaggi per utente
TELEGRAM_MESSAGE_LIMIT = 4096  # Limite caratteri Telegram

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Messaggi sistema (personalizzabili)
WELCOME_MESSAGE = """🔧 **Benvenuto in Teklab AI Assistant**!

Sono il tuo assistente tecnico per i sensori industriali Teklab."""

ERROR_MESSAGE = "❌ Si è verificato un errore nel processare la tua richiesta."

SYSTEM_OFFLINE_MESSAGE = "⚠️ Il sistema AI non è al momento disponibile."