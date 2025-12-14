/**
 * UI Helper functions.
 */

/**
 * Show a toast notification.
 * @param {string} message - The message to display.
 */
export function showToast(message) {
    let toast = document.getElementById('toast');
    
    // Create toast if it doesn't exist contextually (though it should be in HTML)
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast-notification';
        document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.style.display = 'block';
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.style.display = 'none';
        toast.classList.remove('show');
    }, 3000);
}

/**
 * Select an element by ID safely.
 * @param {string} id - Element ID.
 * @returns {HTMLElement|null}
 */
export function getById(id) {
    return document.getElementById(id);
}
