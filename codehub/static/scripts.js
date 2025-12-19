// static/scripts.js

// Optional: Ripple effect for buttons for a nice UI touch
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
  btn.addEventListener('click', function (e) {
    // Remove any existing ripple
    const oldRipple = this.querySelector('.ripple');
    if (oldRipple) {
      oldRipple.remove();
    }

    // Create and position the new ripple
    let ripple = document.createElement('span');
    ripple.className = 'ripple';
    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    
    this.appendChild(ripple);
    
    // Clean up the ripple element after the animation
    setTimeout(() => ripple.remove(), 700);
  });
});

// Optional: Add a class to the navbar on scroll for styling effects
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 10) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});