/**
 * SPIRITUALITY AI - Main Application
 * ChatGPT-like interface
 */

class SpiritualityAI {
    constructor() {
        // State
        this.currentConversation = null;
        this.conversations = [];
        this.isTyping = false;
        this.theme = 'light';

        // DOM Elements
        this.elements = {
            sidebar: document.getElementById('sidebar'),
            messagesContainer: document.getElementById('messagesContainer'),
            welcomeScreen: document.getElementById('welcomeScreen'),
            messageInput: document.getElementById('messageInput'),
            messageForm: document.getElementById('messageForm'),
            sendBtn: document.getElementById('sendBtn'),
            newChatBtn: document.getElementById('newChatBtn'),
            newChatBtnMobile: document.getElementById('newChatBtnMobile'),
            menuToggle: document.getElementById('menuToggle'),
            themeToggle: document.getElementById('themeToggle'),
            themeLabel: document.getElementById('themeLabel'),
            conversationsList: document.getElementById('conversationsList'),
            loadingOverlay: document.getElementById('loadingOverlay'),
            toastContainer: document.getElementById('toastContainer')
        };

        this.init();
    }

    /**
     * Inizializzazione
     */
    async init() {
        console.log('🌟 Spirituality AI initializing...');

        // Load saved data
        this.loadSavedData();

        // Setup event listeners
        this.setupEventListeners();

        // Check backend connection
        await this.checkBackend();

        // Auto-resize textarea
        this.setupAutoResize();

        console.log('✅ Spirituality AI ready!');
    }

