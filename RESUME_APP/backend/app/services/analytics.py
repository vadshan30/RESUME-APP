from typing import Dict, List

class AnalyticsService:
    """Service for generating analytics and insights."""
    
    @staticmethod
    def calculate_resume_strength(resume_skills: List[str], 
                                  match_results: List[Dict] = None) -> Dict:
        """
        Calculate overall resume strength score.
        
        Args:
            resume_skills: List of skills from resume
            match_results: List of previous match results (optional)
            
        Returns:
            Dictionary with analytics data
        """
        # Base score from skill count and diversity
        skill_count = len(resume_skills)
        diversity_score = min(skill_count * 2, 50)  # Max 50 points for diversity
        
        # Calculate average match if match results provided
        avg_match = 0
        if match_results:
            matches = [r.get('match_percentage', 0) for r in match_results]
            avg_match = sum(matches) / len(matches) if matches else 0
        
        # Overall strength score
        strength_score = diversity_score + (avg_match * 0.5)
        strength_score = min(int(strength_score), 100)
        
        # Skill distribution
        distribution = AnalyticsService._categorize_skills(resume_skills)
        
        # Mock data for missing fields
        jobs_matched = len(match_results) if match_results else 5
        missing_skills_count = max(0, 15 - skill_count)
        career_readiness = min(int((strength_score + (skill_count * 2)) / 1.5), 100)
        
        # Mock trend data
        ats_trend = [
            max(0, strength_score - 20),
            max(0, strength_score - 15),
            max(0, strength_score - 10),
            max(0, strength_score - 5),
            strength_score
        ]
        job_match_trend = [
            max(0, int(avg_match) - 15),
            max(0, int(avg_match) - 10),
            max(0, int(avg_match) - 8),
            max(0, int(avg_match) - 2),
            int(avg_match) or 60
        ]
        
        return {
            'strength_score': strength_score,
            'skill_count': skill_count,
            'diversity_score': diversity_score,
            'average_match': round(avg_match, 2),
            'skill_distribution': distribution,
            'jobs_matched': jobs_matched,
            'missing_skills_count': missing_skills_count,
            'career_readiness': career_readiness,
            'ats_trend': ats_trend,
            'job_match_trend': job_match_trend,
            'recommendations': AnalyticsService._get_recommendations(strength_score, skill_count)
        }
    
    @staticmethod
    def _categorize_skills(skills: List[str]) -> Dict:
        """Categorize skills for distribution analysis."""
        # Simple categorization (can be enhanced)
        technical_keywords = ['python', 'javascript', 'java', 'react', 'sql', 'api', 'git']
        soft_keywords = ['communication', 'leadership', 'teamwork', 'problem']
        
        technical = sum(1 for s in skills if any(kw in s.lower() for kw in technical_keywords))
        soft = sum(1 for s in skills if any(kw in s.lower() for kw in soft_keywords))
        other = len(skills) - technical - soft
        
        return {
            'technical': technical,
            'soft': soft,
            'other': other,
            'total': len(skills)
        }
    
    @staticmethod
    def _get_recommendations(strength_score: int, skill_count: int) -> List[str]:
        """Get recommendations based on analytics."""
        recommendations = []
        
        if strength_score < 50:
            recommendations.append("Your resume strength is below average. Focus on adding more relevant skills.")
        
        if skill_count < 10:
            recommendations.append("Consider adding more skills to improve your profile.")
        
        if strength_score >= 80:
            recommendations.append("Great job! Your resume is strong. Keep it updated with latest technologies.")
        
        return recommendations

