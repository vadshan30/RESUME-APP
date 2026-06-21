// Interview preparation functionality
async function generateInterviewQuestions() {
    const topic = document.getElementById('interviewTopic').value;
    const difficulty = document.getElementById('interviewDifficulty').value;
    const jobDescription = document.getElementById('interviewJobDesc').value;
    
    if (!topic.trim() && !jobDescription.trim()) {
        alert('Please enter a Topic or a Job Description');
        return;
    }
    
    showLoading();
    
    try {
        const result = await apiCall('/interview-questions', 'POST', {
            topic: topic,
            difficulty: difficulty,
            job_description: jobDescription,
            num_questions: 5
        });
        
        document.getElementById('interviewResults').style.display = 'block';
        displayInterviewQuestions(result.questions);
        
        // Show the technical tab by default if there are technical questions, otherwise HR
        switchInterviewTab('technical');
        
    } catch (error) {
        alert('Error generating questions: ' + error.message);
        console.error(error);
    } finally {
        hideLoading();
    }
}

function switchInterviewTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab content and set active class to corresponding button
    document.getElementById(`tab-${tabId}`).style.display = 'block';
    event.currentTarget.classList.add('active');
}

function toggleAnswer(btn) {
    const answerDiv = btn.nextElementSibling;
    if (answerDiv.classList.contains('show')) {
        answerDiv.classList.remove('show');
        btn.textContent = 'Show Answer';
    } else {
        answerDiv.classList.add('show');
        btn.textContent = 'Hide Answer';
    }
}

function displayInterviewQuestions(questions) {
    const renderCards = (qList) => {
        if (!qList || qList.length === 0) {
            return '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No questions found for this criteria.</p>';
        }
        
        let html = '';
        qList.forEach((q, idx) => {
            const badgeClass = q.difficulty ? `badge-${q.difficulty.toLowerCase()}` : 'badge-intermediate';
            const diffText = q.difficulty || 'Intermediate';
            
            html += `
                <div class="question-card">
                    <span class="badge ${badgeClass}">${diffText}</span>
                    <span class="badge" style="background: #e0e7ff; color: #3730a3; margin-left: 0.5rem;">${q.category || 'General'}</span>
                    <h4>Q${idx + 1}: ${q.question}</h4>
                    <button class="btn-toggle-answer" onclick="toggleAnswer(this)">Show Answer</button>
                    <div class="answer">
                        <strong>Answer Guidance:</strong>
                        <p style="margin-top: 0.5rem;">${q.answer}</p>
                    </div>
                </div>
            `;
        });
        return html;
    };
    
    // Technical questions
    document.getElementById('tab-technical').innerHTML = renderCards(questions.technical);
    
    // HR questions
    document.getElementById('tab-hr').innerHTML = renderCards(questions.hr);
    
    // Behavioral questions (combine situational and behavioral for simplicity or show just behavioral)
    const combinedBehavioral = [...(questions.behavioral || []), ...(questions.situational || [])];
    document.getElementById('tab-behavioral').innerHTML = renderCards(combinedBehavioral);
}
