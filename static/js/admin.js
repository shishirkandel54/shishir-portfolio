// Admin Dashboard JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const alertInstance = new bootstrap.Alert(alert);
            alertInstance.close();
        });
    }, 5000);

    // Initialize table sorting if DataTables is available
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.data-table').DataTable({
            pageLength: 25,
            responsive: true,
            order: [[0, 'desc']],
            language: {
                search: "Search:",
                lengthMenu: "Show _MENU_ entries",
                info: "Showing _START_ to _END_ of _TOTAL_ entries",
                paginate: {
                    first: "First",
                    last: "Last",
                    next: "Next",
                    previous: "Previous"
                }
            }
        });
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[data-max-length]');
    textareas.forEach(function(textarea) {
        const maxLength = parseInt(textarea.getAttribute('data-max-length'));
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = `<span class="current-length">0</span>/${maxLength}`;
        textarea.parentNode.appendChild(counter);

        const currentLengthSpan = counter.querySelector('.current-length');
        
        textarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            currentLengthSpan.textContent = currentLength;
            
            if (currentLength > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
            
            if (currentLength > maxLength) {
                counter.classList.add('text-danger');
                counter.classList.remove('text-warning');
            } else {
                counter.classList.remove('text-danger');
            }
        });
        
        // Trigger initial count
        textarea.dispatchEvent(new Event('input'));
    });

    // Auto-save functionality for forms
    const autoSaveForms = document.querySelectorAll('.auto-save');
    autoSaveForms.forEach(function(form) {
        let saveTimeout;
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(function(input) {
            input.addEventListener('input', function() {
                clearTimeout(saveTimeout);
                showSaveStatus('saving');
                
                saveTimeout = setTimeout(function() {
                    autoSaveForm(form);
                }, 2000);
            });
        });
    });

    // Bulk selection functionality
    const selectAllCheckbox = document.querySelector('#select-all');
    if (selectAllCheckbox) {
        const itemCheckboxes = document.querySelectorAll('.item-checkbox');
        const bulkActions = document.querySelector('.bulk-actions');
        
        selectAllCheckbox.addEventListener('change', function() {
            itemCheckboxes.forEach(function(checkbox) {
                checkbox.checked = selectAllCheckbox.checked;
            });
            toggleBulkActions();
        });
        
        itemCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                const checkedCount = document.querySelectorAll('.item-checkbox:checked').length;
                selectAllCheckbox.checked = checkedCount === itemCheckboxes.length;
                selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < itemCheckboxes.length;
                toggleBulkActions();
            });
        });
        
        function toggleBulkActions() {
            const checkedCount = document.querySelectorAll('.item-checkbox:checked').length;
            if (bulkActions) {
                bulkActions.style.display = checkedCount > 0 ? 'block' : 'none';
            }
        }
    }

    // File upload drag and drop
    const uploadAreas = document.querySelectorAll('.upload-area');
    uploadAreas.forEach(function(area) {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            area.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
        });
        
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            area.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            handleFileUpload(files, area);
        });
    });

    // Search functionality with debounce
    const searchInputs = document.querySelectorAll('.live-search');
    searchInputs.forEach(function(input) {
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performSearch(input.value, input);
            }, 500);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save form
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const form = document.querySelector('form:not(.no-shortcut)');
            if (form) {
                form.submit();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
});

// Utility Functions

function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = createToast(message, type);
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

function createToast(message, type) {
    const toastTypes = {
        success: { bg: 'bg-success', icon: 'fas fa-check-circle' },
        error: { bg: 'bg-danger', icon: 'fas fa-exclamation-circle' },
        warning: { bg: 'bg-warning', icon: 'fas fa-exclamation-triangle' },
        info: { bg: 'bg-info', icon: 'fas fa-info-circle' }
    };
    
    const config = toastTypes[type] || toastTypes.info;
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="toast-header ${config.bg} text-white">
            <i class="${config.icon} me-2"></i>
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    return toast;
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

function showSaveStatus(status) {
    const statusElement = document.querySelector('.save-status');
    if (!statusElement) return;
    
    const statuses = {
        saving: { text: 'Saving...', class: 'text-warning' },
        saved: { text: 'Saved', class: 'text-success' },
        error: { text: 'Error saving', class: 'text-danger' }
    };
    
    const config = statuses[status];
    if (config) {
        statusElement.textContent = config.text;
        statusElement.className = `save-status ${config.class}`;
    }
}

function autoSaveForm(form) {
    const formData = new FormData(form);
    
    fetch(form.action || window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            showSaveStatus('saved');
            setTimeout(() => showSaveStatus(''), 3000);
        } else {
            throw new Error('Save failed');
        }
    })
    .catch(error => {
        showSaveStatus('error');
        console.error('Auto-save error:', error);
    });
}

function handleFileUpload(files, uploadArea) {
    const formData = new FormData();
    
    Array.from(files).forEach(file => {
        formData.append('files[]', file);
    });
    
    // Add CSRF token if available
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    if (csrfToken) {
        formData.append('csrf_token', csrfToken.getAttribute('content'));
    }
    
    const uploadUrl = uploadArea.getAttribute('data-upload-url') || '/admin/upload';
    
    fetch(uploadUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast('Files uploaded successfully', 'success');
            // Trigger custom event for other scripts to handle
            uploadArea.dispatchEvent(new CustomEvent('upload-success', { detail: data }));
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    })
    .catch(error => {
        showToast('Upload failed: ' + error.message, 'error');
        console.error('Upload error:', error);
    });
}

function performSearch(query, input) {
    const searchUrl = input.getAttribute('data-search-url');
    if (!searchUrl) return;
    
    const params = new URLSearchParams({ q: query });
    
    fetch(`${searchUrl}?${params}`)
    .then(response => response.json())
    .then(data => {
        const resultsContainer = document.querySelector(input.getAttribute('data-results-target'));
        if (resultsContainer) {
            resultsContainer.innerHTML = data.html || '';
        }
    })
    .catch(error => {
        console.error('Search error:', error);
    });
}

// Chart helpers
function createSimpleChart(canvasId, type, data, options = {}) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: type !== 'doughnut'
            }
        }
    };
    
    return new Chart(ctx, {
        type: type,
        data: data,
        options: { ...defaultOptions, ...options }
    });
}

// Export functionality
function exportTable(tableSelector, filename = 'export.csv') {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csvContent = Array.from(rows).map(row => {
        const cells = row.querySelectorAll('th, td');
        return Array.from(cells).map(cell => {
            return '"' + cell.textContent.replace(/"/g, '""') + '"';
        }).join(',');
    }).join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Theme toggle (if needed)
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize theme from localStorage
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
}

// Call theme initialization
initializeTheme();

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // Optionally show user-friendly error message
    // showToast('An error occurred. Please try again.', 'error');
});

// AJAX form submission helper
function submitFormAjax(form, options = {}) {
    const formData = new FormData(form);
    const url = form.action || window.location.href;
    
    return fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (options.onSuccess) {
            options.onSuccess(data);
        }
        return data;
    })
    .catch(error => {
        if (options.onError) {
            options.onError(error);
        } else {
            showToast('An error occurred: ' + error.message, 'error');
        }
        throw error;
    });
}

// Utility for formatting numbers
function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Utility for formatting dates
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    };
    
    return new Intl.DateTimeFormat('en-US', { ...defaultOptions, ...options }).format(new Date(date));
}

// Utility for debouncing functions
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

// Utility for throttling functions
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
    };
}
