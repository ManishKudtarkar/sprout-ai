"""
Comprehensive Symptom Checker
Interactive symptom analysis with guided questions and differential diagnosis
"""

from typing import List, Dict, Set, Tuple
from .advanced_diagnosis import AdvancedDiagnosisEngine
from .enhanced_remedies import EnhancedRemedySystem
from .safety import check_emergency

class ComprehensiveSymptomChecker:
    """Comprehensive symptom checker with guided diagnosis."""
    
    def __init__(self):
        self.diagnosis_engine = AdvancedDiagnosisEngine()
        self.remedy_system = EnhancedRemedySystem()
        self.current_symptoms = []
        self.answered_questions = set()
        self.session_data = {}
    
    def start_symptom_check(self, initial_symptoms: str) -> Dict:
        """Start comprehensive symptom checking process."""
        
        # Reset session
        self.current_symptoms = []
        self.answered_questions = set()
        self.session_data = {
            'initial_input': initial_symptoms,
            'emergency_checked': False,
            'diagnosis_complete': False
        }
        
        # Check for emergency first
        emergency_result = check_emergency(initial_symptoms)
        self.session_data['emergency_checked'] = True
        
        if emergency_result["emergency"]:
            return {
                'type': 'emergency',
                'emergency_info': emergency_result,
                'immediate_actions': self.remedy_system.get_emergency_remedies(
                    emergency_result.get('suspected_condition', 'general')
                ),
                'message': 'MEDICAL EMERGENCY DETECTED - Seek immediate professional help!'
            }
        
        # Extract initial symptoms
        extracted_symptoms = self.diagnosis_engine.extract_symptoms_from_text(initial_symptoms)
        self.current_symptoms.extend(extracted_symptoms)
        
        if not extracted_symptoms:
            return {
                'type': 'clarification_needed',
                'message': 'I need more specific information about your symptoms.',
                'suggestions': self.diagnosis_engine._get_symptom_suggestions(),
                'questions': [
                    'What specific symptoms are you experiencing?',
                    'Where in your body do you feel discomfort?',
                    'How long have you had these symptoms?'
                ]
            }
        
        # Get initial diagnosis
        diagnosis_result = self.diagnosis_engine.advanced_diagnose(initial_symptoms)
        
        # Generate follow-up questions
        follow_up_questions = self._generate_smart_questions(diagnosis_result)
        
        return {
            'type': 'initial_diagnosis',
            'extracted_symptoms': extracted_symptoms,
            'primary_diagnosis': diagnosis_result['primary_diagnosis'],
            'differential_diagnosis': diagnosis_result.get('differential_diagnosis', []),
            'follow_up_questions': follow_up_questions,
            'confidence_level': diagnosis_result['primary_diagnosis']['confidence'],
            'next_action': 'answer_questions' if follow_up_questions else 'get_treatment'
        }
    
    def answer_question(self, question_index: int, answer: str) -> Dict:
        """Process answer to a follow-up question."""
        
        # Mark question as answered
        self.answered_questions.add(question_index)
        
        # Extract additional symptoms from answer
        if answer.lower() in ['yes', 'y', 'yeah', 'yep']:
            # User confirmed a symptom - we need to know which question this was for
            # This would be enhanced with question tracking
            pass
        elif answer.lower() in ['no', 'n', 'nope', 'not really']:
            # User denied a symptom
            pass
        else:
            # User provided descriptive answer - extract symptoms
            additional_symptoms = self.diagnosis_engine.extract_symptoms_from_text(answer)
            self.current_symptoms.extend(additional_symptoms)
        
        # Re-analyze with updated symptoms
        combined_symptoms_text = ' '.join(self.current_symptoms)
        updated_diagnosis = self.diagnosis_engine.advanced_diagnose(combined_symptoms_text)
        
        # Check if we need more questions
        remaining_questions = self._generate_smart_questions(updated_diagnosis)
        
        if not remaining_questions or len(self.answered_questions) >= 5:
            # Diagnosis complete
            return self._generate_final_diagnosis(updated_diagnosis)
        
        return {
            'type': 'continue_questions',
            'updated_diagnosis': updated_diagnosis['primary_diagnosis'],
            'remaining_questions': remaining_questions,
            'progress': f"{len(self.answered_questions)}/5 questions answered"
        }
    
    def _generate_smart_questions(self, diagnosis_result: Dict) -> List[str]:
        """Generate smart follow-up questions based on current diagnosis."""
        
        if not diagnosis_result.get('primary_diagnosis'):
            return []
        
        primary_condition = diagnosis_result['primary_diagnosis']['condition']
        current_symptoms = diagnosis_result.get('extracted_symptoms', [])
        
        # Get condition-specific questions
        questions = self.diagnosis_engine.get_symptom_checker_questions(
            current_symptoms, primary_condition
        )
        
        # Filter out already answered questions
        filtered_questions = []
        for i, question in enumerate(questions):
            if i not in self.answered_questions and len(filtered_questions) < 3:
                filtered_questions.append(question)
        
        return filtered_questions
    
    def _generate_final_diagnosis(self, diagnosis_result: Dict) -> Dict:
        """Generate final comprehensive diagnosis with treatment recommendations."""
        
        primary_diagnosis = diagnosis_result['primary_diagnosis']
        condition = primary_diagnosis['condition']
        
        # Get comprehensive treatment information
        remedies = self.remedy_system.get_remedies(condition)
        precautions = self.remedy_system.get_precautions(condition)
        lifestyle_recommendations = self.remedy_system.get_lifestyle_recommendations(condition)
        dietary_recommendations = self.remedy_system.get_dietary_recommendations(condition)
        
        # Determine urgency level
        urgency = self._determine_urgency(condition, primary_diagnosis['confidence'])
        
        return {
            'type': 'final_diagnosis',
            'primary_diagnosis': primary_diagnosis,
            'differential_diagnosis': diagnosis_result.get('differential_diagnosis', []),
            'treatment_plan': {
                'natural_remedies': remedies,
                'medical_precautions': precautions,
                'lifestyle_changes': lifestyle_recommendations,
                'dietary_recommendations': dietary_recommendations
            },
            'urgency_level': urgency,
            'follow_up_recommendations': self._get_follow_up_recommendations(condition, urgency),
            'when_to_seek_help': self._get_when_to_seek_help(condition),
            'total_symptoms_analyzed': len(self.current_symptoms),
            'session_summary': {
                'initial_input': self.session_data.get('initial_input', ''),
                'questions_answered': len(self.answered_questions),
                'symptoms_identified': self.current_symptoms
            }
        }
    
    def _determine_urgency(self, condition: str, confidence: str) -> str:
        """Determine urgency level for medical attention."""
        
        high_urgency_conditions = [
            'heart attack', 'paralysis (brain hemorrhage)', 'hepatitis e',
            'acute liver failure', 'pneumonia'
        ]
        
        medium_urgency_conditions = [
            'diabetes', 'hypertension', 'bronchial asthma', 'tuberculosis',
            'hepatitis a', 'hepatitis b', 'hepatitis c'
        ]
        
        if condition in high_urgency_conditions:
            return 'high'
        elif condition in medium_urgency_conditions:
            return 'medium'
        elif confidence in ['very high', 'high']:
            return 'medium'
        else:
            return 'low'
    
    def _get_follow_up_recommendations(self, condition: str, urgency: str) -> List[str]:
        """Get follow-up recommendations based on condition and urgency."""
        
        if urgency == 'high':
            return [
                'Seek immediate medical attention',
                'Go to emergency room or call 911',
                'Do not delay professional medical care'
            ]
        elif urgency == 'medium':
            return [
                'Schedule appointment with healthcare provider within 1-2 days',
                'Monitor symptoms closely',
                'Seek immediate care if symptoms worsen',
                'Follow prescribed treatments if any'
            ]
        else:
            return [
                'Monitor symptoms for 3-5 days',
                'Try natural remedies and lifestyle changes',
                'See healthcare provider if symptoms persist or worsen',
                'Keep a symptom diary'
            ]
    
    def _get_when_to_seek_help(self, condition: str) -> List[str]:
        """Get specific warning signs for when to seek immediate help."""
        
        warning_signs = {
            'diabetes': [
                'Blood sugar over 300 mg/dL',
                'Severe dehydration',
                'Difficulty breathing',
                'Persistent vomiting'
            ],
            'hypertension': [
                'Blood pressure over 180/120',
                'Severe headache',
                'Chest pain',
                'Difficulty breathing',
                'Vision changes'
            ],
            'asthma': [
                'Severe difficulty breathing',
                'Cannot speak in full sentences',
                'Blue lips or fingernails',
                'Peak flow less than 50% of personal best'
            ],
            'common cold': [
                'Fever over 103°F (39.4°C)',
                'Symptoms lasting more than 10 days',
                'Severe headache or sinus pain',
                'Difficulty breathing'
            ]
        }
        
        return warning_signs.get(condition, [
            'Symptoms significantly worsen',
            'New concerning symptoms develop',
            'High fever (over 103°F/39.4°C)',
            'Difficulty breathing',
            'Severe pain',
            'Signs of dehydration'
        ])
    
    def get_condition_overview(self, condition: str) -> Dict:
        """Get comprehensive overview of a medical condition."""
        
        condition_overviews = {
            'diabetes': {
                'description': 'A group of metabolic disorders characterized by high blood sugar levels',
                'causes': ['Insulin resistance', 'Autoimmune destruction of beta cells', 'Genetic factors'],
                'risk_factors': ['Obesity', 'Family history', 'Sedentary lifestyle', 'Age over 45'],
                'complications': ['Heart disease', 'Kidney damage', 'Nerve damage', 'Eye problems'],
                'prognosis': 'Well-managed diabetes allows for normal life expectancy'
            },
            'hypertension': {
                'description': 'Persistently elevated blood pressure in the arteries',
                'causes': ['Unknown (primary)', 'Kidney disease', 'Hormonal disorders', 'Medications'],
                'risk_factors': ['Age', 'Family history', 'Obesity', 'High sodium diet', 'Stress'],
                'complications': ['Heart attack', 'Stroke', 'Kidney disease', 'Heart failure'],
                'prognosis': 'Excellent with proper management and lifestyle changes'
            }
        }
        
        return condition_overviews.get(condition, {
            'description': f'Information about {condition} is being compiled.',
            'note': 'Consult healthcare provider for detailed information about this condition.'
        })