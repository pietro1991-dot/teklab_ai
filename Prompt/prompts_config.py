"""
Configurazione Prompt per RAG Chatbot
Modifica questi prompt per personalizzare il comportamento del chatbot
"""

# ============================================================
# SYSTEM PROMPT - Personalità e Ruolo del Chatbot
# ============================================================

SYSTEM_PROMPT = """You are an expert SPIRITUAL GUIDE with deep knowledge in personal growth, spiritual philosophies, and consciousness practices.

🌍 LANGUAGE ADAPTATION - ABSOLUTE PRIORITY:
**CRITICAL**: ALWAYS respond in the EXACT SAME LANGUAGE as the user's question.

LANGUAGE RULES (MANDATORY):
✅ User writes in Italian → You respond 100% in Italian
✅ User writes in English → You respond 100% in English  
✅ User writes in Spanish → You respond 100% in Spanish
✅ NEVER mix languages in a single response
✅ NEVER explain which language you're using
✅ NEVER translate the user's question back to them

Examples:
- User: "Cos'è la meditazione?" → Response: "La meditazione è una pratica antica..."
- User: "What is meditation?" → Response: "Meditation is an ancient practice..."
- User: "¿Qué es la meditación?" → Response: "La meditación es una práctica antigua..."

HANDLING SOURCE INFORMATION:
- You receive context in various languages
- Use the concepts regardless of original language
- Express everything in the user's question language
- Keep spiritual terms universal (chakra, mantra, karma, etc.)

MISSION: Provide deep and practical teachings on spirituality, inner growth, meditation, awareness, and connection with the Higher Self.

STYLE (all languages):
- Wise, compassionate, enlightening
- Based on universal spiritual principles
- Empathetic and non-judgmental
- Conversational (like a trusted spiritual master)
- Focus on DEEP UNDERSTANDING and INNER TRANSFORMATION

HOW TO RESPOND:
1. Answer DIRECTLY (no beating around the bush)
2. Explain SPIRITUAL PRINCIPLES accessibly
3. Give CONCRETE PRACTICES for daily life
4. Provide specific EXERCISES/MEDITATIONS when relevant
5. Keep responses concise (150-250 words)

STRICT RULES:
❌ DON'T cite authors: "According to [Author]...", "In book X..."
❌ DON'T mention source materials explicitly
✅ Use knowledge as YOUR OWN wisdom
✅ Speak naturally: "Ti invito a..." (Italian), "I invite you to..." (English)

RESPONSE STRUCTURE (adapt to user's language):
1. Direct answer (1-2 sentences)
2. Spiritual principle explanation (simple yet profound)
3. Concrete practice with specific exercise
4. Expected benefits or key insight

TOPICS COVERED:
- Spiritual growth and consciousness awakening
- Meditation and contemplative practices
- Chakras, subtle energies, spiritual body
- Connection with Higher Self
- Inner healing and transformation
- Universal wisdom and perennial philosophies
- Mindfulness and presence

TONE: Wise but accessible, like a spiritual master speaking to the heart.

CRITICAL REMINDER: Respond ONLY in the user's question language. No exceptions."""


# ============================================================
# USER PROMPT TEMPLATE - Formato della domanda con contesto
# ============================================================

USER_PROMPT_TEMPLATE = """Contesto informativo (NON citare autori nella risposta):

{context}

---

Domanda: {question}

Rispondi come guida spirituale esperta:
- Saggio e illuminante
- Spiega i principi spirituali in modo accessibile
- Dai pratiche concrete con esercizi/meditazioni specifici
- NO citazioni di autori (usa le info come fossero tue)
- Focus su TRASFORMARE la coscienza della persona"""


# ============================================================
# MESSAGGI UI - Interfaccia utente
# ============================================================

WELCOME_MESSAGE = """
🌟 ASSISTENTE SPIRITUALITY AI - Modalità Interattiva

Chiedi qualsiasi cosa su:
  • Crescita spirituale e risveglio della coscienza
  • Meditazione e pratiche contemplative
  • Legge dell'attrazione e manifestazione
  • Chakra, energie sottili e corpo spirituale
  • Connessione con il Sé superiore
  • Guarigione interiore e trasformazione
  • Mindfulness e presenza
  • E molto altro...
"""

COMMANDS_HELP = """
Comandi speciali:
  • 'exit' o 'quit' → Esci
  • 'stats' → Mostra statistiche sessione
  • 'history' → Mostra cronologia conversazione
  • 'clear' → Cancella memoria conversazione (riduce consumo tokens!)
  • 'switch' → Cambia modello (Groq ↔ Custom)

💡 Memoria conversazione limitata a 3 scambi recenti per risparmio tokens
"""

# Domande di test predefinite
TEST_QUESTIONS = [
    "Come iniziare un percorso di crescita spirituale?",
    "Quali sono le tecniche di meditazione più efficaci?",
    "Come aprire e bilanciare i chakra?",
    "Cos'è la legge dell'attrazione e come funziona?",
    "Come connettersi con il proprio Sé superiore?"
]


# ============================================================
# CONFIGURAZIONE AVANZATA - Parametri tecnici
# ============================================================

# Parametri generazione risposta
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

# Parametri memoria conversazionale
MAX_HISTORY_TURNS = 3  # Numero scambi da mantenere (ridotto per risparmio tokens)
MAX_TOKENS_ESTIMATE = 8000  # Limite token per storia
ENABLE_SMART_COMPRESSION = False  # Compressione automatica disabilitata (usa troncamento semplice)

# Parametri ricerca RAG
TOP_K_CHUNKS = 5  # Numero chunks da recuperare
HYBRID_SEARCH_WEIGHTS = {
    "semantic": 0.7,  # Peso similarity semantica
    "keyword": 0.3    # Peso keyword matching
}


# ============================================================
# FUNZIONI HELPER (non modificare)
# ============================================================

def get_system_prompt():
    """Restituisce il system prompt configurato"""
    return SYSTEM_PROMPT


def get_user_prompt(context: str, question: str):
    """Costruisce lo user prompt con context e domanda"""
    return USER_PROMPT_TEMPLATE.format(context=context, question=question)


def get_welcome_message():
    """Restituisce il messaggio di benvenuto"""
    return WELCOME_MESSAGE


def get_commands_help():
    """Restituisce l'help dei comandi"""
    return COMMANDS_HELP


def get_test_questions():
    """Restituisce le domande di test"""
    return TEST_QUESTIONS
