from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from feature_extractor import FeatureExtractor
import os

app = Flask(__name__)
CORS(app)

# Load model and feature names
try:
    model = joblib.load('phishing_model.pkl')
    feature_names = joblib.load('feature_names.pkl')
    print("Model loaded successfully!")
except:
    print("Model not found. Please run train_model.py first.")
    model = None
    feature_names = None

extractor = FeatureExtractor()

@app.route('/')
def home():
    return jsonify({
        'message': 'Phishing Detection API',
        'status': 'running',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Extract features
        features = extractor.extract_features(url)
        
        # Prepare features for prediction
        feature_df = pd.DataFrame([features])
        
        # Ensure features are in correct order
        feature_df = feature_df[feature_names]
        
        # Make prediction
        prediction = model.predict(feature_df)[0]
        probability = model.predict_proba(feature_df)[0]
        
        result = {
            'url': url,
            'prediction': 'Phishing' if prediction == 1 else 'Legitimate',
            'is_phishing': bool(prediction == 1),
            'confidence': float(max(probability) * 100),
            'phishing_probability': float(probability[1] * 100),
            'legitimate_probability': float(probability[0] * 100),
            'features': features
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    if model is None:
        print("\n" + "="*50)
        print("WARNING: Model not loaded!")
        print("Please run: python train_model.py")
        print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
