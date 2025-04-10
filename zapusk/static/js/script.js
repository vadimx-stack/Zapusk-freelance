document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const loader = document.getElementById('loader-wrapper');
        if (loader) {
            loader.style.opacity = '0';
            loader.style.visibility = 'hidden';
        }
    }, 1000);
    
    initScrollAnimations();
    
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            
            const spans = this.querySelectorAll('span');
            spans.forEach(span => span.classList.toggle('active'));
            
            if (mainNav.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    }
    
    window.addEventListener('scroll', function() {
        const header = document.querySelector('.header');
        if (header) {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
    });
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    animateCards();
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', validateForm);
    });
});

function initScrollAnimations() {
    gsap.registerPlugin(ScrollTrigger);
    
    gsap.utils.toArray('.section-title').forEach(title => {
        gsap.from(title, {
            scrollTrigger: {
                trigger: title,
                start: "top 80%",
                toggleActions: "play none none none"
            },
            y: 50,
            opacity: 0,
            duration: 0.8,
            ease: "power2.out"
        });
    });
    
    gsap.utils.toArray('.card').forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: "top 85%",
                toggleActions: "play none none none"
            },
            y: 100,
            opacity: 0,
            duration: 0.6,
            delay: index * 0.1,
            ease: "power2.out"
        });
    });
    
    gsap.utils.toArray('.icon-animated').forEach(icon => {
        gsap.from(icon, {
            scrollTrigger: {
                trigger: icon,
                start: "top 85%",
                toggleActions: "play none none none"
            },
            scale: 0,
            rotation: -180,
            opacity: 0,
            duration: 0.6,
            ease: "back.out(1.7)"
        });
    });
}

function animateCards() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -10,
                boxShadow: "0 15px 30px rgba(0, 0, 0, 0.1)",
                duration: 0.3,
                ease: "power2.out"
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                duration: 0.3,
                ease: "power2.out"
            });
        });
    });
}

function validateForm(e) {
    let isValid = true;
    const form = e.target;
    
    form.querySelectorAll('.form-error').forEach(error => {
        error.remove();
    });
    
    form.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            showError(field, 'Это поле обязательно для заполнения');
        }
    });
    
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailField.value)) {
            isValid = false;
            showError(emailField, 'Введите корректный email адрес');
        }
    }
    
    const passwordField = form.querySelector('input[name="password"]');
    const confirmPasswordField = form.querySelector('input[name="confirm_password"]');
    
    if (passwordField && confirmPasswordField) {
        if (passwordField.value !== confirmPasswordField.value) {
            isValid = false;
            showError(confirmPasswordField, 'Пароли не совпадают');
        }
        
        if (passwordField.value.length < 8) {
            isValid = false;
            showError(passwordField, 'Пароль должен содержать не менее 8 символов');
        }
    }
    
    if (!isValid) {
        e.preventDefault();
        
        const firstError = form.querySelector('.form-error');
        if (firstError) {
            firstError.previousElementSibling.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }
}

function showError(field, message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    
    field.classList.add('is-invalid');
    field.parentNode.appendChild(errorElement);
    
    field.addEventListener('input', function() {
        this.classList.remove('is-invalid');
        const error = this.parentNode.querySelector('.form-error');
        if (error) {
            error.remove();
        }
    });
} 