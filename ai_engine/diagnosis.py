"""
Core Diagnosis Logic
"""

from .symptoms import SYMPTOM_MAP


def diagnose(symptom_text: str):
    """
    Diagnose condition based on symptom keywords.
    """
    symptom_text = symptom_text.lower()

    matched_conditions = []

    for symptom, condition in SYMPTOM_MAP.items():
        if symptom in symptom_text:
            matched_conditions.append(condition)

    if not matched_conditions:
        return {
            "condition": "unknown",
            "confidence": "low",
            "message": "Symptoms are unclear. Please consult a doctor if they persist."
        }

    # Most frequent condition
    final_condition = max(set(matched_conditions), key=matched_conditions.count)

    confidence = "high" if len(matched_conditions) >= 2 else "medium"

    return {
        "condition": final_condition,
        "confidence": confidence
    }
