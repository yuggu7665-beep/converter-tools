/**
 * Main JavaScript - Converter Tools
 * Handles theme toggle and global functionality
 */

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const html = document.documentElement;

// Load saved theme or default to dark
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

// Theme toggle event
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
}

function updateThemeIcon(theme) {
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Smooth scroll for anchor links
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

// Add scroll animation to elements
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all category cards
document.querySelectorAll('.group').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    observer.observe(el);
});

// Global utility functions
window.ConverterUtils = {

    /**
     * Show loading spinner
     */
    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<div class="spinner mx-auto"></div>';
            element.classList.remove('hidden');
        }
    },

    /**
     * Hide loading spinner
     */
    hideLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '';
            element.classList.add('hidden');
        }
    },

    /**
     * Show success message
     */
    showSuccess(message, containerId = 'messageContainer') {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle mr-2"></i>
                    ${message}
                </div>
            `;
            setTimeout(() => {
                container.innerHTML = '';
            }, 5000);
        }
    },

    /**
     * Show error message
     */
    showError(message, containerId = 'messageContainer') {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-circle mr-2"></i>
                    ${message}
                </div>
            `;
        }
    },

    /**
     * Copy text to clipboard
     */
    async copyToClipboard(text, buttonElement) {
        try {
            await navigator.clipboard.writeText(text);

            // Update button feedback
            const originalText = buttonElement.innerHTML;
            buttonElement.innerHTML = '<i class="fas fa-check mr-2"></i>Copied!';
            buttonElement.classList.add('bg-green-600');

            setTimeout(() => {
                buttonElement.innerHTML = originalText;
                buttonElement.classList.remove('bg-green-600');
            }, 2000);

            return true;
        } catch (err) {
            console.error('Failed to copy:', err);
            alert('Failed to copy to clipboard');
            return false;
        }
    },

    /**
     * Download text as file
     */
    downloadFile(content, filename, mimeType = 'text/plain') {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    },

    /**
     * Download base64 image
     */
    downloadBase64Image(base64Data, filename) {
        const link = document.createElement('a');
        link.href = base64Data;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    },

    /**
     * Format file size
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    },

    /**
     * Validate file size
     */
    validateFileSize(file, maxSizeMB = 10) {
        const maxBytes = maxSizeMB * 1024 * 1024;
        return file.size <= maxBytes;
    },

    /**
     * Read file as text
     */
    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    },

    /**
     * Read file as data URL
     */
    readFileAsDataURL(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsDataURL(file);
        });
    }
};

// Console welcome message
console.log('%c🚀 Converter Tools', 'font-size: 24px; font-weight: bold; color: #3b82f6;');
console.log('%cAPI Documentation: /api/docs', 'font-size: 14px; color: #6b7280;');
