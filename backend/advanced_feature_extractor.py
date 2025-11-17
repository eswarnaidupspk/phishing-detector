import re
import whois
import dns.resolver
import tldextract
import requests
import socket
import ssl
import hashlib
import imagehash
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import Levenshtein
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import json

class AdvancedFeatureExtractor:
    def __init__(self):
        # Popular domains for typosquatting detection
        self.popular_domains = [
            'google.com', 'facebook.com', 'amazon.com', 'apple.com', 'microsoft.com',
            'paypal.com', 'netflix.com', 'instagram.com', 'twitter.com', 'linkedin.com',
            'ebay.com', 'walmart.com', 'chase.com', 'bankofamerica.com', 'wellsfargo.com'
        ]
        
        # Suspicious hosting providers
        self.suspicious_asns = ['AS16276', 'AS8100', 'AS24940']  # Known bulletproof hosting
        
        # Blacklist cache
        self.blacklist_cache = {}
        
    def extract_all_features(self, url):
        """Extract comprehensive features from URL"""
        features = {}
        
        try:
            # Basic URL parsing
            parsed = urlparse(url)
            domain_info = tldextract.extract(url)
            full_domain = f"{domain_info.domain}.{domain_info.suffix}"
            
            # 1. Basic URL Features
            features.update(self._extract_basic_features(url, parsed, domain_info))
            
            # 2. WHOIS / Domain Age & Registrar
            features.update(self._extract_whois_features(full_domain))
            
            # 3. SSL Certificate Analysis
            features.update(self._extract_ssl_features(parsed.netloc))
            
            # 4. IP / Hosting / ASN Reputation
            features.update(self._extract_ip_asn_features(full_domain))
            
            # 5. Blacklist / Threat Feeds
            features.update(self._check_blacklists(url, full_domain))
            
            # 6. Page Content Analysis
            features.update(self._analyze_page_content(url))
            
            # 7. Redirect Chain Analysis
            features.update(self._analyze_redirects(url))
            
            # 8. Typosquatting Detection
            features.update(self._detect_typosquatting(full_domain))
            
            # 9. DNS Features
            features.update(self._extract_dns_features(full_domain))
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            # Return default features on error
            features = self._get_default_features()
        
        return features
    
    def _extract_basic_features(self, url, parsed, domain_info):
        """Extract basic URL structure features"""
        features = {
            'url_length': len(url),
            'domain_length': len(domain_info.domain + '.' + domain_info.suffix),
            'host_length': len(parsed.netloc),
            'num_dots': url.count('.'),
            'num_hyphens': url.count('-'),
            'num_underscores': url.count('_'),
            'num_slashes': url.count('/'),
            'num_question': url.count('?'),
            'num_equal': url.count('='),
            'num_at': url.count('@'),
            'num_ampersand': url.count('&'),
            'num_digits': sum(c.isdigit() for c in url),
            'has_https': 1 if parsed.scheme == 'https' else 0,
            'has_ip': 1 if self._has_ip_address(parsed.netloc) else 0,
            'subdomain_level': len(domain_info.subdomain.split('.')) if domain_info.subdomain else 0,
            'path_length': len(parsed.path),
            'query_length': len(parsed.query) if parsed.query else 0,
        }
        
        # Suspicious words detection
        suspicious_words = ['login', 'verify', 'account', 'update', 'secure', 'banking', 
                          'confirm', 'signin', 'password', 'credential', 'suspend']
        features['has_suspicious_words'] = 1 if any(word in url.lower() for word in suspicious_words) else 0
        
        return features
    
    def _extract_whois_features(self, domain):
        """Extract WHOIS information including domain age and registrar"""
        features = {
            'domain_age_days': -1,
            'domain_expiry_days': -1,
            'registrar_reputation': 0,
            'whois_privacy': 0,
        }
        
        try:
            w = whois.whois(domain)
            
            # Domain age
            if w.creation_date:
                creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
                if creation_date:
                    age = (datetime.now() - creation_date).days
                    features['domain_age_days'] = age if age >= 0 else -1
                    
                    # Newly registered domains (< 30 days) are high risk
                    features['is_newly_registered'] = 1 if 0 <= age < 30 else 0
            
            # Domain expiry
            if w.expiration_date:
                expiry_date = w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date
                if expiry_date:
                    days_to_expiry = (expiry_date - datetime.now()).days
                    features['domain_expiry_days'] = days_to_expiry
            
            # Registrar reputation (simplified - check against known good registrars)
            if w.registrar:
                trusted_registrars = ['GoDaddy', 'Namecheap', 'Google', 'Amazon', 'Cloudflare']
                features['registrar_reputation'] = 1 if any(tr.lower() in str(w.registrar).lower() 
                                                            for tr in trusted_registrars) else 0
            
            # WHOIS privacy protection
            if w.registrant_name:
                privacy_indicators = ['privacy', 'protected', 'redacted', 'whoisguard']
                features['whois_privacy'] = 1 if any(pi in str(w.registrant_name).lower() 
                                                     for pi in privacy_indicators) else 0
                
        except Exception as e:
            print(f"WHOIS lookup failed: {e}")
        
        return features
    
    def _extract_ssl_features(self, hostname):
        """Extract SSL certificate information"""
        features = {
            'has_valid_ssl': 0,
            'ssl_issuer_trusted': 0,
            'ssl_self_signed': 0,
            'ssl_days_to_expiry': -1,
            'ssl_domain_mismatch': 0,
        }
        
        try:
            # Remove port if present
            hostname = hostname.split(':')[0]
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_bin = ssock.getpeercert(binary_form=True)
                    cert = x509.load_der_x509_certificate(cert_bin, default_backend())
                    
                    features['has_valid_ssl'] = 1
                    
                    # Check issuer
                    issuer = cert.issuer.rfc4514_string()
                    trusted_issuers = ['Let\'s Encrypt', 'DigiCert', 'Comodo', 'GeoTrust', 
                                      'Thawte', 'GlobalSign', 'Sectigo']
                    features['ssl_issuer_trusted'] = 1 if any(ti in issuer for ti in trusted_issuers) else 0
                    
                    # Check if self-signed
                    features['ssl_self_signed'] = 1 if cert.issuer == cert.subject else 0
                    
                    # Days to expiry
                    expiry = cert.not_valid_after
                    days_to_expiry = (expiry - datetime.now()).days
                    features['ssl_days_to_expiry'] = days_to_expiry
                    
                    # Domain mismatch check
                    san_list = []
                    try:
                        san_ext = cert.extensions.get_extension_for_oid(
                            x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
                        )
                        san_list = [str(name.value) for name in san_ext.value]
                    except:
                        pass
                    
                    # Check if hostname matches certificate
                    cn = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
                    cn_value = cn[0].value if cn else ''
                    
                    domain_match = hostname == cn_value or hostname in san_list
                    features['ssl_domain_mismatch'] = 0 if domain_match else 1
                    
        except Exception as e:
            print(f"SSL check failed: {e}")
        
        return features
    
    def _extract_ip_asn_features(self, domain):
        """Extract IP address and ASN information"""
        features = {
            'ip_address': '',
            'is_private_ip': 0,
            'asn_reputation': 0,
            'hosting_provider_suspicious': 0,
        }
        
        try:
            # Resolve domain to IP
            ip = socket.gethostbyname(domain)
            features['ip_address'] = ip
            
            # Check if private IP
            ip_parts = ip.split('.')
            if ip_parts[0] in ['10', '172', '192']:
                features['is_private_ip'] = 1
            
            # ASN lookup (simplified - would need external API in production)
            # For now, just check if IP is in known suspicious ranges
            suspicious_ip_prefixes = ['185.', '194.', '46.']  # Example suspicious ranges
            features['hosting_provider_suspicious'] = 1 if any(ip.startswith(prefix) 
                                                               for prefix in suspicious_ip_prefixes) else 0
            
        except Exception as e:
            print(f"IP/ASN lookup failed: {e}")
        
        return features
    
    def _check_blacklists(self, url, domain):
        """Check against threat intelligence feeds"""
        features = {
            'in_phishtank': 0,
            'in_google_safebrowsing': 0,
            'blacklist_score': 0,
        }
        
        try:
            # PhishTank check (simplified - would need API key in production)
            # This is a placeholder - actual implementation would query PhishTank API
            
            # Google Safe Browsing (simplified - would need API key)
            # Placeholder for demonstration
            
            # Simple blacklist check based on domain characteristics
            blacklist_indicators = ['tk', 'ml', 'ga', 'cf', 'gq']  # Free TLDs often used for phishing
            tld = domain.split('.')[-1]
            if tld in blacklist_indicators:
                features['blacklist_score'] += 1
            
        except Exception as e:
            print(f"Blacklist check failed: {e}")
        
        return features
    
    def _analyze_page_content(self, url):
        """Analyze page content for phishing indicators"""
        features = {
            'has_login_form': 0,
            'has_password_field': 0,
            'num_external_links': 0,
            'has_hidden_fields': 0,
            'has_suspicious_js': 0,
            'has_iframes': 0,
            'form_posts_external': 0,
            'page_title_mismatch': 0,
        }
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=True)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Check for login forms
                forms = soup.find_all('form')
                for form in forms:
                    # Check for password fields
                    password_fields = form.find_all('input', {'type': 'password'})
                    if password_fields:
                        features['has_login_form'] = 1
                        features['has_password_field'] = 1
                    
                    # Check if form posts to external domain
                    action = form.get('action', '')
                    if action and action.startswith('http'):
                        parsed_action = urlparse(action)
                        parsed_url = urlparse(url)
                        if parsed_action.netloc != parsed_url.netloc:
                            features['form_posts_external'] = 1
                    
                    # Check for hidden fields
                    hidden_fields = form.find_all('input', {'type': 'hidden'})
                    if len(hidden_fields) > 3:
                        features['has_hidden_fields'] = 1
                
                # Count external links
                links = soup.find_all('a', href=True)
                external_count = 0
                for link in links:
                    href = link['href']
                    if href.startswith('http') and urlparse(url).netloc not in href:
                        external_count += 1
                features['num_external_links'] = external_count
                
                # Check for iframes
                iframes = soup.find_all('iframe')
                features['has_iframes'] = 1 if len(iframes) > 0 else 0
                
                # Check for suspicious JavaScript
                scripts = soup.find_all('script')
                suspicious_js_patterns = ['eval(', 'unescape(', 'fromCharCode', 'document.write']
                for script in scripts:
                    script_content = script.string if script.string else ''
                    if any(pattern in script_content for pattern in suspicious_js_patterns):
                        features['has_suspicious_js'] = 1
                        break
                
        except Exception as e:
            print(f"Page content analysis failed: {e}")
        
        return features
    
    def _analyze_redirects(self, url):
        """Analyze redirect chains"""
        features = {
            'num_redirects': 0,
            'redirect_to_different_domain': 0,
            'redirect_chain_length': 0,
        }
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True, verify=False)
            
            # Count redirects
            if response.history:
                features['num_redirects'] = len(response.history)
                features['redirect_chain_length'] = len(response.history)
                
                # Check if redirected to different domain
                original_domain = urlparse(url).netloc
                final_domain = urlparse(response.url).netloc
                if original_domain != final_domain:
                    features['redirect_to_different_domain'] = 1
                    
        except Exception as e:
            print(f"Redirect analysis failed: {e}")
        
        return features
    
    def _detect_typosquatting(self, domain):
        """Detect typosquatting and homograph attacks"""
        features = {
            'typosquatting_score': 0,
            'min_edit_distance': 100,
            'has_unicode_chars': 0,
            'homograph_score': 0,
        }
        
        try:
            # Check edit distance to popular domains
            min_distance = 100
            for popular in self.popular_domains:
                distance = Levenshtein.distance(domain.lower(), popular.lower())
                if distance < min_distance:
                    min_distance = distance
            
            features['min_edit_distance'] = min_distance
            
            # Typosquatting score (lower distance = higher risk)
            if min_distance <= 2:
                features['typosquatting_score'] = 3
            elif min_distance <= 4:
                features['typosquatting_score'] = 2
            elif min_distance <= 6:
                features['typosquatting_score'] = 1
            
            # Check for Unicode/homograph characters
            try:
                domain.encode('ascii')
            except UnicodeEncodeError:
                features['has_unicode_chars'] = 1
                features['homograph_score'] = 1
            
        except Exception as e:
            print(f"Typosquatting detection failed: {e}")
        
        return features
    
    def _extract_dns_features(self, domain):
        """Extract DNS-related features"""
        features = {
            'dns_record_exists': 0,
            'has_mx_record': 0,
            'num_dns_records': 0,
        }
        
        try:
            # Check A record
            try:
                answers = dns.resolver.resolve(domain, 'A')
                features['dns_record_exists'] = 1
                features['num_dns_records'] = len(answers)
            except:
                pass
            
            # Check MX record
            try:
                mx_answers = dns.resolver.resolve(domain, 'MX')
                features['has_mx_record'] = 1 if len(mx_answers) > 0 else 0
            except:
                pass
                
        except Exception as e:
            print(f"DNS feature extraction failed: {e}")
        
        return features
    
    def _has_ip_address(self, netloc):
        """Check if URL contains IP address"""
        ip_pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        return bool(ip_pattern.search(netloc))
    
    def _get_default_features(self):
        """Return default feature values"""
        return {
            'url_length': 0, 'domain_length': 0, 'host_length': 0,
            'num_dots': 0, 'num_hyphens': 0, 'num_underscores': 0,
            'num_slashes': 0, 'num_question': 0, 'num_equal': 0,
            'num_at': 0, 'num_ampersand': 0, 'num_digits': 0,
            'has_https': 0, 'has_ip': 0, 'subdomain_level': 0,
            'path_length': 0, 'query_length': 0, 'has_suspicious_words': 0,
            'domain_age_days': -1, 'domain_expiry_days': -1,
            'registrar_reputation': 0, 'whois_privacy': 0, 'is_newly_registered': 0,
            'has_valid_ssl': 0, 'ssl_issuer_trusted': 0, 'ssl_self_signed': 0,
            'ssl_days_to_expiry': -1, 'ssl_domain_mismatch': 0,
            'ip_address': '', 'is_private_ip': 0, 'asn_reputation': 0,
            'hosting_provider_suspicious': 0, 'in_phishtank': 0,
            'in_google_safebrowsing': 0, 'blacklist_score': 0,
            'has_login_form': 0, 'has_password_field': 0, 'num_external_links': 0,
            'has_hidden_fields': 0, 'has_suspicious_js': 0, 'has_iframes': 0,
            'form_posts_external': 0, 'page_title_mismatch': 0,
            'num_redirects': 0, 'redirect_to_different_domain': 0,
            'redirect_chain_length': 0, 'typosquatting_score': 0,
            'min_edit_distance': 100, 'has_unicode_chars': 0, 'homograph_score': 0,
            'dns_record_exists': 0, 'has_mx_record': 0, 'num_dns_records': 0,
        }
    
    def get_feature_explanations(self, features):
        """Generate human-readable explanations for features"""
        explanations = []
        
        # High-risk indicators
        if features.get('is_newly_registered', 0) == 1:
            explanations.append("⚠️ Domain registered within last 30 days (high risk)")
        
        if features.get('ssl_self_signed', 0) == 1:
            explanations.append("⚠️ Self-signed SSL certificate detected")
        
        if features.get('has_login_form', 0) == 1 and features.get('form_posts_external', 0) == 1:
            explanations.append("🚨 Login form posts to external domain (critical risk)")
        
        if features.get('typosquatting_score', 0) >= 2:
            explanations.append("⚠️ Domain similar to popular brand (possible typosquatting)")
        
        if features.get('has_unicode_chars', 0) == 1:
            explanations.append("⚠️ Unicode characters detected (homograph attack risk)")
        
        if features.get('has_ip', 0) == 1:
            explanations.append("⚠️ URL contains IP address instead of domain")
        
        if features.get('redirect_to_different_domain', 0) == 1:
            explanations.append("⚠️ Redirects to different domain")
        
        # Positive indicators
        if features.get('has_valid_ssl', 0) == 1 and features.get('ssl_issuer_trusted', 0) == 1:
            explanations.append("✓ Valid SSL certificate from trusted issuer")
        
        if features.get('domain_age_days', -1) > 365:
            explanations.append("✓ Domain registered over 1 year ago")
        
        if features.get('registrar_reputation', 0) == 1:
            explanations.append("✓ Registered with reputable registrar")
        
        return explanations
