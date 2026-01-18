"""
Symptom to Condition Mapping
"""

import json
import os

def load_symptom_map():
    """Load symptom mapping from JSON file."""
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'symptoms.json')
        with open(data_path, 'r') as f:
            data = json.load(f)
        return data['symptom_map']
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        # Fallback to hardcoded data if JSON file is not available
        return {
            "fever": "viral infection",
            "high temperature": "viral infection",
            "cold": "common cold",
            "runny nose": "common cold",
            "cough": "respiratory irritation",
            "dry cough": "respiratory irritation",
            "sore throat": "throat infection",
            "throat pain": "throat infection",
            "body pain": "viral infection",
            "headache": "stress or dehydration",
            "acidity": "gastric issue",
            "burning sensation": "gastric issue",
            "stomach pain": "gastric issue",
            "vomiting": "digestive upset",
            "loose motion": "digestive upset"
        }

SYMPTOM_MAP = load_symptom_map()
