// Main JavaScript for LearnHub

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Auto-hide messages after 5 seconds
setTimeout(() => {
    const messages = document.querySelector('.messages-container');
    if (messages) {
        messages.style.transition = 'opacity 0.5s ease-out';
        messages.style.opacity = '0';
        setTimeout(() => {
            messages.style.display = 'none';
        }, 500);
    }
}, 5000);

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'var(--danger)';
        } else {
            input.style.borderColor = 'var(--gray-300)';
        }
    });

    return isValid;
}

// Add input listeners to clear error states
document.querySelectorAll('.form-input, .form-textarea, .form-select').forEach(input => {
    input.addEventListener('input', function() {
        this.style.borderColor = 'var(--gray-300)';
    });

    input.addEventListener('focus', function() {
        this.style.borderColor = 'var(--primary)';
    });

    input.addEventListener('blur', function() {
        if (!this.value.trim() && this.hasAttribute('required')) {
            this.style.borderColor = 'var(--danger)';
        } else {
            this.style.borderColor = 'var(--gray-300)';
        }
    });
});

console.log('LearnHub initialized successfully!');
