#!/usr/bin/env python3
"""
ChatGPT-like Medical Diagnosis Interface
Natural conversational AI for symptom analysis with advanced diagnosis
"""

import sys
import re
from typing import Dict
from ai_engine import analyze_symptoms, advanced_analyze_symptoms, comprehensive_symptom_check
from ai_engine.nlp_processor import SymptomNLPProcessor

class MedicalChatBot:
    """ChatGPT-like medical diagnosis chatbot with advanced features."""
    
    def __init__(self):
        self.nlp_processor = SymptomNLPProcessor()
        self.conversation_history = []
        self.user_context = {}
        self.last_diagnosis = None  # Track last diagnosis for context
        self.current_symptoms = []  # Track current symptoms being discussed
        self.advanced_mode = False  # Toggle for advanced diagnosis
        self.symptom_check_session = None  # For comprehensive symptom checking
        
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate ChatGPT-like response."""
        
        # Store conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check for mode switching commands
        if user_input.lower().strip() in ['advanced', 'advanced mode', 'detailed analysis']:
            self.advanced_mode = True
            response = "🔬 **Advanced Mode Activated!**\n\nI'll now provide detailed differential diagnosis with multiple possible conditions, comprehensive treatment plans, and guided symptom checking.\n\nPlease describe your symptoms for advanced analysis."
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        if user_input.lower().strip() in ['simple', 'simple mode', 'basic']:
            self.advanced_mode = False
            response = "✅ **Simple Mode Activated**\n\nI'll provide straightforward symptom analysis and natural remedies.\n\nHow can I help you today?"
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # Check if this is a follow-up response to a previous question
        response = self._handle_follow_up_context(user_input)
        if response:
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        
        # Process with NLP
        nlp_result = self.nlp_processor.process_natural_language(user_input)
        
        # Handle different types of input
        if nlp_result["type"] == "greeting":
            response = nlp_result["response"] + "\n\n💡 **Tip:** Type 'advanced' for detailed analysis or 'simple' for basic mode."
            
        elif nlp_result["type"] == "system_info":
            response = nlp_result["response"]
            
        elif nlp_result["type"] == "clarification_needed":
            response = nlp_result["response"]
            if "suggestions" in nlp_result:
                response += "\n\n**Common symptoms I can help with:**\n"
                for suggestion in nlp_result["suggestions"]:
                    response += f"• {suggestion}\n"
                    
        elif nlp_result["type"] == "symptoms_found":
            # Store current symptoms for context
            self.current_symptoms = nlp_result["symptoms"]
            
            # Choose analysis method based on mode
            if self.advanced_mode:
                response = self._handle_advanced_analysis(nlp_result["normalized_text"])
            else:
                response = self._handle_simple_analysis(nlp_result["normalized_text"])
        
        else:
            response = "I'm here to help with your health concerns. Please describe your symptoms and I'll do my best to provide helpful information.\n\n💡 **Tip:** Type 'advanced' for detailed analysis with multiple diagnoses."
        
        # Store response
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _handle_simple_analysis(self, symptoms_text: str) -> str:
        """Handle simple symptom analysis."""
        # Analyze symptoms
        diagnosis_result = analyze_symptoms(symptoms_text)
        
        # Store last diagnosis for follow-up context
        self.last_diagnosis = diagnosis_result
        
        # Generate conversational response
        response = self.nlp_processor.generate_conversational_response(diagnosis_result)
        
        # Add context-aware follow-up
        if not diagnosis_result.get("emergency", {}).get("emergency"):
            response += self._generate_follow_up_questions(diagnosis_result)
        
        return response
    
    def _handle_advanced_analysis(self, symptoms_text: str) -> str:
        """Handle advanced symptom analysis with differential diagnosis."""
        # Perform advanced analysis
        advanced_result = advanced_analyze_symptoms(symptoms_text)
        
        if advanced_result["type"] == "emergency":
            response = "🚨 **MEDICAL EMERGENCY DETECTED** 🚨\n\n"
            response += f"**Condition:** {advanced_result['emergency'].get('suspected_condition', 'Critical')}\n"
            response += f"**Urgency:** {advanced_result['emergency']['level'].upper()}\n"
            response += f"**Action Required:** {advanced_result['emergency']['message']}\n\n"
            
            if advanced_result.get('emergency_remedies'):
                emergency_remedies = advanced_result['emergency_remedies']
                if emergency_remedies.get('immediate_actions'):
                    response += "**Immediate Actions:**\n"
                    for action in emergency_remedies['immediate_actions']:
                        response += f"• {action}\n"
                    response += f"\n⚠️ {emergency_remedies.get('warning', '')}"
            
            return response
        
        elif advanced_result["type"] == "unknown":
            response = f"🤔 **Analysis Result:** {advanced_result['message']}\n\n"
            
            if advanced_result.get('extracted_symptoms'):
                response += f"**Symptoms I detected:** {', '.join(advanced_result['extracted_symptoms'])}\n\n"
            
            if advanced_result.get('suggestions'):
                response += "**Common symptoms I can analyze:**\n"
                for suggestion in advanced_result['suggestions']:
                    response += f"• {suggestion}\n"
            
            return response
        
        elif advanced_result["type"] == "advanced_diagnosis":
            return self._format_advanced_diagnosis(advanced_result)
        
        return "I encountered an issue with the advanced analysis. Please try again."
    
    def _format_advanced_diagnosis(self, advanced_result: Dict) -> str:
        """Format advanced diagnosis results for display."""
        response = "🔬 **Advanced Medical Analysis**\n\n"
        
        # Primary diagnosis
        primary = advanced_result['primary_diagnosis']
        response += f"**Primary Diagnosis:** {primary['condition'].title()}\n"
        response += f"**Confidence Level:** {primary['confidence'].title()}"
        
        if 'score' in primary:
            response += f" ({primary['score']:.1%})"
        response += "\n\n"
        
        # Matching symptoms
        if primary.get('matching_symptoms'):
            response += f"**Your symptoms that match:** {', '.join(primary['matching_symptoms'])}\n\n"
        
        # Differential diagnosis
        if advanced_result.get('differential_diagnosis'):
            response += "**Alternative Possibilities:**\n"
            for i, alt_diagnosis in enumerate(advanced_result['differential_diagnosis'][:2], 1):
                response += f"{i}. {alt_diagnosis['disease'].title()} (confidence: {alt_diagnosis['confidence']})\n"
            response += "\n"
        
        # Treatment plan
        treatment = advanced_result.get('treatment_plan', {})
        
        # Natural remedies
        if treatment.get('natural_remedies'):
            response += "🌿 **Recommended Natural Remedies:**\n"
            for i, remedy in enumerate(treatment['natural_remedies'][:3], 1):
                response += f"{i}. **{remedy['remedy']}**\n"
                response += f"   • Benefit: {remedy['benefit']}\n"
                response += f"   • How it works: {remedy['explanation']}\n"
                if 'usage' in remedy:
                    response += f"   • Usage: {remedy['usage']}\n"
                response += "\n"
        
        # Lifestyle recommendations
        if treatment.get('lifestyle_recommendations'):
            response += "🏃 **Lifestyle Recommendations:**\n"
            for rec in treatment['lifestyle_recommendations'][:4]:
                response += f"• {rec}\n"
            response += "\n"
        
        # Dietary recommendations
        if treatment.get('dietary_recommendations'):
            dietary = treatment['dietary_recommendations']
            if dietary.get('foods_to_include'):
                response += "🥗 **Foods to Include:**\n"
                response += f"• {', '.join(dietary['foods_to_include'][:5])}\n\n"
        
        # Medical precautions
        if treatment.get('medical_precautions'):
            response += "⚠️ **Important Precautions:**\n"
            for precaution in treatment['medical_precautions'][:3]:
                response += f"• {precaution}\n"
            response += "\n"
        
        # Analysis summary
        response += f"**Analysis Summary:** Analyzed {advanced_result.get('total_symptoms_analyzed', 0)} symptoms\n\n"
        
        # Disclaimer
        response += "**Important Note:** This is preliminary guidance based on symptom analysis. Please consult with a healthcare professional for proper medical diagnosis and treatment, especially if symptoms persist or worsen.\n\n"
        
        # Follow-up options
        response += "**What would you like to know more about?**\n"
        response += "• Ask about specific remedies or treatments\n"
        response += "• Get more details about your condition\n"
        response += "• Discuss lifestyle changes\n"
        response += "• Type 'comprehensive check' for guided symptom analysis"
        
        return response
    
    def _handle_follow_up_context(self, user_input: str) -> str:
        """Handle follow-up responses that provide additional context."""
        
        # Check if we have recent conversation history
        if len(self.conversation_history) < 1:
            return None
        
        # Get the last assistant message
        last_assistant_message = None
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
                last_assistant_message = msg["content"]
                break
        
        # Check if the last message contained follow-up questions
        if last_assistant_message and "Follow-up questions:" in last_assistant_message:
            
            # Handle duration responses
            duration_patterns = [
                r"(\d+)\s*(day|days|week|weeks|month|months)",
                r"(few|several|many)\s*(day|days|week|weeks|month|months)",
                r"since\s+(yesterday|last week|last month)",
                r"for\s+(a while|long time|some time)"
            ]
            
            for pattern in duration_patterns:
                if re.search(pattern, user_input.lower()):
                    return self._handle_duration_response(user_input)
            
            # Handle yes/no responses to follow-up questions
            if user_input.lower().strip() in ["yes", "yeah", "yep", "no", "nope", "not really"]:
                return self._handle_yes_no_response(user_input)
            
            # Handle exposure/contact responses
            if any(word in user_input.lower() for word in ["around", "contact", "exposed", "family", "work", "school"]):
                return self._handle_exposure_response(user_input)
        
        return None
    
    def _handle_duration_response(self, user_input: str) -> str:
        """Handle duration-related responses."""
        
        # Extract duration
        duration_match = re.search(r"(\d+)\s*(day|days|week|weeks|month|months)", user_input.lower())
        
        if duration_match:
            number = duration_match.group(1)
            unit = duration_match.group(2)
            
            if "week" in unit and int(number) >= 2:
                return f"""That's quite a long time to have these symptoms ({number} {unit}). 

