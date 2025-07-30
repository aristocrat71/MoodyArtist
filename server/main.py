from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import our modular components
from validators import validate_preferences, get_art_forms_for_experience
from prompt_builder import build_creative_prompt
from hf_client import HuggingFaceClient

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Required for sessions
CORS(app)

# Initialize HuggingFace client
try:
    hf_client = HuggingFaceClient()
except ValueError as e:
    print(f"Warning: {e}")
    hf_client = None

@app.route('/api/preferences', methods=['POST'])
def set_preferences():
    """Set user preferences in session"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate input
        is_valid, error_message = validate_preferences(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Store preferences in session
        session['experience'] = data['experience']
        session['artform'] = data['artform']
        session['moods'] = data['moods']
        
        return jsonify({'status': 'success', 'message': 'Preferences saved successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/generate', methods=['POST'])
def generate_idea():
    """Generate creative idea based on stored preferences"""
    try:
        # Check if preferences are stored in session
        if 'experience' not in session or 'artform' not in session or 'moods' not in session:
            return jsonify({'error': 'No preferences found. Please set preferences first.'}), 400
        
        # Check if HF client is available
        if not hf_client:
            return jsonify({'error': 'HuggingFace API not configured'}), 500
        
        # Build creative prompt
        prompt = build_creative_prompt(
            session['experience'],
            session['artform'],
            session['moods']
        )
        
        # Generate idea using HuggingFace
        result = hf_client.generate_idea(prompt)
        
        if result['success']:
            return jsonify({'idea': result['idea']})
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/art-forms/<experience>', methods=['GET'])
def get_art_forms(experience):
    """Get available art forms for a given experience level"""
    try:
        art_forms = get_art_forms_for_experience(experience)
        return jsonify({'art_forms': art_forms})
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)