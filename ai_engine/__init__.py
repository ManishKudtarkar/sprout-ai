"""
AI Medical Diagnosis Engine

A natural remedy-focused medical diagnosis system that provides
preliminary health assessments and suggests natural remedies.
Enhanced with ChatGPT-like natural language processing.
"""

from .diagnosis import diagnose
from .remedies import get_remedies, get_precautions
from .safety import check_emergency
from .symptoms import SYMPTOM_MAP
from .nlp_processor import SymptomNLPProcessor

__version__ = "2.0.0"
__all__ = ["diagnose", "get_remedies", "get_precautions", "check_emergency", "SYMPTOM_MAP", "analyze_symptoms_conversational"]

# Initialize NLP processor
nlp_processor = SymptomNLPProcessor()


def analyze_symptoms(symptom_text: str):
    """
    Complete symptom analysis including emergency check, diagnosis, and remedies.
    
    Args:
        symptom_text (str): Description of symptoms
        
    Returns:
        dict: Complete analysis including emergency status, diagnosis, remedies, and precautions
    """
    # Check for emergency first
    emergency_result = check_emergency(symptom_text)
    
    if emergency_result["emergency"]:
        return {
            "emergency": emergency_result,
            "diagnosis": None,
            "remedies": [],
            "precautions": [],
            "warning": "EMERGENCY DETECTED - Seek immediate medical attention!"
        }
    
    # Perform diagnosis
    diagnosis_result = diagnose(symptom_text)
    
    # Get remedies and precautions for the diagnosed condition
    remedies = get_remedies(diagnosis_result["condition"])
    precautions = get_precautions(diagnosis_result["condition"])
    
    return {
        "emergency": emergency_result,
        "diagnosis": diagnosis_result,
        "remedies": remedies,
        "precautions": precautions,
        "disclaimer": "This is for informational purposes only. Consult a healthcare professional for proper medical advice."
    }


def analyze_symptoms_conversational(user_input: str):
    """
    ChatGPT-like conversational symptom analysis.
    
    Args:
        user_input (str): Natural language input from user
        
    Returns:
        dict: Conversational response with analysis
    """
    # Process with NLP
    nlp_result = nlp_processor.process_natural_language(user_input)
    
    # Handle different types of input
    if nlp_result["type"] in ["greeting", "system_info", "clarification_needed"]:
        return {
            "type": nlp_result["type"],
            "response": nlp_result["response"],
            "suggestions": nlp_result.get("suggestions", [])
        }
    
    elif nlp_result["type"] == "symptoms_found":
        # Analyze symptoms
        symptoms_text = nlp_result["normalized_text"]
        diagnosis_result = analyze_symptoms(symptoms_text)
        
        # Generate conversational response
        conversational_response = nlp_processor.generate_conversational_response(diagnosis_result)
        
        return {
            "type": "medical_analysis",
            "response": conversational_response,
            "diagnosis_result": diagnosis_result,
            "extracted_symptoms": nlp_result["symptoms"],
            "intensity": nlp_result.get("intensity", "moderate"),
            "duration": nlp_result.get("duration", "unknown")
        }
    
    else:
        return {
            "type": "general",
            "response": "I'm here to help with your health concerns. Please describe your symptoms and I'll do my best to provide helpful information."
        }