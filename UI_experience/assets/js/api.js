/**
 * API COMMUNICATION
 * Gestisce tutte le chiamate al backend
 */

const API = {
    baseURL: CONFIG.API_URL,
    timeout: CONFIG.REQUEST_TIMEOUT,

    /**
     * Check se backend è online
     */
    async checkHealth() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);

            const response = await fetch(`${this.baseURL}/health`, {
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            return {
                success: true,
                data: data
            };

        } catch (error) {
            console.error('Health check failed:', error);
            return {
                success: false,
                error: error.message
            };
        }
    },

    /**
     * Invia messaggio al chatbot
     */
    async sendMessage(message, resetHistory = false) {
        try {
            if (!message || !message.trim()) {
                throw new Error('Messaggio vuoto');
            }

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);

            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message.trim(),
                    reset_history: resetHistory
                }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            const data = await response.json();

            return {
                success: true,
                response: data.response,
                timestamp: data.timestamp
            };

        } catch (error) {
            console.error('Send message failed:', error);

            // Gestione errori specifici
            if (error.name === 'AbortError') {
                return {
                    success: false,
                    error: 'Timeout: il server impiega troppo tempo a rispondere'
                };
            }

            if (error.message.includes('Failed to fetch')) {
                return {
                    success: false,
                    error: 'Backend non raggiungibile. Assicurati che sia avviato su http://localhost:5000'
                };
            }

            return {
                success: false,
                error: error.message || 'Errore sconosciuto'
            };
        }
    },

    /**
     * Get cronologia conversazione
     */
    async getHistory() {
        try {
            const response = await fetch(`${this.baseURL}/history`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            return {
                success: true,
                history: data.history,
                count: data.count
            };

        } catch (error) {
            console.error('Get history failed:', error);
            return {
                success: false,
                error: error.message
            };
        }
    },

    /**
     * Cancella cronologia
     */
    async clearHistory() {
        try {
            const response = await fetch(`${this.baseURL}/clear`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return {
                success: true
            };

        } catch (error) {
            console.error('Clear history failed:', error);
            return {
                success: false,
                error: error.message
            };
        }
    },

    /**
     * Get statistiche
     */
    async getStats() {
        try {
            const response = await fetch(`${this.baseURL}/stats`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            return {
                success: true,
                stats: data
            };

        } catch (error) {
            console.error('Get stats failed:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
};

// Export
window.API = API;
