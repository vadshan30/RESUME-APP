from flask import Blueprint, request, jsonify
from backend.app.services.career_analyzer import CareerAnalyzer
from backend.app.services.skill_extractor import SkillExtractor

bp = Blueprint('career', __name__, url_prefix='/api')

@bp.route('/career-path', methods=['POST'])
def analyze_career_path():
    """Analyze career path and identify skill gaps."""
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    resume_skills = data.get('resume_skills', [])
    target_role = data.get('target_role')
    
    try:
        # Extract skills if not provided
        if not resume_skills and resume_text:
            skill_extractor = SkillExtractor()
            skills_data = skill_extractor.extract_skills(resume_text)
            resume_skills = skills_data['all_skills']
        elif not resume_skills:
            return jsonify({'error': 'Resume skills or text is required'}), 400
        
        analyzer = CareerAnalyzer()
        analysis = analyzer.analyze_career_path(resume_skills, target_role)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

