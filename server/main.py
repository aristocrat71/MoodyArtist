from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/generate-idea', methods=['POST'])
def generate_idea():
    data = request.get_json()
    words = data.get('words', [])
    # Placeholder logic for now
    idea = f"Generated idea for: {' '.join(words)}"
    return jsonify({'idea': idea})

if __name__ == '__main__':
    app.run(debug=True)