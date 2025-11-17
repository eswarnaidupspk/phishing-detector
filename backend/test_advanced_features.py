#!/usr/bin/env python3
"""
Test script for advanced phishing detection features
"""

import requests
import json
from advanced_feature_extractor import AdvancedFeatureExtractor

def test_local_extraction():
    """Test feature extraction locally"""
    print("=" * 60)
    print("Testing Advanced Feature Extraction Locally")
    print("=" * 60)
    
    extractor = AdvancedFeatureExtractor()
    
    # Test URLs
    test_urls = [
        "https://google.com",
        "https://paypal.com",
        "http://suspicious-site-12345.tk",
    ]
    
    for url in test_urls:
        print(f"\n\nTesting URL: {url}")
        print("-" * 60)
        
        try:
            features = extractor.extract_all_features(url)
            
            # Display key features
            print(f"✓ URL Length: {features.get('url_length', 'N/A')}")
            print(f"✓ Domain Age: {features.get('domain_age_days', 'N/A')} days")
            print(f"✓ Newly Registered: {'Yes' if features.get('is_newly_registered') else 'No'}")
            print(f"✓ Has Valid SSL: {'Yes' if features.get('has_valid_ssl') else 'No'}")
            print(f"✓ SSL Self-Signed: {'Yes' if features.get('ssl_self_signed') else 'No'}")
            print(f"✓ Has Login Form: {'Yes' if features.get('has_login_form') else 'No'}")
            print(f"✓ Typosquatting Score: {features.get('typosquatting_score', 'N/A')}")
            print(f"✓ Min Edit Distance: {features.get('min_edit_distance', 'N/A')}")
            
            # Get explanations
            explanations = extractor.get_feature_explanations(features)
            if explanations:
                print("\nKey Findings:")
                for exp in explanations:
                    print(f"  {exp}")
            
            print("\n✅ Feature extraction successful!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def test_api_endpoint(api_url):
    """Test the API endpoint"""
    print("\n\n" + "=" * 60)
    print("Testing API Endpoint")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "Legitimate Site (Google)",
            "url": "https://google.com",
            "expected": "Legitimate"
        },
        {
            "name": "Legitimate Site (PayPal)",
            "url": "https://paypal.com",
            "expected": "Legitimate"
        },
        {
            "name": "Suspicious URL with IP",
            "url": "http://192.168.1.1/login",
            "expected": "Phishing"
        }
    ]
    
    for test in test_cases:
        print(f"\n\nTest: {test['name']}")
        print(f"URL: {test['url']}")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{api_url}/predict",
                json={"url": test['url'], "advanced": True},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✓ Prediction: {result.get('prediction', 'N/A')}")
                print(f"✓ Confidence: {result.get('confidence', 'N/A'):.1f}%")
                print(f"✓ Risk Level: {result.get('risk_level', 'N/A')}")
                print(f"✓ Risk Score: {result.get('risk_score', 'N/A')}")
                
                if result.get('explanations'):
                    print("\nKey Findings:")
                    for exp in result['explanations'][:5]:  # Show first 5
                        print(f"  {exp}")
                
                if result.get('advanced_analysis'):
                    adv = result['advanced_analysis']
                    print("\nAdvanced Analysis:")
                    print(f"  WHOIS - Domain Age: {adv['whois']['domain_age_days']} days")
                    print(f"  SSL - Valid: {adv['ssl']['has_valid_ssl']}")
                    print(f"  Content - Login Form: {adv['content']['has_login_form']}")
                    print(f"  Reputation - Typosquatting: {adv['reputation']['typosquatting_score']}")
                
                print("\n✅ API test successful!")
            else:
                print(f"❌ API returned status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out (this is normal for complex analysis)")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_health_check(api_url):
    """Test health check endpoint"""
    print("\n\n" + "=" * 60)
    print("Testing Health Check")
    print("=" * 60)
    
    try:
        response = requests.get(f"{api_url}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Status: {result.get('status', 'N/A')}")
            print(f"✓ Model Loaded: {result.get('model_loaded', 'N/A')}")
            print("\n✅ Health check passed!")
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🔍 Advanced Phishing Detection - Test Suite\n")
    
    # Test 1: Local feature extraction
    test_local_extraction()
    
    # Test 2: API endpoint (local)
    print("\n\nWould you like to test the API endpoint?")
    print("1. Local API (http://localhost:5000)")
    print("2. Production API (https://phishing-detector-98j4.onrender.com)")
    print("3. Skip API tests")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_health_check("http://localhost:5000")
        test_api_endpoint("http://localhost:5000")
    elif choice == "2":
        test_health_check("https://phishing-detector-98j4.onrender.com")
        test_api_endpoint("https://phishing-detector-98j4.onrender.com")
    else:
        print("\nSkipping API tests.")
    
    print("\n\n" + "=" * 60)
    print("Test Suite Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Review test results above")
    print("2. Fix any errors found")
    print("3. Deploy to production")
    print("4. Monitor logs for issues")
    print("\n")
