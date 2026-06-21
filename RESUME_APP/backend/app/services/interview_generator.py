import json
import os
from typing import Dict, List
from backend.app.services.skill_extractor import SkillExtractor

class InterviewGenerator:
    """Service for generating interview questions based on topic, difficulty, and job description."""
    
    def __init__(self):
        self.questions_db = self._load_questions()
        self.skill_extractor = SkillExtractor()
    
    def _load_questions(self) -> Dict:
        """Load interview questions from JSON file."""
        questions_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'interview_questions.json'
        )
        try:
            with open(questions_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"technical": [], "behavioral": [], "situational": [], "hr": []}
    
    def generate_questions(self, topic: str = "", difficulty: str = "Intermediate", job_description: str = "", num_questions: int = 5) -> Dict:
        """
        Generate interview questions based on topic and difficulty.
        
        Args:
            topic: Technical topic (e.g., 'Java', 'Python', 'HR')
            difficulty: Difficulty level ('Beginner', 'Intermediate', 'Advanced')
            job_description: Job description text (optional)
            num_questions: Number of questions per category
            
        Returns:
            Dictionary with categorized questions
        """
        # If job description is provided, we can extract skills.
        # But we prioritize the explicit topic and difficulty filters.
        skills = []
        if job_description:
            extracted = self.skill_extractor.extract_skills(job_description)
            skills = extracted.get('all_skills', [])
            
        topic = topic.strip()
        difficulty = difficulty.strip()
        
        # Select relevant questions
        technical = self._select_questions('technical', topic, difficulty, num_questions)
        hr = self._select_questions('hr', topic, difficulty, num_questions)
        behavioral = self._select_questions('behavioral', topic, difficulty, num_questions)
        situational = self._select_questions('situational', topic, difficulty, num_questions)
        
        return {
            'technical': technical,
            'hr': hr,
            'behavioral': behavioral,
            'situational': situational,
            'preparation_tips': self._get_preparation_tips()
        }
    
    def _select_questions(self, category: str, topic: str, difficulty: str, num: int) -> List[Dict]:
        """Select relevant questions from a category, filtering by topic and difficulty."""
        questions = self.questions_db.get(category, [])
        filtered = []
        
        # Determine if we should filter by topic (mostly for technical)
        filter_topic = topic and category == 'technical'
        
        for q in questions:
            # Check difficulty (case insensitive)
            q_diff = q.get('difficulty', '').lower()
            diff_match = not difficulty or q_diff == difficulty.lower()
            
            # Check topic (case insensitive)
            q_topic = q.get('category', '').lower()
            topic_match = not filter_topic or (topic.lower() in q_topic or q_topic in topic.lower())
            
            if diff_match and topic_match:
                filtered.append(q)
                
        # If we filter too strictly and get nothing, try without difficulty
        if not filtered and difficulty:
             for q in questions:
                 q_topic = q.get('category', '').lower()
                 if not filter_topic or (topic.lower() in q_topic or q_topic in topic.lower()):
                     filtered.append(q)

        # If still nothing, return the first N of the category as fallback
        if not filtered:
            filtered = questions

        return filtered[:num]
    
    def _get_preparation_tips(self) -> List[str]:
        """Get general interview preparation tips."""
        return [
            "Research the company and role thoroughly",
            "Prepare specific examples using the STAR method (Situation, Task, Action, Result)",
            "Practice explaining your technical projects and achievements",
            "Prepare thoughtful questions to ask the interviewer",
            "Review common questions for your role and industry",
            "Practice your answers out loud",
            "Prepare for both technical and behavioral questions",
            "Dress appropriately and arrive on time (or log in early for virtual interviews)"
        ]

