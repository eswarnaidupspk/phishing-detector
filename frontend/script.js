const API_URL = 'http://localhost:5000';

// Allow Enter key to submit
document.getElementById('urlInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        checkURL();
    }
});

async function checkURL() {
    const urlInput = document.getElementById('urlInput');
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a URL');
        return;
    }
    
    // Hide previous results and errors
    document.getElementById('result').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    
    // Show loading state
    const checkBtn = document.getElementById('checkBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    
    checkBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        if (!response.ok) {
            throw new Error('Failed to analyze URL');
        }
        
        const data = await response.json();
        displayResult(data);
        
    } catch (error) {
        showError('Error: ' + error.message + '. Make sure the backend server is running on port 5000.');
    } finally {
        // Reset button state
        checkBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
}

function displayResult(data) {
    const resultSection = document.getElementById('result');
    const resultCard = document.querySelector('.result-card');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const confidenceValue = document.getElementById('confidenceValue');
    const progressFill = document.getElementById('progressFill');
    const legitProb = document.getElementById('legitProb');
    const phishProb = document.getElementById('phishProb');
    
    // Set result styling
    if (data.is_phishing) {
        resultCard.className = 'result-card danger';
        resultIcon.textContent = '⚠️';
        resultTitle.textContent = 'Phishing Detected!';
        resultTitle.style.color = '#8b0000';
    } else {
        resultCard.className = 'result-card safe';
        resultIcon.textContent = '✅';
        resultTitle.textContent = 'Legitimate Website';
        resultTitle.style.color = '#2d5016';
    }
    
    // Set confidence
    confidenceValue.textContent = `${data.confidence.toFixed(1)}%`;
    progressFill.style.width = `${data.confidence}%`;
    
    // Set probabilities
    legitProb.textContent = `${data.legitimate_probability.toFixed(1)}%`;
    phishProb.textContent = `${data.phishing_probability.toFixed(1)}%`;
    
    // Display features
    displayFeatures(data.features);
    
    // Show result
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayFeatures(features) {
    const featuresList = document.getElementById('featuresList');
    featuresList.innerHTML = '';
    
    const featureLabels = {
        'url_length': 'URL Length',
        'domain_length': 'Domain Length',
        'host_length': 'Host Length',
        'num_dots': 'Dots Count',
        'num_hyphens': 'Hyphens Count',
        'num_underscores': 'Underscores',
        'num_slashes': 'Slashes Count',
        'num_question': 'Question Marks',
        'num_equal': 'Equal Signs',
        'num_at': 'At Symbols (@)',
        'num_ampersand': 'Ampersands',
        'num_digits': 'Digits Count',
        'has_https': 'HTTPS',
        'has_ip': 'Has IP Address',
        'domain_age': 'Domain Age (days)',
        'dns_record': 'DNS Record',
        'subdomain_level': 'Subdomain Level',
        'has_suspicious_words': 'Suspicious Words'
    };
    
    for (const [key, value] of Object.entries(features)) {
        const featureItem = document.createElement('div');
        featureItem.className = 'feature-item';
        
        const featureName = document.createElement('span');
        featureName.className = 'feature-name';
        featureName.textContent = featureLabels[key] || key;
        
        const featureValue = document.createElement('span');
        featureValue.className = 'feature-value';
        
        // Format value
        if (key === 'has_https' || key === 'has_ip' || key === 'dns_record' || key === 'has_suspicious_words') {
            featureValue.textContent = value === 1 ? 'Yes' : 'No';
        } else if (key === 'domain_age' && value === -1) {
            featureValue.textContent = 'Unknown';
        } else {
            featureValue.textContent = value;
        }
        
        featureItem.appendChild(featureName);
        featureItem.appendChild(featureValue);
        featuresList.appendChild(featureItem);
    }
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
