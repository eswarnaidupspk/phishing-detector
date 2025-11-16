# Phishing Website Detection System

A full-stack web application that uses machine learning to detect phishing websites based on URL features.

## Features
- Domain name analysis
- Domain age checking
- Host length analysis
- URL pattern detection
- Real-time prediction using ML model

## Tech Stack
- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- ML: scikit-learn
- Features: Domain age, DNS records, URL length, special characters, etc.

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
Open `frontend/index.html` in a browser or serve via:
```bash
cd frontend
python -m http.server 8000
```

## Usage
1. Start the backend server (runs on port 5000)
2. Open the frontend (port 8000 or directly in browser)
3. Enter a URL to check if it's phishing or legitimate
