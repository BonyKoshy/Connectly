document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    // Initialize chat functionality
    const socket = io();
    
    // Listen for user join event
    socket.on('user_joined', function(username) {
        showToast(`${username} has joined the room`);
    });

    // Listen for user leave event
    socket.on('user_left', function(username) {
        showToast(`${username} has left the room`);
    });

    let currentRoom = null;
    const username = document.body.dataset.username || 'Anonymous';
    
    // Validate required elements exist
    const requiredElements = {
        sendButton: document.getElementById('sendButton'),
        messageInput: document.getElementById('messageInput'),
        messagesContainer: document.getElementById('messages-container')
    };

    for (const [elementName, element] of Object.entries(requiredElements)) {
        if (!element) {
            console.error(`Required element not found: ${elementName}`);
            return;
        }
    }

    console.log('Chat initialized - Username:', username);

    // Handle connection status
    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    // Handle incoming messages
    socket.on('message', (data) => {
        try {
            const messagesContainer = document.getElementById('messages-container');
            const noMessages = document.getElementById('no-messages');
            
            if (noMessages) {
                noMessages.style.display = 'none';
            }

            if (!data.message) {
                console.error('Received message with undefined content');
                return;
            }
            
            // Format timestamp from server or use current time
            const timestamp = data.timestamp ? 
                new Date(data.timestamp).toLocaleTimeString() : 
                new Date().toLocaleTimeString();
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${data.user === username ? 'sent' : 'received'}`;
            messageDiv.innerHTML = `
                <div class="message-content">${data.message}</div>
                <div class="message-info">
                    <span class="message-user">${data.user || 'Unknown'}</span>
                    <span class="message-time">${timestamp}</span>
                </div>
            `;

            if (messagesContainer) {
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        } catch (error) {
            console.error('Error handling message:', error);
        }
    });

    // Handle errors
    socket.on('error', (error) => {
        const messagesContainer = document.getElementById('messages-container');
        if (messagesContainer) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'message error';
            errorDiv.textContent = error.message || 'An error occurred';
            messagesContainer.appendChild(errorDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    });

    // Handle message sending
    const sendButton = document.getElementById('sendButton');
    const messageInput = document.getElementById('messageInput');

    const sendMessage = () => {
        const message = messageInput.value.trim();
        if (message && currentRoom) {
            // Disable input while sending
            messageInput.disabled = true;
            sendButton.disabled = true;

            socket.emit('message', {
                room: currentRoom,
                message: message,
                user: username
            }, (ack) => {
                // Re-enable input after server acknowledges
                messageInput.disabled = false;
                sendButton.disabled = false;
                
                if (ack && ack.error) {
                    console.error('Message send error:', ack.error);
                } else {
                    messageInput.value = '';
                    messageInput.focus();
                }
            });
        }
    };

    if (sendButton && messageInput) {
        // Handle click event
        sendButton.addEventListener('click', sendMessage);
        
        // Handle Enter key press
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Initialize chat room
    const initializeChatRoom = () => {
        const room = window.location.pathname.split('/').pop();
        if (room) {
            currentRoom = room;
            socket.emit('join', { room: room, username: username });
            console.log('Joined room:', room);
        }
    };

    // Toast Helper
    function showToast(message) {
        const toast = document.getElementById('toast');
        if (toast) {
            toast.textContent = message;
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 3000);
        }
    }

    initializeChatRoom();
});
