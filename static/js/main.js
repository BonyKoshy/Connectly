/* static/js/main.js */

document.addEventListener("DOMContentLoaded", () => {
  // --- 1. Theme Toggle Logic ---
  const themeToggleBtn = document.getElementById("themeToggle");
  const htmlElement = document.documentElement;
  const navLogo = document.getElementById("nav-logo");

  function setTheme(isDark) {
    if (isDark) {
      htmlElement.classList.add("dark");
      localStorage.theme = "dark";
      if (themeToggleBtn) themeToggleBtn.checked = true;
      if (navLogo) navLogo.style.filter = "brightness(0) invert(1)";
    } else {
      htmlElement.classList.remove("dark");
      localStorage.theme = "light";
      if (themeToggleBtn) themeToggleBtn.checked = false;
      if (navLogo) navLogo.style.filter = "none";
    }
  }

  const savedTheme = localStorage.theme;
  const systemDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(savedTheme === "dark" || (!savedTheme && systemDark));

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("change", function () {
      setTheme(this.checked);
    });
  }

  // --- 2. Navbar Scroll Effect ---
  const navbar = document.getElementById("navbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 20) {
        navbar.classList.add(
          "shadow-lg",
          "bg-white/95",
          "dark:bg-slate-900/95"
        );
        navbar.classList.remove("bg-white/80", "dark:bg-slate-900/80");
      } else {
        navbar.classList.remove(
          "shadow-lg",
          "bg-white/95",
          "dark:bg-slate-900/95"
        );
        navbar.classList.add("bg-white/80", "dark:bg-slate-900/80");
      }
    });
  }

  // --- 3. Powered By Strip Logic ---
  const poweredTrack = document.querySelector(".powered-track");
  const poweredSection = document.getElementById("powered-section");

  if (poweredTrack && poweredSection) {
    // A. Mobile Infinite Scroll (Duplication)
    // We clone the content to ensure the loop is seamless
    if (window.innerWidth < 768) {
      const content = poweredTrack.innerHTML;
      // Duplicate content 4 times to ensure enough width for smooth looping
      poweredTrack.innerHTML = content + content + content + content;
      poweredTrack.classList.add("mobile-scroll");
    }
    // B. Desktop Scroll-Linked Animation
    else {
      window.addEventListener("scroll", () => {
        // Calculate position relative to viewport
        const sectionTop = poweredSection.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;

        // Only animate when section is roughly in view
        if (
          sectionTop < windowHeight &&
          sectionTop > -poweredSection.offsetHeight
        ) {
          // Move the strip based on scroll position (Parallax)
          // Adjust the '0.2' multiplier to change speed/direction
          const moveAmount = (window.scrollY - poweredSection.offsetTop) * 0.2;
          poweredTrack.style.transform = `translateX(${moveAmount}px)`;
        }
      });
    }
  }
});
