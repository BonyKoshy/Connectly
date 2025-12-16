export class SocketClient {
    constructor(url, room, handlers) {
        this.url = url;
        this.room = room;
        this.handlers = handlers; // Object with onMessage, onJoin, onLeave
        this.socket = null;
    }
    
    connect() {
        this.socket = io.connect(this.url);
        
        this.socket.on("connect", () => {
            console.log("Connected to websocket");
            this.joinRoom();
            if (this.handlers.onConnect) this.handlers.onConnect();
        });
        
        this.socket.on("message", (data) => {
            if (this.handlers.onMessage) this.handlers.onMessage(data);
        });
        
        // Debugging
        this.socket.on("disconnect", () => {
            console.log("Disconnected");
        });
    }
    
    joinRoom() {
        this.socket.emit("join", { room: this.room });
    }
    
    leaveRoom() {
        this.socket.emit("leave", { room: this.room });
    }
    
    sendMessage(message) {
        if (message && message.trim()) {
            this.socket.emit("message", {
                room: this.room,
                message: message
            });
        }
    }
}
