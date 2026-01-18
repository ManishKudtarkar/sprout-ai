"""
Advanced Medical Diagnosis Engine
Enhanced with comprehensive symptom analysis and disease correlation
"""

import json
import os
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set
import re

class AdvancedDiagnosisEngine:
    """Advanced diagnosis engine with multi-symptom analysis and confidence scoring."""
    
    def __init__(self):
        self.symptom_map = {}
        self.disease_symptoms = {}
        self.symptom_weights = {}
        self.disease_prevalence = {}
        self.load_medical_data()
        self.calculate_symptom_weights()
    
    def load_medical_data(self):
        """Load comprehensive medical data from symptoms.json."""
        try:
            data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'symptoms.json')
            with open(data_path, 'r') as f:
                data = json.load(f)
            
            self.symptom_map = data.get('symptom_map', {})
            self.disease_symptoms = data.get('disease_symptoms', {})
            
            # Calculate disease prevalence based on symptom count
            for disease, symptoms in self.disease_symptoms.items():
                self.disease_prevalence[disease] = len(symptoms)
                
        except Exception as e:
            print(f"Error loading medical data: {e}")
            self.symptom_map = {}
            self.disease_symptoms = {}
    
    def calculate_symptom_weights(self):
        """Calculate weights for symptoms based on their specificity."""
        symptom_disease_count = defaultdict(int)
        
        # Count how many diseases each symptom appears in
        for disease, symptoms in self.disease_symptoms.items():
            for symptom in symptoms:
                symptom_disease_count[symptom] += 1
        
        # Calculate weights (more specific symptoms get higher weights)
        total_diseases = len(self.disease_symptoms)
        for symptom, disease_count in symptom_disease_count.items():
            # Inverse frequency weighting - rare symptoms are more diagnostic
            self.symptom_weights[symptom] = max(1.0, total_diseases / disease_count)
    
    def extract_symptoms_from_text(self, text: str) -> List[str]:
        """Extract symptoms from natural language text."""
        text = text.lower().strip()
        found_symptoms = []
        
        # Direct matching
        for symptom in self.symptom_map.keys():
            if symptom in text:
                found_symptoms.append(symptom)
        
        # Fuzzy matching for common variations
        symptom_variations = {
            'headache': ['head pain', 'head ache', 'migraine'],
            'stomach pain': ['belly pain', 'tummy ache', 'abdominal pain'],
            'chest pain': ['chest ache', 'heart pain'],
            'joint pain': ['arthritis pain', 'bone pain'],
            'muscle pain': ['body ache', 'muscle ache'],
            'high fever': ['fever', 'temperature', 'hot'],
            'cough': ['coughing', 'dry cough'],
            'vomiting': ['throwing up', 'nausea', 'sick'],
            'diarrhea': ['loose motion', 'loose stool'],
            'fatigue': ['tired', 'exhausted', 'weakness'],
            'breathlessness': ['shortness of breath', 'difficulty breathing']
        }
        
        for standard_symptom, variations in symptom_variations.items():
            if standard_symptom not in found_symptoms:
                for variation in variations:
                    if variation in text:
                        if standard_symptom in self.symptom_map:
                            found_symptoms.append(standard_symptom)
                        break
        
        return list(set(found_symptoms))
    
    def calculate_disease_probability(self, symptoms: List[str]) -> Dict[str, float]:
        """Calculate probability scores for diseases based on symptoms."""
        disease_scores = defaultdict(float)
        
        if not symptoms:
            return {}
        
        # Score diseases based on symptom matches
        for symptom in symptoms:
            if symptom in self.symptom_map:
                primary_disease = self.symptom_map[symptom]
                weight = self.symptom_weights.get(symptom, 1.0)
                disease_scores[primary_disease] += weight
        
        # Also check reverse mapping from disease_symptoms
        for disease, disease_symptom_list in self.disease_symptoms.items():
            matched_symptoms = set(symptoms) & set(disease_symptom_list)
            if matched_symptoms:
                # Calculate match percentage
                match_percentage = len(matched_symptoms) / len(disease_symptom_list)
                # Weight by symptom specificity
                weighted_score = sum(self.symptom_weights.get(s, 1.0) for s in matched_symptoms)
                disease_scores[disease] += match_percentage * weighted_score
        
        # Normalize scores
        if disease_scores:
            max_score = max(disease_scores.values())
            for disease in disease_scores:
                disease_scores[disease] = disease_scores[disease] / max_score
        
        return dict(disease_scores)
    
    def get_confidence_level(self, top_score: float, symptom_count: int) -> str:
        """Determine confidence level based on score and symptom count."""
        if top_score >= 0.8 and symptom_count >= 3:
            return "very high"
        elif top_score >= 0.6 and symptom_count >= 2:
            return "high"
        elif top_score >= 0.4:
            return "medium"
        elif top_score >= 0.2:
            return "low"
        else:
            return "very low"
    
    def get_related_symptoms(self, disease: str) -> List[str]:
        """Get all symptoms related to a disease."""
        return self.disease_symptoms.get(disease, [])
    
    def get_differential_diagnosis(self, symptoms: List[str], top_n: int = 3) -> List[Dict]:
        """Get differential diagnosis with multiple possible conditions."""
        disease_scores = self.calculate_disease_probability(symptoms)
        
        # Sort by score
        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for i, (disease, score) in enumerate(sorted_diseases[:top_n]):
            confidence = self.get_confidence_level(score, len(symptoms))
            
            # Get matching and missing symptoms
            disease_symptom_set = set(self.disease_symptoms.get(disease, []))
            user_symptom_set = set(symptoms)
            
            matching_symptoms = list(disease_symptom_set & user_symptom_set)
            missing_symptoms = list(disease_symptom_set - user_symptom_set)
            
            results.append({
                'disease': disease,
                'confidence': confidence,
                'score': round(score, 3),
                'rank': i + 1,
                'matching_symptoms': matching_symptoms,
                'missing_symptoms': missing_symptoms[:5],  # Top 5 missing symptoms
                'total_disease_symptoms': len(disease_symptom_set)
            })
        
        return results
    
    def advanced_diagnose(self, symptom_text: str) -> Dict:
        """Perform advanced diagnosis with multiple possibilities."""
        # Extract symptoms
        symptoms = self.extract_symptoms_from_text(symptom_text)
        
        if not symptoms:
            return {
                'primary_diagnosis': {
                    'condition': 'unknown',
                    'confidence': 'very low',
                    'message': 'No recognizable symptoms found. Please describe your symptoms more specifically.'
                },
                'differential_diagnosis': [],
                'extracted_symptoms': [],
                'suggestions': self._get_symptom_suggestions()
            }
        
        # Get differential diagnosis
        differential = self.get_differential_diagnosis(symptoms)
        
        if not differential:
            return {
                'primary_diagnosis': {
                    'condition': 'unknown',
                    'confidence': 'very low',
                    'message': 'Unable to match symptoms to known conditions.'
                },
                'differential_diagnosis': [],
                'extracted_symptoms': symptoms,
                'suggestions': []
            }
        
        # Primary diagnosis is the top result
        primary = differential[0]
        
        return {
            'primary_diagnosis': {
                'condition': primary['disease'],
                'confidence': primary['confidence'],
                'score': primary['score'],
                'matching_symptoms': primary['matching_symptoms'],
                'missing_symptoms': primary['missing_symptoms']
            },
            'differential_diagnosis': differential[1:],  # Alternative diagnoses
            'extracted_symptoms': symptoms,
            'total_symptoms_analyzed': len(symptoms)
        }
    
    def _get_symptom_suggestions(self) -> List[str]:
        """Get common symptom suggestions."""
        common_symptoms = [
            'fever', 'headache', 'cough', 'stomach pain', 'chest pain',
            'fatigue', 'nausea', 'vomiting', 'diarrhea', 'joint pain',
            'muscle pain', 'skin rash', 'breathlessness', 'dizziness'
        ]
        return [s for s in common_symptoms if s in self.symptom_map]
    
    def get_symptom_checker_questions(self, current_symptoms: List[str], suspected_disease: str) -> List[str]:
        """Generate follow-up questions to improve diagnosis accuracy."""
        if suspected_disease not in self.disease_symptoms:
            return []
        
        disease_symptoms = set(self.disease_symptoms[suspected_disease])
        current_symptom_set = set(current_symptoms)
        missing_symptoms = disease_symptoms - current_symptom_set
        
        # Convert to questions
        questions = []
        symptom_to_question = {
            'high fever': 'Do you have a high fever (over 101°F/38.3°C)?',
            'chest pain': 'Are you experiencing any chest pain or discomfort?',
            'breathlessness': 'Do you have difficulty breathing or shortness of breath?',
            'fatigue': 'Are you feeling unusually tired or fatigued?',
            'headache': 'Do you have a headache?',
            'nausea': 'Are you feeling nauseous or sick to your stomach?',
            'vomiting': 'Have you been vomiting?',
            'diarrhea': 'Do you have diarrhea or loose stools?',
            'joint pain': 'Are you experiencing any joint pain?',
            'muscle pain': 'Do you have muscle aches or pain?',
            'skin rash': 'Do you have any skin rash or skin changes?',
            'weight loss': 'Have you experienced unexplained weight loss?',
            'loss of appetite': 'Have you lost your appetite?',
            'sweating': 'Are you experiencing excessive sweating?',
            'dizziness': 'Do you feel dizzy or lightheaded?'
        }
        
        for symptom in list(missing_symptoms)[:5]:  # Top 5 questions
            if symptom in symptom_to_question:
                questions.append(symptom_to_question[symptom])
        
        return questions