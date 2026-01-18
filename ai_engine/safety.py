"""
Emergency Detection Logic
"""

import json
import os

def load_emergency_symptoms():
    """Load emergency symptoms from JSON file."""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'remedies.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
        return data['emergency_symptoms']
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Fallback to hardcoded data if JSON file is not available
        return [
            "chest pain",
            "difficulty breathing",
            "severe bleeding",
            "unconscious",
            "seizure",
            "high fever",
            "blurred vision",
            "severe headache"
        ]

EMERGENCY_SYMPTOMS = load_emergency_symptoms()


def check_emergency(symptom_text: str):
    """
    Detect emergency symptoms.
    """
    symptom_text = symptom_text.lower()

    for danger in EMERGENCY_SYMPTOMS:
        if danger in symptom_text:
            return {
                "emergency": True,
                "level": "critical",
                "message": "Possible medical emergency detected. Seek immediate medical help."
            }

    return {
        "emergency": False,
        "level": "normal"
    }
