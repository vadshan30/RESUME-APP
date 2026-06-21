// API Configuration - use relative base to avoid CORS issues when served from same host
window.API_BASE_URL = '/api';

// Utility function for API calls
async function apiCall(endpoint, method = 'GET', data = null, rawBody = false) {
    const base = window.API_BASE_URL || '/api';
    const url = `${base}${endpoint}`;

    const options = {
        method: method,
        headers: {}
    };

    if (data && method !== 'GET') {
        if (rawBody) {
            // Caller will provide FormData or other body already serialized
            options.body = data;
        } else {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        }
    }

    try {
        const response = await fetch(url, options);

        // Try to parse JSON safely
        const text = await response.text();
        let result = null;
        try {
            result = text ? JSON.parse(text) : null;
        } catch (e) {
            result = { raw: text };
        }

        if (!response.ok) {
            const message = (result && result.error) ? result.error : `HTTP ${response.status}`;
            const err = new Error(message);
            err.status = response.status;
            err.body = result;
            throw err;
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Show/hide loading overlay
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
    // Also ensure it's hidden after a timeout (safety net)
    setTimeout(() => {
        if (overlay) {
            overlay.style.display = 'none';
        }
    }, 5000); // Hide after 5 seconds max
}

// Store resume data in session
let resumeData = {
    text: '',
    skills: []
};

function setResumeData(text, skills) {
    resumeData.text = text;
    resumeData.skills = skills;
    // Update UI for buttons that require a resume
    try {
        updateFeatureButtonsState();
    } catch (e) {
        // ignore if function not yet available
    }
}

function getResumeData() {
    return resumeData;
}

function isResumePresent() {
    return (resumeData.text && resumeData.text.trim()) || (resumeData.skills && resumeData.skills.length > 0);
}

// Enable/disable homepage feature buttons that require a resume.
function updateFeatureButtonsState() {
    const requires = document.querySelectorAll('[data-requires-resume]');
    const present = isResumePresent();
    requires.forEach(el => {
        if (el.tagName === 'BUTTON' || el.tagName === 'INPUT') {
            el.disabled = !present;
            el.title = present ? '' : 'Upload a resume to enable this feature';
            el.classList.toggle('disabled', !present);
        } else if (el.tagName === 'A') {
            if (!present) {
                el.dataset._href = el.getAttribute('href') || '';
                el.setAttribute('href', 'javascript:void(0)');
                el.classList.add('disabled');
                el.title = 'Upload a resume to enable this feature';
            } else {
                if (el.dataset._href) {
                    el.setAttribute('href', el.dataset._href);
                    delete el.dataset._href;
                }
                el.classList.remove('disabled');
                el.title = '';
            }
        }
    });
}

// Initialize button state on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => updateFeatureButtonsState(), 50);
});

