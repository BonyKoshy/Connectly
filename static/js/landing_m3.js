document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Theme Toggling ---
    // The ID 'themeToggle' is now on the INPUT element
    const themeToggleInput = document.getElementById('themeToggle');
    const html = document.documentElement;

    // Check saved preference
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    
    // Set initial state of checkbox
    // If savedTheme is 'light', checkbox should be checked (Sun)
    // If savedTheme is 'dark', checkbox should be unchecked (Moon)
    if (savedTheme === 'light') {
        themeToggleInput.checked = true;
    } else {
        themeToggleInput.checked = false;
    }

    themeToggleInput.addEventListener('change', () => {
        if (themeToggleInput.checked) {
            html.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        } else {
            html.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        }
    });

    // --- 2. Navbar Scroll Effect ---
    const navbar = document.querySelector('.m3-navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // --- 3. Intersection Observer for Reveals ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    const hiddenElements = document.querySelectorAll(
        '.reveal, .reveal-delay-1, .reveal-delay-2, .reveal-delay-3, .reveal-side, .reveal-up'
    );
    hiddenElements.forEach(el => observer.observe(el));

    // --- 4. Ripple Effect ---
    const buttons = document.querySelectorAll('.ripple');
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            let x = e.clientX - e.target.offsetLeft;
            let y = e.clientY - e.target.offsetTop;
            
            let ripples = document.createElement('span');
            ripples.style.left = x + 'px';
            ripples.style.top = y + 'px';
            ripples.classList.add('ripple-span');
            
            this.appendChild(ripples);
            
            setTimeout(() => {
                ripples.remove();
            }, 600);
        });
    });

    // --- 5. Scroll-Driven Marquee ---
    const marqueeTrack = document.querySelector('.marquee-track');
    if (marqueeTrack) {
        window.addEventListener('scroll', () => {
            // Only use JS scroll effect on desktop
            if (window.innerWidth > 768) {
                const scrollPos = window.scrollY;
                // Move left as we scroll down
                const moveAmount = scrollPos * -0.5; 
                marqueeTrack.style.transform = `translateX(${moveAmount}px)`;
            }
        });
    }

    // --- 6. Google Translate Integration ---
    // --- 6. Google Translate Integration & Custom Dropdown ---
    const customDropdown = document.getElementById('languageDropdown');
    
    if (customDropdown) {
        const selectedDisplay = customDropdown.querySelector('.dropdown-selected');
        const optionsList = customDropdown.querySelector('.dropdown-options');
        const options = customDropdown.querySelectorAll('.dropdown-option');

        // Toggle Dropdown
        selectedDisplay.addEventListener('click', (e) => {
            e.stopPropagation();
            customDropdown.classList.toggle('active');
        });

        // Handle Option Click
        options.forEach(option => {
            option.addEventListener('click', function() {
                const langCode = this.getAttribute('data-value');
                const langName = this.textContent;

                // Update Display
                selectedDisplay.textContent = langName;
                customDropdown.classList.remove('active');

                // Trigger Google Translate
                const googleCombo = document.querySelector('.goog-te-combo');
                if (googleCombo) {
                    googleCombo.value = langCode;
                    googleCombo.dispatchEvent(new Event('change'));
                } else {
                    console.warn('Google Translate widget not ready.');
                }
            });
        });

        // Close on Outside Click
        document.addEventListener('click', (e) => {
            if (!customDropdown.contains(e.target)) {
                customDropdown.classList.remove('active');
            }
        });
    }

    // Initialize Google Translate
    window.googleTranslateElementInit = function() {
        new google.translate.TranslateElement({
            pageLanguage: 'en',
            // includedLanguages: 'en,es,fr,de,zh-CN,ja...', // Optional: limit languages
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
            autoDisplay: false
        }, 'google_translate_element');
    };

    // --- 7. Layout Fixer (MutationObserver) ---
    // Google Translate adds style="top: 40px" to body. We must fight it.
    const observer2 = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                const body = document.body;
                if (body.style.top && body.style.top !== '0px') {
                    body.style.top = '0px';
                }
                if (body.style.position === 'relative') {
                    body.style.position = 'static';
                }
            }
        });
    });
    
    observer2.observe(document.body, { attributes: true, attributeFilter: ['style'] });
    
    // Also Force Remove the Banner Frame if it exists in DOM
    setInterval(() => {
        const banners = document.querySelectorAll('.goog-te-banner-frame');
        banners.forEach(banner => {
            banner.style.display = 'none';
            banner.style.visibility = 'hidden';
            banner.height = 0;
        });
        document.body.style.top = '0px'; // Redundant check
    }, 1000);

    // Inject Script
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.head.appendChild(script);

});