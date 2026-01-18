# AI Medical Diagnosis System (Enhanced)

A ChatGPT-like medical diagnosis system with advanced differential diagnosis, natural language understanding, and comprehensive treatment plans. Enhanced with Kaggle dataset integration providing 161 symptom mappings and 41 medical conditions.

## 🚀 Quick Start

### **ChatGPT-Style Interface** (Recommended)
```bash
# Interactive conversation with advanced features
python chatgpt_interface.py

# Single query
python chatgpt_interface.py "I have a headache and feel nauseous"
```

### **Web Interface** (Enhanced)
```bash
python web_interface.py
# Open http://localhost:5000 in your browser
# Features: Simple/Advanced mode toggle, conversation context
```

### **CLI with Advanced Options**
```bash
# Simple analysis
python main.py "fever and headache"

# Advanced differential diagnosis
python main.py --advanced "fever and headache for 3 days"
```

## ✨ New Advanced Features

### 🔬 **Advanced Diagnosis Mode**
- **Differential Diagnosis**: Multiple possible conditions with confidence scores
- **Symptom Matching**: Shows which symptoms match each condition
- **Confidence Scoring**: Probability-based diagnosis ranking
- **Missing Symptoms**: Identifies symptoms that could confirm diagnosis

### 🌿 **Enhanced Treatment Plans**
- **Comprehensive Remedies**: 41 conditions with detailed natural treatments
- **Scientific Explanations**: How each remedy works at molecular level
- **Usage Instructions**: Specific dosages and application methods
- **Lifestyle Recommendations**: Diet, exercise, and lifestyle changes
- **Medical Precautions**: When to seek professional help

### 💬 **Improved Conversational AI**
- **Context Awareness**: Remembers conversation history
- **Follow-up Questions**: Intelligent symptom clarification
- **Mode Switching**: Toggle between simple and advanced analysis
- **Duration Tracking**: Understands "for 3 days", "since yesterday"

## 📋 Example Advanced Analysis

```
💬 You: advanced mode
🤖 Assistant: 🔬 Advanced Mode Activated! I'll now provide detailed differential diagnosis...

💬 You: I have headache, fever, and fatigue for 3 days
🤖 Assistant: 🔬 Advanced Medical Analysis

Primary Diagnosis: Viral Infection (confidence: high, 85%)
Your symptoms that match: headache, fever, fatigue

Alternative Possibilities:
1. Common Cold (confidence: medium)
2. Stress or Dehydration (confidence: low)

🌿 Recommended Natural Remedies:
1. Elderberry Syrup
   • Benefit: Boosts immune system and reduces viral load
   • How it works: Anthocyanins block viral replication
   • Usage: 1 tablespoon 3x daily during illness

🏃 Lifestyle Recommendations:
• Get adequate rest (8-9 hours sleep)
• Stay hydrated with clear fluids
• Avoid strenuous activities
• Maintain good hygiene

Analysis Summary: Analyzed 3 symptoms
```

## 🚨 Emergency Detection

```
💬 You: chest pain and difficulty breathing
🤖 Assistant: 🚨 MEDICAL EMERGENCY DETECTED 🚨

Condition: Heart Attack
Urgency: CRITICAL
Action Required: Seek immediate medical attention

Immediate Actions:
• Call 911 immediately
• Chew aspirin if available and not allergic
• Sit down and rest
• Loosen tight clothing

⚠️ This is a life-threatening emergency requiring immediate medical attention
```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/ManishKudtarkar/sprout-ai.git
cd sprout-ai

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_system.py

# Start using (enhanced interface)
python chatgpt_interface.py
```

## 🔄 Dataset Management

The system comes with comprehensive pre-loaded data from Kaggle's medical dataset:

### **Update System Data** (Recommended)
```bash
# Download and integrate latest Kaggle dataset
python update_dataset.py
```

### **Just Download Dataset** (For exploration)
```bash
# Download dataset to explore manually
python download_kaggle_dataset.py
```

**Note**: You'll need Kaggle API credentials configured. Visit [Kaggle API Documentation](https://www.kaggle.com/docs/api) for setup instructions.

## 📁 Project Structure

```
├── ai_engine/                    # Core diagnosis engine
│   ├── __init__.py              # Main API with advanced functions
│   ├── diagnosis.py             # Basic diagnosis logic
│   ├── advanced_diagnosis.py    # Advanced differential diagnosis
│   ├── enhanced_remedies.py     # Comprehensive remedy system
│   ├── symptom_checker.py       # Guided symptom checking
│   ├── nlp_processor.py         # Natural language processing
│   ├── remedies.py              # Basic remedies database
│   ├── safety.py                # Emergency detection
│   └── symptoms.py              # Symptom mapping
├── data/                        # Medical data
│   ├── remedies.json            # Remedies and precautions
│   └── symptoms.json            # 161 symptom mappings, 41 conditions
├── chatgpt_interface.py         # Enhanced ChatGPT-like interface
├── web_interface.py             # Enhanced web interface
├── main.py                      # CLI with advanced options
├── update_dataset.py            # Kaggle dataset updater
├── download_kaggle_dataset.py   # Simple dataset downloader
└── test_system.py               # System tests
```

## 🎯 Comprehensive Medical Coverage

### **41 Medical Conditions** with Advanced Analysis:
- **Infectious**: Viral infections, Fungal infections, Common cold
- **Respiratory**: Bronchial asthma, Pneumonia, Tuberculosis
- **Digestive**: GERD, Peptic ulcer disease, Gastroenteritis
- **Metabolic**: Diabetes, Hypothyroidism, Hyperthyroidism
- **Cardiovascular**: Hypertension, Heart attack
- **Neurological**: Migraine, Paralysis
- **Musculoskeletal**: Arthritis, Joint pain
- **And many more with detailed treatment plans**

### **161 Symptom Mappings** with Natural Language Understanding:
- "My head is killing me" → Severe headache
- "I can't keep food down" → Vomiting/Nausea
- "Burning in my chest" → GERD/Heartburn
- "Can't catch my breath" → Breathlessness (Emergency detection)

## 🔬 Advanced Features Details

### **Differential Diagnosis Engine**
- Multi-symptom correlation analysis
- Confidence scoring based on symptom specificity
- Missing symptom identification
- Disease probability calculations

### **Enhanced Remedy System**
- 200+ natural remedies with scientific backing
- Molecular-level explanations
- Specific usage instructions and dosages
- Lifestyle and dietary recommendations
- Emergency remedy protocols

### **Comprehensive Symptom Checker**
- Guided question-based diagnosis
- Interactive symptom exploration
- Progressive diagnosis refinement
- Treatment plan customization

## ⚠️ Medical Disclaimer

This AI assistant provides general health information and natural remedy suggestions for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns, especially for emergencies or persistent symptoms.

The advanced diagnosis features are designed to provide comprehensive information but should never replace professional medical consultation.
