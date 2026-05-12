// script.js
// This file can be used for any interactive elements, animations,
// or dynamic content loading on your ELENOR OMNI marketing site.

document.addEventListener('DOMContentLoaded', () => {
    console.log('ELENOR OMNI website loaded!');

    // Example: Add a subtle animation to the main title on scroll
    const mainTitle = document.querySelector('h1');
    if (mainTitle) {
        window.addEventListener('scroll', () => {
            const scrollPos = window.scrollY;
            if (scrollPos > 50) {
                mainTitle.style.opacity = '0.8';
                mainTitle.style.transform = 'scale(0.98)';
            } else {
                mainTitle.style.opacity = '1';
                mainTitle.style.transform = 'scale(1)';
            }
        });
    }

    // You can add more JavaScript for:
    // - Smooth scrolling
    // - Feature carousel/slider
    // - Contact form validation
    // - Dynamic content updates
    // - Integration with analytics
});
