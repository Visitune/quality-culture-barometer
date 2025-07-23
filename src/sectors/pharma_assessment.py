"""
Pharmaceutical Sector Quality Culture Assessment
Based on PDA Quality Culture Assessment Tool and FDA QMM requirements
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class PharmaAssessmentConfig:
    """Configuration for pharmaceutical sector assessment"""
    regulatory_framework: str = "FDA QMM"
    maturity_levels: int = 5
    assessment_type: str = "Combined Audit + Survey"
    
class PharmaQualityCultureAssessment:
    """
    Pharmaceutical-specific quality culture assessment
    Implements PDA framework with FDA QMM compliance
    """
    
    def __init__(self, config: PharmaAssessmentConfig = None):
        self.config = config or PharmaAssessmentConfig()
        self.domains = {
            "Leadership": [
                "Executive commitment to quality",
                "Quality vision communication",
                "Resource allocation for quality",
                "Quality in strategic planning"
            ],
            "Communication": [
                "Open communication channels",
                "Quality message clarity",
                "Cross-functional collaboration",
                "Escalation processes"
            ],
            "Ownership": [
                "Individual accountability",
                "Team responsibility",
                "Quality ownership culture",
                "Proactive behavior"
            ],
            "Continuous Improvement": [
                "Learning from mistakes",
                "Process improvement initiatives",
                "Innovation encouragement",
                "Best practice sharing"
            ],
            "Technical Excellence": [
                "Scientific rigor",
                "Technical competency",
                "Quality systems knowledge",
                "Risk-based thinking"
            ]
        }
        
        self.maturity_matrix = {
            1: "Initial/Ad-hoc",
            2: "Developing",
            3: "Defined",
            4: "Managed",
            5: "Optimizing"
        }
    
    def get_assessment_items(self) -> Dict[str, List[str]]:
        """Get pharmaceutical-specific assessment items"""
        return self.domains
    
    def calculate_maturity_score(self, responses: pd.DataFrame) -> Dict[str, float]:
        """Calculate maturity scores for each domain"""
        scores = {}
        
        for domain, items in self.domains.items():
            if all(item in responses.columns for item in items):
                domain_scores = responses[items].mean()
                scores[domain] = (domain_scores.mean() / 5.0) * 100
        
        return scores
    
    def generate_compliance_report(self, scores: Dict[str, float]) -> Dict[str, str]:
        """Generate FDA QMM compliance report"""
        report = {
            "Overall Maturity": self._get_maturity_level(np.mean(list(scores.values()))),
            "Critical Areas": self._identify_critical_areas(scores),
            "Recommendations": self._generate_recommendations(scores),
            "Next Steps": self._define_next_steps(scores)
        }
        
        return report
    
    def _get_maturity_level(self, score: float) -> str:
        """Convert score to maturity level"""
        level = max(1, min(5, int(np.ceil(score / 20))))
        return self.maturity_matrix[level]
    
    def _identify_critical_areas(self, scores: Dict[str, float]) -> List[str]:
        """Identify areas needing improvement"""
        threshold = 60  # Below 60% is critical
        return [domain for domain, score in scores.items() if score < threshold]
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        if scores.get("Leadership", 0) < 70:
            recommendations.append("Enhance executive quality commitment through regular communication")
        
        if scores.get("Communication", 0) < 70:
            recommendations.append("Implement structured quality communication channels")
        
        if scores.get("Ownership", 0) < 70:
            recommendations.append("Develop quality accountability programs")
        
        if scores.get("Continuous Improvement", 0) < 70:
            recommendations.append("Establish systematic improvement processes")
        
        if scores.get("Technical Excellence", 0) < 70:
            recommendations.append("Invest in technical training and competency development")
        
        return recommendations
    
    def _define_next_steps(self, scores: Dict[str, float]) -> List[str]:
        """Define concrete next steps"""
        return [
            "Conduct gap analysis for critical areas",
            "Develop targeted improvement plans",
            "Schedule follow-up assessment in 6 months",
            "Train quality culture ambassadors",
            "Integrate findings into QMM roadmap"
        ]

class HealthcareAssessment(PharmaQualityCultureAssessment):
    """Healthcare-specific assessment based on NACCHO QI SAT 2.0"""
    
    def __init__(self):
        super().__init__()
        self.domains = {
            "Leadership Commitment": [
                "Executive leadership involvement",
                "Quality as strategic priority",
                "Resource allocation"
            ],
            "Customer Focus": [
                "Patient-centered care",
                "Community engagement",
                "Service quality"
            ],
            "Process Management": [
                "Standardized processes",
                "Performance monitoring",
                "Continuous improvement"
            ],
            "Workforce Development": [
                "Staff competency",
                "Training programs",
                "Performance management"
            ]
        }

class EducationAssessment(PharmaQualityCultureAssessment):
    """Education sector assessment based on QCI framework"""
    
    def __init__(self):
        super().__init__()
        self.domains = {
            "Leadership & Governance": [
                "Institutional commitment",
                "Policy development",
                "Resource allocation"
            ],
            "Teaching & Learning": [
                "Curriculum quality",
                "Assessment practices",
                "Student engagement"
            ],
            "Continuous Improvement": [
                "Feedback mechanisms",
                "Quality enhancement",
                "Innovation culture"
            ],
            "Stakeholder Engagement": [
                "Student involvement",
                "Industry partnerships",
                "Community engagement"
            ]
        }

# Example usage
if __name__ == "__main__":
    # Create pharmaceutical assessment
    pharma = PharmaQualityCultureAssessment()
    print("Pharmaceutical domains:", pharma.get_assessment_items())
    
    # Generate demo data
    demo_data = pd.DataFrame({
        "Executive commitment to quality": np.random.uniform(3, 5, 100),
        "Quality vision communication": np.random.uniform(3, 5, 100),
        "Resource allocation for quality": np.random.uniform(3, 5, 100),
        "Quality in strategic planning": np.random.uniform(3, 5, 100)
    })
    
    # Calculate scores
    scores = pharma.calculate_maturity_score(demo_data)
    print("Maturity scores:", scores)
    
    # Generate compliance report
    report = pharma.generate_compliance_report(scores)
    print("Compliance report:", report)