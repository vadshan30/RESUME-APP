// Career path analysis functionality
async function analyzeCareerPath() {
    const resumeData = getResumeData();
    const targetRole = document.getElementById('targetRole').value;
    
    if (!resumeData.text && resumeData.skills.length === 0) {
        alert('Please upload a resume first');
        showSection('upload');
        return;
    }
    
    showLoading();
    
    try {
        const result = await apiCall('/career-path', 'POST', {
            resume_text: resumeData.text,
            resume_skills: resumeData.skills,
            target_role: targetRole || null
        });
        
        displayCareerAnalysis(result.analysis);
        
    } catch (error) {
        alert('Error analyzing career path: ' + error.message);
        console.error(error);
    } finally {
        hideLoading();
    }
}

function displayCareerAnalysis(analysis) {
    const analysisDiv = document.getElementById('careerAnalysis');
    
    let html = '';
    
    // Current skills
    html += `<div class="career-section"><h3>Current Skills</h3><p>You have ${analysis.current_skills_count} skills identified.</p></div>`;
    
    // Target role analysis
    if (analysis.target_role_analysis) {
        const target = analysis.target_role_analysis;
        html += `
            <div class="career-section">
                <h3>Target Role: ${target.role}</h3>
                <div class="recommendation-score">${target.match_percentage}% Match</div>
                ${target.missing_skills.length > 0 ? `
                    <div style="margin-top: 1rem;">
                        <strong>Missing Skills:</strong>
                        <div class="skills-display" style="margin-top: 0.5rem;">
                            ${target.missing_skills.map(skill => `<span class="skill-tag" style="background: var(--danger-color);">${skill}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    // Recommended roles
    if (analysis.recommended_roles && analysis.recommended_roles.length > 0) {
        html += '<div class="career-section"><h3>Recommended Roles</h3>';
        analysis.recommended_roles.forEach(role => {
            html += `
                <div class="recommendation-card" style="margin-bottom: 1rem;">
                    <h4>${role.role}</h4>
                    <p>${role.industry} - ${role.level}</p>
                    <div class="recommendation-score">${role.match_percentage}% Match</div>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Learning path
    if (analysis.learning_path && analysis.learning_path.length > 0) {
        html += '<div class="career-section"><h3>Learning Path</h3>';
        analysis.learning_path.forEach(item => {
            html += `
                <div class="suggestion-card">
                    <h4>${item.skill}</h4>
                    <p><strong>Priority:</strong> ${item.priority}</p>
                    <ul>
                        ${item.suggested_resources.map(resource => `<li>${resource}</li>`).join('')}
                    </ul>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Next steps
    if (analysis.next_steps && analysis.next_steps.length > 0) {
        html += '<div class="career-section"><h3>Next Steps</h3><ul>';
        analysis.next_steps.forEach(step => {
            html += `<li>${step}</li>`;
        });
        html += '</ul></div>';
    }
    
    analysisDiv.innerHTML = html;
}

