import re
import whois
import dns.resolver
import tldextract
from urllib.parse import urlparse
from datetime import datetime

class FeatureExtractor:
    def __init__(self):
        pass
    
    def extract_features(self, url):
        """Extract all features from URL"""
        features = {}
        
        # Basic URL parsing
        parsed = urlparse(url)
        domain_info = tldextract.extract(url)
        
        # 1. URL Length
        features['url_length'] = len(url)
        
        # 2. Domain Length
        features['domain_length'] = len(domain_info.domain + '.' + domain_info.suffix)
        
        # 3. Host Length
        features['host_length'] = len(parsed.netloc)
        
        # 4. Number of dots
        features['num_dots'] = url.count('.')
        
        # 5. Number of hyphens
        features['num_hyphens'] = url.count('-')
        
        # 6. Number of underscores
        features['num_underscores'] = url.count('_')
        
        # 7. Number of slashes
        features['num_slashes'] = url.count('/')
        
        # 8. Number of question marks
        features['num_question'] = url.count('?')
        
        # 9. Number of equal signs
        features['num_equal'] = url.count('=')
        
        # 10. Number of at symbols
        features['num_at'] = url.count('@')
        
        # 11. Number of ampersands
        features['num_ampersand'] = url.count('&')
        
        # 12. Number of digits
        features['num_digits'] = sum(c.isdigit() for c in url)
        
        # 13. Has HTTPS
        features['has_https'] = 1 if parsed.scheme == 'https' else 0
        
        # 14. Has IP address
        features['has_ip'] = 1 if self._has_ip_address(parsed.netloc) else 0
        
        # 15. Domain age (in days)
        features['domain_age'] = self._get_domain_age(domain_info.domain + '.' + domain_info.suffix)
        
        # 16. DNS record exists
        features['dns_record'] = self._check_dns_record(domain_info.domain + '.' + domain_info.suffix)
        
        # 17. Subdomain level
        features['subdomain_level'] = len(domain_info.subdomain.split('.')) if domain_info.subdomain else 0
        
        # 18. Has suspicious words
        suspicious_words = ['login', 'verify', 'account', 'update', 'secure', 'banking', 'confirm']
        features['has_suspicious_words'] = 1 if any(word in url.lower() for word in suspicious_words) else 0
        
        return features
    
    def _has_ip_address(self, netloc):
        """Check if URL contains IP address"""
        ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        return bool(ip_pattern.search(netloc))
    
    def _get_domain_age(self, domain):
        """Get domain age in days"""
        try:
            w = whois.whois(domain)
            if w.creation_date:
                creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
                age = (datetime.now() - creation_date).days
                return age if age >= 0 else -1
        except:
            pass
        return -1
    
    def _check_dns_record(self, domain):
        """Check if DNS record exists"""
        try:
            dns.resolver.resolve(domain, 'A')
            return 1
        except:
            return 0
