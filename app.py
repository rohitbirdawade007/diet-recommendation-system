# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from src.predict import predict_diet
from src.recommendation import get_diet_advice, get_all_diets

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.json.ensure_ascii = False
CORS(app)

VALID_MODELS = ['logistic_regression','decision_tree','random_forest','xgboost','ann']

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    model_name = data.pop('model', 'random_forest')
    if model_name not in VALID_MODELS:
        return jsonify({'error': f'Unknown model: {model_name}'}), 400
    required = ['Age','Gender','Height_cm','Weight_kg','BMI','Activity_Level','Sugar_Level','Cholesterol','Goal']
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400
    try:
        result = predict_diet(model_name, data)
        result['advice'] = get_diet_advice(result['diet'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)