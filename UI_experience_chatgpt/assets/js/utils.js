/**
 * UTILITY FUNCTIONS
 * Helper per varie operazioni
 */

const Utils = {
    /**
     * Genera ID univoco
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    },

    /**
     * Formatta data in formato leggibile
     */
    formatDate(date) {
        const d = new Date(date);
        const now = new Date();
        const diffMs = now - d;
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffDays === 0) return 'Today';
        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return 'Previous 7 days';
        if (diffDays < 30) return 'Previous 30 days';
        return d.toLocaleDateString('it-IT', { month: 'long', year: 'numeric' });
    },

    /**
     * Tronca testo
     */
    truncate(text, maxLength = 50) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    },

    /**
     * Escape HTML per prevenire XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * Parse markdown semplice (bold, italic, lists)
     */
    parseMarkdown(text) {
        // Bold
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Code inline
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        
        // Line breaks
        text = text.replace(/\n/g, '<br>');
        
        return text;
    },

    /**
     * Formatta messaggio con paragrafi
     */
    formatMessage(text) {
        // Split in paragrafi
        const paragraphs = text.split('\n\n');
        
        return paragraphs.map(p => {
            // Check se è una lista
            if (p.trim().startsWith('•') || p.trim().startsWith('-') || p.trim().startsWith('*')) {
                const items = p.split('\n').map(item => {
                    const cleaned = item.trim().replace(/^[•\-*]\s*/, '');
                    return `<li>${this.parseMarkdown(cleaned)}</li>`;
                }).join('');
                return `<ul>${items}</ul>`;
            }
            
            // Check se è numerata
            if (/^\d+\./.test(p.trim())) {
                const items = p.split('\n').map(item => {
                    const cleaned = item.trim().replace(/^\d+\.\s*/, '');
                    return `<li>${this.parseMarkdown(cleaned)}</li>`;
                }).join('');
                return `<ol>${items}</ol>`;
            }
            
            // Paragrafo normale
            return `<p>${this.parseMarkdown(p)}</p>`;
        }).join('');
    },

    /**
     * Copy testo negli appunti
     */
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback per browser vecchi
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            const success = document.execCommand('copy');
            document.body.removeChild(textarea);
            return success;
        }
    },

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Smooth scroll to bottom
     */
    scrollToBottom(element, smooth = true) {
        if (smooth) {
            element.scrollTo({
                top: element.scrollHeight,
                behavior: 'smooth'
            });
        } else {
            element.scrollTop = element.scrollHeight;
        }
    },

    /**
     * Save to localStorage
     */
    saveToStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
            return true;
        } catch (err) {
            console.error('Storage error:', err);
            return false;
        }
    },

    /**
     * Load from localStorage
     */
    loadFromStorage(key, defaultValue = null) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : defaultValue;
        } catch (err) {
            console.error('Storage error:', err);
            return defaultValue;
        }
    },

    /**
     * Remove from localStorage
     */
    removeFromStorage(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (err) {
            console.error('Storage error:', err);
            return false;
        }
    },

    /**
     * Clear all storage
     */
    clearStorage() {
        try {
            localStorage.clear();
            return true;
        } catch (err) {
            console.error('Storage error:', err);
            return false;
        }
    },

    /**
     * Detect mobile
     */
    isMobile() {
        return window.innerWidth <= 768;
    },

    /**
     * Get storage size (approssimato)
     */
    getStorageSize() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                total += localStorage[key].length + key.length;
            }
        }
        return (total / 1024).toFixed(2); // KB
    }
};

// Export
window.Utils = Utils;
