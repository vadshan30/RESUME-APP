// Resume upload functionality
document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('resumeFile');
    
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
        uploadArea.style.background = 'var(--bg-secondary)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--border-color)';
        uploadArea.style.background = 'var(--bg-primary)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        uploadArea.style.background = 'var(--bg-primary)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
});

async function handleFileUpload(file) {
    // Validate file
    const allowedTypes = ['application/pdf', 'text/plain'];
    if (!allowedTypes.includes(file.type)) {
        alert('Please upload a PDF or TXT file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }
    
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${window.API_BASE_URL || '/api'}/upload-resume`, {
            method: 'POST',
            body: formData
        });

        const text = await response.text();
        let result = null;
        try {
            result = text ? JSON.parse(text) : null;
        } catch (e) {
            result = { raw: text };
        }

        if (!response.ok) {
            throw new Error((result && result.error) ? result.error : `Upload failed (status ${response.status})`);
        }
        
        // Store resume data
        setResumeData(result.text, result.skills.all_skills);
        
        // Display results
        displayUploadResult(result);
        
    } catch (error) {
        alert('Error uploading file: ' + error.message);
        console.error(error);
    } finally {
        hideLoading();
    }
}

function displayUploadResult(result) {
    const resultDiv = document.getElementById('uploadResult');
    const skillsDiv = document.getElementById('resumeSkills');
    
    // Display skills
    let skillsHTML = '<h4>Extracted Skills</h4>';
    
    if (result.skills.technical_skills.length > 0) {
        skillsHTML += '<div><strong>Technical Skills:</strong><div class="skills-display">';
        result.skills.technical_skills.forEach(skill => {
            skillsHTML += `<span class="skill-tag technical">${skill}</span>`;
        });
        skillsHTML += '</div></div>';
    }
    
    if (result.skills.soft_skills.length > 0) {
        skillsHTML += '<div style="margin-top: 1rem;"><strong>Soft Skills:</strong><div class="skills-display">';
        result.skills.soft_skills.forEach(skill => {
            skillsHTML += `<span class="skill-tag soft">${skill}</span>`;
        });
        skillsHTML += '</div></div>';
    }
    
    if (result.skills.certifications.length > 0) {
        skillsHTML += '<div style="margin-top: 1rem;"><strong>Certifications:</strong><div class="skills-display">';
        result.skills.certifications.forEach(skill => {
            skillsHTML += `<span class="skill-tag certification">${skill}</span>`;
        });
        skillsHTML += '</div></div>';
    }
    
    skillsDiv.innerHTML = skillsHTML;
    resultDiv.style.display = 'block';
    
    // Show text preview (optional)
    const textPreview = document.getElementById('resumeText');
    textPreview.textContent = result.text.substring(0, 500) + '...';
    textPreview.style.display = 'block';
}

