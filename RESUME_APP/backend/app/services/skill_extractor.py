import json
import os
import re
from typing import Dict, List, Set
from backend.app.utils.skill_normalizer import SkillNormalizer

class SkillExtractor:
    """Service for extracting skills from text using pattern matching and NLP."""
    
    def __init__(self):
        self.skills_db = self._load_skills_database()
        self.normalizer = SkillNormalizer()
        self.all_skills = self._get_all_skills()
    
    def _load_skills_database(self) -> dict:
        """Load skills database from JSON file."""
        skills_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'skills_database.json'
        )
        try:
            with open(skills_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"technical_skills": {}, "soft_skills": [], "certifications": []}
    
    def _get_all_skills(self) -> Set[str]:
        """Get all skills from database as a set for fast lookup."""
        skills = set()
        
        # Technical skills
        for category, skill_list in self.skills_db.get('technical_skills', {}).items():
            skills.update(skill_list)
        
        # Soft skills
        skills.update(self.skills_db.get('soft_skills', []))
        
        # Certifications
        skills.update(self.skills_db.get('certifications', []))
        
        return skills
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from text.
        
        Args:
            text: Input text to extract skills from
            
        Returns:
            Dictionary with categorized skills
        """
        if not text:
            return {
                'technical_skills': [],
                'soft_skills': [],
                'certifications': [],
                'all_skills': []
            }
        
        text_lower = text.lower()
        found_skills = set()
        
        # Pattern matching against skills database
        for skill in self.all_skills:
            # Check for exact match (case insensitive)
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)
        
        # Also check for common abbreviations and variations
        found_skills.update(self._extract_variations(text_lower))
        
        # Normalize all found skills
        normalized_skills = self.normalizer.normalize_list(list(found_skills))
        
        # Categorize skills
        categorized = self._categorize_skills(normalized_skills)
        
        return {
            'technical_skills': categorized['technical'],
            'soft_skills': categorized['soft'],
            'certifications': categorized['certifications'],
            'all_skills': list(normalized_skills)
        }
    
    def _extract_variations(self, text: str) -> Set[str]:
        """Extract skills using common variations and abbreviations."""
        found = set()
        
        # Common abbreviations
        abbreviations = {
            'js': 'JavaScript',
            'py': 'Python',
            'ml': 'Machine Learning',
            'ai': 'Artificial Intelligence',
            'api': 'Application Programming Interface',
            'sql': 'SQL',
            'nosql': 'NoSQL',
            'ui': 'User Interface',
            'ux': 'User Experience',
            'ci/cd': 'CI/CD',
            'aws': 'AWS',
            'gcp': 'Google Cloud Platform',
            'azure': 'Microsoft Azure'
        }
        
        for abbrev, full_name in abbreviations.items():
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            if re.search(pattern, text):
                found.add(full_name)
        
        return found
    
    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Categorize skills into technical, soft, and certifications."""
        technical = []
        soft = []
        certifications = []
        
        tech_categories = self.skills_db.get('technical_skills', {})
        all_tech = set()
        for category_skills in tech_categories.values():
            all_tech.update(category_skills)
        
        soft_skills_list = set(self.skills_db.get('soft_skills', []))
        certs_list = set(self.skills_db.get('certifications', []))
        
        for skill in skills:
            if skill in all_tech:
                technical.append(skill)
            elif skill in soft_skills_list:
                soft.append(skill)
            elif skill in certs_list:
                certifications.append(skill)
            else:
                # Default to technical if not found
                technical.append(skill)
        
        return {
            'technical': sorted(technical),
            'soft': sorted(soft),
            'certifications': sorted(certifications)
        }

