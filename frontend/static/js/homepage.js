// ========================================================================
// HOMEPAGE SPECIFIC JAVASCRIPT
// Portfolio and Skills API integration
// ========================================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================================================
    // API ENDPOINTS
    // ========================================================================
    
    const API = {
        portfolio: '/api/portfolio',
        skills: '/api/skills',
        contact: '/api/contact'
    };
    
    // ========================================================================
    // LOAD PORTFOLIO DATA
    // ========================================================================
    
    async function loadPortfolio() {
        try {
            const response = await fetch(API.portfolio);
            const projects = await response.json();
            
            const container = document.getElementById('portfolio-container');
            if (!container) return;
            
            // Clear loading state
            container.innerHTML = '';
            
            // Show only featured projects on homepage (max 3)
            const featuredProjects = projects.filter(p => p.is_featured).slice(0, 3);
            
            if (featuredProjects.length === 0) {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-muted">No featured projects available yet.</p>
                    </div>
                `;
                return;
            }
            
            featuredProjects.forEach((project, index) => {
                const projectCard = createPortfolioCard(project, index);
                container.appendChild(projectCard);
            });
            
            // Animate cards in sequence
            animateCardsIn('.portfolio-card');
            
        } catch (error) {
            console.error('Error loading portfolio:', error);
            const container = document.getElementById('portfolio-container');
            if (container) {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-danger">Unable to load portfolio. Please try again later.</p>
                    </div>
                `;
            }
        }
    }
    
    // ========================================================================
    // CREATE PORTFOLIO CARD
    // ========================================================================
    
    function createPortfolioCard(project, index) {
        const col = document.createElement('div');
        col.className = getResponsiveColumnClass();
        
        const tags = Array.isArray(project.tags) ? project.tags : 
                     (typeof project.tags === 'string' ? project.tags.split(',') : []);
        
        col.innerHTML = `
            <div class="portfolio-card fade-in" style="animation-delay: ${index * 0.2}s">
                <div class="portfolio-image">
                    <img src="${project.image_url || '/static/images/placeholder.jpg'}" 
                         alt="${project.title}"
                         loading="lazy">
                    <div class="portfolio-overlay">
                        <div class="text-white text-center">
                            <i class="fas fa-eye fa-2x mb-2"></i>
                            <p>View Project</p>
                        </div>
                    </div>
                </div>
                <div class="portfolio-content">
                    <h4 class="portfolio-title">${project.title}</h4>
                    <p class="portfolio-description">${project.description || 'Creative design project'}</p>
                    <div class="portfolio-tags">
                        ${tags.map(tag => `<span class="portfolio-tag">${tag.trim()}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
        
        return col;
    }
    
    // ========================================================================
    // LOAD SKILLS DATA
    // ========================================================================
    
    async function loadSkills() {
        try {
            const response = await fetch(API.skills);
            const skillsData = await response.json();
            
            const container = document.getElementById('skills-container');
            if (!container) return;
            
            container.innerHTML = '';
            
            if (Object.keys(skillsData).length === 0) {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-muted">No skills data available yet.</p>
                    </div>
                `;
                return;
            }
            
            let cardIndex = 0;
            
            // Create skill cards for each category
            Object.entries(skillsData).forEach(([category, skills]) => {
                const categoryTitle = document.createElement('div');
                categoryTitle.className = 'col-12 mb-3';
                categoryTitle.innerHTML = `<h4 class="text-center text-primary">${category}</h4>`;
                container.appendChild(categoryTitle);
                
                skills.forEach(skill => {
                    const skillCard = createSkillCard(skill, cardIndex);
                    container.appendChild(skillCard);
                    cardIndex++;
                });
            });
            
            // Animate skill bars when visible
            animateSkillBars();
            
        } catch (error) {
            console.error('Error loading skills:', error);
            const container = document.getElementById('skills-container');
            if (container) {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-danger">Unable to load skills. Please try again later.</p>
                    </div>
                `;
            }
        }
    }
    
    // ========================================================================
    // CREATE SKILL CARD
    // ========================================================================
    
    function createSkillCard(skill, index) {
        const col = document.createElement('div');
        col.className = getSkillColumnClass();
        
        col.innerHTML = `
            <div class="skill-card fade-in" style="animation-delay: ${index * 0.1}s">
                <div class="skill-icon" style="background: ${skill.color || 'var(--gradient-primary)'}">
                    <i class="${skill.icon_class || 'fas fa-tools'}"></i>
                </div>
                <h5 class="skill-name">${skill.name}</h5>
                <div class="skill-proficiency">
                    <div class="skill-progress" 
                         data-percentage="${skill.proficiency || 80}"></div>
                </div>
                <small class="text-muted">${skill.proficiency || 80}% Proficiency</small>
            </div>
        `;
        
        return col;
    }
    
    // ========================================================================
    // RESPONSIVE COLUMN CLASSES
    // ========================================================================
    
    function getResponsiveColumnClass() {
        // Portfolio: 1 column on mobile, 2 on tablet, 3 on desktop
        return 'col-12 col-md-6 col-lg-4 mb-4';
    }
    
    function getSkillColumnClass() {
        // Skills: 1 column on mobile, 2 on tablet, 3 on desktop, 4 on large screens
        return 'col-12 col-sm-6 col-md-4 col-lg-3 mb-3';
    }
    
    // ========================================================================
    // ANIMATIONS
    // ========================================================================
    
    function animateCardsIn(selector) {
        const cards = document.querySelectorAll(selector);
        
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
    
    function animateSkillBars() {
        const skillBars = document.querySelectorAll('.skill-progress');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const percentage = progressBar.getAttribute('data-percentage');
                    
                    setTimeout(() => {
                        progressBar.style.width = percentage + '%';
                    }, 300);
                    
                    observer.unobserve(progressBar);
                }
            });
        }, {
            threshold: 0.1
        });
        
        skillBars.forEach(bar => {
            observer.observe(bar);
        });
    }
    
    // ========================================================================
    // RESPONSIVE BEHAVIOR
    // ========================================================================
    
    function handleResize() {
        // Refresh layout if needed
        const deviceType = getDeviceType();
        
        // Adjust floating elements for mobile
        const floatingElements = document.querySelectorAll('.floating-element');
        
        if (deviceType === 'mobile') {
            floatingElements.forEach(el => {
                el.style.display = 'none'; // Hide on mobile for performance
            });
        } else {
            floatingElements.forEach(el => {
                el.style.display = 'block';
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
    // ERROR HANDLING
    // ========================================================================
    
    function showError(container, message) {
        if (!container) return;
        
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-warning text-center" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${message}
                    <br>
                    <button class="btn btn-sm btn-outline-warning mt-2" onclick="location.reload()">
                        <i class="fas fa-refresh me-1"></i>Try Again
                    </button>
                </div>
            </div>
        `;
    }
    
    // ========================================================================
    // LOADING STATES
    // ========================================================================
    
    function showLoadingState(container, itemCount = 3) {
        if (!container) return;
        
        let loadingHTML = '';
        for (let i = 0; i < itemCount; i++) {
            loadingHTML += `
                <div class="col-12 col-md-6 col-lg-4 mb-4">
                    <div class="card">
                        <div class="card-body">
                            <div class="placeholder-glow">
                                <div class="placeholder col-6 mb-2"></div>
                                <div class="placeholder col-4"></div>
                                <div class="placeholder col-8"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
        container.innerHTML = loadingHTML;
    }
    
    // ========================================================================
    // INITIALIZATION
    // ========================================================================
    
    // Show loading states initially
    const portfolioContainer = document.getElementById('portfolio-container');
    const skillsContainer = document.getElementById('skills-container');
    
    if (portfolioContainer) {
        showLoadingState(portfolioContainer, 3);
    }
    
    if (skillsContainer) {
        showLoadingState(skillsContainer, 6);
    }
    
    // Load data
    loadPortfolio();
    loadSkills();
    
    // Handle resize events
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(handleResize, 250);
    });
    
    // Initial resize check
    handleResize();
});

// ========================================================================
// UTILITY FUNCTIONS
// ========================================================================

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long'
    });
}

function truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength).trim() + '...';
}