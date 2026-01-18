"""
AI Medical Diagnosis Engine

A natural remedy-focused medical diagnosis system that provides
preliminary health assessments and suggests natural remedies.
Enhanced with ChatGPT-like natural language processing and advanced diagnosis.
"""

from .diagnosis import diagnose
from .remedies import get_remedies, get_precautions
from .safety import check_emergency
from .symptoms import SYMPTOM_MAP
from .nlp_processor import SymptomNLPProcessor
from .advanced_diagnosis import AdvancedDiagnosisEngine
from .enhanced_remedies import EnhancedRemedySystem
from .symptom_checker import ComprehensiveSymptomChecker

__version__ = "3.0.0"
__all__ = [
    "diagnose", "get_remedies", "get_precautions", "check_emergency", "SYMPTOM_MAP", 
    "analyze_symptoms_conversational", "advanced_analyze_symptoms", "comprehensive_symptom_check",
    "AdvancedDiagnosisEngine", "EnhancedRemedySystem", "ComprehensiveSymptomChecker"
]

# Initialize advanced systems
nlp_processor = SymptomNLPProcessor()
advanced_diagnosis_engine = AdvancedDiagnosisEngine()
enhanced_remedy_system = EnhancedRemedySystem()
comprehensive_symptom_checker = ComprehensiveSymptomChecker()


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


def advanced_analyze_symptoms(symptom_text: str):
    """
    Advanced symptom analysis with differential diagnosis and comprehensive remedies.
    
    Args:
        symptom_text (str): Description of symptoms
        
    Returns:
        dict: Advanced analysis with multiple diagnoses, confidence scores, and comprehensive treatment
    """
    # Check for emergency first
    emergency_result = check_emergency(symptom_text)
    
    if emergency_result["emergency"]:
        emergency_remedies = enhanced_remedy_system.get_emergency_remedies(
            emergency_result.get('suspected_condition', 'general')
        )
        return {
            "type": "emergency",
            "emergency": emergency_result,
            "emergency_remedies": emergency_remedies,
            "warning": "MEDICAL EMERGENCY DETECTED - Seek immediate professional help!"
        }
    
    # Perform advanced diagnosis
    advanced_diagnosis = advanced_diagnosis_engine.advanced_diagnose(symptom_text)
    
    if advanced_diagnosis['primary_diagnosis']['condition'] == 'unknown':
        return {
            "type": "unknown",
            "message": advanced_diagnosis['primary_diagnosis']['message'],
            "suggestions": advanced_diagnosis.get('suggestions', []),
            "extracted_symptoms": advanced_diagnosis.get('extracted_symptoms', [])
        }
    
    # Get comprehensive treatment information
    primary_condition = advanced_diagnosis['primary_diagnosis']['condition']
    remedies = enhanced_remedy_system.get_remedies(primary_condition)
    precautions = enhanced_remedy_system.get_precautions(primary_condition)
    lifestyle_recommendations = enhanced_remedy_system.get_lifestyle_recommendations(primary_condition)
    dietary_recommendations = enhanced_remedy_system.get_dietary_recommendations(primary_condition)
    
    return {
        "type": "advanced_diagnosis",
        "primary_diagnosis": advanced_diagnosis['primary_diagnosis'],
        "differential_diagnosis": advanced_diagnosis.get('differential_diagnosis', []),
        "treatment_plan": {
            "natural_remedies": remedies,
            "medical_precautions": precautions,
            "lifestyle_recommendations": lifestyle_recommendations,
            "dietary_recommendations": dietary_recommendations
        },
        "extracted_symptoms": advanced_diagnosis.get('extracted_symptoms', []),
        "total_symptoms_analyzed": advanced_diagnosis.get('total_symptoms_analyzed', 0),
        "disclaimer": "This is for informational purposes only. Consult a healthcare professional for proper medical advice."
    }


def comprehensive_symptom_check(symptom_text: str):
    """
    Start comprehensive symptom checking with guided questions.
    
    Args:
        symptom_text (str): Initial symptom description
        
    Returns:
        dict: Comprehensive symptom check result with follow-up questions
    """
    return comprehensive_symptom_checker.start_symptom_check(symptom_text)


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