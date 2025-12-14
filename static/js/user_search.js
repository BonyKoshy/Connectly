import { debounce } from './modules/utils.js';
import { getById } from './modules/ui.js';

class UserSearchManager {
    constructor() {
        this.ele = {
            input: getById('search'),
            resultsList: getById('results-list'),
            resultsContainer: getById('search-results')
        };
        
        if (this.ele.input) {
            this.init();
        }
    }
    
    init() {
        // Apply debounce to the search handler (300ms delay)
        const debouncedSearch = debounce((e) => this.handleSearch(e), 300);
        
        this.ele.input.addEventListener('input', debouncedSearch);
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-container') && this.ele.resultsContainer) {
                this.ele.resultsContainer.style.display = 'none';
            }
        });
    }
    
    async handleSearch(event) {
        const query = event.target.value.trim();
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }
        
        try {
            const response = await fetch(`/search_users?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Search failed');
            
            const users = await response.json();
            this.renderResults(users);
            
        } catch (err) {
            console.error(err);
            this.ele.resultsList.innerHTML = '<li class="error" style="padding:16px; color:var(--md-sys-color-error);">Error loading results</li>';
            this.ele.resultsContainer.style.display = 'block';
        }
    }
    
    renderResults(users) {
        if (!users || users.length === 0) {
            this.ele.resultsList.innerHTML = '<li class="no-results" style="padding:16px; text-align:center;">No users found</li>';
        } else {
            this.ele.resultsList.innerHTML = users.map(user => `
                <li class="result-item" data-username="${user.username}" style="padding: 12px 16px; cursor: pointer; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--md-sys-color-outline-variant);">
                    <i class="bi bi-person-circle" style="font-size: 1.25rem;"></i>
                    <span class="username" style="font-weight: 500;">${user.username}</span>
                </li>
            `).join('');
            
            // Add click handlers
            this.ele.resultsList.querySelectorAll('.result-item').forEach(item => {
                item.addEventListener('click', () => {
                    const username = item.dataset.username;
                    window.location.href = `/start_chat/${username}`;
                });
            });
        }
        
        this.ele.resultsContainer.style.display = 'block';
    }
    
    hideResults() {
        if (this.ele.resultsContainer) {
            this.ele.resultsContainer.style.display = 'none';
        }
        if (this.ele.resultsList) {
            this.ele.resultsList.innerHTML = '';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UserSearchManager();
});
