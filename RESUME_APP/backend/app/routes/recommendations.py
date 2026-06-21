from flask import Blueprint, request, jsonify
from backend.app.services.job_recommender import JobRecommender
from backend.app.services.skill_extractor import SkillExtractor

bp = Blueprint('recommendations', __name__, url_prefix='/api')

@bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get job recommendations based on resume skills. Works even without resume."""
    data = request.get_json() or {}
    resume_text = data.get('resume_text', '')
    resume_skills = data.get('resume_skills', [])
    industry = data.get('industry')
    level = data.get('level')
    limit = data.get('limit', 10)
    
    try:
        # Extract skills if not provided
        if not resume_skills and resume_text:
            skill_extractor = SkillExtractor()
            skills_data = skill_extractor.extract_skills(resume_text)
            resume_skills = skills_data.get('all_skills', []) if isinstance(skills_data, dict) else []

        # Ensure resume_skills is a list
        if not isinstance(resume_skills, list):
            resume_skills = []

        # Get recommendations (works even with empty skills list)
        recommender = JobRecommender()
        recommendations = recommender.recommend_jobs(
            resume_skills,
            limit=limit,
            industry=industry,
            level=level
        )

        # If no recommendations returned, provide sensible fallbacks
        if not recommendations:
            fallback = []
            # Use job templates as fallback (provide minimal info)
            for job in (recommender.job_templates or [])[:limit]:
                fallback.append({
                    'role': job.get('role', 'Unknown Role'),
                    'industry': job.get('industry', 'General'),
                    'level': job.get('level', 'Mid'),
                    'description': job.get('description', ''),
                    'required_skills': job.get('required_skills', []),
                    'match_percentage': 10.0,
                    'matching_skills': [],
                    'missing_skills': job.get('required_skills', [])[:5],
                    'note': 'Fallback recommendation — upload resume for personalized results'
                })

            recommendations = fallback

        # Debug logging
        print(f"DEBUG: Returning {len(recommendations)} recommendations")

        # Return success
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations),
            'has_resume': len(resume_skills) > 0
        }), 200

    except Exception as e:
        import traceback
        print(f"ERROR in recommendations: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': True,
            'recommendations': [],
            'total': 0,
            'has_resume': False,
            'error': 'Unable to generate recommendations at this time'
        })

