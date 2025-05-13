// Display current date in the Hero section
const options = { month: 'long', day: 'numeric', year: 'numeric' };
const today = new Date().toLocaleDateString('en-US', options);
document.getElementById('current-date').textContent = today;


// Section Animation using IntersectionObserver
const sections = document.querySelectorAll('section');
const observerOptions = { threshold: 0.5 };
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('active');
  });
}, observerOptions);
sections.forEach(section => sectionObserver.observe(section));

// Toggle expansion for System Specifications cards
function toggleRequirements() {
  const specCards = document.querySelectorAll('.spec-card');
  specCards.forEach(card => card.classList.toggle('expanded'));
}

// Carousel Functionality for Co-developed Section
const carouselTrack = document.querySelector('.carousel-track');
const prevButton = document.querySelector('.carousel-btn.prev');
const nextButton = document.querySelector('.carousel-btn.next');
let carouselIndex = 0;

function updateCarousel() {
  const carouselItems = document.querySelectorAll('.carousel-item');
  const itemWidth = carouselItems[0].offsetWidth + 20; // include margin
  carouselTrack.style.transform = `translateX(-${carouselIndex * itemWidth}px)`;
}

prevButton.addEventListener('click', () => {
  if (carouselIndex > 0) { carouselIndex--; updateCarousel(); }
});

nextButton.addEventListener('click', () => {
  const carouselItems = document.querySelectorAll('.carousel-item');
  if (carouselIndex < carouselItems.length - 1) { carouselIndex++; updateCarousel(); }
});

// Tooltip for Data Flow Diagram Elements
document.querySelectorAll('.dfd-node').forEach(node => {
  node.addEventListener('mouseover', function (event) {
    const tooltip = document.getElementById('tooltip');
    tooltip.textContent = this.getAttribute('data-tooltip');
    tooltip.style.left = `${event.pageX + 10}px`;
    tooltip.style.top = `${event.pageY + 10}px`;
    tooltip.style.display = 'block';
  });
  node.addEventListener('mouseout', () => {
    document.getElementById('tooltip').style.display = 'none';
  });
});
