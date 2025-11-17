from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from feature_extractor import FeatureExtractor
from advanced_feature_extractor import AdvancedFeatureExtractor
import os
import warnings
warnings.filterwarnings('ignore')

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
advanced_extractor = AdvancedFeatureExtractor()

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
        use_advanced = data.get('advanced', True)  # Use advanced features by default
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if use_advanced:
            # Extract advanced features
            all_features = advanced_extractor.extract_all_features(url)
            
            # Extract basic features for model prediction
            basic_features = extractor.extract_features(url)
            
            # Prepare features for prediction
            feature_df = pd.DataFrame([basic_features])
            feature_df = feature_df[feature_names]
            
            # Make prediction
            prediction = model.predict(feature_df)[0]
            probability = model.predict_proba(feature_df)[0]
            
            # Calculate risk score based on advanced features
            risk_score = calculate_risk_score(all_features)
            
            # Get feature explanations
            explanations = advanced_extractor.get_feature_explanations(all_features)
            
            # Adjust confidence based on advanced features
            adjusted_confidence = adjust_confidence(probability, risk_score)
            
            result = {
                'url': url,
                'prediction': 'Phishing' if prediction == 1 else 'Legitimate',
                'is_phishing': bool(prediction == 1),
                'confidence': float(adjusted_confidence * 100),
                'phishing_probability': float(probability[1] * 100),
                'legitimate_probability': float(probability[0] * 100),
                'risk_score': risk_score,
                'risk_level': get_risk_level(risk_score),
                'features': all_features,
                'explanations': explanations,
                'advanced_analysis': {
                    'whois': {
                        'domain_age_days': all_features.get('domain_age_days', -1),
                        'is_newly_registered': all_features.get('is_newly_registered', 0),
                        'registrar_reputation': all_features.get('registrar_reputation', 0),
                    },
                    'ssl': {
                        'has_valid_ssl': all_features.get('has_valid_ssl', 0),
                        'ssl_issuer_trusted': all_features.get('ssl_issuer_trusted', 0),
                        'ssl_self_signed': all_features.get('ssl_self_signed', 0),
                        'ssl_days_to_expiry': all_features.get('ssl_days_to_expiry', -1),
                    },
                    'content': {
                        'has_login_form': all_features.get('has_login_form', 0),
                        'form_posts_external': all_features.get('form_posts_external', 0),
                        'has_suspicious_js': all_features.get('has_suspicious_js', 0),
                    },
                    'reputation': {
                        'typosquatting_score': all_features.get('typosquatting_score', 0),
                        'min_edit_distance': all_features.get('min_edit_distance', 100),
                        'blacklist_score': all_features.get('blacklist_score', 0),
                    }
                }
            }
        else:
            # Basic prediction (original functionality)
            features = extractor.extract_features(url)
            feature_df = pd.DataFrame([features])
            feature_df = feature_df[feature_names]
            
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
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def calculate_risk_score(features):
    """Calculate overall risk score from 0-100"""
    score = 0
    
    # Critical risk factors (high weight)
    if features.get('is_newly_registered', 0) == 1:
        score += 20
    if features.get('ssl_self_signed', 0) == 1:
        score += 15
    if features.get('form_posts_external', 0) == 1:
        score += 25
    if features.get('has_ip', 0) == 1:
        score += 15
    if features.get('typosquatting_score', 0) >= 2:
        score += 20
    
    # Medium risk factors
    if features.get('has_login_form', 0) == 1:
        score += 10
    if features.get('has_suspicious_js', 0) == 1:
        score += 10
    if features.get('redirect_to_different_domain', 0) == 1:
        score += 10
    if features.get('has_unicode_chars', 0) == 1:
        score += 10
    if features.get('blacklist_score', 0) > 0:
        score += 15
    
    # Positive factors (reduce score)
    if features.get('has_valid_ssl', 0) == 1 and features.get('ssl_issuer_trusted', 0) == 1:
        score -= 10
    if features.get('domain_age_days', -1) > 365:
        score -= 15
    if features.get('registrar_reputation', 0) == 1:
        score -= 5
    
    return max(0, min(100, score))

def adjust_confidence(probability, risk_score):
    """Adjust ML confidence based on risk score"""
    ml_confidence = max(probability)
    
    # If risk score is high, increase phishing confidence
    if risk_score > 60:
        return max(ml_confidence, 0.85)
    elif risk_score > 40:
        return max(ml_confidence, 0.70)
    elif risk_score < 20:
        return max(ml_confidence, 0.80)
    
    return ml_confidence

def get_risk_level(score):
    """Convert risk score to risk level"""
    if score >= 70:
        return 'Critical'
    elif score >= 50:
        return 'High'
    elif score >= 30:
        return 'Medium'
    elif score >= 10:
        return 'Low'
    else:
        return 'Very Low'

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
