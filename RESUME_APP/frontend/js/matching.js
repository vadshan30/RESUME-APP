// Job matching functionality
async function matchResume() {
    const jobDescription = document.getElementById('jobDescription').value;
    
    if (!jobDescription.trim()) {
        alert('Please enter a job description');
        return;
    }
    
    const resumeData = getResumeData();
    const hasResume = resumeData.text || resumeData.skills.length > 0;
    
    // Warn but allow proceeding without resume
    if (!hasResume) {
        const proceed = confirm('No resume uploaded. Matching will be based on job description only. Upload a resume for better results. Continue?');
        if (!proceed) {
            showSection('upload');
            return;
        }
    }
    
    showLoading();
    
    try {
        const result = await apiCall('/match', 'POST', {
            resume_text: resumeData.text || '',
            resume_skills: resumeData.skills || [],
            job_description: jobDescription
        });
        
        displayMatchResult(result, hasResume);
        
    } catch (error) {
        console.error('Matching error:', error);
        // Show error in UI instead of alert
        const matchResult = document.getElementById('matchResult');
        if (matchResult) {
            matchResult.style.display = 'block';
            matchResult.innerHTML = `
                <div style="padding: 2rem; text-align: center; color: var(--danger-color);">
                    <p>⚠️ Error matching resume: ${error.message || 'Unknown error'}</p>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); margin-top: 0.5rem;">
                        Please try again or upload a resume for better results.
                    </p>
                </div>
            `;
        }
    } finally {
        hideLoading();
    }
}

function displayMatchResult(result, hasResume = true) {
    const matchResult = result.match_result;
    const resultDiv = document.getElementById('matchResult');
    
    // Show warning if no resume
    let warningHtml = '';
    if (!hasResume) {
        warningHtml = `
            <div class="info-banner" style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 1rem; margin-bottom: 1.5rem; border-radius: 6px;">
                <p style="margin: 0;"><strong>💡 Note:</strong> Upload a resume for more accurate matching and skill analysis.</p>
            </div>
        `;
    }
    
    // Display match percentage
    const percentageDiv = document.getElementById('matchPercentage');
    percentageDiv.textContent = `${matchResult.match_percentage.toFixed(1)}%`;
    
    // Update circle color based on percentage
    if (matchResult.match_percentage >= 70) {
        percentageDiv.style.background = 'linear-gradient(135deg, #10b981, #059669)';
    } else if (matchResult.match_percentage >= 50) {
        percentageDiv.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
    } else {
        percentageDiv.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
    }
    
    // Display matching skills
    const matchingDiv = document.getElementById('matchingSkills');
    matchingDiv.innerHTML = matchResult.matching_skills.length > 0
        ? matchResult.matching_skills.map(skill => `<span class="skill-tag technical">${skill}</span>`).join('')
        : '<p>No matching skills found</p>';
    
    // Display missing skills
    const missingDiv = document.getElementById('missingSkills');
    missingDiv.innerHTML = matchResult.missing_skills.length > 0
        ? matchResult.missing_skills.map(skill => `<span class="skill-tag" style="background: var(--danger-color);">${skill}</span>`).join('')
        : '<p>No missing skills! Great job!</p>';
    
    // Display extra skills
    const extraDiv = document.getElementById('extraSkills');
    extraDiv.innerHTML = matchResult.extra_skills.length > 0
        ? matchResult.extra_skills.map(skill => `<span class="skill-tag" style="background: var(--warning-color);">${skill}</span>`).join('')
        : '<p>No extra skills</p>';
    
    // Display suggestions
    const suggestionsDiv = document.getElementById('suggestions');
    let suggestionsHTML = '<h3>Improvement Suggestions</h3>';
    
    if (result.suggestions && result.suggestions.length > 0) {
        result.suggestions.forEach(suggestion => {
            suggestionsHTML += `
                <div class="suggestion-card">
                    <h4>${suggestion.title}</h4>
                    <p>${suggestion.description}</p>
                    ${suggestion.action_items ? `
                        <ul>
                            ${suggestion.action_items.map(item => `<li>${item}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        });
    } else {
        suggestionsHTML += '<p style="color: var(--text-secondary);">No specific suggestions at this time.</p>';
    }
    
    suggestionsDiv.innerHTML = suggestionsHTML;
    
    // Insert warning at the top if exists
    if (warningHtml) {
        resultDiv.insertAdjacentHTML('afterbegin', warningHtml);
    }
    
    resultDiv.style.display = 'block';
    
    // Scroll to results
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

