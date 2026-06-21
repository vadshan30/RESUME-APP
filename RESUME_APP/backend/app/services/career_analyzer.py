from typing import Dict, List
from backend.app.services.matching_engine import MatchingEngine
from backend.app.services.job_recommender import JobRecommender

class CareerAnalyzer:
    """Service for analyzing career paths and skill gaps."""
    
    def __init__(self):
        self.matching_engine = MatchingEngine()
        self.job_recommender = JobRecommender()
    
    def analyze_career_path(self, current_skills: List[str], target_role: str = None) -> Dict:
        """
        Analyze career path and identify skill gaps.
        
        Args:
            current_skills: List of current skills
            target_role: Target role name (optional)
            
        Returns:
            Dictionary with career analysis
        """
        # Get job recommendations
        recommendations = self.job_recommender.recommend_jobs(current_skills, limit=3)
        
        # If target role specified, find it
        target_analysis = None
        if target_role:
            for job in self.job_recommender.job_templates:
                if job.get('role') == target_role:
                    match_result = self.matching_engine.calculate_match(
                        current_skills, 
                        job.get('required_skills', [])
                    )
                    target_analysis = {
                        'role': target_role,
                        'match_percentage': match_result['match_percentage'],
                        'missing_skills': match_result['missing_skills'],
                        'matching_skills': match_result['matching_skills'],
                        'required_skills': job.get('required_skills', [])
                    }
                    break
        
        # Generate learning path
        learning_path = self._generate_learning_path(current_skills, recommendations)
        
        return {
            'current_skills_count': len(current_skills),
            'recommended_roles': recommendations,
            'target_role_analysis': target_analysis,
            'learning_path': learning_path,
            'next_steps': self._get_next_steps(current_skills, recommendations)
        }
    
    def _generate_learning_path(self, current_skills: List[str], recommendations: List[Dict]) -> List[Dict]:
        """Generate a learning path based on missing skills."""
        # Collect all missing skills from top recommendations
        all_missing = set()
        for rec in recommendations[:3]:
            all_missing.update(rec.get('missing_skills', []))
        
        learning_path = []
        for skill in list(all_missing)[:5]:  # Top 5 missing skills
            learning_path.append({
                'skill': skill,
                'priority': 'high',
                'suggested_resources': self._get_learning_resources(skill)
            })
        
        return learning_path
    
    def _get_learning_resources(self, skill: str) -> List[str]:
        """Get learning resources for a skill."""
        # In a real implementation, this would query a learning resources database
        return [
            f"Online courses for {skill}",
            f"Practice projects using {skill}",
            f"Documentation and tutorials for {skill}"
        ]
    
    def _get_next_steps(self, current_skills: List[str], recommendations: List[Dict]) -> List[str]:
        """Get actionable next steps."""
        steps = []
        
        if recommendations:
            top_role = recommendations[0]
            missing = top_role.get('missing_skills', [])
            if missing:
                steps.append(f"Focus on learning: {', '.join(missing[:3])}")
        
        steps.extend([
            "Build projects using your target skills",
            "Contribute to open-source projects",
            "Network with professionals in your target industry",
            "Update your resume with new skills as you learn them"
        ])
        
        return steps

