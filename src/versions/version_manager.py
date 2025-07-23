"""
Version Management System
Handles Freemium vs Premium feature sets
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import pandas as pd

@dataclass
class VersionConfig:
    """Configuration for different versions"""
    name: str
    max_respondents: int
    features: List[str]
    price: str
    support_level: str
    data_retention_days: int

class VersionManager:
    """
    Manages different versions of the quality culture barometer
    """
    
    def __init__(self):
        self.versions = {
            "freemium": VersionConfig(
                name="Freemium",
                max_respondents=100,
                features=[
                    "Basic assessment",
                    "Simple dashboard",
                    "PDF report",
                    "Email support",
                    "Basic analytics"
                ],
                price="Free",
                support_level="Community",
                data_retention_days=90
            ),
            "premium": VersionConfig(
                name="Premium",
                max_respondents=10000,
                features=[
                    "Full assessment",
                    "Advanced dashboard",
                    "Custom reports",
                    "Priority support",
                    "Advanced analytics",
                    "Multi-site comparison",
                    "Benchmarking",
                    "API access",
                    "White-label options",
                    "Custom branding"
                ],
                price="Contact sales",
                support_level="Dedicated",
                data_retention_days=365
            ),
            "enterprise": VersionConfig(
                name="Enterprise",
                max_respondents=100000,
                features=[
                    "Unlimited assessment",
                    "Custom framework",
                    "On-premise deployment",
                    "24/7 support",
                    "Advanced AI insights",
                    "Custom integrations",
                    "Dedicated account manager",
                    "Training programs",
                    "Compliance consulting"
                ],
                price="Custom pricing",
                support_level="Enterprise",
                data_retention_days=2555
            )
        }
    
    def get_version_config(self, version: str) -> VersionConfig:
        """Get configuration for specific version"""
        return self.versions.get(version.lower(), self.versions["freemium"])
    
    def check_feature_access(self, version: str, feature: str) -> bool:
        """Check if feature is available in version"""
        config = self.get_version_config(version)
        return feature in config.features
    
    def get_upgrade_path(self, current_version: str) -> Dict[str, str]:
        """Get upgrade recommendations"""
        upgrade_paths = {
            "freemium": {
                "next": "premium",
                "reason": "Need more respondents and advanced features",
                "benefits": [
                    "Up to 10,000 respondents",
                    "Advanced analytics",
                    "Multi-site comparison",
                    "Priority support"
                ]
            },
            "premium": {
                "next": "enterprise",
                "reason": "Need unlimited scale and custom solutions",
                "benefits": [
                    "Unlimited respondents",
                    "Custom framework",
                    "On-premise deployment",
                    "24/7 support"
                ]
            }
        }
        
        return upgrade_paths.get(current_version, {})
    
    def generate_feature_comparison(self) -> pd.DataFrame:
        """Generate feature comparison matrix"""
        features = [
            "Basic assessment", "Advanced assessment", "Custom framework",
            "Max respondents", "Multi-site", "Benchmarking", "API access",
            "Custom reports", "White-label", "Priority support", "24/7 support"
        ]
        
        comparison = []
        for version_name, config in self.versions.items():
            row = {"Feature": version_name.capitalize()}
            
            for feature in features:
                if feature == "Max respondents":
                    row[feature] = config.max_respondents
                else:
                    row[feature] = "✓" if feature in config.features else "✗"
            
            comparison.append(row)
        
        return pd.DataFrame(comparison)

class FreemiumAssessment:
    """Freemium version implementation"""
    
    def __init__(self):
        self.max_respondents = 100
        self.basic_items = [
            "Quality is a top priority in our organization",
            "I understand how my work impacts quality",
            "Quality issues are addressed promptly",
            "We continuously improve our processes",
            "I feel empowered to report quality concerns"
        ]
    
    def create_assessment(self, organization_name: str) -> Dict:
        """Create basic assessment"""
        return {
            "name": f"{organization_name} - Basic Assessment",
            "items": self.basic_items,
            "scale": "1-5 Likert",
            "max_respondents": self.max_respondents,
            "report_type": "PDF summary",
            "analytics": "Basic"
        }

class PremiumAssessment:
    """Premium version implementation"""
    
    def __init__(self):
        self.max_respondents = 10000
        self.advanced_items = {
            "Leadership": [
                "Executive team demonstrates visible commitment to quality",
                "Quality objectives are clearly communicated",
                "Resources are allocated to support quality initiatives",
                "Quality performance is regularly reviewed"
            ],
            "Process": [
                "Processes are standardized and documented",
                "Quality controls are integrated into processes",
                "Process performance is monitored",
                "Improvements are systematically implemented"
            ],
            "People": [
                "Employees are trained on quality requirements",
                "Quality responsibilities are clearly defined",
                "Employee feedback is encouraged",
                "Recognition programs support quality"
            ],
            "Results": [
                "Quality metrics are tracked and reported",
                "Customer satisfaction is measured",
                "Continuous improvement is demonstrated",
                "Benchmarking is performed"
            ]
        }
    
    def create_assessment(self, organization_name: str) -> Dict:
        """Create advanced assessment"""
        return {
            "name": f"{organization_name} - Advanced Assessment",
            "domains": self.advanced_items,
            "scale": "1-7 Likert + open questions",
            "max_respondents": self.max_respondents,
            "report_type": "Interactive dashboard + PDF",
            "analytics": "Advanced with AI insights",
            "features": [
                "Multi-site comparison",
                "Benchmarking",
                "Custom reporting",
                "API access"
            ]
        }

# Example usage
if __name__ == "__main__":
    manager = VersionManager()
    
    # Display version comparison
    comparison = manager.generate_feature_comparison()
    print("Feature Comparison:")
    print(comparison.to_string(index=False))
    
    # Check upgrade path
    upgrade = manager.get_upgrade_path("freemium")
    print(f"\nUpgrade from Freemium: {upgrade}")
    
    # Create assessments
    freemium = FreemiumAssessment()
    basic_assessment = freemium.create_assessment("Demo Company")
    print(f"\nFreemium Assessment: {basic_assessment}")
    
    premium = PremiumAssessment()
    advanced_assessment = premium.create_assessment("Demo Company")
    print(f"\nPremium Assessment: {advanced_assessment}")