    /**
     * Load dati salvati (conversazioni, theme)
     */
    loadSavedData() {
        // Load theme
        this.theme = Utils.loadFromStorage('theme', CONFIG.DEFAULT_THEME);
        this.applyTheme(this.theme);

        // Load conversations
        this.conversations = Utils.loadFromStorage('conversations', []);
        this.renderConversations();

        // Load current conversation
        const currentId = Utils.loadFromStorage('currentConversation');
        if (currentId) {
            this.currentConversation = this.conversations.find(c => c.id === currentId);
            if (this.currentConversation) {
                this.renderMessages();
            }
        }
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Form submit
        this.elements.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Input change
        this.elements.messageInput.addEventListener('input', () => {
            const hasText = this.elements.messageInput.value.trim().length > 0;
            this.elements.sendBtn.disabled = !hasText;
        });

        // Enter to send (Shift+Enter per newline)
        this.elements.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!this.elements.sendBtn.disabled) {
                    this.sendMessage();
                }
            }
        });

        // New chat
        this.elements.newChatBtn.addEventListener('click', () => this.startNewChat());
        this.elements.newChatBtnMobile.addEventListener('click', () => {
            this.startNewChat();
            this.closeSidebar();
        });

        // Mobile menu toggle
        this.elements.menuToggle.addEventListener('click', () => this.toggleSidebar());

        // Theme toggle
        this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());

        // Suggestion cards
        document.querySelectorAll('.suggestion-card').forEach(card => {
            card.addEventListener('click', () => {
                const prompt = card.dataset.prompt;
                this.elements.messageInput.value = prompt;
                this.elements.sendBtn.disabled = false;
                this.elements.messageInput.focus();
            });
        });

        // Close sidebar on backdrop click (mobile)
        document.addEventListener('click', (e) => {
            if (Utils.isMobile() && 
                this.elements.sidebar.classList.contains('active') && 
                !this.elements.sidebar.contains(e.target) &&
                !this.elements.menuToggle.contains(e.target)) {
                this.closeSidebar();
            }
        });
    }

    /**
     * Auto-resize textarea
     */
    setupAutoResize() {
        const textarea = this.elements.messageInput;
        textarea.addEventListener('input', () => {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
        });
    }

    /**
     * Check backend connection
     */
    async checkBackend() {
        this.showLoading('Connecting to backend...');

        const result = await API.checkHealth();

        this.hideLoading();

        if (result.success) {
            console.log('✅ Backend connected:', result.data);
            this.showToast('Backend connected successfully', 'success');
        } else {
            console.error('❌ Backend connection failed:', result.error);
            this.showToast(
                'Backend offline. Start it with: python backend_api/app.py',
                'error',
                10000
            );
        }
    }

    /**
     * Invia messaggio
     */
    async sendMessage() {
        const text = this.elements.messageInput.value.trim();
        if (!text || this.isTyping) return;

        // Crea conversazione se non esiste
        if (!this.currentConversation) {
            this.currentConversation = {
                id: Utils.generateId(),
                title: Utils.truncate(text, 30),
                messages: [],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };
            this.conversations.unshift(this.currentConversation);
        }

        // Hide welcome screen
        this.elements.welcomeScreen.style.display = 'none';

        // Add user message
        const userMessage = {
            role: 'user',
            content: text,
            timestamp: new Date().toISOString()
        };

        this.currentConversation.messages.push(userMessage);
        this.renderMessage(userMessage);

        // Clear input
        this.elements.messageInput.value = '';
        this.elements.messageInput.style.height = 'auto';
        this.elements.sendBtn.disabled = true;

        // Scroll to bottom
        this.scrollToBottom();

        // Show typing indicator
        this.showTypingIndicator();
        this.isTyping = true;

        // Send to backend
        const result = await API.sendMessage(text);

        // Hide typing indicator
        this.hideTypingIndicator();
        this.isTyping = false;

        if (result.success) {
            // Add bot response
            const botMessage = {
                role: 'assistant',
                content: result.response,
                timestamp: result.timestamp
            };

            this.currentConversation.messages.push(botMessage);
            this.renderMessage(botMessage);

            // Update conversation
            this.currentConversation.updatedAt = new Date().toISOString();
            this.saveConversations();
            this.renderConversations();

        } else {
            // Show error
            this.showToast(`Error: ${result.error}`, 'error', 5000);
        }

        // Scroll to bottom
        this.scrollToBottom();
    }

    /**
     * Render messaggio
     */
    renderMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';

        const isBot = message.role === 'assistant';

        messageDiv.innerHTML = `
            <div class="message-avatar ${isBot ? 'bot' : 'user'}">
                ${isBot ? '🌟' : '👤'}
            </div>
            <div class="message-content">
                <div class="message-role">${isBot ? 'Spirituality AI' : 'You'}</div>
                <div class="message-text">
                    ${Utils.formatMessage(message.content)}
                </div>
                ${isBot ? `
                    <div class="message-actions">
                        <button class="btn-message-action btn-copy" data-text="${Utils.escapeHtml(message.content)}">
                            📋 Copy
                        </button>
                    </div>
                ` : ''}
            </div>
        `;

        this.elements.messagesContainer.appendChild(messageDiv);

        // Copy button handler
        if (isBot) {
            const copyBtn = messageDiv.querySelector('.btn-copy');
            copyBtn.addEventListener('click', async () => {
                const text = copyBtn.dataset.text;
                const success = await Utils.copyToClipboard(text);
                if (success) {
                    copyBtn.textContent = '✅ Copied!';
                    setTimeout(() => {
                        copyBtn.textContent = '📋 Copy';
                    }, 2000);
                }
            });
        }
    }

    /**
     * Render tutti i messaggi
     */
    renderMessages() {
        this.elements.messagesContainer.innerHTML = '';

        if (!this.currentConversation || this.currentConversation.messages.length === 0) {
            // Show welcome screen
            const welcomeScreen = document.createElement('div');
            welcomeScreen.className = 'welcome-screen';
            welcomeScreen.id = 'welcomeScreen';
            welcomeScreen.innerHTML = `
                <div class="welcome-content">
                    <div class="logo-large">
                        <span class="logo-emoji-large">🌟</span>
                        <h2>Spirituality AI</h2>
                    </div>
                    <p class="welcome-subtitle">La tua guida spirituale personale</p>
                    
                    <div class="suggestions">
                        <button class="suggestion-card" data-prompt="Come posso iniziare a meditare?">
                            <div class="suggestion-icon">🧘</div>
                            <div class="suggestion-text">Come posso iniziare a meditare?</div>
                        </button>
                        
                        <button class="suggestion-card" data-prompt="Spiegami cosa sono i chakra">
                            <div class="suggestion-icon">⚡</div>
                            <div class="suggestion-text">Spiegami cosa sono i chakra</div>
                        </button>
                        
                        <button class="suggestion-card" data-prompt="Cos'è il terzo occhio?">
                            <div class="suggestion-icon">👁️</div>
                            <div class="suggestion-text">Cos'è il terzo occhio?</div>
                        </button>
                        
                        <button class="suggestion-card" data-prompt="Come risvegliare la kundalini?">
                            <div class="suggestion-icon">🐍</div>
                            <div class="suggestion-text">Come risvegliare la kundalini?</div>
                        </button>
                    </div>
                </div>
            `;
            this.elements.messagesContainer.appendChild(welcomeScreen);

            // Re-attach suggestion handlers
            welcomeScreen.querySelectorAll('.suggestion-card').forEach(card => {
                card.addEventListener('click', () => {
                    const prompt = card.dataset.prompt;
                    this.elements.messageInput.value = prompt;
                    this.elements.sendBtn.disabled = false;
                    this.elements.messageInput.focus();
                });
            });

            return;
        }

        // Render messages
        this.currentConversation.messages.forEach(msg => this.renderMessage(msg));
        this.scrollToBottom(false);
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'message';
        indicator.id = 'typingIndicator';
        indicator.innerHTML = `
            <div class="message-avatar bot">🌟</div>
            <div class="message-content">
                <div class="message-role">Spirituality AI</div>
                <div class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        `;
        this.elements.messagesContainer.appendChild(indicator);
        this.scrollToBottom();
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    }

    /**
     * Scroll to bottom
     */
    scrollToBottom(smooth = true) {
        Utils.scrollToBottom(this.elements.messagesContainer.parentElement, smooth);
    }

    /**
     * Start new chat
     */
    startNewChat() {
        this.currentConversation = null;
        Utils.removeFromStorage('currentConversation');
        this.renderMessages();
        this.elements.messageInput.focus();
    }

    /**
     * Load conversation
     */
    loadConversation(conversationId) {
        this.currentConversation = this.conversations.find(c => c.id === conversationId);
        if (this.currentConversation) {
            Utils.saveToStorage('currentConversation', conversationId);
            this.renderMessages();
            this.renderConversations(); // Update active state
        }
    }

    /**
     * Delete conversation
     */
    deleteConversation(conversationId) {
        this.conversations = this.conversations.filter(c => c.id !== conversationId);
        
        if (this.currentConversation && this.currentConversation.id === conversationId) {
            this.startNewChat();
        }
        
        this.saveConversations();
        this.renderConversations();
    }

    /**
     * Render conversations list
     */
    renderConversations() {
        this.elements.conversationsList.innerHTML = '';

        if (this.conversations.length === 0) {
            this.elements.conversationsList.innerHTML = '<p style="padding: 1rem; color: var(--text-tertiary); font-size: 14px;">No conversations yet</p>';
            return;
        }

        // Group by date
        const groups = {
            today: [],
            yesterday: [],
            week: [],
            month: [],
            older: []
        };

        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        const weekAgo = new Date(today);
        weekAgo.setDate(weekAgo.getDate() - 7);
        const monthAgo = new Date(today);
        monthAgo.setDate(monthAgo.getDate() - 30);

        this.conversations.forEach(conv => {
            const convDate = new Date(conv.createdAt);
            if (convDate >= today) groups.today.push(conv);
            else if (convDate >= yesterday) groups.yesterday.push(conv);
            else if (convDate >= weekAgo) groups.week.push(conv);
            else if (convDate >= monthAgo) groups.month.push(conv);
            else groups.older.push(conv);
        });

        // Render groups
        const groupTitles = {
            today: 'Today',
            yesterday: 'Yesterday',
            week: 'Previous 7 days',
            month: 'Previous 30 days',
            older: 'Older'
        };

        for (const [key, convs] of Object.entries(groups)) {
            if (convs.length === 0) continue;

            const groupDiv = document.createElement('div');
            groupDiv.className = 'conversation-group-section';

            groupDiv.innerHTML = `
                <div class="conversation-group-title">${groupTitles[key]}</div>
            `;

            convs.forEach(conv => {
                const isActive = this.currentConversation && this.currentConversation.id === conv.id;
                const convItem = document.createElement('div');
                convItem.className = `conversation-item ${isActive ? 'active' : ''}`;
                convItem.innerHTML = `
                    <span class="conversation-icon">💬</span>
                    <span class="conversation-title">${Utils.escapeHtml(conv.title)}</span>
                `;

                convItem.addEventListener('click', () => {
                    this.loadConversation(conv.id);
                    if (Utils.isMobile()) {
                        this.closeSidebar();
                    }
                });

                groupDiv.appendChild(convItem);
            });

            this.elements.conversationsList.appendChild(groupDiv);
        }
    }

    /**
     * Save conversations
     */
    saveConversations() {
        Utils.saveToStorage('conversations', this.conversations);
    }

    /**
     * Toggle sidebar (mobile)
     */
    toggleSidebar() {
        this.elements.sidebar.classList.toggle('active');
    }

    /**
     * Close sidebar
     */
    closeSidebar() {
        this.elements.sidebar.classList.remove('active');
    }

    /**
     * Toggle theme
     */
    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.theme);
        Utils.saveToStorage('theme', this.theme);
    }

    /**
     * Apply theme
     */
    applyTheme(theme) {
        document.body.className = `${theme}-theme`;
        this.elements.themeLabel.textContent = theme === 'light' ? 'Light mode' : 'Dark mode';
    }

    /**
     * Show loading overlay
     */
    showLoading(message = 'Loading...') {
        this.elements.loadingOverlay.querySelector('p').textContent = message;
        this.elements.loadingOverlay.classList.add('active');
    }

    /**
     * Hide loading overlay
     */
    hideLoading() {
        this.elements.loadingOverlay.classList.remove('active');
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        this.elements.toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// Initialize app when DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new SpiritualityAI();
});
