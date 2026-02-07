// Enhanced Features JavaScript

// Theme Management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme();
        this.bindEvents();
    }

    bindEvents() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme();
        localStorage.setItem('theme', this.currentTheme);
    }

    applyTheme() {
        document.body.setAttribute('data-theme', this.currentTheme);
        const icon = document.querySelector('#themeToggle i');
        if (icon) {
            icon.className = this.currentTheme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
}

// Animated Counter
class AnimatedCounter {
    static countUp(element, target, duration = 2000) {
        const start = parseInt(element.textContent) || 0;
        const increment = (target - start) / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }
}

// Preloader Management
class PreloaderManager {
    constructor() {
        this.preloader = document.getElementById('preloader');
        this.init();
    }

    init() {
        window.addEventListener('load', () => {
            setTimeout(() => this.hidePreloader(), 1500);
        });
    }

    hidePreloader() {
        if (this.preloader) {
            this.preloader.style.opacity = '0';
            setTimeout(() => {
                this.preloader.style.display = 'none';
            }, 500);
        }
    }
}

// Quick Planner
class QuickPlanner {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        const quickWeight = document.getElementById('quickWeight');
        const quickHeight = document.getElementById('quickHeight');
        const generateBtn = document.getElementById('quickGenerate');

        if (quickWeight && quickHeight) {
            quickWeight.addEventListener('input', () => this.calculateQuickBMI());
            quickHeight.addEventListener('input', () => this.calculateQuickBMI());
        }

        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateQuickPlan());
        }
    }

    calculateQuickBMI() {
        const weight = parseFloat(document.getElementById('quickWeight').value);
        const height = parseFloat(document.getElementById('quickHeight').value);

        if (weight && height) {
            const bmi = weight / ((height / 100) ** 2);
            this.displayQuickBMI(bmi);
        }
    }

    displayQuickBMI(bmi) {
        const bmiDisplay = document.getElementById('quickBMI');
        const bmiValue = document.getElementById('quickBMIValue');

        if (bmiDisplay && bmiValue) {
            bmiValue.textContent = bmi.toFixed(1);
            bmiDisplay.style.display = 'flex';
            
            // Add color coding
            let color = '#28a745'; // Normal
            if (bmi < 18.5) color = '#17a2b8'; // Underweight
            else if (bmi > 25) color = '#ffc107'; // Overweight
            else if (bmi > 30) color = '#dc3545'; // Obese

            bmiDisplay.style.background = `linear-gradient(45deg, ${color}, ${this.lightenColor(color, 20)})`;
        }
    }

    generateQuickPlan() {
        const weight = document.getElementById('quickWeight').value;
        const height = document.getElementById('quickHeight').value;
        const budget = document.getElementById('quickBudget').value;
        const cuisine = document.getElementById('quickCuisine').value;

        if (!weight || !height || !budget) {
            this.showAlert('error', 'Please fill in weight, height, and budget fields');
            return;
        }

        const generateBtn = document.getElementById('quickGenerate');
        const originalText = generateBtn.innerHTML;
        
        // Show loading
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        generateBtn.disabled = true;

        // Simulate generation
        setTimeout(() => {
            this.displayQuickResults(cuisine);
            generateBtn.innerHTML = originalText;
            generateBtn.disabled = false;
        }, 2000);
    }

    displayQuickResults(cuisine) {
        const resultsDiv = document.getElementById('quickResults');
        const breakfast = document.getElementById('quickBreakfast');
        const lunch = document.getElementById('quickLunch');
        const dinner = document.getElementById('quickDinner');

        const meals = this.getSampleMeals(cuisine);

        if (breakfast) breakfast.textContent = meals.breakfast;
        if (lunch) lunch.textContent = meals.lunch;
        if (dinner) dinner.textContent = meals.dinner;

        if (resultsDiv) {
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    getSampleMeals(cuisine) {
        const meals = {
            'Mediterranean': {
                breakfast: 'Greek yogurt with honey, walnuts, and fresh berries',
                lunch: 'Quinoa tabbouleh with grilled chicken and olive oil',
                dinner: 'Baked salmon with roasted vegetables and lemon'
            },
            'Asian': {
                breakfast: 'Congee with ginger and scallions',
                lunch: 'Miso soup with tofu and brown rice',
                dinner: 'Stir-fried vegetables with lean beef and jasmine rice'
            },
            'Mexican': {
                breakfast: 'Scrambled eggs with black beans and avocado',
                lunch: 'Chicken and vegetable burrito bowl',
                dinner: 'Grilled fish tacos with cabbage slaw'
            },
            'Italian': {
                breakfast: 'Whole grain toast with ricotta and fresh tomatoes',
                lunch: 'Caprese salad with grilled chicken',
                dinner: 'Zucchini noodles with turkey meatballs'
            },
            'No Preference': {
                breakfast: 'Oatmeal with fresh fruits and nuts',
                lunch: 'Grilled chicken salad with mixed vegetables',
                dinner: 'Baked sweet potato with lean protein'
            }
        };

        return meals[cuisine] || meals['No Preference'];
    }

    showAlert(type, message) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alert.style.cssText = `
            position: fixed;
            top: 100px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            min-width: 300px;
        `;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alert);

        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    lightenColor(color, percent) {
        const num = parseInt(color.replace("#", ""), 16);
        const amt = Math.round(2.55 * percent);
        const R = (num >> 16) + amt;
        const B = (num >> 8 & 0x00FF) + amt;
        const G = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 + (B < 255 ? B < 1 ? 0 : B : 255) * 0x100 + (G < 255 ? G < 1 ? 0 : G : 255)).toString(16).slice(1);
    }
}

