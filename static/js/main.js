document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const spinner = document.getElementById('spinner');
    const submitBtn = form.querySelector('button[type="submit"]');

    if (form) {
        form.addEventListener('submit', function() {
            spinner.style.display = 'inline-block';
            submitBtn.disabled = true;
        });
    }

    // Auto-focus on news textarea if empty
    const newsInput = document.getElementById('news');
    if (newsInput && newsInput.value === '') {
        newsInput.focus();
    }

    // Character count for textarea
    if (newsInput) {
        newsInput.addEventListener('input', function() {
            const charCount = this.value.length;
            if (charCount < 50) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    }

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
        });
    });

    // Add toast notification support
    console.log('🔍 Fake News Detection System Loaded');
});

// Function to show alerts
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
}
