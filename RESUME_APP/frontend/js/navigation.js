// Navigation functionality
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Trigger dashboard load if navigating to dashboard
        if (sectionId === 'dashboard') {
            setTimeout(() => {
                if (typeof loadDashboard === 'function') {
                    loadDashboard();
                }
            }, 100);
        }
        
        // Auto-load recommendations if navigating to recommendations
        if (sectionId === 'recommendations') {
            setTimeout(() => {
                const listDiv = document.getElementById('recommendationsList');
                if (listDiv && !listDiv.querySelector('.recommendation-card')) {
                    // Only auto-load if list is empty
                    if (listDiv.innerHTML.trim() === '' || listDiv.innerHTML.includes('Click "Get Recommendations"')) {
                        // Don't auto-load, let user click button
                    }
                }
            }, 100);
        }
    }
    
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    const activeLink = document.querySelector(`[onclick="showSection('${sectionId}')"]`) || 
                      document.querySelector(`a[href="#${sectionId}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Initialize navigation
document.addEventListener('DOMContentLoaded', () => {
    // Set up nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            if (href && href.startsWith('#')) {
                showSection(href.substring(1));
            }
        });
    });
    
    // Mobile menu toggle
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
        });
    }
    
    // Show home section by default
    showSection('home');
});

