import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Web.Header_Analyzer.header_analyzer import HeaderAnalyzer

class HeaderAnalyzerBuilder:
    def __init__(self, url):
        self.url = url

    def run(self):
        analyzer = HeaderAnalyzer(self.url)
        return analyzer.analyze_headers()
