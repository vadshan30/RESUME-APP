import json
import os
from typing import Dict, List
from backend.app.services.matching_engine import MatchingEngine

class JobRecommender:
    """Service for recommending job roles based on resume skills."""
    
    def __init__(self):
        self.job_templates = self._load_job_templates()
        self.matching_engine = MatchingEngine()
    
    def _load_job_templates(self) -> List[Dict]:
        """Load job templates from JSON file."""
        templates_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'job_templates.json'
        )
        try:
            with open(templates_path, 'r', encoding='utf-8') as f:
                templates = json.load(f)
                print(f"DEBUG: Loaded {len(templates)} job templates from {templates_path}")
                return templates
        except Exception as e:
            print(f"ERROR loading job templates: {e}")
            print(f"Tried path: {templates_path}")
            return []
    
    def recommend_jobs(self, resume_skills: List[str], limit: int = 5, 
                      industry: str = None, level: str = None) -> List[Dict]:
        """
        Recommend job roles based on resume skills.
        Works even with minimal or no skills using partial matching.
        
        Args:
            resume_skills: List of skills from resume (can be empty)
            limit: Maximum number of recommendations
            industry: Filter by industry (optional)
            level: Filter by career level (optional)
            
        Returns:
            List of recommended job roles with compatibility scores
        """
        # Ensure we have job templates
        if not self.job_templates:
            return []
        
        recommendations = []
        # Handle empty or None resume_skills
        has_skills = resume_skills and len(resume_skills) > 0
        resume_skills_lower = [s.lower() for s in resume_skills] if has_skills else []
        
        for job in self.job_templates:
            # Apply filters
            if industry and job.get('industry') != industry:
                continue
            if level and job.get('level') != level:
                continue
            
            # Calculate match
            job_skills = job.get('required_skills', [])
            
            # If no resume skills, provide all jobs with base scores
            if not has_skills:
                # Provide all jobs with a base score, prioritize entry-level
                if job.get('level') == 'Entry':
                    match_percentage = 25.0
                elif job.get('level') == 'Mid':
                    match_percentage = 15.0
                else:
                    match_percentage = 10.0
                
                recommendations.append({
                    'role': job.get('role', 'Unknown Role'),
                    'industry': job.get('industry', 'General'),
                    'level': job.get('level', 'Mid'),
                    'description': job.get('description', ''),
                    'required_skills': job_skills if job_skills else [],
                    'match_percentage': match_percentage,
                    'matching_skills': [],
                    'missing_skills': job_skills[:5] if job_skills else [],
                    'note': 'Upload resume for personalized matching'
                })
            else:
                # Use normal matching
                match_result = self.matching_engine.calculate_match(resume_skills, job_skills)
                
                # Also check for partial matches (skill name contains or is contained)
                partial_matches = self._find_partial_matches(resume_skills_lower, job_skills)
                if partial_matches:
                    # Boost score for partial matches
                    match_result['match_percentage'] = min(
                        match_result['match_percentage'] + (len(partial_matches) * 8), 
                        100
                    )
                    # Add partial matches to matching skills
                    existing_matching = set(match_result['matching_skills'])
                    for pm in partial_matches:
                        if pm not in existing_matching:
                            match_result['matching_skills'].append(pm)
                
                # Boost low scores for better recommendations
                if match_result['match_percentage'] < 20 and len(resume_skills) > 0:
                    # Give minimum 20% for any job if user has skills
                    match_result['match_percentage'] = max(match_result['match_percentage'], 20.0)
                
                recommendations.append({
                    'role': job.get('role', 'Unknown Role'),
                    'industry': job.get('industry', 'General'),
                    'level': job.get('level', 'Mid'),
                    'description': job.get('description', ''),
                    'required_skills': job_skills if job_skills else [],
                    'match_percentage': match_result['match_percentage'],
                    'matching_skills': match_result['matching_skills'],
                    'missing_skills': match_result['missing_skills']
                })
        
        # Always return results - sort by match percentage (descending)
        recommendations.sort(key=lambda x: x.get('match_percentage', 0), reverse=True)
        
        # Return at least some recommendations (always return something if we have jobs)
        return recommendations[:limit] if recommendations else []
    
    def _find_partial_matches(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        """Find partial skill matches (e.g., 'python' matches 'Python Developer')."""
        partial = []
        for job_skill in job_skills:
            job_skill_lower = job_skill.lower()
            for resume_skill in resume_skills:
                # Check for substring matches and similar skills
                if (resume_skill in job_skill_lower or 
                    job_skill_lower in resume_skill or
                    self._are_similar_skills(resume_skill, job_skill_lower)):
                    if job_skill not in partial:
                        partial.append(job_skill)
        return partial
    
    def _are_similar_skills(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are similar (basic similarity check)."""
        # Simple similarity checks
        synonyms = {
            'js': 'javascript',
            'ts': 'typescript', 
            'py': 'python',
            'react': 'reactjs',
            'vue': 'vuejs',
            'node': 'nodejs',
            'sql': 'database',
            'db': 'database',
            'ai': 'artificial intelligence',
            'ml': 'machine learning'
        }
        
        s1, s2 = skill1.lower(), skill2.lower()
        
        # Check direct synonyms
        if s1 in synonyms and synonyms[s1] in s2:
            return True
        if s2 in synonyms and synonyms[s2] in s1:
            return True
            
        # Check if one contains the other (with word boundaries)
        words1 = s1.split()
        words2 = s2.split()
        
        for w1 in words1:
            for w2 in words2:
                if len(w1) > 2 and len(w2) > 2 and (w1 in w2 or w2 in w1):
                    return True
                    
        return False

