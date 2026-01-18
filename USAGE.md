# Quick Usage Guide

## 🚀 Three Ways to Use the AI Medical Diagnosis System

### 1. ChatGPT-Style Interface (Best Experience)
```bash
python chatgpt_interface.py
```
- Natural conversation like ChatGPT
- Follow-up questions
- Formatted responses with emojis

### 2. Web Interface (Modern UI)
```bash
python web_interface.py
```
- Open http://localhost:5000 in browser
- Mobile-friendly design
- Real-time chat interface

### 3. Simple Command Line
```bash
python main.py "your symptoms here"
```
- Quick one-time queries
- Basic formatted output

## 📋 Example Commands

```bash
# ChatGPT-style conversation
python chatgpt_interface.py

# Single query
python chatgpt_interface.py "I have a headache and fever"

# Web interface
python web_interface.py

# Simple CLI
python main.py "stomach pain and nausea"

# Run tests
python test_system.py

# Update with latest Kaggle dataset
python update_dataset.py

# Download Kaggle dataset for exploration
python download_kaggle_dataset.py
```

## 💡 Tips

- Use natural language: "My head really hurts" works better than just "headache"
- Be specific about symptoms for better diagnosis
- Emergency symptoms (chest pain, difficulty breathing) trigger special alerts
- The system recognizes 161 different symptoms and 41 medical conditions
- Update dataset periodically for the latest medical data