// Dashboard and analytics functionality
let skillsChart = null;
let atsTrendChart = null;
let jobMatchChart = null;

async function loadDashboard() {
    const resumeData = getResumeData();
    
    // Show loading state
    const strengthEl = document.getElementById('strengthScore');
    const totalEl = document.getElementById('totalSkills');
    const jobsMatchedEl = document.getElementById('jobsMatched');
    const missingSkillsEl = document.getElementById('missingSkillsCount');
    const readinessEl = document.getElementById('careerReadiness');
    
    [strengthEl, totalEl, jobsMatchedEl, missingSkillsEl, readinessEl].forEach(el => {
        if (el) el.textContent = '...';
    });
    
    showLoading();
    
    try {
        let result;
        try {
            result = await apiCall('/analytics', 'POST', {
                resume_text: resumeData.text || '',
                resume_skills: resumeData.skills || [],
                match_history: [] // could pass stored matches here if implemented
            });
        } catch (postError) {
            console.log('POST failed, trying GET:', postError.message);
            result = await apiCall('/analytics', 'GET');
        }
        
        console.log('Dashboard API result:', result);
        
        if (result && result.analytics) {
            displayDashboard(result.analytics);
        } else {
            throw new Error('Invalid response from server');
        }
        
    } catch (error) {
        console.error('Dashboard error:', error);
        displayEmptyDashboard();
    } finally {
        hideLoading();
    }
}

function displayEmptyDashboard() {
    // Show placeholder when no data
    const elements = {
        strengthScore: '0',
        totalSkills: '0',
        jobsMatched: '0',
        missingSkillsCount: '0',
        careerReadiness: '0%'
    };
    
    for (const [id, val] of Object.entries(elements)) {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
    }
    
    renderCharts(null);
}

function displayDashboard(analytics) {
    if (!analytics || analytics.empty) {
        displayEmptyDashboard();
        return;
    }
    
    // Update stats cards
    const strengthEl = document.getElementById('strengthScore');
    const totalEl = document.getElementById('totalSkills');
    const jobsMatchedEl = document.getElementById('jobsMatched');
    const missingSkillsEl = document.getElementById('missingSkillsCount');
    const readinessEl = document.getElementById('careerReadiness');
    
    if (strengthEl) strengthEl.textContent = analytics.strength_score || 0;
    if (totalEl) totalEl.textContent = analytics.skill_count || 0;
    if (jobsMatchedEl) jobsMatchedEl.textContent = analytics.jobs_matched || 0;
    if (missingSkillsEl) missingSkillsEl.textContent = analytics.missing_skills_count || 0;
    if (readinessEl) readinessEl.textContent = (analytics.career_readiness || 0) + '%';
    
    // Update charts
    renderCharts(analytics);
}

function renderCharts(analytics) {
    const defaultDistribution = { technical: 1, soft: 1, other: 1 };
    const distribution = analytics && analytics.skill_distribution ? analytics.skill_distribution : defaultDistribution;
    
    // 1. Skill Distribution (Doughnut)
    const ctxSkills = document.getElementById('skillsChart');
    if (ctxSkills) {
        if (skillsChart) skillsChart.destroy();
        skillsChart = new Chart(ctxSkills.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Technical', 'Soft', 'Other'],
                datasets: [{
                    data: [distribution.technical || 0, distribution.soft || 0, distribution.other || 0],
                    backgroundColor: ['#4f46e5', '#10b981', '#f59e0b'],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
        });
    }

    // 2. ATS Trend (Line)
    const ctxAts = document.getElementById('atsTrendChart');
    if (ctxAts) {
        if (atsTrendChart) atsTrendChart.destroy();
        const atsData = analytics && analytics.ats_trend ? analytics.ats_trend : [0, 0, 0, 0, 0];
        atsTrendChart = new Chart(ctxAts.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'],
                datasets: [{
                    label: 'ATS Score',
                    data: atsData,
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { min: 0, max: 100 } },
                plugins: { legend: { display: false } }
            }
        });
    }

    // 3. Job Match Trend (Bar)
    const ctxMatch = document.getElementById('jobMatchChart');
    if (ctxMatch) {
        if (jobMatchChart) jobMatchChart.destroy();
        const matchData = analytics && analytics.job_match_trend ? analytics.job_match_trend : [0, 0, 0, 0, 0];
        jobMatchChart = new Chart(ctxMatch.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Role A', 'Role B', 'Role C', 'Role D', 'Target Role'],
                datasets: [{
                    label: 'Match Percentage',
                    data: matchData,
                    backgroundColor: '#10b981',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { min: 0, max: 100 } },
                plugins: { legend: { display: false } }
            }
        });
    }
}

// Load dashboard when section is shown
document.addEventListener('DOMContentLoaded', () => {
    // Check initial active state
    const dashboardSection = document.getElementById('dashboard');
    if (dashboardSection && dashboardSection.classList.contains('active')) {
        loadDashboard();
    }
    
    // Monitor class changes
    const observer = new MutationObserver(() => {
        if (dashboardSection && dashboardSection.classList.contains('active')) {
            setTimeout(() => { loadDashboard(); }, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true, subtree: true, attributes: true, attributeFilter: ['class']
    });
    
    // Listen for navigation clicks
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.getAttribute('href') === '#dashboard') {
                setTimeout(() => { loadDashboard(); }, 200);
            }
        });
    });
});
