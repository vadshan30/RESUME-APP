// Cover letter generation functionality
async function generateCoverLetter() {
    const jobDescription = document.getElementById('coverLetterJobDesc').value;
    const name = document.getElementById('applicantName').value || 'Your Name';
    const tone = document.getElementById('coverLetterTone').value;
    
    if (!jobDescription.trim()) {
        alert('Please enter a job description');
        return;
    }
    
    const resumeData = getResumeData();
    
    if (!resumeData.text) {
        alert('Please upload a resume first');
        showSection('upload');
        return;
    }
    
    showLoading();
    
    try {
        const result = await apiCall('/generate-cover-letter', 'POST', {
            resume_text: resumeData.text,
            job_description: jobDescription,
            tone: tone,
            name: name
        });
        
        displayCoverLetter(result.cover_letter);
        
    } catch (error) {
        alert('Error generating cover letter: ' + error.message);
        console.error(error);
    } finally {
        hideLoading();
    }
}

function displayCoverLetter(coverLetter) {
    const resultDiv = document.getElementById('coverLetterResult');
    resultDiv.textContent = coverLetter;
    resultDiv.style.display = 'block';
    
    // Add download button
    const downloadBtn = document.createElement('button');
    downloadBtn.className = 'btn btn-primary';
    downloadBtn.textContent = 'Download as Text';
    downloadBtn.style.marginTop = '1rem';
    downloadBtn.onclick = () => {
        const blob = new Blob([coverLetter], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'cover_letter.txt';
        a.click();
        URL.revokeObjectURL(url);
    };
    
    if (!resultDiv.querySelector('button')) {
        resultDiv.appendChild(downloadBtn);
    }
}

