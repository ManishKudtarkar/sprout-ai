"""
Natural Remedy Knowledge Base
"""

import json
import os

def load_remedy_database():
    """Load remedy database from JSON file."""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'remedies.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
        return data.get('remedy_database', {}), data.get('disease_precautions', {})
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Fallback to hardcoded data if JSON file is not available
        return {
            "viral infection": [
                {
                    "remedy": "Ginger Tea",
                    "benefit": "Boosts immunity and reduces inflammation",
                    "explanation": "Ginger contains gingerol which helps fight viral infections"
                },
                {
                    "remedy": "Turmeric Milk",
                    "benefit": "Natural antiseptic",
                    "explanation": "Curcumin in turmeric reduces internal inflammation"
                }
            ],
            "common cold": [
                {
                    "remedy": "Tulsi Tea",
                    "benefit": "Relieves congestion",
                    "explanation": "Tulsi has antiviral and immunity boosting properties"
                }
            ],
            "throat infection": [
                {
                    "remedy": "Salt Water Gargle",
                    "benefit": "Kills throat bacteria",
                    "explanation": "Salt reduces swelling and removes infection-causing microbes"
                }
            ],
            "gastric issue": [
                {
                    "remedy": "Aloe Vera Juice",
                    "benefit": "Soothes stomach lining",
                    "explanation": "Aloe reduces acid irritation naturally"
                }
            ],
            "digestive upset": [
                {
                    "remedy": "Jeera Water",
                    "benefit": "Improves digestion",
                    "explanation": "Cumin stimulates digestive enzymes"
                }
            ]
        }, {}

REMEDY_DB, PRECAUTIONS_DB = load_remedy_database()


def get_remedies(condition: str):
    """
    Return list of remedies for a condition.
    """
    return REMEDY_DB.get(condition, [])


def get_precautions(condition: str):
    """
    Return list of precautions for a condition.
    """
    return PRECAUTIONS_DB.get(condition, [])
