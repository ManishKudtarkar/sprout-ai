"""
Natural Language Processing for Medical Symptoms
Enhanced conversational understanding like ChatGPT
"""

import re
from typing import List, Dict, Tuple

class SymptomNLPProcessor:
    """Process natural language symptom descriptions."""
    
    def __init__(self):
        # Common symptom synonyms and variations
        self.symptom_synonyms = {
            # Pain variations
            "hurt": "pain", "hurts": "pain", "ache": "pain", "aches": "pain",
            "sore": "pain", "tender": "pain", "throbbing": "pain",
            
            # Fever variations
            "hot": "fever", "burning up": "fever", "temperature": "fever",
            "feverish": "fever", "chills": "fever", "shivering": "fever",
            
            # Digestive variations
            "nausea": "vomiting", "sick to stomach": "vomiting", "queasy": "vomiting",
            "throw up": "vomiting", "upset stomach": "stomach pain",
            "tummy ache": "stomach pain", "belly pain": "stomach pain",
            
            # Respiratory variations
            "stuffy nose": "runny nose", "congested": "runny nose",
            "blocked nose": "runny nose", "sniffles": "runny nose",
            "wheezing": "difficulty breathing", "short of breath": "difficulty breathing",
            
            # Skin variations
            "rash": "skin rash", "bumps": "skin rash", "spots": "skin rash",
            "red skin": "skin rash", "irritated skin": "itching",
            
            # Head variations
            "migraine": "headache", "head pain": "headache",
            "dizzy": "headache", "lightheaded": "headache",
            
            # Throat variations
            "scratchy throat": "sore throat", "throat hurts": "sore throat",
            "swollen throat": "sore throat",
            
            # Energy variations
            "tired": "fatigue", "exhausted": "fatigue", "weak": "fatigue",
            "no energy": "fatigue", "worn out": "fatigue"
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            "severe": 3, "extreme": 3, "terrible": 3, "awful": 3,
            "bad": 2, "strong": 2, "intense": 2, "sharp": 2,
            "mild": 1, "slight": 1, "little": 1, "minor": 1
        }
        
        # Duration indicators
        self.duration_patterns = {
            r"for (\d+) days?": "chronic",
            r"(\d+) days? ago": "recent",
            r"all week": "chronic",
            r"since yesterday": "recent",
            r"just started": "acute",
            r"suddenly": "acute",
            r"gradually": "chronic"
        }
        
        # Question patterns for follow-up
        self.clarification_questions = {
            "pain": [
                "Can you describe the type of pain? (sharp, dull, throbbing, burning)",
                "Where exactly is the pain located?",
                "On a scale of 1-10, how severe is the pain?"
            ],
            "fever": [
                "Do you have chills or sweating?",
                "Have you measured your temperature?",
                "Are you experiencing body aches along with the fever?"
            ],
            "headache": [
                "Is it a throbbing or constant headache?",
                "Where in your head do you feel it most?",
                "Are you sensitive to light or sound?"
            ],
            "stomach": [
                "Is the pain cramping, burning, or sharp?",
                "Have you eaten anything unusual recently?",
                "Are you experiencing nausea or vomiting?"
            ]
        }

    def process_natural_language(self, text: str) -> Dict:
        """Process natural language symptom description."""
        text = text.lower().strip()
        
        # Handle common conversational patterns
        if self._is_greeting(text):
            return {
                "type": "greeting",
                "response": "Hello! I'm here to help analyze your symptoms. Please describe how you're feeling or what symptoms you're experiencing."
            }
        
        if self._is_question_about_system(text):
            return {
                "type": "system_info",
                "response": "I'm an AI medical diagnosis assistant that can help analyze symptoms and suggest natural remedies. I can recognize over 160 different symptoms and provide information about 40+ medical conditions. What symptoms are you experiencing?"
            }
        
        # Extract and normalize symptoms
        extracted_symptoms = self._extract_symptoms(text)
        intensity = self._extract_intensity(text)
        duration = self._extract_duration(text)
        
        # Generate conversational response
        if not extracted_symptoms:
            return {
                "type": "clarification_needed",
                "response": self._generate_clarification_response(text),
                "suggestions": self._get_symptom_suggestions()
            }
        
        return {
            "type": "symptoms_found",
            "symptoms": extracted_symptoms,
            "intensity": intensity,
            "duration": duration,
            "normalized_text": " ".join(extracted_symptoms)
        }
    
    def _is_greeting(self, text: str) -> bool:
        """Check if text is a greeting."""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        # Don't treat emergency symptoms as greetings
        emergency_keywords = ["chest pain", "difficulty breathing", "severe bleeding", "unconscious", "seizure"]
        
        if any(emergency in text for emergency in emergency_keywords):
            return False
            
        return any(greeting in text for greeting in greetings)
    
    def _is_question_about_system(self, text: str) -> bool:
        """Check if user is asking about the system."""
        system_questions = [
            "what can you do", "how do you work", "what are you",
            "help me", "what is this", "how does this work"
        ]
        return any(question in text for question in system_questions)
    
    def _extract_symptoms(self, text: str) -> List[str]:
        """Extract and normalize symptoms from text."""
        symptoms = []
        
        # Replace synonyms first
        normalized_text = text
        for synonym, standard in self.symptom_synonyms.items():
            if synonym in normalized_text:
                normalized_text = normalized_text.replace(synonym, standard)
        
        # Direct symptom matching from our database (prioritize exact matches)
        from .symptoms import SYMPTOM_MAP
        for symptom in SYMPTOM_MAP.keys():
            if symptom in normalized_text:
                symptoms.append(symptom)
        
        # If no direct matches found, try more aggressive extraction
        if not symptoms:
            # Check if the entire input is a single symptom or close to it
            cleaned_input = normalized_text.strip().lower()
            
            # Direct match check
            if cleaned_input in SYMPTOM_MAP:
                symptoms.append(cleaned_input)
            else:
                # Partial matching for single words
                words = cleaned_input.split()
                if len(words) == 1:
                    word = words[0]
                    # Check if this word is part of any known symptom
                    for symptom in SYMPTOM_MAP.keys():
                        if word in symptom.split():
                            symptoms.append(symptom)
                            break
        
        # Enhanced symptom extraction patterns
        if not symptoms:
            symptom_patterns = [
                r"i have (?:a |an |some |really |very |quite |pretty |)?(?:bad |severe |terrible |awful |mild |slight |little |minor |)?(.*?)(?:\s+and|\s*,|\s*$|\s+that|\s+which)",
                r"i'm feeling (.*?)(?:\s+and|\s*,|\s*$)",
                r"experiencing (.*?)(?:\s+and|\s*,|\s*$)",
                r"my (.*?) (?:hurts?|aches?|is sore|feels? bad|feels? terrible|really hurts?)",
                r"(headache|fever|nausea|vomiting|cough|pain|ache|sick|hurt|hurts)",
                r"feeling (nauseous|sick|dizzy|tired|weak|feverish)",
                r"(itching|burning|throbbing|sharp|dull) (?:pain|sensation|feeling)",
                r"(?:really |very |quite |)?(sick|nauseous|hurt|pain|ache|fever|headache|cough)",
                r"stomach (?:really |very |)?(?:hurts?|aches?|pain)",
                r"feel (?:really |very |)?sick"
            ]
            
            for pattern in symptom_patterns:
                matches = re.findall(pattern, normalized_text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0] if match[0] else match[1] if len(match) > 1 else ""
                    
                    cleaned = self._clean_symptom_text(match.strip())
                    if cleaned and len(cleaned.split()) <= 4:
                        # Map common terms to our symptom database
                        mapped_symptom = self._map_to_known_symptoms(cleaned)
                        if mapped_symptom:
                            symptoms.extend(mapped_symptom)
        
        # Special case handling for complex phrases
        if "stomach" in normalized_text and ("hurt" in normalized_text or "pain" in normalized_text):
            symptoms.append("stomach pain")
        
        if "sick" in normalized_text and "stomach" in normalized_text:
            symptoms.append("vomiting")
        
        if "head" in normalized_text and ("hurt" in normalized_text or "pain" in normalized_text):
            symptoms.append("headache")
        
        return list(set(symptoms))  # Remove duplicates
    
    def _map_to_known_symptoms(self, symptom_text: str) -> List[str]:
        """Map extracted text to known symptoms in our database."""
        from .symptoms import SYMPTOM_MAP
        
        mapped = []
        symptom_text = symptom_text.lower()
        
        # Direct matches
        if symptom_text in SYMPTOM_MAP:
            mapped.append(symptom_text)
            return mapped
        
        # Partial matches and mappings
        symptom_mappings = {
            "headache": ["headache"],
            "head pain": ["headache"],
            "nauseous": ["vomiting"],
            "sick": ["vomiting"],
            "queasy": ["vomiting"],
            "stomach": ["stomach pain"],
            "belly": ["stomach pain"],
            "tummy": ["stomach pain"],
            "throat": ["sore throat"],
            "nose": ["runny nose"],
            "stuffy": ["runny nose"],
            "congested": ["runny nose"],
            "temperature": ["fever"],
            "hot": ["fever"],
            "chills": ["fever"],
            "shivering": ["fever"],
            "ache": ["body pain"],
            "aches": ["body pain"],
            "tired": ["fatigue"],
            "exhausted": ["fatigue"],
            "weak": ["fatigue"],
            "rash": ["skin rash"],
            "itchy": ["itching"],
            "scratchy": ["itching"],
            "burning": ["burning sensation"],
            "acid": ["acidity"],
            "heartburn": ["acidity"]
        }
        
        for key, symptoms in symptom_mappings.items():
            if key in symptom_text:
                mapped.extend(symptoms)
        
        # Check for compound symptoms
        if "head" in symptom_text and ("pain" in symptom_text or "ache" in symptom_text or "hurt" in symptom_text):
            mapped.append("headache")
        
        if "stomach" in symptom_text and ("pain" in symptom_text or "hurt" in symptom_text or "ache" in symptom_text):
            mapped.append("stomach pain")
            
        if "throat" in symptom_text and ("pain" in symptom_text or "sore" in symptom_text or "hurt" in symptom_text):
            mapped.append("sore throat")
        
        if "sick" in symptom_text and ("stomach" in symptom_text or "nausea" in symptom_text):
            mapped.append("vomiting")
        
        return mapped
    
    def _clean_symptom_text(self, text: str) -> str:
        """Clean and normalize symptom text."""
        # Remove common filler words
        filler_words = ["a", "an", "the", "some", "really", "very", "quite", "pretty", "kind of"]
        words = text.split()
        cleaned_words = [word for word in words if word not in filler_words]
        return " ".join(cleaned_words)
    
    def _extract_intensity(self, text: str) -> str:
        """Extract symptom intensity."""
        for modifier, level in self.intensity_modifiers.items():
            if modifier in text:
                if level == 3:
                    return "severe"
                elif level == 2:
                    return "moderate"
                else:
                    return "mild"
        return "moderate"  # Default
    
    def _extract_duration(self, text: str) -> str:
        """Extract symptom duration."""
        for pattern, duration_type in self.duration_patterns.items():
            if re.search(pattern, text):
                return duration_type
        return "unknown"
    
    def _generate_clarification_response(self, text: str) -> str:
        """Generate helpful clarification response."""
        
        # If user typed a single word that might be a symptom, be more helpful
        if len(text.split()) == 1:
            word = text.lower().strip()
            
            # Check if it's a known symptom
            from .symptoms import SYMPTOM_MAP
            if word in SYMPTOM_MAP:
                return f"I see you mentioned '{word}'. Let me analyze that for you. For a more complete assessment, you could also tell me about any other symptoms you're experiencing."
            
            # Check if it's a partial symptom match
            partial_matches = [symptom for symptom in SYMPTOM_MAP.keys() if word in symptom]
            if partial_matches:
                return f"I see you mentioned '{word}'. This could relate to: {', '.join(partial_matches[:3])}. Could you be more specific about your symptoms?"
        
        responses = [
            "I'd like to help you better. Could you describe your symptoms more specifically?",
            "To provide accurate information, please tell me what specific symptoms you're experiencing.",
            "I can help analyze your symptoms. What exactly are you feeling? For example, do you have pain, fever, nausea, or other symptoms?",
            "Let me help you. Please describe your symptoms in more detail - what part of your body is affected and how you're feeling."
        ]
        
        # Try to be more specific based on partial information
        if "pain" in text or "hurt" in text:
            return "I see you mentioned pain. Can you tell me where the pain is located and what type of pain it is?"
        elif "sick" in text or "unwell" in text:
            return "I understand you're not feeling well. Can you describe your specific symptoms? For example, do you have fever, nausea, headache, or other symptoms?"
        elif "tired" in text or "fatigue" in text:
            return "Fatigue can have many causes. Are you experiencing any other symptoms along with tiredness, such as fever, headache, or body aches?"
        
        return responses[0]
    
    def _get_symptom_suggestions(self) -> List[str]:
        """Get common symptom suggestions."""
        return [
            "fever or high temperature",
            "headache or head pain", 
            "cough or throat problems",
            "stomach pain or nausea",
            "body aches or joint pain",
            "skin rash or itching",
            "difficulty breathing",
            "runny or stuffy nose"
        ]

    def generate_conversational_response(self, diagnosis_result: Dict) -> str:
        """Generate a conversational response like ChatGPT."""
        if diagnosis_result.get("emergency", {}).get("emergency"):
            return f"""🚨 **URGENT MEDICAL ATTENTION NEEDED** 🚨

Based on your symptoms, this could be a medical emergency. Please:
- Call emergency services immediately (911)
- Go to the nearest emergency room
- Don't delay seeking professional medical help

Your safety is the top priority. Please get medical attention right away."""

        condition = diagnosis_result.get("diagnosis", {}).get("condition", "unknown")
        confidence = diagnosis_result.get("diagnosis", {}).get("confidence", "low")
        remedies = diagnosis_result.get("remedies", [])
        precautions = diagnosis_result.get("precautions", [])

        if condition == "unknown":
            return """I understand you're not feeling well, but I need more specific information to help you better. 

Could you please describe:
- What specific symptoms you're experiencing
- Where in your body you feel discomfort
- How long you've been feeling this way
- How severe the symptoms are

For example, you could say "I have a headache and fever" or "My stomach hurts and I feel nauseous." The more specific you are, the better I can help you."""

        # Generate conversational response
        response = f"""Based on your symptoms, it appears you might have **{condition.title()}** (confidence: {confidence}).

"""

        if remedies:
            response += "**🌿 Natural Remedies I'd Recommend:**\n"
            for i, remedy in enumerate(remedies, 1):
                response += f"{i}. **{remedy['remedy']}** - {remedy['benefit']}\n   *How it helps: {remedy['explanation']}*\n\n"

        if precautions:
            response += "**⚠️ Important Precautions:**\n"
            for i, precaution in enumerate(precautions, 1):
                response += f"{i}. {precaution.title()}\n"
            response += "\n"

        response += """**Important Note:** This is preliminary guidance based on symptom analysis. Please consult with a healthcare professional for proper medical diagnosis and treatment, especially if symptoms persist or worsen.

Is there anything specific about your symptoms you'd like me to explain further?"""

        return response