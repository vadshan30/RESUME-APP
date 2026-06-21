from flask import Blueprint, request, jsonify
from backend.app.services.interview_generator import InterviewGenerator

bp = Blueprint('interview', __name__, url_prefix='/api')

@bp.route('/interview-questions', methods=['POST'])
def get_interview_questions():
    """Generate interview questions based on topic, difficulty, or job description."""
    data = request.get_json()
    job_description = data.get('job_description', '')
    topic = data.get('topic', '')
    difficulty = data.get('difficulty', '')
    num_questions = data.get('num_questions', 5)
    
    if not job_description and not topic:
        return jsonify({'error': 'Either Job description or Topic is required'}), 400
    
    try:
        generator = InterviewGenerator()
        questions = generator.generate_questions(
            topic=topic,
            difficulty=difficulty,
            job_description=job_description,
            num_questions=num_questions
        )
        
        return jsonify({
            'success': True,
            'questions': questions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
