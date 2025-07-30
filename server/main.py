from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Hugging Face API configuration
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')

@app.route('/generate-idea', methods=['POST'])
def generate_idea():
    data = request.get_json()
    words = data.get('words', [])
    
    if not words:
        return jsonify({'error': 'No words provided'}), 400
    
    # Create a creative prompt for idea generation
    prompt = f"""<s>[INST] You are a creative artist and idea generator. Given these words: {', '.join(words)}, 
    generate a unique, creative artistic idea or concept. 
    
    The idea should be:
    - Creative and original
    - Feasible to create
    - Interesting and engaging
    - Related to the provided words
    
    Please provide a brief but inspiring description of the artistic idea: [/INST]"""
    
    try:
        # Call Hugging Face Inference API
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        payload = {"inputs": prompt}
        
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            # Extract the generated text from the response
            if isinstance(result, list) and len(result) > 0:
                idea = result[0].get('generated_text', '').strip()
                # Clean up the response to get just the generated part
                if '[/INST]' in idea:
                    idea = idea.split('[/INST]')[-1].strip()
            else:
                idea = str(result).strip()
            
            return jsonify({'idea': idea})
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return jsonify({'error': 'Failed to generate idea'}), 500
        
    except Exception as e:
        print(f"Error generating idea: {e}")
        return jsonify({'error': 'Failed to generate idea'}), 500

if __name__ == '__main__':
    app.run(debug=True)