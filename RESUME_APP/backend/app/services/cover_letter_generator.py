import json
import os
from typing import Dict, List
from backend.app.services.skill_extractor import SkillExtractor

class CoverLetterGenerator:
    """Service for generating personalized cover letters."""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.skill_extractor = SkillExtractor()
    
    def _load_templates(self) -> Dict:
        """Load cover letter templates from JSON file."""
        templates_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'cover_letter_templates.json'
        )
        try:
            with open(templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def generate_cover_letter(self, resume_text: str, job_description: str, 
                             tone: str = 'formal', name: str = 'Your Name') -> str:
        """
        Generate a personalized cover letter.
        
        Args:
            resume_text: Resume text
            job_description: Job description text
            tone: 'formal' or 'casual'
            name: Applicant's name
            
        Returns:
            Generated cover letter text
        """
        # Extract skills
        resume_skills = self.skill_extractor.extract_skills(resume_text)
        job_skills = self.skill_extractor.extract_skills(job_description)
        
        # Get template
        template = self.templates.get(tone, self.templates.get('formal', {}))
        
        # Prepare template variables
        key_skills = ', '.join(resume_skills['all_skills'][:5])
        role = self._extract_role(job_description)
        
        # Build cover letter
        cover_letter = template.get('opening', 'Dear Hiring Manager,') + '\n\n'
        
        body = template.get('body_template', '')
        body = body.replace('{role}', role)
        body = body.replace('{skills}', key_skills)
        body = body.replace('{key_skills}', key_skills)
        body = body.replace('{achievement}', 'delivered high-quality solutions')
        body = body.replace('{experience}', 'several')
        body = body.replace('{reason}', 'the opportunity to work with innovative technologies')
        
        cover_letter += body + '\n\n'
        cover_letter += template.get('closing', 'Sincerely,').replace('{name}', name)
        
        return cover_letter
    
    def _extract_role(self, job_description: str) -> str:
        """Extract job role from description."""
        # Simple extraction - look for common patterns
        import re
        patterns = [
            r'position[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'role[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'seeking[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return 'this position'

