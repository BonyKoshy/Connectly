document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    const resultsList = document.getElementById('results-list');
    
    // Show/hide search results container
    const searchResults = document.getElementById('search-results');
    
    if (searchInput) {
        searchInput.addEventListener('input', async function() {
            const query = this.value.trim();
            if (query.length < 2) {
                searchResults.style.display = 'none';
                resultsList.innerHTML = '';
                return;
            }
            
            try {
                const response = await fetch(`/search_users?q=${encodeURIComponent(query)}`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const users = await response.json();
                
                if (users.length > 0) {
                    resultsList.innerHTML = users.map(user => `
                        <li class="result-item" data-username="${user.username}">
                            <i class="bi bi-person-circle"></i>
                            <span class="username">${user.username}</span>
                        </li>
                    `).join('');
                    searchResults.style.display = 'block';
                } else {
                    resultsList.innerHTML = '<li class="no-results">No users found</li>';
                    searchResults.style.display = 'block';
                }
                
                // Add click handlers to result items
                document.querySelectorAll('.result-item').forEach(item => {
                    item.addEventListener('click', function() {
                        const username = this.dataset.username;
                        window.location.href = `/start_chat/${username}`;
                    });
                });
            } catch (error) {
                console.error('Search failed:', error);
                resultsList.innerHTML = '<li class="error">Error loading search results</li>';
                searchResults.style.display = 'block';
            }
        });

        // Hide results when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.search-container')) {
                searchResults.style.display = 'none';
            }
        });
    }
});
