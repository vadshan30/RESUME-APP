// Job recommendations functionality
async function getRecommendations() {
    const resumeData = getResumeData();
    const hasResume = (resumeData.text && resumeData.text.trim()) || (resumeData.skills && resumeData.skills.length > 0);
    
    // Show info but proceed automatically (no blocking confirm)
    if (!hasResume) {
        // Just show a note, don't block
        console.log('No resume uploaded - showing general recommendations');
    }
    
    showLoading();
    
    const listDiv = document.getElementById('recommendationsList');
    if (listDiv) {
        listDiv.innerHTML = '<p style="text-align: center; padding: 1rem;">Loading recommendations...</p>';
    }
    
    try {
        const result = await apiCall('/recommendations', 'POST', {
            resume_text: resumeData.text || '',
            resume_skills: resumeData.skills || [],
            limit: 10  // Get more to ensure we have results
        });
        
        console.log('Recommendations API result:', result);
        
        // Handle response - check for recommendations array
        if (result) {
            const recommendations = result.recommendations || [];
            const hasResumeFlag = result.has_resume !== undefined ? result.has_resume : hasResume;
            
            console.log(`Found ${recommendations.length} recommendations`);
            
            if (recommendations.length > 0) {
                displayRecommendations(recommendations, hasResumeFlag);
            } else {
                // No recommendations - show helpful message
                displayRecommendations([], hasResumeFlag);
            }
        } else {
            throw new Error('No response from server');
        }
        
    } catch (error) {
        console.error('Recommendations error:', error);
        // Show error but still try to show something
        if (listDiv) {
            listDiv.innerHTML = `
                <div class="error-message" style="padding: 2rem; text-align: center; background: var(--bg-primary); border-radius: 8px; box-shadow: var(--shadow);">
                    <p style="color: var(--danger-color); margin-bottom: 1rem;">⚠️ Error loading recommendations</p>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1.5rem;">
                        ${error.message || 'Unable to connect to server. Please check if the backend is running.'}
                    </p>
                    <button class="btn btn-primary" onclick="getRecommendations()">Retry</button>
                    <p style="margin-top: 1rem; font-size: 0.875rem; color: var(--text-secondary);">
                        Make sure the Flask server is running on http://localhost:5000
                    </p>
                </div>
            `;
        }
    } finally {
        hideLoading();
    }
}

function displayRecommendations(recommendations, hasResume = true) {
    const listDiv = document.getElementById('recommendationsList');
    
    if (!listDiv) {
        console.error('Recommendations list container not found');
        return;
    }
    
    // Always show something - even if empty, show helpful message
    if (!recommendations || recommendations.length === 0) {
        listDiv.innerHTML = `
            <div style="padding: 2rem; text-align: center; background: var(--bg-primary); border-radius: 8px; box-shadow: var(--shadow);">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📋 No recommendations available at the moment.</p>
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                    ${!hasResume ? 'Upload a resume to get personalized job recommendations.' : 'Try adjusting your filters or check back later.'}
                </p>
                ${!hasResume ? `
                    <button class="btn btn-primary" onclick="showSection('upload')">Upload Resume</button>
                ` : `
                    <button class="btn btn-primary" onclick="getRecommendations()">Refresh</button>
                `}
            </div>
        `;
        return;
    }
    
    let html = '';
    
    // Show info message if no resume
    if (!hasResume) {
        html += `
            <div class="info-banner" style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 1rem; margin-bottom: 1.5rem; border-radius: 6px;">
                <p style="margin: 0;"><strong>💡 Tip:</strong> Upload a resume for personalized matching and better recommendations.</p>
            </div>
        `;
    }
    
    recommendations.forEach(rec => {
        html += `
            <div class="recommendation-card">
                <h3>${rec.role}</h3>
                <p><strong>Industry:</strong> ${rec.industry}</p>
                <p><strong>Level:</strong> ${rec.level}</p>
                <div class="recommendation-score" style="color: ${rec.match_percentage >= 50 ? '#10b981' : rec.match_percentage >= 25 ? '#f59e0b' : '#ef4444'}">
                    ${rec.match_percentage.toFixed(1)}% Match
                </div>
                ${rec.note ? `<p style="font-size: 0.875rem; color: var(--text-secondary); font-style: italic;">${rec.note}</p>` : ''}
                <p>${rec.description}</p>
                <div style="margin-top: 1rem;">
                    <strong>Required Skills:</strong>
                    <div class="skills-display" style="margin-top: 0.5rem;">
                        ${rec.required_skills.slice(0, 8).map(skill => `<span class="skill-tag technical">${skill}</span>`).join('')}
                        ${rec.required_skills.length > 8 ? `<span class="skill-tag" style="background: var(--text-secondary);">+${rec.required_skills.length - 8} more</span>` : ''}
                    </div>
                </div>
                ${rec.matching_skills && rec.matching_skills.length > 0 ? `
                    <div style="margin-top: 1rem;">
                        <strong>Your Matching Skills:</strong>
                        <div class="skills-display" style="margin-top: 0.5rem;">
                            ${rec.matching_skills.map(skill => `<span class="skill-tag" style="background: var(--secondary-color);">${skill}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
                ${rec.missing_skills && rec.missing_skills.length > 0 ? `
                    <div style="margin-top: 1rem;">
                        <strong>Skills to Develop:</strong>
                        <div class="skills-display" style="margin-top: 0.5rem;">
                            ${rec.missing_skills.slice(0, 5).map(skill => `<span class="skill-tag" style="background: var(--danger-color);">${skill}</span>`).join('')}
                            ${rec.missing_skills.length > 5 ? `<span class="skill-tag" style="background: var(--text-secondary);">+${rec.missing_skills.length - 5} more</span>` : ''}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    listDiv.innerHTML = html;
}

