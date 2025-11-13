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
     * Invia messaggio con streaming SSE (Server-Sent Events)
     * Callbacks: onQueue(position), onToken(token), onSources(sources), onDone(), onError(error)
     */
    async sendMessageStream(message, callbacks, resetHistory = false) {
        try {
            if (!message || !message.trim()) {
                throw new Error('Messaggio vuoto');
            }

            const { onQueue, onToken, onSources, onDone, onError, onTranslation } = callbacks;

            console.log('🔵 Starting SSE stream request...');

            // Invia richiesta POST per iniziare streaming
            const response = await fetch(`${this.baseURL}/chat/stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',  // Include cookies per session
                body: JSON.stringify({
                    message: message.trim(),
                    reset_history: resetHistory
                })
            });

            console.log('📡 Response received, status:', response.status);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            // Crea reader per streaming
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            console.log('📖 Starting to read stream...');

            // Leggi stream progressivamente
            while (true) {
                const { done, value } = await reader.read();
                
                if (done) {
                    console.log('✅ Stream completed');
                    break;
                }

                // Decodifica chunk
                buffer += decoder.decode(value, { stream: true });
                console.log('📦 Received chunk, buffer length:', buffer.length);

                // Processa righe complete (SSE format: "data: {...}\n\n")
                const lines = buffer.split('\n\n');
                buffer = lines.pop() || ''; // Mantieni ultima riga incompleta

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const jsonStr = line.substring(6); // Rimuovi "data: "
                            const data = JSON.parse(jsonStr);

                            // Gestisci tipo evento
                            switch (data.type) {
                                case 'init':
                                    // 🎬 Connessione SSE stabilita
                                    console.log('🎬 SSE connection established, request_id:', data.request_id);
                                    break;
                                
                                case 'heartbeat':
                                    // 💓 Heartbeat per mantenere connessione viva
                                    console.log('💓 Heartbeat:', data.message);
                                    break;
                                    
                                case 'queue':
                                    // 🔵 NUOVO: Queue position update
                                    if (onQueue) onQueue(data.position, data.message);
                                    break;

                                case 'sources':
                                    if (onSources) onSources(data.sources);
                                    break;

                                case 'translation_start':
                                    // 🌍 NUOVO: Segnala inizio risposta tradotta
                                    console.log('🌍 Translation completed, starting stream', {
                                        language: data.language,
                                        translation_time: data.translation_time
                                    });
                                    break;

                                case 'token':
                                    // ⚡ Ora i token sono SEMPRE nella lingua corretta (tradotti)
                                    if (onToken) onToken(data.token);
                                    break;

                                case 'translated_response':
                                    // 🌍 DEPRECATO: Non più usato (ora streammiamo token tradotti)
                                    // Mantenuto per retrocompatibilità se necessario
                                    console.log('⚠️ Received deprecated translated_response event');
                                    break;

                                case 'done':
                                    // Passa doneData con metriche adaptive generation
                                    if (onDone) onDone(data);
                                    return { success: true, timestamp: data.timestamp };

                                case 'error':
                                    if (onError) onError(data.error);
                                    return { success: false, error: data.error };
                            }
                        } catch (e) {
                            console.error('Errore parsing SSE:', e, line);
                        }
                    }
                }
            }

            return { success: true };

        } catch (error) {
            console.error('Send message stream failed:', error);

            if (error.message.includes('Failed to fetch')) {
                return {
                    success: false,
                    error: 'Backend non raggiungibile. Assicurati che sia avviato su http://localhost:5000'
                };
            }

            return {
                success: false,
                error: error.message || 'Errore streaming'
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
