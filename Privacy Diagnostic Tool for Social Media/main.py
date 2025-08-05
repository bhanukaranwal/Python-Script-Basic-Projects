# Privacy Diagnostic Tool for Social Media — main.py

import re

class PrivacyDiagnosticTool:
    def __init__(self, profile_data):
        self.profile_data = profile_data

    def detect_exposed_info(self):
        exposed_info = {}
        # Patterns for risky info
        patterns = {
            'email': r'[\w.-]+@[\w.-]+\.\w+',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'address': r'\d{1,5} \w+ (Street|St|Avenue|Ave|Road|Rd|Lane|Ln)\b',
            'dob': r'\b\d{1,2}/\d{1,2}/\d{2,4}\b'
        }
        for key, pattern in patterns.items():
            matches = re.findall(pattern, self.profile_data)
            if matches:
                exposed_info[key] = list(set(matches))
        return exposed_info

    def calculate_privacy_score(self, exposed_info):
        score = 100
        for info_type, entries in exposed_info.items():
            score -= len(entries) * 10  # Penalize for each found info
        return max(score, 0)

    def generate_privacy_report(self):
        exposed_info = self.detect_exposed_info()
        privacy_score = self.calculate_privacy_score(exposed_info)
        report = {
            'privacy_score': privacy_score,
            'exposed_info': exposed_info,
            'recommendations': []
        }
        if privacy_score < 70:
            report['recommendations'].append('Review your profile to remove personal details.')
        if 'email' in exposed_info:
            report['recommendations'].append('Consider hiding your email address.')
        if 'phone' in exposed_info:
            report['recommendations'].append('Remove or mask phone numbers.')
        return report

if __name__ == '__main__':
    # Example simulated social media profile data
    profile_data = """
    Hello, my name is Jane Doe. You can reach me at jane.doe@example.com or call 123-456-7890.
    I live at 123 Maple Street.
    Born on 01/01/1990.
    """

    tool = PrivacyDiagnosticTool(profile_data)
    report = tool.generate_privacy_report()

    print(f"Privacy Score: {report['privacy_score']}%")
    print("Exposed Information:")
    for k, v in report['exposed_info'].items():
        print(f"- {k.capitalize()}: {', '.join(v)}")
    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"- {rec}")

# Suggestions to extend:
# - Crawl live social media profiles with user permission
# - Visualize exposure network graphs
# - Suggest or auto-correct privacy settings
# - Export privacy “score card” for user review