**For symptoms lasting this long, I strongly recommend:**
• Consulting with a healthcare professional for proper evaluation
• Getting a thorough medical examination
• Discussing any changes in symptom severity or new symptoms

**In the meantime, continue with:**
• The natural remedies I suggested earlier
• Adequate rest and hydration
• Monitoring for any worsening symptoms

Is there anything else about your symptoms that has changed or worsened recently?"""
            
            elif "day" in unit and int(number) >= 7:
                return f"""Having symptoms for {number} {unit} suggests this might need medical attention.

**I recommend:**
• Seeing a healthcare provider if symptoms persist beyond a week
• Continuing with natural remedies for symptom relief
• Monitoring for any changes or worsening

Are you experiencing any other symptoms along with what you mentioned earlier?"""
            
            else:
                return f"""Thank you for letting me know about the duration ({number} {unit}).

**For symptoms of this duration:**
• The natural remedies I suggested should help provide relief
• Continue monitoring your symptoms
• Seek medical care if symptoms worsen or don't improve

How are you feeling right now compared to when the symptoms started?"""
        
        return "Thank you for the additional information. Is there anything else about your symptoms you'd like to discuss?"
    
    def _handle_yes_no_response(self, user_input: str) -> str:
        """Handle yes/no responses to follow-up questions."""
        
        if user_input.lower().strip() in ["yes", "yeah", "yep"]:
            return """Thank you for confirming. Based on this additional information:

