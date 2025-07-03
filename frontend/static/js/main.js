// ========================================================================
// SHISHIR PORTFOLIO - MAIN JAVASCRIPT
// Responsive interactions and animations
// ========================================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================================================
    // MOBILE NAVIGATION
    // ========================================================================
    
    const navbar = document.querySelector('.navbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    // Smooth scrolling for anchor links
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - navbar.offsetHeight;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (window.innerWidth < 992) {
                    navbarCollapse.classList.remove('show');
                }
            }
        });
    });
    
    // Navbar background on scroll
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.background = 'rgba(30, 41, 59, 0.98)';
        } else {
            navbar.style.background = 'rgba(30, 41, 59, 0.95)';
        }
        
        // Hide navbar on scroll down, show on scroll up (mobile)
        if (window.innerWidth <= 768) {
            if (scrollTop > lastScrollTop && scrollTop > 200) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
    
    // ========================================================================
    // RESPONSIVE UTILITIES
    // ========================================================================
    
    // Detect device type
    function getDeviceType() {
        const width = window.innerWidth;
        if (width <= 768) return 'mobile';
        if (width <= 1024) return 'tablet';
        return 'desktop';
    }
    
    // Adjust animations based on device
    function adjustAnimationsForDevice() {
        const deviceType = getDeviceType();
        const animatedElements = document.querySelectorAll('.floating-element, .orbit-item');
        
        if (deviceType === 'mobile') {
            // Reduce animations on mobile for better performance
            animatedElements.forEach(el => {
                el.style.animationDuration = '8s';
            });
        } else {
            animatedElements.forEach(el => {
                el.style.animationDuration = '6s';
            });
        }
    }
    
    // ========================================================================
    // INTERSECTION OBSERVER FOR ANIMATIONS
    // ========================================================================
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Special handling for different elements
                if (entry.target.classList.contains('stat-number')) {
                    animateCounter(entry.target);
                }
                
                if (entry.target.classList.contains('skill-progress')) {
                    animateSkillBar(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateOnScroll = document.querySelectorAll('.fade-in, .stat-number, .skill-card');
    animateOnScroll.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
    
    // ========================================================================
    // COUNTER ANIMATION
    // ========================================================================
    
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                element.textContent = target + '+';
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }
    
    // ========================================================================
    // SKILL BAR ANIMATION
    // ========================================================================
    
    function animateSkillBar(element) {
        const percentage = element.getAttribute('data-percentage');
        setTimeout(() => {
            element.style.width = percentage + '%';
        }, 200);
    }
    
    // ========================================================================
    // TYPING EFFECT
    // ========================================================================
    
    const typingText = document.querySelector('.typing-text');
    if (typingText) {
        const texts = [
            'UI/UX Designer',
            'Brand Strategist', 
            'Creative Director',
            'Visual Designer'
        ];
        
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        
        function typeText() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                typingText.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingText.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
            }
            
            let typeSpeed = isDeleting ? 50 : 100;
            
            if (!isDeleting && charIndex === currentText.length) {
                typeSpeed = 2000;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
            }
            
            setTimeout(typeText, typeSpeed);
        }
        
        typeText();
    }
    
    // ========================================================================
    // FLOATING ELEMENTS ANIMATION
    // ========================================================================
    
    function initFloatingElements() {
        const floatingElements = document.querySelectorAll('.floating-element');
        
        floatingElements.forEach((element, index) => {
            const speed = element.getAttribute('data-speed') || 1;
            
            // Mouse move effect (desktop only)
            if (window.innerWidth > 1024) {
                document.addEventListener('mousemove', (e) => {
                    const x = (e.clientX / window.innerWidth) * 100;
                    const y = (e.clientY / window.innerHeight) * 100;
                    
                    const moveX = (x - 50) * speed * 0.1;
                    const moveY = (y - 50) * speed * 0.1;
                    
                    element.style.transform = `translate(${moveX}px, ${moveY}px)`;
                });
            }
        });
    }
    
    // ========================================================================
    // FORM HANDLING
    // ========================================================================
    
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', handleFormSubmit);
    }
    
    async function handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        const submitButton = e.target.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        
        // Show loading state
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                showNotification('Thank you! Your message has been sent successfully.', 'success');
                e.target.reset();
            } else {
                showNotification(result.message || 'There was an error sending your message.', 'error');
            }
        } catch (error) {
            showNotification('Network error. Please try again.', 'error');
        } finally {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    }
    
    // ========================================================================
    // NOTIFICATION SYSTEM
    // ========================================================================
    
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(n => n.remove());
        
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
                <span>${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add notification styles
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            z-index: 9999;
            background: ${type === 'success' ? '#10B981' : '#EF4444'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            transform: translateX(100%);
            transition: transform 0.3s ease;
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }
    
    // ========================================================================
    // RESIZE HANDLER
    // ========================================================================
    
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            adjustAnimationsForDevice();
            initFloatingElements();
        }, 250);
    });
    
    // ========================================================================
    // LAZY LOADING FOR IMAGES
    // ========================================================================
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    const lazyImages = document.querySelectorAll('img[data-src]');
    lazyImages.forEach(img => imageObserver.observe(img));
    
    // ========================================================================
    // PERFORMANCE OPTIMIZATION
    // ========================================================================
    
    // Reduce motion for users who prefer it
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const animatedElements = document.querySelectorAll('[class*="animate"], [class*="float"]');
        animatedElements.forEach(el => {
            el.style.animation = 'none';
            el.style.transition = 'none';
        });
    }
    
    // Initialize everything
    adjustAnimationsForDevice();
    initFloatingElements();
    
    // Add loaded class to body for CSS transitions
    document.body.classList.add('loaded');
});

// ========================================================================
// UTILITY FUNCTIONS
// ========================================================================

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}