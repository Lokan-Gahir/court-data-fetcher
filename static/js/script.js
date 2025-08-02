document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus on first input field
    const firstInput = document.querySelector('form input, form select');
    if (firstInput) firstInput.focus();
    
    // Error page functionality
    if (document.querySelector('.error-container')) {
        // Auto-scroll to error message
        document.querySelector('.error-message').scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
        
        // Copy error details feedback
        const copyBtn = document.querySelector('[onclick^="navigator.clipboard"]');
        if (copyBtn) {
            copyBtn.addEventListener('click', function() {
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check me-1"></i>Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            });
        }
    }
    
    // Form validation enhancements
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Scroll to first invalid field
                const invalidField = form.querySelector('.is-invalid');
                if (invalidField) {
                    invalidField.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            }
            form.classList.add('was-validated');
        }, false);
    });
});