// Testimonials Carousel
class TestimonialsCarousel {
    constructor() {
        this.currentIndex = 0;
        this.testimonials = document.querySelectorAll('.testimonial-card');
        this.init();
    }

    init() {
        if (this.testimonials.length > 0) {
            this.startAutoplay();
        }
    }

    startAutoplay() {
        setInterval(() => {
            this.nextTestimonial();
        }, 5000);
    }

    nextTestimonial() {
        this.testimonials[this.currentIndex].classList.remove('active');
        this.currentIndex = (this.currentIndex + 1) % this.testimonials.length;
        this.testimonials[this.currentIndex].classList.add('active');
    }
}

// Smooth Scrolling
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
}

// Back to Top Button
class BackToTop {
    constructor() {
        this.button = document.getElementById('backToTop');
        this.init();
    }

    init() {
        if (this.button) {
            window.addEventListener('scroll', () => this.toggleVisibility());
            this.button.addEventListener('click', () => this.scrollToTop());
        }
    }

    toggleVisibility() {
        if (window.pageYOffset > 300) {
            this.button.classList.add('visible');
        } else {
            this.button.classList.remove('visible');
        }
    }

    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Floating Elements Animation
class FloatingElements {
    constructor() {
        this.elements = document.querySelectorAll('.floating-element');
        this.init();
    }

    init() {
        this.elements.forEach((element, index) => {
            this.animateElement(element, index);
        });
    }

    animateElement(element, index) {
        const delay = index * 0.5;
        const duration = 3 + Math.random() * 2;
        
        element.style.animationDelay = `${delay}s`;
        element.style.animationDuration = `${duration}s`;
        element.classList.add('floating-animation');
    }
}

// Newsletter Subscription
class Newsletter {
    constructor() {
        this.form = document.querySelector('.newsletter');
        this.init();
    }

    init() {
        if (this.form) {
            const button = this.form.querySelector('button');
            if (button) {
                button.addEventListener('click', (e) => this.subscribe(e));
            }
        }
    }

    subscribe(e) {
        e.preventDefault();
        const input = this.form.querySelector('input[type="email"]');
        const email = input.value;

        if (this.validateEmail(email)) {
            this.showSuccess('Thank you for subscribing!');
            input.value = '';
        } else {
            this.showError('Please enter a valid email address');
        }
    }

    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show mt-2`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        this.form.appendChild(alert);

        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    }
}

// Global Functions
window.scrollToSection = function(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
};

// Initialize all features when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all classes
    new PreloaderManager();
    new ThemeManager();
    new QuickPlanner();
    new TestimonialsCarousel();
    new SmoothScroll();
    new BackToTop();
    new FloatingElements();
    new Newsletter();

    // Animated counters on scroll
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('[data-count]');
                counters.forEach(counter => {
                    const target = parseInt(counter.getAttribute('data-count'));
                    AnimatedCounter.countUp(counter, target);
                });
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
        observer.observe(statsSection);
    }

    // Add custom CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        .floating-animation {
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            33% { transform: translateY(-20px) rotate(5deg); }
            66% { transform: translateY(10px) rotate(-3deg); }
        }
        
        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }
        
        .back-to-top:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        [data-theme="dark"] {
            --bs-body-bg: #1a1a1a;
            --bs-body-color: #e9ecef;
        }
        
        [data-theme="dark"] .navbar {
            background: #2d2d2d !important;
        }
        
        [data-theme="dark"] .card {
            background: #2d2d2d;
            border-color: #404040;
        }
        
        [data-theme="dark"] .feature-card-enhanced {
            background: #2d2d2d;
            border-color: #404040;
        }
        
        .preloader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            transition: opacity 0.5s ease;
        }
        
        .preloader-content {
            text-align: center;
            color: white;
        }
        
        .cooking-animation {
            font-size: 3rem;
            animation: cooking 2s ease-in-out infinite;
        }
        
        @keyframes cooking {
            0%, 100% { transform: rotate(0deg); }
            25% { transform: rotate(-10deg); }
            75% { transform: rotate(10deg); }
        }
    `;
    document.head.appendChild(style);
});
