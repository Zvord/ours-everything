"""
Data models and structures for the Russian Noun Cases Drill application.
"""

import json
import os
import random
from typing import Dict, List, Tuple, Optional, Any

class DrillData:
    """Class to manage drill data and operations."""

    def __init__(self):
        """Initialize the drill data."""
        self.case_options = {
            "nomn": "Nominative",
            "gent": "Genitive",
            "datv": "Dative",
            "accs": "Accusative",
            "ablt": "Instrumental",
            "loct": "Prepositional"
        }

        self.number_options = {
            "sing": "Singular",
            "plur": "Plural"
        }

        # Load data from JSON files
        self.top_nouns = self._load_nouns()
        self.insert_sentences = self._load_sentences()

    def _load_nouns(self) -> List[str]:
        """Load nouns from the JSON file."""
        try:
            with open(os.path.join('data', 'nouns.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('top_nouns', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading nouns: {e}")
            # Fallback to hardcoded list if file can't be loaded
            return [
                "слово", "человек", "время", "дело", "жизнь",
                "день", "рука", "работа", "место", "право"
            ]

    def _load_sentences(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load insert drill sentences from the JSON file."""
        try:
            with open(os.path.join('data', 'sentences.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('insert_sentences', {})
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading sentences: {e}")
            # Return empty dict if file can't be loaded
            return {}

    def get_case_options(self, lang: str) -> Dict[str, str]:
        """Get case options based on language."""
        if lang == 'ru':
            return {
                "nomn": "Именительный",
                "gent": "Родительный",
                "datv": "Дательный",
                "accs": "Винительный",
                "ablt": "Творительный",
                "loct": "Предложный"
            }
        return self.case_options

    def get_number_options(self, lang: str) -> Dict[str, str]:
        """Get number options based on language."""
        if lang == 'ru':
            return {
                "sing": "Единственное число",
                "plur": "Множественное число"
            }
        return self.number_options

    def get_random_noun(self) -> str:
        """Get a random noun from the list."""
        return random.choice(self.top_nouns)

    def get_random_sentence(self) -> Tuple[str, Dict[str, Any]]:
        """Get a random sentence for the insert drill."""
        if not self.insert_sentences:
            return "", {}

        # Choose a random case
        chosen_case = random.choice(list(self.insert_sentences.keys()))
        # Choose a random sentence from that case
        sentence_data = random.choice(self.insert_sentences[chosen_case])

        return chosen_case, sentence_data
