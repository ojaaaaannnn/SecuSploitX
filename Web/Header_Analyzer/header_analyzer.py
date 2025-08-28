import requests
from urllib.parse import urlparse

class HeaderAnalyzer:
    def __init__(self, url):
        self.url = url
        self.headers = {}
        self.security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'X-XSS-Protection',
            'Content-Security-Policy',
            'Referrer-Policy',
            'Feature-Policy',
            'Permissions-Policy'
        ]

    def analyze_headers(self):
        try:
            response = requests.get(self.url, timeout=10, verify=False, allow_redirects=True)
            self.headers = dict(response.headers)

            analysis = {
                'url': self.url,
                'status_code': response.status_code,
                'headers_found': list(self.headers.keys()),
                'security_analysis': {},
                'missing_security_headers': [],
                'server_info': self.headers.get('Server', 'Unknown'),
                'powered_by': self.headers.get('X-Powered-By', 'Unknown')
            }

            for header in self.security_headers:
                value = self.headers.get(header, "Missing")
                present = header in self.headers
                analysis['security_analysis'][header] = {
                    'present': present,
                    'value': value
                }
                if not present:
                    analysis['missing_security_headers'].append(header)

            return analysis

        except requests.exceptions.RequestException as e:
            return {'error': f"Request failed: {str(e)}"}
        except Exception as e:
            return {'error': f"Unexpected error: {str(e)}"}
