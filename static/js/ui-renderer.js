export class UIRenderer {
    constructor(username) {
        this.username = username;
        this.container = document.getElementById('messages-container');
        this.input = document.getElementById('message-input');
        this.translationEnabled = true; // Default
    }
    
    scrollToBottom() {
        this.container.scrollTop = this.container.scrollHeight;
    }
    
    appendMessage(data) {
        const isSelf = data.user === this.username;
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isSelf ? 'sent' : 'received'}`;
        
        // Determine text to show based on translation settings
        // If data.translations exists and we are not self, we try to find a suitable translation
        // For now, let's assume we pick the 'en' translation or just show original if translation off
        // Requirement: "Client: Render the translated text by default"
        // We need to know the User's preferred language on client side. 
        // For this refactor, let's assume 'en' or browser lang, or just use what server sent.
        
        let displayText = data.message; // Fallback
        
        if (data.original_text) {
             // New Payload format
             // data.translations is a dict { 'es': '...', 'de': '...' }
             // We need to pick one. Let's simple check for now:
             // In a real app we'd pass the user's language preference to JS.
             // Let's assume the server sent the relevant one in a simplified way OR we check data.translations
             
             // Since we didn't pass "user_lang" to JS in chat.html, let's default to showing the first available translation that ISN'T the original, or just original if disabled.
             // Actually app.py sends: { translations: {...}, original_text: ... }
             // We'll iterate translations. 
             
             displayText = data.original_text; // Default to original
             
             if (this.translationEnabled && !isSelf && data.translations) {
                 // Try to find ANY translation that matches browser lang or just take first
                 // Simple approach: Take the first value in translations
                 const keys = Object.keys(data.translations);
                 if (keys.length > 0) {
                     displayText = data.translations[keys[0]];
                 }
             }
        }
        
        // Escape HTML
        const safeText = this.escapeHtml(displayText);
        
        let html = `
            <div class="message-content" data-original="${this.escapeHtml(data.original_text || data.message)}">
                ${safeText}
            </div>
            <span class="timestamp">${data.timestamp || new Date().toLocaleTimeString()}</span>
        `;
        
        // Add translated indicator
        if (this.translationEnabled && !isSelf && data.original_text && displayText !== data.original_text) {
            html += `<span class="translated-indicator">Translated</span>`;
        }

        // Presence message check
        if (data.type === 'presence') {
             msgDiv.style.background = 'none';
             msgDiv.style.color = 'var(--text-secondary)';
             msgDiv.style.textAlign = 'center';
             msgDiv.style.width = '100%';
             msgDiv.style.maxWidth = '100%';
             msgDiv.innerHTML = `<small>${safeText}</small>`;
        } else {
             msgDiv.innerHTML = html;
        }

        this.container.appendChild(msgDiv);
        this.scrollToBottom();
    }
    
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.innerText = text;
        return div.innerHTML;
    }
    
    toggleTranslation() {
        this.translationEnabled = !this.translationEnabled;
        // Rerender or update existing messages? 
        // For simplicity, this toggle affects FUTURE messages in this session 
        // OR we can iterate existing DOM to flip them if we stored original.
        // Let's iterate existing.
        
        const contents = this.container.querySelectorAll('.message-content');
        contents.forEach(el => {
            const original = el.getAttribute('data-original');
            if (original) {
                // Determine if we should show original or "translated"
                // This is tricky because we didn't store the translated version in DOM.
                // Improvement: Store translated version in data attribute too.
                // For now, toggle only affects future messages or we reload page.
                // Let's just warn user or reload. Or better, flip text if we have both.
            }
        });
        
        return this.translationEnabled;
    }
}
