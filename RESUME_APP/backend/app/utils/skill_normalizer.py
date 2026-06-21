import json
import os
from typing import List, Set

class SkillNormalizer:
    """Utility for normalizing skill names using synonyms."""
    
    def __init__(self):
        self.synonyms = self._load_synonyms()
        self.normalized_map = self._build_normalized_map()
    
    def _load_synonyms(self) -> dict:
        """Load skill synonyms from JSON file."""
        synonyms_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'data', 'synonyms.json'
        )
        try:
            with open(synonyms_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _build_normalized_map(self) -> dict:
        """Build a map from all variations to normalized skill names."""
        normalized_map = {}
        for normalized, variations in self.synonyms.items():
            for variation in variations:
                normalized_map[variation.lower()] = normalized
            normalized_map[normalized.lower()] = normalized
        return normalized_map
    
    def normalize(self, skill: str) -> str:
        """Normalize a skill name to its canonical form."""
        skill_lower = skill.strip().lower()
        return self.normalized_map.get(skill_lower, skill.strip())
    
    def normalize_list(self, skills: List[str]) -> Set[str]:
        """Normalize a list of skills and return unique normalized skills."""
        return {self.normalize(skill) for skill in skills if skill.strip()}

