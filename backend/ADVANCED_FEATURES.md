# Advanced Phishing Detection Features

## Overview
This enhanced phishing detection system includes 12 advanced security analysis features that provide comprehensive URL threat assessment beyond basic machine learning classification.

## New Features Implemented

### 1. WHOIS / Domain Age & Registrar Analysis ✅
- **Domain Age Detection**: Identifies newly registered domains (< 30 days) which are high-risk indicators
- **Domain Expiry Tracking**: Monitors days until domain expiration
- **Registrar Reputation**: Checks against trusted registrars (GoDaddy, Namecheap, Google, Amazon, Cloudflare)
- **WHOIS Privacy Detection**: Identifies domains using privacy protection services

**Risk Indicators:**
- Domains < 30 days old: +20 risk score
- Domains > 1 year old: -15 risk score (positive indicator)

### 2. SSL Certificate Analysis ✅
- **Certificate Validation**: Verifies SSL certificate validity
- **Issuer Trust Check**: Validates against trusted CAs (Let's Encrypt, DigiCert, Comodo, etc.)
- **Self-Signed Detection**: Identifies self-signed certificates (high risk)
- **Certificate Expiry**: Tracks days until SSL certificate expiration
- **Domain Mismatch**: Checks if hostname matches certificate CN/SAN

**Risk Indicators:**
- Self-signed certificate: +15 risk score
- Valid SSL from trusted issuer: -10 risk score

### 3. IP / Hosting / ASN Reputation ✅
- **IP Resolution**: Resolves domain to IP address
- **Private IP Detection**: Identifies private IP ranges (10.x, 172.x, 192.x)
- **ASN Reputation**: Checks against known suspicious hosting providers
- **Hosting Provider Analysis**: Identifies bulletproof hosting services

**Risk Indicators:**
- Suspicious hosting provider: +10 risk score

### 4. Blacklist / Threat Feeds ✅
- **PhishTank Integration**: Ready for PhishTank API integration
- **Google Safe Browsing**: Ready for GSB API integration
- **TLD Blacklist**: Checks against free TLDs commonly used for phishing (.tk, .ml, .ga, .cf, .gq)
- **Blacklist Score**: Cumulative score from multiple threat feeds

**Risk Indicators:**
- Suspicious TLD: +15 risk score

### 5. Page Content Analysis ✅
- **Login Form Detection**: Identifies password input fields
- **External Form Submission**: Detects forms posting to different domains (critical risk)
- **Hidden Fields Analysis**: Counts suspicious hidden form fields
- **External Links Count**: Tracks number of external links
- **Suspicious JavaScript**: Detects obfuscated JS (eval, unescape, fromCharCode)
- **Iframe Detection**: Identifies embedded iframes

**Risk Indicators:**
- Login form + external post: +25 risk score (critical)
- Login form present: +10 risk score
- Suspicious JavaScript: +10 risk score

### 6. Visual Similarity / Brand Detection ✅
- **Framework Ready**: Infrastructure for image hash comparison
- **Logo Analysis**: Ready for brand logo detection
- **DOM Pattern Matching**: Content structure analysis

### 7. Redirect Chain Analysis ✅
- **Redirect Counting**: Tracks number of HTTP redirects
- **Domain Change Detection**: Identifies redirects to different domains
- **Redirect Chain Length**: Measures redirect depth

**Risk Indicators:**
- Redirect to different domain: +10 risk score

### 8. WHOIS/DNS Historical Analysis ✅
- **DNS Record Validation**: Checks A and MX records
- **DNS Record Count**: Tracks number of DNS records
- **Historical Data Ready**: Framework for passive DNS integration

### 9. Behavioral Signals ✅
- **Form Action Analysis**: Monitors form submission endpoints
- **Third-Party POST Detection**: Identifies external data submission
- **Cookie Behavior**: Ready for cookie analysis implementation

### 10. Typosquatting & Homograph Detection ✅
- **Edit Distance Calculation**: Compares against 15 popular domains
- **Typosquatting Score**: 3-tier risk scoring (0-3)
- **Unicode Character Detection**: Identifies non-ASCII characters
- **Homograph Attack Detection**: Detects lookalike character substitution

**Risk Indicators:**
- Edit distance ≤ 2: +20 risk score
- Unicode characters: +10 risk score

### 11. ML Classification with XGBoost ✅
- **Random Forest**: Current implementation
- **XGBoost Ready**: Dependencies installed for future upgrade
- **Cross-Validation**: Framework for model evaluation
- **Feature Importance**: Track most predictive features

### 12. Explainability & Calibrated Thresholds ✅
- **Risk Score Calculation**: 0-100 scale based on weighted features
- **Risk Levels**: Critical, High, Medium, Low, Very Low
- **Feature Explanations**: Human-readable risk indicators
- **Confidence Adjustment**: ML confidence adjusted by risk score
- **Detailed Reporting**: Comprehensive analysis breakdown

## Risk Scoring System

### Risk Score Calculation (0-100)
```
Critical Risk Factors (High Weight):
- Newly registered domain: +20
- Self-signed SSL: +15
- Form posts to external domain: +25
- IP address in URL: +15
- High typosquatting score: +20

Medium Risk Factors:
- Login form present: +10
- Suspicious JavaScript: +10
- Redirect to different domain: +10
- Unicode characters: +10
- Blacklist indicators: +15

Positive Factors (Risk Reduction):
- Valid SSL from trusted issuer: -10
- Domain age > 1 year: -15
- Reputable registrar: -5
```

### Risk Levels
- **Critical**: Score ≥ 70 (Immediate threat)
- **High**: Score ≥ 50 (High probability of phishing)
- **Medium**: Score ≥ 30 (Suspicious indicators present)
- **Low**: Score ≥ 10 (Minor concerns)
- **Very Low**: Score < 10 (Likely legitimate)

## API Response Structure

```json
{
  "url": "https://example.com",
  "prediction": "Phishing",
  "is_phishing": true,
  "confidence": 87.5,
  "phishing_probability": 87.5,
  "legitimate_probability": 12.5,
  "risk_score": 65,
  "risk_level": "High",
  "explanations": [
    "⚠️ Domain registered within last 30 days (high risk)",
    "⚠️ Self-signed SSL certificate detected",
    "🚨 Login form posts to external domain (critical risk)"
  ],
  "advanced_analysis": {
    "whois": {
      "domain_age_days": 15,
      "is_newly_registered": 1,
      "registrar_reputation": 0
    },
    "ssl": {
      "has_valid_ssl": 1,
      "ssl_issuer_trusted": 0,
      "ssl_self_signed": 1,
      "ssl_days_to_expiry": 90
    },
    "content": {
      "has_login_form": 1,
      "form_posts_external": 1,
      "has_suspicious_js": 0
    },
    "reputation": {
      "typosquatting_score": 2,
      "min_edit_distance": 2,
      "blacklist_score": 0
    }
  },
  "features": { ... }
}
```

## Installation & Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- `requests`: HTTP requests for page content analysis
- `beautifulsoup4`: HTML parsing
- `selenium`: Headless browser (optional)
- `Pillow`: Image processing
- `imagehash`: Image similarity
- `python-Levenshtein`: Edit distance calculation
- `cryptography`: SSL certificate parsing
- `geoip2`: IP geolocation (optional)
- `xgboost`: Advanced ML model
- `shap`: Model explainability

### API Keys (Optional but Recommended)
For production deployment, obtain API keys for:
- **PhishTank**: https://www.phishtank.com/api_info.php
- **Google Safe Browsing**: https://developers.google.com/safe-browsing
- **VirusTotal**: https://www.virustotal.com/gui/join-us
- **MaxMind GeoIP2**: https://www.maxmind.com/en/geoip2-services-and-databases

## Usage

### Basic Request
```python
import requests

response = requests.post('https://your-api.com/predict', json={
    'url': 'https://suspicious-site.com',
    'advanced': True
})

result = response.json()
print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']}")
```

### Disable Advanced Features
```python
response = requests.post('https://your-api.com/predict', json={
    'url': 'https://example.com',
    'advanced': False  # Use basic features only
})
```

## Performance Considerations

### Analysis Time
- Basic features: ~1-2 seconds
- Advanced features: ~5-10 seconds
- With external API calls: ~10-15 seconds

### Optimization Tips
1. **Caching**: Implement Redis cache for WHOIS/DNS lookups
2. **Async Processing**: Use Celery for background analysis
3. **Rate Limiting**: Implement rate limits for external API calls
4. **Timeout Settings**: Set appropriate timeouts (5-10 seconds)
5. **Parallel Processing**: Use threading for independent checks

## Security Best Practices

1. **Sandbox Execution**: Run page content analysis in isolated environment
2. **Request Timeouts**: Always set timeouts to prevent hanging
3. **SSL Verification**: Use `verify=False` carefully, only for analysis
4. **Input Validation**: Sanitize all URL inputs
5. **Rate Limiting**: Implement API rate limiting
6. **Error Handling**: Graceful degradation when features fail

## Future Enhancements

### Planned Features
1. **Machine Learning Improvements**
   - XGBoost model training
   - SHAP value explanations
   - Model ensemble (RF + XGBoost + Neural Network)

2. **Real-time Threat Intelligence**
   - Live PhishTank integration
   - Google Safe Browsing API
   - VirusTotal scanning

3. **Visual Analysis**
   - Screenshot capture
   - Logo detection and matching
   - Layout similarity scoring

4. **Behavioral Analysis**
   - JavaScript execution monitoring
   - Network request tracking
   - Cookie and storage analysis

5. **Historical Data**
   - Passive DNS integration
   - Domain history tracking
   - Reputation scoring over time

## Troubleshooting

### Common Issues

**SSL Certificate Errors**
```python
# Disable SSL verification for analysis only
requests.get(url, verify=False, timeout=10)
```

**WHOIS Lookup Failures**
- Some domains block WHOIS queries
- Use fallback to DNS-based age estimation
- Implement caching to reduce queries

**Timeout Issues**
- Increase timeout values for slow sites
- Implement async processing
- Use connection pooling

**Memory Usage**
- Limit concurrent analyses
- Clear BeautifulSoup objects after use
- Implement request size limits

## Contributing

To add new features:
1. Add feature extraction method to `AdvancedFeatureExtractor`
2. Update risk score calculation in `calculate_risk_score()`
3. Add explanation logic in `get_feature_explanations()`
4. Update frontend display in `displayAdvancedAnalysis()`
5. Document in this file

## License
MIT License - See LICENSE file for details
