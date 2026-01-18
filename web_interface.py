#!/usr/bin/env python3
"""
Simple Web Interface for AI Medical Diagnosis System
ChatGPT-like web interface using Flask
"""

try:
    from flask import Flask, render_template, request, jsonify
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from ai_engine import analyze_symptoms_conversational
import json

app = Flask(__name__)

# HTML template as string (to avoid needing separate template files)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Medical Assistant</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .header p {
            color: #7f8c8d;
            font-size: 16px;
        }
        .chat-container {
            min-height: 400px;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #fafafa;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
            margin-right: auto;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        .input-field {
            flex: 1;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
        }
        .input-field:focus {
            border-color: #007bff;
        }
        .send-button {
            padding: 12px 25px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
        }
        .send-button:hover {
            background-color: #0056b3;
        }
        .send-button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        .disclaimer {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin-top: 20px;
            font-size: 14px;
            color: #856404;
        }
        .loading {
            display: none;
            text-align: center;
            color: #666;
            font-style: italic;
        }
        .emergency {
            background-color: #f8d7da !important;
            border: 2px solid #dc3545 !important;
            color: #721c24 !important;
            font-weight: bold;
        }
        .suggestions {
            margin-top: 10px;
            font-size: 14px;
            color: #666;
        }
        .suggestions ul {
            margin: 5px 0;
            padding-left: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 AI Medical Assistant</h1>
            <p>Describe your symptoms and get natural remedy suggestions</p>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message bot-message">
                Hello! I'm your AI medical assistant. I can help analyze symptoms, suggest natural remedies, and provide health guidance. Please describe your symptoms or how you're feeling.
            </div>
        </div>
        
        <div class="loading" id="loading">
            🤔 Analyzing your symptoms...
        </div>
        
        <div class="input-container">
            <input type="text" class="input-field" id="userInput" 
                   placeholder="Describe your symptoms (e.g., 'I have a headache and fever')" 
                   onkeypress="handleKeyPress(event)">
            <button class="send-button" id="sendButton" onclick="sendMessage()">Send</button>
        </div>
        
        <div class="disclaimer">
            <strong>⚠️ Medical Disclaimer:</strong> This AI assistant provides general health information and natural remedy suggestions for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns, especially for emergencies or persistent symptoms.
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            
            // Clear input and disable button
            input.value = '';
            document.getElementById('sendButton').disabled = true;
            document.getElementById('loading').style.display = 'block';
            
            try {
                // Send to backend
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const result = await response.json();
                
                // Add bot response
                addMessage(result.response, 'bot', result.type === 'medical_analysis' && result.diagnosis_result?.emergency?.emergency);
                
            } catch (error) {
                console.error('Error:', error);
                addMessage('Sorry, I encountered an error analyzing your symptoms. Please try again.', 'bot');
            }
            
            // Re-enable button and hide loading
            document.getElementById('sendButton').disabled = false;
            document.getElementById('loading').style.display = 'none';
            input.focus();
        }

        function addMessage(text, sender, isEmergency = false) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            
            messageDiv.className = `message ${sender}-message`;
            if (isEmergency) {
                messageDiv.className += ' emergency';
            }
            
            // Format text with basic markdown-like formatting
            const formattedText = text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n/g, '<br>');
            
            messageDiv.innerHTML = formattedText;
            chatContainer.appendChild(messageDiv);
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Focus input on page load
        document.getElementById('userInput').focus();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page."""
    return HTML_TEMPLATE

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze symptoms endpoint."""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Process with conversational AI
        result = analyze_symptoms_conversational(user_message)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'type': 'error',
            'response': f'Sorry, I encountered an error: {str(e)}'
        }), 500

def main():
    """Main function to run the web interface."""
    if not FLASK_AVAILABLE:
        print("❌ Flask is not installed. Installing Flask...")
        import subprocess
        import sys
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully!")
            print("Please run this script again to start the web interface.")
            return
        except subprocess.CalledProcessError:
            print("❌ Failed to install Flask. Please install it manually:")
            print("pip install flask")
            return
    
    print("🌐 Starting AI Medical Assistant Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped. Goodbye!")

if __name__ == "__main__":
    main()