from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from backend.app.services.resume_parser import ResumeParser
from backend.app.services.skill_extractor import SkillExtractor

bp = Blueprint('upload', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'text'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload and extraction."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF and TXT files are allowed.'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # Extract text
        parser = ResumeParser()
        file_type = file.content_type
        result = parser.extract_text(file_path, file_type)
        
        if not result['success']:
            return jsonify({'error': result.get('error', 'Failed to extract text')}), 500
        
        # Clean text
        cleaned_text = parser.clean_text(result['text'])
        
        # Extract skills
        skill_extractor = SkillExtractor()
        skills = skill_extractor.extract_skills(cleaned_text)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'text': cleaned_text,
            'word_count': result['word_count'],
            'char_count': result['char_count'],
            'skills': skills
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/extract-skills', methods=['POST'])
def extract_skills():
    """Extract skills from text."""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        skill_extractor = SkillExtractor()
        skills = skill_extractor.extract_skills(text)
        
        return jsonify({
            'success': True,
            'skills': skills
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

