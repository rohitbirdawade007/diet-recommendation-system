# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.json.ensure_ascii = False  # allow emoji in JSON responses
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify({'diet': 'Balanced', 'confidence': 95.0})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)