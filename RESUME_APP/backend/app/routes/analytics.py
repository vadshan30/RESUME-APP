from flask import Blueprint, request, jsonify
from backend.app.services.analytics import AnalyticsService
from backend.app.services.skill_extractor import SkillExtractor

bp = Blueprint('analytics', __name__, url_prefix='/api')

@bp.route('/analytics', methods=['POST', 'GET'])
def get_analytics():
    """Get resume analytics and strength score. Handles empty data gracefully."""
    if request.method == 'GET':
        data = {}
    else:
        data = request.get_json() or {}
    
    resume_text = data.get('resume_text', '')
    resume_skills = data.get('resume_skills', [])
    match_history = data.get('match_history', [])
    
    try:
        # Extract skills if not provided
        if not resume_skills and resume_text:
            skill_extractor = SkillExtractor()
            skills_data = skill_extractor.extract_skills(resume_text)
            resume_skills = skills_data.get('all_skills', []) if isinstance(skills_data, dict) else []
        
        # Handle empty data gracefully - return placeholder analytics
        if not resume_skills:
            return jsonify({
                'success': True,
                'analytics': {
                    'strength_score': 0,
                    'skill_count': 0,
                    'diversity_score': 0,
                    'average_match': 0,
                    'skill_distribution': {
                        'technical': 0,
                        'soft': 0,
                        'other': 0,
                        'total': 0
                    },
                    'recommendations': [
                        'Upload a resume to see your analytics and strength score.',
                        'Your resume strength will be calculated based on your skills.'
                    ],
                    'empty': True
                }
            })
        
        analytics = AnalyticsService.calculate_resume_strength(
            resume_skills,
            match_history
        )
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
    
    except Exception as e:
        import traceback
        print(f"ERROR in analytics: {str(e)}")
        print(traceback.format_exc())
        # Return empty analytics instead of error
        return jsonify({
            'success': True,
            'analytics': {
                'strength_score': 0,
                'skill_count': 0,
                'diversity_score': 0,
                'average_match': 0,
                'skill_distribution': {
                    'technical': 0,
                    'soft': 0,
                    'other': 0,
                    'total': 0
                },
                'recommendations': ['Error loading analytics. Please try again.'],
                'empty': True
            }
        })

