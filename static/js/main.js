// Main JavaScript file for Notes Portal

// Global functions
window.confirmDelete = function(type, id, name) {
    const typeMap = {
        'class': 'class',
        'subject': 'subject',
        'note': 'note'
    };
    
    const message = `Are you sure you want to delete this ${typeMap[type]} "${name}"?`;
    const warning = type === 'class' ? 
        '\n\nThis will delete ALL subjects and notes within this class!' :
        type === 'subject' ? 
        '\n\nThis will delete ALL notes within this subject!' : 
        '\n\nThis note will be permanently deleted!';
    
    if (confirm(message + warning + '\n\nThis action cannot be undone.')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/delete_${type}/${id}`;
        document.body.appendChild(form);
        form.submit();
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasError = false;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    hasError = true;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (hasError) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Add loading states to buttons
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            const form = button.closest('form');
            if (form && form.checkValidity()) {
                // Only add loading state if form is valid
                setTimeout(function() {
                    button.disabled = true;
                    const originalText = button.innerHTML;
                    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                    
                    // Reset button after 10 seconds (fallback)
                    setTimeout(function() {
                        button.disabled = false;
                        button.innerHTML = originalText;
                    }, 10000);
                }, 100);
            }
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(function(modal) {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });
    
    // Tooltip initialization for elements with title attribute
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // File size formatter utility
    window.formatFileSize = function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };
    
    // Date formatter utility
    window.formatDate = function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };
    
    // Search enhancement
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        if (searchInput) {
            // Add search suggestions (simple implementation)
            searchInput.addEventListener('input', function() {
                // This could be enhanced with AJAX search suggestions
                const query = this.value.toLowerCase();
                if (query.length >= 2) {
                    // Simple client-side filtering could be implemented here
                    console.log('Searching for:', query);
                }
            });
        }
    }
    
    // Console message for developers
    console.log('%c📚 Notes Portal', 'color: #0d6efd; font-size: 24px; font-weight: bold;');
    console.log('%cWelcome to the Notes Portal! This application helps you organize your academic materials.', 'color: #6c757d; font-size: 14px;');
    
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js')
        //     .then(function(registration) {
        //         console.log('SW registered: ', registration);
        //     })
        //     .catch(function(registrationError) {
        //         console.log('SW registration failed: ', registrationError);
        //     });
    });
}

// Export functions for use in other scripts
window.NotesPortal = {
    confirmDelete: window.confirmDelete,
    formatFileSize: window.formatFileSize,
    formatDate: window.formatDate
};
