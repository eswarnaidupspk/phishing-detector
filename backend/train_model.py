import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def create_synthetic_data():
    """Create synthetic training data for demonstration"""
    np.random.seed(42)
    n_samples = 1000
    
    # Phishing websites (label = 1)
    phishing_data = {
        'url_length': np.random.randint(50, 200, n_samples//2),
        'domain_length': np.random.randint(15, 40, n_samples//2),
        'host_length': np.random.randint(20, 50, n_samples//2),
        'num_dots': np.random.randint(3, 8, n_samples//2),
        'num_hyphens': np.random.randint(2, 6, n_samples//2),
        'num_underscores': np.random.randint(1, 4, n_samples//2),
        'num_slashes': np.random.randint(3, 8, n_samples//2),
        'num_question': np.random.randint(1, 4, n_samples//2),
        'num_equal': np.random.randint(1, 5, n_samples//2),
        'num_at': np.random.randint(0, 2, n_samples//2),
        'num_ampersand': np.random.randint(0, 3, n_samples//2),
        'num_digits': np.random.randint(5, 20, n_samples//2),
        'has_https': np.random.choice([0, 1], n_samples//2, p=[0.7, 0.3]),
        'has_ip': np.random.choice([0, 1], n_samples//2, p=[0.6, 0.4]),
        'domain_age': np.random.randint(-1, 180, n_samples//2),
        'dns_record': np.random.choice([0, 1], n_samples//2, p=[0.3, 0.7]),
        'subdomain_level': np.random.randint(2, 5, n_samples//2),
        'has_suspicious_words': np.random.choice([0, 1], n_samples//2, p=[0.3, 0.7]),
        'label': np.ones(n_samples//2)
    }
    
    # Legitimate websites (label = 0)
    legitimate_data = {
        'url_length': np.random.randint(20, 80, n_samples//2),
        'domain_length': np.random.randint(8, 20, n_samples//2),
        'host_length': np.random.randint(10, 25, n_samples//2),
        'num_dots': np.random.randint(1, 3, n_samples//2),
        'num_hyphens': np.random.randint(0, 2, n_samples//2),
        'num_underscores': np.random.randint(0, 1, n_samples//2),
        'num_slashes': np.random.randint(2, 5, n_samples//2),
        'num_question': np.random.randint(0, 2, n_samples//2),
        'num_equal': np.random.randint(0, 2, n_samples//2),
        'num_at': np.zeros(n_samples//2),
        'num_ampersand': np.random.randint(0, 1, n_samples//2),
        'num_digits': np.random.randint(0, 5, n_samples//2),
        'has_https': np.random.choice([0, 1], n_samples//2, p=[0.2, 0.8]),
        'has_ip': np.zeros(n_samples//2),
        'domain_age': np.random.randint(365, 5000, n_samples//2),
        'dns_record': np.ones(n_samples//2),
        'subdomain_level': np.random.randint(0, 2, n_samples//2),
        'has_suspicious_words': np.random.choice([0, 1], n_samples//2, p=[0.8, 0.2]),
        'label': np.zeros(n_samples//2)
    }
    
    # Combine data
    df_phishing = pd.DataFrame(phishing_data)
    df_legitimate = pd.DataFrame(legitimate_data)
    df = pd.concat([df_phishing, df_legitimate], ignore_index=True)
    
    return df

def train_model():
    """Train the phishing detection model"""
    print("Creating synthetic training data...")
    df = create_synthetic_data()
    
    # Split features and labels
    X = df.drop('label', axis=1)
    y = df['label']
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))
    
    # Save model
    joblib.dump(model, 'phishing_model.pkl')
    print("\nModel saved as 'phishing_model.pkl'")
    
    # Save feature names
    feature_names = X.columns.tolist()
    joblib.dump(feature_names, 'feature_names.pkl')
    print("Feature names saved as 'feature_names.pkl'")

if __name__ == '__main__':
    train_model()
