from flask import Blueprint, request, jsonify
from backend.app.services.cover_letter_generator import CoverLetterGenerator

bp = Blueprint('cover_letter', __name__, url_prefix='/api')

@bp.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate a personalized cover letter."""
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    job_description = data.get('job_description', '')
    tone = data.get('tone', 'formal')
    name = data.get('name', 'Your Name')
    
    if not resume_text or not job_description:
        return jsonify({'error': 'Resume text and job description are required'}), 400
    
    try:
        generator = CoverLetterGenerator()
        cover_letter = generator.generate_cover_letter(
            resume_text, 
            job_description, 
            tone=tone,
            name=name
        )
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

