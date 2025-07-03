// ========================================================================
// PORTFOLIO PAGE JAVASCRIPT
// Enhanced portfolio display with filtering and modal functionality
// ========================================================================

document.addEventListener('DOMContentLoaded', function() {
    
    let allProjects = [];
    let currentFilter = 'all';
    
    // ========================================================================
    // LOAD PORTFOLIO DATA
    // ========================================================================
    
    async function loadPortfolio() {
        const loadingElement = document.getElementById('portfolio-loading');
        const gridElement = document.getElementById('portfolio-grid');
        const emptyElement = document.getElementById('portfolio-empty');
        
        try {
            const response = await fetch('/api/portfolio');
            const projects = await response.json();
            
            allProjects = projects;
            
            // Hide loading
            loadingElement.style.display = 'none';
            
            if (projects.length === 0) {
                emptyElement.classList.remove('d-none');
                return;
            }
            
            renderProjects(projects);
            setupFilters();
            
        } catch (error) {
            console.error('Error loading portfolio:', error);
            loadingElement.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-exclamation-triangle text-warning fa-2x mb-3"></i>
                    <h5>Unable to load portfolio</h5>
                    <p class="text-muted">Please check your connection and try again.</p>
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-refresh me-2"></i>Retry
                    </button>
                </div>
            `;
        }
    }
    
    // ========================================================================
    // RENDER PROJECTS
    // ========================================================================
    
    function renderProjects(projects) {
        const gridElement = document.getElementById('portfolio-grid');
        const emptyElement = document.getElementById('portfolio-empty');
        
        if (projects.length === 0) {
            gridElement.innerHTML = '';
            emptyElement.classList.remove('d-none');
            return;
        }
        
        emptyElement.classList.add('d-none');
        gridElement.innerHTML = '';
        
        projects.forEach((project, index) => {
            const projectCard = createProjectCard(project, index);
            gridElement.appendChild(projectCard);
        });
        
        // Animate cards in
        animateCardsIn();
    }
    
    // ========================================================================
    // CREATE PROJECT CARD
    // ========================================================================
    
    function createProjectCard(project, index) {
        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6 col-12 mb-4';
        col.setAttribute('data-category', project.category?.toLowerCase().replace(/\s+/g, '-') || 'other');
        
        const tags = Array.isArray(project.tags) ? project.tags : 
                     (typeof project.tags === 'string' ? project.tags.split(',') : []);
        
        const featuredBadge = project.is_featured ? 
            '<span class="badge bg-primary position-absolute top-0 start-0 m-2">Featured</span>' : '';
        
        col.innerHTML = `
            <div class="portfolio-card fade-in" style="animation-delay: ${index * 0.1}s">
                <div class="portfolio-image position-relative">
                    ${featuredBadge}
                    <img src="${project.image_url || '/static/images/placeholder.jpg'}" 
                         alt="${project.title}"
                         loading="lazy"
                         class="w-100">
                    <div class="portfolio-overlay">
                        <div class="text-white text-center">
                            <i class="fas fa-expand-alt fa-2x mb-2"></i>
                            <p class="mb-0">View Details</p>
                        </div>
                    </div>
                </div>
                <div class="portfolio-content">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h4 class="portfolio-title mb-0">${project.title}</h4>
                        ${project.project_url ? `
                            <a href="${project.project_url}" target="_blank" 
                               class="btn btn-sm btn-outline-primary" title="Live Project">
                                <i class="fas fa-external-link-alt"></i>
                            </a>
                        ` : ''}
                    </div>
                    <p class="portfolio-description">${truncateText(project.description || 'Creative design project', 120)}</p>
                    <div class="portfolio-meta mb-3">
                        <small class="text-muted">
                            <i class="fas fa-folder me-1"></i>${project.category || 'Design'}
                        </small>
                        ${project.created_at ? `
                            <small class="text-muted ms-3">
                                <i class="fas fa-calendar me-1"></i>${formatDate(project.created_at)}
                            </small>
                        ` : ''}
                    </div>
                    <div class="portfolio-tags">
                        ${tags.map(tag => `<span class="portfolio-tag">${tag.trim()}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
        
        // Add click handler for modal
        const card = col.querySelector('.portfolio-card');
        card.addEventListener('click', () => openProjectModal(project));
        
        return col;
    }
    
    // ========================================================================
    // FILTERING SYSTEM
    // ========================================================================
    
    function setupFilters() {
        const filterButtons = document.querySelectorAll('[data-filter]');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filter = this.getAttribute('data-filter');
                
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Filter projects
                filterProjects(filter);
                currentFilter = filter;
            });
        });
    }
    
    function filterProjects(filter) {
        const filteredProjects = filter === 'all' ? 
            allProjects : 
            allProjects.filter(project => {
                const category = project.category?.toLowerCase().replace(/\s+/g, '-') || 'other';
                return category === filter;
            });
        
        renderProjects(filteredProjects);
    }
    
    // ========================================================================
    // PROJECT MODAL
    // ========================================================================
    
    function openProjectModal(project) {
        const modal = document.getElementById('portfolioModal');
        const modalContent = document.getElementById('modal-content');
        
        const tags = Array.isArray(project.tags) ? project.tags : 
                     (typeof project.tags === 'string' ? project.tags.split(',') : []);
        
        modalContent.innerHTML = `
            <div class="row g-0">
                <div class="col-md-6">
                    <img src="${project.image_url || '/static/images/placeholder.jpg'}" 
                         alt="${project.title}" 
                         class="img-fluid rounded-start w-100 h-100" 
                         style="object-fit: cover; min-height: 300px;">
                </div>
                <div class="col-md-6">
                    <div class="p-4">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <h3 class="mb-0">${project.title}</h3>
                            ${project.is_featured ? '<span class="badge bg-primary">Featured</span>' : ''}
                        </div>
                        
                        <div class="project-meta mb-3">
                            <small class="text-muted">
                                <i class="fas fa-folder me-1"></i>${project.category || 'Design'}
                            </small>
                            ${project.created_at ? `
                                <small class="text-muted ms-3">
                                    <i class="fas fa-calendar me-1"></i>${formatDate(project.created_at)}
                                </small>
                            ` : ''}
                        </div>
                        
                        <p class="text-muted mb-4">${project.description || 'Creative design project showcasing innovative solutions and modern design principles.'}</p>
                        
                        ${tags.length > 0 ? `
                            <div class="mb-4">
                                <h6 class="mb-2">Technologies & Skills:</h6>
                                <div class="d-flex flex-wrap gap-2">
                                    ${tags.map(tag => `<span class="badge bg-light text-dark">${tag.trim()}</span>`).join('')}
                                </div>
                            </div>
                        ` : ''}
                        
                        <div class="project-actions">
                            ${project.project_url ? `
                                <a href="${project.project_url}" target="_blank" class="btn btn-primary me-2">
                                    <i class="fas fa-external-link-alt me-2"></i>View Live Project
                                </a>
                            ` : ''}
                            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times me-2"></i>Close
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Show modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
    }
    
    // ========================================================================
    // ANIMATIONS
    // ========================================================================
    
    function animateCardsIn() {
        const cards = document.querySelectorAll('.portfolio-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        cards.forEach(card => {
            observer.observe(card);
        });
    }
    
    // ========================================================================
    // SEARCH FUNCTIONALITY
    // ========================================================================
    
    function setupSearch() {
        const searchInput = document.getElementById('portfolio-search');
        if (!searchInput) return;
        
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase().trim();
            
            searchTimeout = setTimeout(() => {
                const filteredProjects = allProjects.filter(project => {
                    const searchText = `${project.title} ${project.description} ${project.tags || ''}`.toLowerCase();
                    const matchesSearch = query === '' || searchText.includes(query);
                    const matchesFilter = currentFilter === 'all' || 
                        (project.category?.toLowerCase().replace(/\s+/g, '-') || 'other') === currentFilter;
                    
                    return matchesSearch && matchesFilter;
                });
                
                renderProjects(filteredProjects);
            }, 300);
        });
    }
    
    // ========================================================================
    // RESPONSIVE GRID ADJUSTMENTS
    // ========================================================================
    
    function adjustGridForDevice() {
        const deviceType = getDeviceType();
        const cards = document.querySelectorAll('.portfolio-card');
        
        if (deviceType === 'mobile') {
            // Optimize for mobile performance
            cards.forEach(card => {
                const overlay = card.querySelector('.portfolio-overlay');
                if (overlay) {
                    overlay.style.opacity = '0.8'; // Always slightly visible on mobile
                }
            });
        }
    }
    
    function getDeviceType() {
        const width = window.innerWidth;
        if (width <= 768) return 'mobile';
        if (width <= 1024) return 'tablet';
        return 'desktop';
    }
    
    // ========================================================================
    // UTILITY FUNCTIONS
    // ========================================================================
    
    function truncateText(text, maxLength = 100) {
        if (!text || text.length <= maxLength) return text;
        return text.substring(0, maxLength).trim() + '...';
    }
    
    function formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long'
        });
    }
    
    // ========================================================================
    // KEYBOARD NAVIGATION
    // ========================================================================
    
    function setupKeyboardNavigation() {
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const modal = bootstrap.Modal.getInstance(document.getElementById('portfolioModal'));
                if (modal) modal.hide();
            }
        });
    }
    
    // ========================================================================
    // INITIALIZATION
    // ========================================================================
    
    // Load portfolio data
    loadPortfolio();
    
    // Setup additional functionality
    setupSearch();
    setupKeyboardNavigation();
    
    // Handle resize events
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(adjustGridForDevice, 250);
    });
    
    // Initial device adjustment
    adjustGridForDevice();
});