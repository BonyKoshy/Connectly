/**
 * Index/Landing Page Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // Current Date
    const dateEl = document.getElementById('current-date');
    if (dateEl) {
        const options = { month: 'long', day: 'numeric', year: 'numeric' };
        dateEl.textContent = new Date().toLocaleDateString('en-US', options);
    }
    
    // Intersection Observer for Animations
    const sections = document.querySelectorAll('section');
    const observerOptions = { threshold: 0.1 };
    
    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
            // Optional: Stop observing once active if you want one-time animation
            // sectionObserver.unobserve(entry.target);
        }
      });
    }, observerOptions);
    
    sections.forEach(section => sectionObserver.observe(section));
    
    // Carousel
    setupCarousel();
});

function setupCarousel() {
    const track = document.querySelector('.carousel-track');
    // Simple auto-scroll or manual logic can go here if we had buttons
    // The current HTML template didn't explicitly include buttons in the new M3 redesign
    // but the CSS suggests a simple flex row.
    // If we want auto-scroll:
    if (track) {
        // Optional: Simple auto-scroll animation or logic
    }
}
