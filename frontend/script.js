const API_URL = 'https://phishing-detector-backend.onrender.com';



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
    const riskLevel = document.getElementById('riskLevel');
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
    
    // Display risk level if available
    if (data.risk_level) {
        riskLevel.textContent = `Risk Level: ${data.risk_level}`;
        riskLevel.className = `risk-level risk-${data.risk_level.toLowerCase().replace(' ', '-')}`;
        riskLevel.style.display = 'block';
    } else {
        riskLevel.style.display = 'none';
    }
    
    // Set confidence
    confidenceValue.textContent = `${data.confidence.toFixed(1)}%`;
    progressFill.style.width = `${data.confidence}%`;
    
    // Set probabilities
    legitProb.textContent = `${data.legitimate_probability.toFixed(1)}%`;
    phishProb.textContent = `${data.phishing_probability.toFixed(1)}%`;
    
    // Display explanations if available
    if (data.explanations && data.explanations.length > 0) {
        displayExplanations(data.explanations);
    }
    
    // Display advanced analysis if available
    if (data.advanced_analysis) {
        displayAdvancedAnalysis(data.advanced_analysis);
    }
    
    // Display features
    displayFeatures(data.features);
    
    // Show result
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function displayExplanations(explanations) {
    const explanationsCard = document.getElementById('explanationsCard');
    const explanationsList = document.getElementById('explanationsList');
    
    if (explanations.length === 0) {
        explanationsCard.style.display = 'none';
        return;
    }
    
    explanationsList.innerHTML = '';
    explanations.forEach(exp => {
        const expItem = document.createElement('div');
        expItem.className = 'explanation-item';
        expItem.textContent = exp;
        explanationsList.appendChild(expItem);
    });
    
    explanationsCard.style.display = 'block';
}

function displayAdvancedAnalysis(analysis) {
    // SSL Analysis
    const sslAnalysis = document.getElementById('sslAnalysis');
    sslAnalysis.innerHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Valid SSL Certificate:</span>
            <span class="analysis-value ${analysis.ssl.has_valid_ssl ? 'positive' : 'negative'}">
                ${analysis.ssl.has_valid_ssl ? '✓ Yes' : '✗ No'}
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Trusted Issuer:</span>
            <span class="analysis-value ${analysis.ssl.ssl_issuer_trusted ? 'positive' : 'neutral'}">
                ${analysis.ssl.ssl_issuer_trusted ? '✓ Yes' : '✗ No'}
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Self-Signed:</span>
            <span class="analysis-value ${analysis.ssl.ssl_self_signed ? 'negative' : 'positive'}">
                ${analysis.ssl.ssl_self_signed ? '⚠ Yes' : '✓ No'}
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Days to Expiry:</span>
            <span class="analysis-value">${analysis.ssl.ssl_days_to_expiry >= 0 ? analysis.ssl.ssl_days_to_expiry + ' days' : 'Unknown'}</span>
        </div>
    `;
    
    // WHOIS Analysis
    const whoisAnalysis = document.getElementById('whoisAnalysis');
    const domainAge = analysis.whois.domain_age_days;
    const ageDisplay = domainAge >= 0 ? `${domainAge} days (${Math.floor(domainAge / 365)} years)` : 'Unknown';
    const ageClass = domainAge < 30 && domainAge >= 0 ? 'negative' : domainAge > 365 ? 'positive' : 'neutral';
    
    whoisAnalysis.innerHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Domain Age:</span>
            <span class="analysis-value ${ageClass}">${ageDisplay}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Newly Registered:</span>
            <span class="analysis-value ${analysis.whois.is_newly_registered ? 'negative' : 'positive'}">
                ${analysis.whois.is_newly_registered ? '⚠ Yes (High Risk)' : '✓ No'}
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Reputable Registrar:</span>
            <span class="analysis-value ${analysis.whois.registrar_reputation ? 'positive' : 'neutral'}">
                ${analysis.whois.registrar_reputation ? '✓ Yes' : '✗ No'}
            </span>
        </div>
    `;
    
    // Content Analysis
    const contentAnalysis = document.getElementById('contentAnalysis');
    contentAnalysis.innerHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Login Form Detected:</span>
            <span class="analysis-value ${analysis.content.has_login_form ? 'warning' : 'neutral'}">
                ${analysis.content.has_login_form ? '⚠ Yes' : '✓ No'}
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Form Posts to External Domain:</span>
            <span class="analysis-value ${analysis.content.form_posts_external ? 'negative' : 'positive'}">
                ${analysis.content.form_posts_external ? '🚨 Yes (Critical)' : '✓ No'}
            </span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Suspicious JavaScript:</span>
            <span class="analysis-value ${analysis.content.has_suspicious_js ? 'negative' : 'positive'}">
                ${analysis.content.has_suspicious_js ? '⚠ Yes' : '✓ No'}
            </span>
        </div>
    `;
    
    // Reputation Analysis
    const reputationAnalysis = document.getElementById('reputationAnalysis');
    const typoScore = analysis.reputation.typosquatting_score;
    const typoClass = typoScore >= 2 ? 'negative' : typoScore >= 1 ? 'warning' : 'positive';
    const typoText = typoScore >= 2 ? '⚠ High Risk' : typoScore >= 1 ? '⚠ Medium Risk' : '✓ Low Risk';
    
    reputationAnalysis.innerHTML = `
        <div class="analysis-item">
            <span class="analysis-label">Typosquatting Risk:</span>
            <span class="analysis-value ${typoClass}">${typoText}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Edit Distance to Popular Brands:</span>
            <span class="analysis-value">${analysis.reputation.min_edit_distance}</span>
        </div>
        <div class="analysis-item">
            <span class="analysis-label">Blacklist Score:</span>
            <span class="analysis-value ${analysis.reputation.blacklist_score > 0 ? 'negative' : 'positive'}">
                ${analysis.reputation.blacklist_score > 0 ? '⚠ ' + analysis.reputation.blacklist_score : '✓ Clean'}
            </span>
        </div>
    `;
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
