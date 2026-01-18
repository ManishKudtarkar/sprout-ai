# AI Medical Diagnosis System

A ChatGPT-like medical diagnosis system with natural language understanding, enhanced with Kaggle dataset integration. Provides conversational symptom analysis, natural remedy suggestions, and medical precautions.

## 🚀 Quick Start

### **ChatGPT-Style Interface** (Recommended)
```bash
# Interactive conversation
python chatgpt_interface.py

# Single query
python chatgpt_interface.py "I have a headache and feel nauseous"
```

### **Web Interface**
```bash
python web_interface.py
# Open http://localhost:5000 in your browser
```

### **Simple CLI**
```bash
python main.py "fever and headache"
```

## ✨ Features

- **Natural Language**: "My stomach really hurts" → Recognizes gastric issues
- **ChatGPT-Style Responses**: Formatted conversations with follow-up questions
- **161 Symptom Mappings**: Enhanced with Kaggle medical dataset
- **41 Medical Conditions**: Comprehensive condition coverage
- **Natural Remedies**: Traditional and evidence-based treatments
- **Medical Precautions**: Professional recommendations
- **Emergency Detection**: Critical symptom alerts

## 📋 Example Conversation

```
💬 You: Hello, I'm not feeling well
🤖 Assistant: Hello! I'm here to help analyze your symptoms. Please describe how you're feeling.

💬 You: My stomach really hurts and I feel sick
🤖 Assistant: Based on your symptoms, it appears you might have Gastric Issue (confidence: high).

🌿 Natural Remedies I'd Recommend:
1. Aloe Vera Juice - Soothes stomach lining
   How it helps: Aloe reduces acid irritation naturally

Follow-up questions:
• What have you eaten recently?
• Are you experiencing this on an empty stomach?
```

## 🚨 Emergency Detection

```
💬 You: I'm having chest pain and can't breathe
🤖 Assistant: 🚨 URGENT MEDICAL ATTENTION NEEDED 🚨

Based on your symptoms, this could be a medical emergency. Please:
- Call emergency services immediately (911)
- Go to the nearest emergency room
```

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_system.py

# Start using
python chatgpt_interface.py
```

## 📁 Project Structure

```
├── ai_engine/              # Core diagnosis engine
│   ├── __init__.py         # Main API
│   ├── diagnosis.py        # Diagnosis logic
│   ├── nlp_processor.py    # Natural language processing
│   ├── remedies.py         # Natural remedies database
│   ├── safety.py           # Emergency detection
│   └── symptoms.py         # Symptom mapping
├── data/                   # Medical data
│   ├── remedies.json       # Remedies and precautions
│   └── symptoms.json       # Symptom mappings (161 total)
├── chatgpt_interface.py    # ChatGPT-like interface
├── web_interface.py        # Web interface
├── main.py                 # Simple CLI
└── test_system.py          # Tests
```

## ⚠️ Medical Disclaimer

This AI assistant provides general health information and natural remedy suggestions for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns, especially for emergencies or persistent symptoms.

## 🎯 Supported Conditions

**41 Medical Conditions** including:
- Viral infections, Common cold, Allergies
- Gastric issues, Digestive problems
- Respiratory conditions, Throat infections
- Skin conditions, Headaches, Fever
- And many more from the Kaggle medical dataset

**161 Symptom Mappings** with natural language understanding for symptoms like:
- "My head hurts" → Headache
- "I feel nauseous" → Vomiting/Nausea
- "Stomach pain" → Gastric issues
- "Can't breathe" → Emergency detection