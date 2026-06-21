# Career Assistant Web Application

> An AI-powered career intelligence platform that helps job seekers improve their employability through resume analysis, intelligent job matching, interview preparation, and personalized career guidance.

[![Status](https://img.shields.io/badge/status-ready-green)]()
[![Tech Stack](https://img.shields.io/badge/stack-Flask%20%7C%20JavaScript-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Deployment](#deployment)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Career Assistant Web Application is a portfolio-grade, interview-ready project designed to help job seekers:

- **Analyze Resumes:** Extract skills and identify strengths/weaknesses
- **Match with Jobs:** Calculate compatibility between resumes and job descriptions
- **Get Recommendations:** Receive personalized job role suggestions
- **Prepare for Interviews:** Generate role-specific interview questions and answers
- **Plan Career Paths:** Identify skill gaps and suggest learning paths
- **Generate Cover Letters:** Create personalized cover letters
- **Track Progress:** Visualize skills and match history through analytics

This application demonstrates full-stack development capabilities, AI/NLP integration, and real-world engineering practices.

---

## ✨ Features

### Core Features (MVP)
- ✅ Resume upload and text extraction (PDF & text formats)
- ✅ Skill extraction from resumes and job descriptions
- ✅ Resume-job compatibility matching with percentage scores
- ✅ Missing skills identification
- ✅ Resume improvement suggestions

### Advanced Features
- 🚀 Job opportunity recommendation engine
- 🚀 Interview preparation assistant
- 🚀 Career path & skill gap analyzer
- 🚀 Cover letter generator
- 🚀 Analytics dashboard with visualizations
- 🚀 Export & report generation (PDF/text)

---

## 🛠 Tech Stack

### Frontend
- **HTML5/CSS3:** Semantic markup, modern CSS (Grid, Flexbox)
- **Vanilla JavaScript (ES6+):** No framework overhead, full control
- **Chart.js:** Data visualization for analytics dashboard

### Backend
- **Flask (Python):** Lightweight, flexible web framework
- **spaCy/NLTK:** Natural Language Processing for skill extraction
- **PyPDF2/pdfplumber:** PDF text extraction
- **ReportLab:** PDF report generation

### Data Storage
- **SQLite:** Lightweight database for session storage
- **JSON Files:** Skill databases, job templates, configuration

### Deployment
- **Platform:** Heroku, Railway, Render, or Vercel
- **Environment:** Production-ready with environment variables

---

## 🏗 Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Frontend      │  HTML/CSS/JavaScript
│   (Client)      │
└────────┬────────┘
         │ HTTP/REST API
┌────────▼────────┐
│   Backend       │  Flask Routes & Services
│   (Server)      │
└────────┬────────┘
         │
┌────────▼────────┐
│   Services      │  Resume Parser, Skill Extractor,
│   Layer         │  Matching Engine, AI Services
└────────┬────────┘
         │
┌────────▼────────┐
│   Data Layer    │  SQLite, JSON Files, File Storage
└─────────────────┘
```

### Module Responsibilities

- **Frontend:** UI components, API client, state management, visualization
- **Backend Routes:** RESTful API endpoints
- **Services:** Business logic (parsing, extraction, matching, AI)
- **Data Layer:** Storage and retrieval of resumes, skills, jobs

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12** (required - not 3.11 or 3.13)
- pip (Python package manager)
- Git (optional, for version control)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resumeapp.git
   cd resumeapp
   ```

2. **Verify Python version**
   ```bash
   python --version
   # Must be Python 3.12.x
   ```
   
   If you need Python 3.12:
   - **Windows:** Download from [python.org](https://www.python.org/downloads/)
   - **Linux:** `sudo apt install python3.12 python3.12-venv`
   - **Mac:** `brew install python@3.12`

3. **Set up Python virtual environment**
   ```bash
   # Create virtual environment with Python 3.12
   python3.12 -m venv venv
   
   # Activate virtual environment
   # Windows (PowerShell):
   venv\Scripts\Activate.ps1
   # Windows (CMD):
   venv\Scripts\activate.bat
   # Mac/Linux:
   source venv/bin/activate
   ```
   
   You should see `(venv)` in your terminal prompt.

4. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```

5. **Download spaCy language model (optional but recommended)**
   ```bash
   python -m spacy download en_core_web_sm
   ```
   Note: The app works without this, but NLP features will be basic.

6. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

7. **Run the application**
   ```bash
   python run.py
   ```
   
   You should see:
   ```
   🚀 Career Assistant Web Application
   ✅ Application initialized successfully
   📡 Starting server on http://localhost:5000
   ```

8. **Open in browser**
   ```
   http://localhost:5000
   ```

See [SETUP.md](./SETUP.md) for detailed setup instructions and troubleshooting.

### Development Setup

See [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for detailed development instructions.

---

## 📁 Project Structure

```
resumeapp/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app initialization
│   │   ├── routes/              # API route handlers
│   │   │   ├── upload.py
│   │   │   ├── matching.py
│   │   │   ├── recommendations.py
│   │   │   └── ...
│   │   ├── services/            # Business logic
│   │   │   ├── resume_parser.py
│   │   │   ├── skill_extractor.py
│   │   │   ├── matching_engine.py
│   │   │   └── ...
│   │   ├── utils/               # Helper functions
│   │   │   ├── skill_normalizer.py
│   │   │   └── ...
│   │   └── config.py            # Configuration
│   ├── uploads/                 # Uploaded resume storage
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── main.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── upload.js
│   │   ├── matching.js
│   │   ├── dashboard.js
│   │   └── ...
│   └── assets/
├── data/
│   ├── skills_database.json
│   ├── job_templates.json
│   └── synonyms.json
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── APP_REQUIREMENTS_DOCUMENT.md
│   ├── DEVELOPMENT_PLAN.md
│   └── TECHNICAL_INTERVIEW_GUIDE.md
├── README.md
└── .gitignore
```

---

## 📚 Documentation

- **[App Requirements Document](./APP_REQUIREMENTS_DOCUMENT.md):** Complete SRS with functional/non-functional requirements
- **[Development Plan](./DEVELOPMENT_PLAN.md):** Phased implementation guide
- **[Technical Interview Guide](./TECHNICAL_INTERVIEW_GUIDE.md):** Interview preparation and portfolio review

---

## 🚢 Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create resumeapp`
4. Set environment variables: `heroku config:set KEY=value`
5. Deploy: `git push heroku main`

### Railway Deployment

1. Connect GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy automatically on push

### Environment Variables

```env
PORT=5000
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=10485760
FLASK_ENV=production
```

See [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for detailed deployment steps.

---

## 🔮 Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Resume templates and ATS optimization
- [ ] Integration with job boards (LinkedIn, Indeed APIs)
- [ ] Advanced ML models for better skill extraction
- [ ] Multi-language support
- [ ] Mobile app (React Native or PWA)
- [ ] Collaboration features (share with career counselors)

---

## 🤝 Contributing

This is a portfolio project, but contributions and suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Portfolio: [Your Portfolio](https://yourportfolio.com)

---

## 🙏 Acknowledgments

- spaCy and NLTK communities for excellent NLP tools
- Flask community for the amazing framework
- All open-source contributors whose libraries made this possible

---

## 📊 Project Status

**Current Phase:** ✅ Complete  
**Status:** All features implemented and ready for use  
**Next Steps:** Deploy to production or customize for your needs

---

**⭐ If you find this project helpful, please give it a star!**

---

**Last Updated:** 2024

