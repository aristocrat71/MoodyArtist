import json
from typing import Dict, List, Tuple

def load_art_styles() -> Dict[str, List[str]]:
    """Load art styles from JSON file"""
    try:
        with open('art-styles.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def validate_preferences(data: Dict) -> Tuple[bool, str]:
    """
    Validate preferences input
    Returns: (is_valid, error_message)
    """
    # Check required fields
    required_fields = ['experience', 'artform', 'moods']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate experience level
    valid_experiences = ["Beginner", "Somewhat good?", "Experttt"]
    if data['experience'] not in valid_experiences:
        return False, f"Invalid experience level. Must be one of: {valid_experiences}"
    
    # Validate art form based on experience level
    art_styles = load_art_styles()
    if data['experience'] in art_styles:
        valid_artforms = art_styles[data['experience']]
        if data['artform'] not in valid_artforms:
            return False, f"Invalid art form for {data['experience']} level. Must be one of: {valid_artforms}"
    
    # Validate moods
    if not isinstance(data['moods'], list):
        return False, "Moods must be a list"
    
    if len(data['moods']) < 1:
        return False, "At least one mood word is required"
    
    for mood in data['moods']:
        if not isinstance(mood, str) or not mood.strip():
            return False, "All mood words must be non-empty strings"
    
    return True, ""

def get_art_forms_for_experience(experience: str) -> List[str]:
    """Get available art forms for a given experience level"""
    art_styles = load_art_styles()
    return art_styles.get(experience, []) 