import { getSocket } from './modules/socket.js';
import { showToast, getById } from './modules/ui.js';
import { formatTime, escapeHtml } from './modules/utils.js';

class ChatManager {
    constructor() {
        this.socket = getSocket();
        this.username = document.body.dataset.username || 'Anonymous';
        this.currentRoom = null;
        
        // UI Elements
        this.ele = {
            sendButton: getById('sendButton'),
            messageInput: getById('messageInput'),
            messagesContainer: getById('messages-container'),
            chatName: getById('chat-name'),
            toast: getById('toast')
        };
        
        this.init();
    }
    
    init() {
        if (!this.socket) return;
        
        this.setupSocketListeners();
        this.setupUIListeners();
        this.joinCurrentRoom();
        
        console.log(`ChatManager initialized for user: ${this.username}`);
    }
    
    setupSocketListeners() {
        // User Join/Leave
        this.socket.on('user_joined', (username) => showToast(`${username} has joined`));
        this.socket.on('user_left', (username) => showToast(`${username} has left`));
        
        // Messages
        this.socket.on('message', (data) => this.handleIncomingMessage(data));
        
        // Errors
        this.socket.on('error', (err) => {
            console.error('Socket error:', err);
            showToast(`Error: ${err.message || 'Unknown error'}`);
        });
    }
    
    setupUIListeners() {
        if (this.ele.sendButton && this.ele.messageInput) {
            this.ele.sendButton.addEventListener('click', () => this.sendMessage());
            
            this.ele.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        }
    }
    
    joinCurrentRoom() {
        // Extract room from URL: /chat/<room>
        const pathParts = window.location.pathname.split('/');
        // Assuming last part is room, or second to last if trailing slash
        const room = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2];
        
        if (room && window.location.pathname.includes('/chat/')) {
            this.currentRoom = room;
            this.socket.emit('join', { room: this.currentRoom, username: this.username });
            console.log(`Joined room: ${this.currentRoom}`);
        }
    }
    
    handleIncomingMessage(data) {
        if (!data.message) return;
        
        const isSent = data.user === this.username;
        const time = formatTime(data.timestamp);
        const safeMessage = escapeHtml(data.message);
        
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isSent ? 'sent' : 'received'}`;
        msgDiv.innerHTML = `
            <div class="message-content">${safeMessage}</div>
            <div class="message-info" style="font-size: 0.75rem; opacity: 0.7; margin-top: 4px;">
                <span class="message-user">${escapeHtml(data.user)}</span> • 
                <span class="message-time">${time}</span>
            </div>
        `;
        
        if (this.ele.messagesContainer) {
            this.ele.messagesContainer.appendChild(msgDiv);
            this.scrollToBottom();
        }
    }
    
    sendMessage() {
        const text = this.ele.messageInput.value.trim();
        if (!text || !this.currentRoom) return;
        
        this.setLoading(true);
        
        this.socket.emit('message', {
            room: this.currentRoom,
            message: text,
            user: this.username
        }, (ack) => {
            this.setLoading(false);
            if (ack && ack.error) {
                showToast(`Failed to send: ${ack.error}`);
            } else {
                this.ele.messageInput.value = '';
                this.ele.messageInput.focus();
            }
        });
    }
    
    setLoading(isLoading) {
        if (this.ele.sendButton) this.ele.sendButton.disabled = isLoading;
        if (this.ele.messageInput) this.ele.messageInput.disabled = isLoading;
    }
    
    scrollToBottom() {
        if (this.ele.messagesContainer) {
            this.ele.messagesContainer.scrollTop = this.ele.messagesContainer.scrollHeight;
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new ChatManager();
});
