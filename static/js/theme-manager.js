export class ThemeManager {
    constructor() {
        this.toggleBtn = document.getElementById('theme-toggle');
        this.html = document.documentElement;
        this.icon = this.toggleBtn.querySelector('i');
        
        // Init
        this.init();
    }
    
    init() {
        // Check local storage or system preference
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme) {
            this.setTheme(savedTheme);
        } else if (systemPrefersDark) {
            this.setTheme('dark');
        } else {
            this.setTheme('light');
        }
        
        this.toggleBtn.addEventListener('click', () => this.toggle());
    }
    
    setTheme(theme) {
        this.html.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.updateIcon(theme);
    }
    
    toggle() {
        const current = this.html.getAttribute('data-theme');
        const newTheme = current === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
    
    updateIcon(theme) {
        if (theme === 'dark') {
            this.icon.classList.replace('bi-moon', 'bi-sun');
        } else {
            this.icon.classList.replace('bi-sun', 'bi-moon');
        }
    }
}
