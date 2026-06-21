from flask import Blueprint, request, jsonify
from backend.app.services.skill_extractor import SkillExtractor
from backend.app.services.matching_engine import MatchingEngine
from backend.app.services.suggestion_generator import SuggestionGenerator

bp = Blueprint('matching', __name__, url_prefix='/api')

@bp.route('/match', methods=['POST'])
def match_resume_job():
    """Match resume skills with job description."""
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    job_description = data.get('job_description', '')
    resume_skills = data.get('resume_skills', [])
    
    if not job_description:
        return jsonify({'error': 'Job description is required'}), 400
    
    try:
        skill_extractor = SkillExtractor()
        matching_engine = MatchingEngine()
        suggestion_generator = SuggestionGenerator()
        
        # Extract skills if not provided
        if not resume_skills and resume_text:
            resume_skills_data = skill_extractor.extract_skills(resume_text)
            resume_skills = resume_skills_data['all_skills']
        elif not resume_skills:
            return jsonify({'error': 'Resume skills or text is required'}), 400
        
        # Extract job skills
        job_skills_data = skill_extractor.extract_skills(job_description)
        job_skills = job_skills_data['all_skills']
        
        # Calculate match
        match_result = matching_engine.calculate_match(resume_skills, job_skills)
        
        # Generate suggestions
        suggestions = suggestion_generator.generate_suggestions(match_result)
        
        return jsonify({
            'success': True,
            'match_result': match_result,
            'suggestions': suggestions,
            'resume_skills': resume_skills,
            'job_skills': job_skills
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

