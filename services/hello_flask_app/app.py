from flask import Flask, render_template, request, session, redirect, url_for
import os
import uuid
from datetime import datetime

# Check if OpenAI is available, otherwise use fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    import random

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())  # Generate a random secret key for sessions

# Sample responses for fallback mode
FALLBACK_RESPONSES = {
    "what is vibebox": "VibeBox is a lightweight development environment designed to kickstart 'vibe coding' projects. It provides a Docker Compose setup with containerized services that are easy to develop and deploy.",
    "how do i create a new service": "To create a new service in VibeBox:\n1. Add a new directory under services/\n2. Create a Dockerfile and necessary files\n3. Add your service to docker-compose.yml\n4. Restart with `docker-compose up -d`",
    "tell me about docker compose": "Docker Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services, then create and start all the services with a single command.",
    "what is vibe coding": "Vibe coding is an approach that emphasizes lightweight, containerized development environments with clear separation of concerns. It focuses on developer joy by making it easy to experiment, iterate, and deploy services."
}

# Setup OpenAI if available and API key is provided
if OPENAI_AVAILABLE:
    openai.api_key = os.environ.get('OPENAI_API_KEY', '')
    if not openai.api_key:
        print("Warning: OPENAI_API_KEY environment variable not set. Falling back to demo mode.")
        OPENAI_AVAILABLE = False

def get_fallback_response(message):
    """Get a fallback response when OpenAI is not available"""
    message_lower = message.lower()
    
    for key, response in FALLBACK_RESPONSES.items():
        if key in message_lower:
            return response
    
    default_responses = [
        "I'm just a simple demo bot. I can tell you about VibeBox, Docker Compose, and vibe coding.",
        "That's an interesting question! This is just a demo, so I can only respond to basic questions about VibeBox.",
        "As a demo bot, I have limited knowledge. Try asking about VibeBox or Docker Compose."
    ]
    return random.choice(default_responses)

def get_openai_response(message, history):
    """Get a response using the OpenAI API"""
    try:
        # Format the conversation history for the API
        messages = []
        
        # Add system message to provide context
        messages.append({
            "role": "system", 
            "content": "You are a helpful assistant for VibeBox, a lightweight development environment. Keep responses concise but informative."
        })
        
        # Add conversation history
        for msg in history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Make the API call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Sorry, I encountered an error: {str(e)[:100]}... Please check your API key or try again later."

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize session if it doesn't exist
    if 'messages' not in session:
        session['messages'] = []
    
    # Check if API key is available for the template
    api_configured = OPENAI_AVAILABLE and openai.api_key
    
    if request.method == 'POST':
        user_message = request.form.get('user_message', '').strip()
        
        if user_message:
            # Add user message to session
            session['messages'].append({
                'role': 'user',
                'content': user_message,
                'timestamp': datetime.now().strftime('%H:%M')
            })
            
            # Generate response based on availability
            if OPENAI_AVAILABLE and openai.api_key:
                bot_response = get_openai_response(user_message, session['messages'])
            else:
                bot_response = get_fallback_response(user_message)
            
            # Add bot response to session
            session['messages'].append({
                'role': 'assistant',
                'content': bot_response,
                'timestamp': datetime.now().strftime('%H:%M')
            })
            
            # Save session
            session.modified = True
        
        # Redirect to avoid form resubmission
        return redirect(url_for('index'))
    
    return render_template('index.html', messages=session.get('messages', []), api_configured=api_configured)

@app.route('/reset')
def reset():
    """Reset the chat session"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/api-status')
def api_status():
    """Check API status"""
    has_key = bool(OPENAI_AVAILABLE and openai.api_key)
    return {
        "openai_available": OPENAI_AVAILABLE,
        "api_key_configured": has_key
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
