# ============================================
# CONFIGURAZIONE CHATBOT SPIRITUALITY AI
# ============================================

# Modello da utilizzare
MODEL_NAME = "Llama-3.2-3B-Instruct"  # Opzioni: "Llama-3.2-3B-Instruct", "TinyLlama-1.1B-Chat"
MODEL_PATH = "ai_system/models/Llama-3.2-3B-Instruct"

# Parametri generazione (BILANCIATO: qualità + velocità)
MAX_NEW_TOKENS = 350  # 350 token per risposte complete senza troncamento
TEMPERATURE = 0.7  # Creatività (0.1 = preciso, 1.0 = creativo)
TOP_P = 0.9  # Nucleus sampling
TOP_K = 50  # Top-K sampling (limita scelte per velocità)
REPETITION_PENALTY = 1.1  # Evita ripetizioni (1.0 = nessuna penalità)
USE_CACHE = True  # KV-cache per velocizzare generazione
NUM_BEAMS = 1  # Greedy decoding (beam=1 più veloce)

# Parametri RAG (RIDOTTI per velocità)
RAG_TOP_K = 2  # RIDOTTO: 2 chunk invece di 3 = meno context = più veloce
RAG_MIN_SIMILARITY = 0.4  # ALZATO: solo chunk molto rilevanti

# Performance
USE_GPU = True  # True per GPU, False per CPU
MAX_GPU_MEMORY = "3.5GB"  # Memoria GPU massima da usare
TORCH_DTYPE = "float16"  # float16 per GPU, float32 per CPU

# Chatbot
SAVE_CONVERSATIONS = True  # Salva conversazioni per training
SESSION_TIMEOUT_MINUTES = 30  # Timeout sessione

# Debug
VERBOSE = False  # Stampa dettagli tecnici
SHOW_RAG_CONTEXT = True  # Mostra chunk RAG recuperati