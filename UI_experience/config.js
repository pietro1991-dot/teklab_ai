/**
 * Configurazione API Spirituality AI
 * 
 * LOCALE (sviluppo):
 *   API_URL = 'http://localhost:5000'
 * 
 * ONLINE (produzione):
 *   API_URL = 'https://tuo-dominio.com/api'
 */

const CONFIG = {
    // Backend API endpoint
    API_URL: 'http://localhost:5000',
    
    // Timeout richieste (ms)
    REQUEST_TIMEOUT: 120000, // 2 minuti
    
    // Numero massimo messaggi in history
    MAX_HISTORY: 50,
    
    // Auto-save conversazioni in localStorage
    AUTO_SAVE: true,
    
    // Animazioni typing
    TYPING_SPEED: 30, // ms per carattere
    
    // Theme default
    DEFAULT_THEME: 'light', // 'light' o 'dark'
    
    // Debug mode
    DEBUG: true
};

// Export per uso in altri file
window.CONFIG = CONFIG;
