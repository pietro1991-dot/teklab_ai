/**
 * Configurazione API Teklab B2B AI
 * 
 * TAILSCALE DEPLOYMENT:
 *   - Backend API: http://100.111.187.7:5000 (Tailscale VPN)
 *   - Frontend UI: http://100.111.187.7:8081 (Python HTTP server)
 *   - LOCALE (sviluppo): http://localhost:5000
 */

const CONFIG = {
    // Backend API endpoint - ChatGPT Version
    // LOCALE: http://localhost:5000
    // TAILSCALE: Sostituisci con il tuo IP Tailscale (es: http://100.111.187.7:5000)
    API_URL: 'http://100.111.187.7:5000',  // ← Cambia con il TUO IP Tailscale
    
    // Bot name
    BOT_NAME: 'Teklab Assistant',
    
    // Bot description
    BOT_DESCRIPTION: 'Technical Sales Assistant for Industrial Sensors',
    
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
