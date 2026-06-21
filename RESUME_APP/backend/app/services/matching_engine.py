from typing import Dict, List, Set
from backend.app.utils.skill_normalizer import SkillNormalizer

class MatchingEngine:
    """Service for matching resume skills with job requirements."""
    
    def __init__(self):
        self.normalizer = SkillNormalizer()
    
    def calculate_match(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """
        Calculate compatibility between resume and job skills.
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of required skills from job description
            
        Returns:
            Dictionary with match results
        """
        # Normalize skills
        resume_normalized = self.normalizer.normalize_list(resume_skills)
        job_normalized = self.normalizer.normalize_list(job_skills)
        
        # Find matches
        matching_skills = resume_normalized.intersection(job_normalized)
        missing_skills = job_normalized - resume_normalized
        extra_skills = resume_normalized - job_normalized
        
        # Calculate match percentage
        if len(job_normalized) == 0:
            match_percentage = 100.0
        else:
            match_percentage = (len(matching_skills) / len(job_normalized)) * 100
        
        # Calculate strength score (0-100)
        strength_score = self._calculate_strength_score(
            len(matching_skills),
            len(job_normalized),
            len(extra_skills)
        )
        
        return {
            'match_percentage': round(match_percentage, 2),
            'strength_score': strength_score,
            'matching_skills': sorted(list(matching_skills)),
            'missing_skills': sorted(list(missing_skills)),
            'extra_skills': sorted(list(extra_skills)),
            'total_resume_skills': len(resume_normalized),
            'total_job_skills': len(job_normalized),
            'matching_count': len(matching_skills)
        }
    
    def _calculate_strength_score(self, matching: int, required: int, extra: int) -> int:
        """
        Calculate overall resume strength score.
        
        Args:
            matching: Number of matching skills
            required: Total required skills
            extra: Number of extra skills
            
        Returns:
            Strength score (0-100)
        """
        if required == 0:
            return 100
        
        # Base score from match percentage (0-70 points)
        base_score = (matching / required) * 70
        
        # Bonus for extra skills (0-30 points, capped)
        extra_bonus = min((extra / max(required, 1)) * 30, 30)
        
        total_score = base_score + extra_bonus
        return min(int(total_score), 100)

