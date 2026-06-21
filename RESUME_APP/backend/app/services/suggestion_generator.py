from typing import Dict, List

class SuggestionGenerator:
    """Service for generating resume improvement suggestions."""
    
    @staticmethod
    def generate_suggestions(match_result: Dict) -> List[Dict]:
        """
        Generate actionable suggestions based on match results.
        
        Args:
            match_result: Result from matching engine
            
        Returns:
            List of suggestion dictionaries
        """
        suggestions = []
        
        missing_skills = match_result.get('missing_skills', [])
        matching_skills = match_result.get('matching_skills', [])
        match_percentage = match_result.get('match_percentage', 0)
        
        # Suggestions for missing skills
        if missing_skills:
            suggestions.append({
                'type': 'critical',
                'category': 'skills',
                'title': 'Add Missing Skills',
                'description': f"Add these {len(missing_skills)} skills to improve your match: {', '.join(missing_skills[:5])}",
                'action_items': [f"Add '{skill}' to your skills section" for skill in missing_skills[:10]]
            })
        
        # Suggestions for low match percentage
        if match_percentage < 50:
            suggestions.append({
                'type': 'important',
                'category': 'optimization',
                'title': 'Low Compatibility Score',
                'description': f"Your resume matches {match_percentage}% of required skills. Focus on acquiring or highlighting the missing skills.",
                'action_items': [
                    "Review the job description carefully",
                    "Highlight relevant experience that demonstrates missing skills",
                    "Consider taking courses or certifications for key missing skills"
                ]
            })
        
        # Suggestions for keyword optimization
        if matching_skills:
            suggestions.append({
                'type': 'enhancement',
                'category': 'keywords',
                'title': 'Keyword Optimization',
                'description': f"Your resume already includes {len(matching_skills)} matching skills. Make sure these are prominently featured.",
                'action_items': [
                    f"Ensure '{skill}' appears in your resume" for skill in matching_skills[:5]
                ]
            })
        
        # General suggestions
        suggestions.append({
            'type': 'general',
            'category': 'format',
            'title': 'Resume Formatting Tips',
            'description': 'Optimize your resume format for better ATS compatibility.',
            'action_items': [
                "Use standard section headings (Skills, Experience, Education)",
                "Include relevant keywords naturally in your descriptions",
                "Keep formatting simple and clean",
                "Use bullet points for easy scanning"
            ]
        })
        
        return suggestions