**I recommend:**
• Continue with the natural remedies I suggested
• Get adequate rest and stay well-hydrated
• Monitor your symptoms closely
• Consider seeing a healthcare provider if symptoms persist or worsen

Is there anything specific about your current symptoms that concerns you most?"""
        
        else:  # no, nope, not really
            return """I understand. Even without additional exposure or risk factors:

**Please continue to:**
• Use the natural remedies I recommended
• Rest and stay hydrated
• Monitor your symptoms
• Seek medical care if you feel worse

What would you like to know more about regarding your symptoms or the suggested remedies?"""
    
    def _handle_exposure_response(self, user_input: str) -> str:
        """Handle responses about exposure or contact with others."""
        
        return f"""Thank you for sharing that information about potential exposure.

**Given this context:**
• The natural remedies I suggested can help support your recovery
• It's important to rest and stay hydrated
• Consider isolating if you might be contagious
• Monitor for any worsening symptoms

**Please seek medical care if you experience:**
• Difficulty breathing
• High fever that won't break
• Severe symptoms that worsen rapidly

Is there anything else about your current condition you'd like to discuss?"""
    
    def _generate_follow_up_questions(self, diagnosis_result: Dict) -> str:
        """Generate contextual follow-up questions."""
        condition = diagnosis_result.get("diagnosis", {}).get("condition", "")
        
        follow_ups = {
            "viral infection": "\n\n**Follow-up questions:**\n• How long have you had these symptoms?\n• Have you been around anyone who was sick recently?\n• Are you getting enough rest and fluids?",
            
            "common cold": "\n\n**Follow-up questions:**\n• Are you staying hydrated?\n• Have you tried any remedies yet?\n• Is this affecting your sleep?",
            
            "allergy": "\n\n**Follow-up questions:**\n• Do you know what might have triggered this?\n• Have you been exposed to any new substances?\n• Do you have a history of allergies?",
            
            "gastric issue": "\n\n**Follow-up questions:**\n• What have you eaten recently?\n• Are you experiencing this on an empty stomach?\n• Have you had similar issues before?",
            
            "throat infection": "\n\n**Follow-up questions:**\n• Is it painful to swallow?\n• Do you see any white spots in your throat?\n• Have you tried gargling with salt water?"
        }
        
        return follow_ups.get(condition, "\n\n**Is there anything else about your symptoms you'd like to discuss?**")

