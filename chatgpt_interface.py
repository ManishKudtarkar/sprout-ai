#!/usr/bin/env python3
"""
ChatGPT-like Medical Diagnosis Interface
Natural conversational AI for symptom analysis
"""

import sys
from typing import Dict
from ai_engine import analyze_symptoms
from ai_engine.nlp_processor import SymptomNLPProcessor

class MedicalChatBot:
    """ChatGPT-like medical diagnosis chatbot."""
    
    def __init__(self):
        self.nlp_processor = SymptomNLPProcessor()
        self.conversation_history = []
        self.user_context = {}
        
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate ChatGPT-like response."""
        
        # Store conversation
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Process with NLP
        nlp_result = self.nlp_processor.process_natural_language(user_input)
        
        # Handle different types of input
        if nlp_result["type"] == "greeting":
            response = nlp_result["response"]
            
        elif nlp_result["type"] == "system_info":
            response = nlp_result["response"]
            
        elif nlp_result["type"] == "clarification_needed":
            response = nlp_result["response"]
            if "suggestions" in nlp_result:
                response += "\n\n**Common symptoms I can help with:**\n"
                for suggestion in nlp_result["suggestions"]:
                    response += f"• {suggestion}\n"
                    
        elif nlp_result["type"] == "symptoms_found":
            # Analyze symptoms
            symptoms_text = nlp_result["normalized_text"]
            diagnosis_result = analyze_symptoms(symptoms_text)
            
            # Generate conversational response
            response = self.nlp_processor.generate_conversational_response(diagnosis_result)
            
            # Add context-aware follow-up
            if not diagnosis_result.get("emergency", {}).get("emergency"):
                response += self._generate_follow_up_questions(diagnosis_result)
        
        else:
            response = "I'm here to help with your health concerns. Please describe your symptoms and I'll do my best to provide helpful information."
        
        # Store response
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
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
    
    print("🏥 AI Medical Assistant - ChatGPT Style")
    print("=" * 50)
    print("Hello! I'm your AI medical assistant. I can help analyze symptoms,")
    print("suggest natural remedies, and provide health guidance.")
    print("Type 'quit', 'exit', or 'bye' to end our conversation.")
    print("=" * 50)
    
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