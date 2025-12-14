/**
 * Socket.IO Instance Manager.
 * Wraps the global io() object to ensure singleton access.
 */

let socketInstance = null;

export function getSocket() {
    if (!socketInstance) {
        if (typeof io === 'undefined') {
            console.error('Socket.IO client not loaded');
            return null;
        }
        socketInstance = io();
        
        // Default handlers
        socketInstance.on('connect', () => console.log('Socket connected'));
        socketInstance.on('disconnect', () => console.log('Socket disconnected'));
    }
    return socketInstance;
}