def chat_interface():
    """Main chat interface like ChatGPT."""
    
    print("🏥 AI Medical Assistant - ChatGPT Style (Enhanced)")
    print("=" * 60)
    print("Hello! I'm your AI medical assistant with advanced diagnosis capabilities.")
    print("I can help analyze symptoms, suggest natural remedies, and provide health guidance.")
    print()
    print("💡 **New Features:**")
    print("• Type 'advanced' for detailed differential diagnosis")
    print("• Type 'simple' for basic symptom analysis")
    print("• Type 'comprehensive check' for guided symptom analysis")
    print()
    print("Type 'quit', 'exit', or 'bye' to end our conversation.")
    print("=" * 60)
    
    chatbot = MedicalChatBot()
    
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 Assistant: Take care of yourself! Remember to consult healthcare professionals for serious concerns. Goodbye! 👋")
                break
            
            if not user_input:
                print("\n🤖 Assistant: I'm here to help! Please tell me about your symptoms or health concerns.")
                continue
            
            # Process and respond
            print("\n🤖 Assistant: ", end="")
            response = chatbot.process_user_input(user_input)
            
            # Format and display response
            formatted_response = format_chat_response(response)
            print(formatted_response)
            
        except KeyboardInterrupt:
            print("\n\n🤖 Assistant: Goodbye! Stay healthy! 👋")
            break
        except Exception as e:
            print(f"\n🤖 Assistant: I apologize, but I encountered an error: {e}")
            print("Please try describing your symptoms again.")

def format_chat_response(response: str) -> str:
    """Format response for better readability."""
    # Add proper spacing and formatting
    lines = response.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip():
            # Add proper indentation for lists
            if line.strip().startswith(('•', '-', '*')):
                formatted_lines.append(f"  {line.strip()}")
            elif line.strip().startswith(tuple('123456789')):
                formatted_lines.append(f"  {line.strip()}")
            else:
                formatted_lines.append(line)
        else:
            formatted_lines.append("")
    
    return '\n'.join(formatted_lines)

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Single query mode
        user_input = " ".join(sys.argv[1:])
        chatbot = MedicalChatBot()
        response = chatbot.process_user_input(user_input)
        print("🤖 AI Medical Assistant:")
        print("=" * 30)
        print(format_chat_response(response))
    else:
        # Interactive chat mode
        chat_interface()

if __name__ == "__main__":
    main()