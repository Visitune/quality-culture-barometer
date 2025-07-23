"""
Continuous Improvement Loop
PDCA integration with quality management systems
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
import json

@dataclass
class ImprovementAction:
    """Represents a single improvement action"""
    id: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    owner: str
    target_date: datetime
    status: str  # Planned, In Progress, Completed, Cancelled
    metrics: Dict[str, float]
    dependencies: List[str]

class PDCALoop:
    """
    Plan-Do-Check-Act continuous improvement loop
    Integrates with quality management systems
    """
    
    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.improvement_actions = []
        self.assessment_history = []
        self.benchmarks = {}
        
    def plan_phase(self, assessment_results: Dict) -> List[ImprovementAction]:
        """Plan phase - identify improvement opportunities"""
        actions = []
        
        # Analyze assessment results
        low_scoring_areas = self._identify_low_scoring_areas(assessment_results)
        
        for area, score in low_scoring_areas.items():
            if score < 70:  # Threshold for improvement
                action = ImprovementAction(
                    id=f"IMP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(actions)}",
                    title=f"Improve {area}",
                    description=f"Address low performance in {area} (score: {score:.1f})",
                    priority="High" if score < 50 else "Medium",
                    owner="Quality Manager",
                    target_date=datetime.now() + timedelta(days=90),
                    status="Planned",
                    metrics={"target_score": 80, "current_score": score},
                    dependencies=[]
                )
                actions.append(action)
        
        self.improvement_actions.extend(actions)
        return actions
    
    def do_phase(self, action_id: str, progress_update: Dict):
        """Do phase - execute improvement actions"""
        action = next((a for a in self.improvement_actions if a.id == action_id), None)
        if action:
            action.status = "In Progress"
            # Update progress metrics
            action.metrics.update(progress_update)
    
    def check_phase(self, reassessment_results: Dict) -> Dict[str, bool]:
        """Check phase - measure improvement effectiveness"""
        results = {}
        
        for action in self.improvement_actions:
            if action.status == "In Progress":
                area = action.title.replace("Improve ", "")
                if area in reassessment_results:
                    new_score = reassessment_results[area]
                    old_score = action.metrics.get("current_score", 0)
                    
                    improvement = new_score - old_score
                    results[action.id] = improvement > 5  # 5 point improvement threshold
                    
                    if results[action.id]:
                        action.status = "Completed"
                        action.metrics["final_score"] = new_score
    
        return results
    
    def act_phase(self, successful_actions: List[str]) -> Dict[str, str]:
        """Act phase - standardize successful improvements"""
        standardizations = {}
        
        for action_id in successful_actions:
            action = next((a for a in self.improvement_actions if a.id == action_id), None)
            if action and action.status == "Completed":
                # Create standardization document
                standardizations[action.title] = self._create_standardization(action)
        
        return standardizations
    
    def _identify_low_scoring_areas(self, results: Dict) -> Dict[str, float]:
        """Identify areas with low scores"""
        low_scoring = {}
        
        for category, score in results.items():
            if isinstance(score, (int, float)) and score < 80:
                low_scoring[category] = score
        
        return low_scoring
    
    def _create_standardization(self, action: ImprovementAction) -> str:
        """Create standardization document for successful improvement"""
        return f"""
        Standardization: {action.title}
        
        Description: {action.description}
        
        Success Metrics:
        - Initial Score: {action.metrics.get('current_score', 0)}
        - Target Score: {action.metrics.get('target_score', 80)}
        - Final Score: {action.metrics.get('final_score', 0)}
        
        Standardization Actions:
        1. Document the improvement process
        2. Train relevant personnel
        3. Update procedures and work instructions
        4. Monitor ongoing performance
        5. Schedule periodic reviews
        
        Next Review Date: {(datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')}
        """
    
    def generate_improvement_report(self) -> Dict:
        """Generate comprehensive improvement report"""
        report = {
            "organization_id": self.organization_id,
            "report_date": datetime.now().isoformat(),
            "total_actions": len(self.improvement_actions),
            "completed_actions": len([a for a in self.improvement_actions if a.status == "Completed"]),
            "in_progress": len([a for a in self.improvement_actions if a.status == "In Progress"]),
            "planned_actions": len([a for a in self.improvement_actions if a.status == "Planned"]),
            "improvement_trends": self._calculate_improvement_trends(),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _calculate_improvement_trends(self) -> Dict[str, float]:
        """Calculate improvement trends over time"""
        trends = {}
        
        # Group actions by category
        categories = {}
        for action in self.improvement_actions:
            category = action.title.split()[1]  # Extract category from title
            if category not in categories:
                categories[category] = []
            categories[category].append(action)
        
        # Calculate average improvement per category
        for category, actions in categories.items():
            completed = [a for a in actions if a.status == "Completed"]
            if completed:
                avg_improvement = np.mean([
                    a.metrics.get('final_score', 0) - a.metrics.get('current_score', 0)
                    for a in completed
                ])
                trends[category] = avg_improvement
        
        return trends
    
    def _generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Analyze action completion rates
        total = len(self.improvement_actions)
        completed = len([a for a in self.improvement_actions if a.status == "Completed"])
        
        if total > 0:
            completion_rate = completed / total
            
            if completion_rate < 0.7:
                recommendations.append("Improve action execution - consider resource allocation")
            
            if len([a for a in self.improvement_actions if a.priority == "High"]) > 5:
                recommendations.append("Focus on high-priority improvements to maximize impact")
        
        # Analyze trends
        trends = self._calculate_improvement_trends()
        low_improvement_areas = [k for k, v in trends.items() if v < 5]
        
        if low_improvement_areas:
            recommendations.append(f"Investigate low improvement areas: {', '.join(low_improvement_areas)}")
        
        return recommendations
    
    def integrate_with_qms(self, qms_system: str) -> Dict[str, str]:
        """Integrate with existing Quality Management System"""
        integrations = {
            "ISO9001": {
                "clause_6.2": "Quality objectives and planning",
                "clause_9.1": "Monitoring and measurement",
                "clause_10.2": "Nonconformity and corrective action"
            },
            "ISO13485": {
                "clause_5.4": "Quality planning",
                "clause_8.2": "Monitoring and measurement",
                "clause_8.5": "Improvement"
            },
            "FDA_QMM": {
                "management_review": "Quality culture assessment results",
                "corrective_action": "Improvement actions",
                "continuous_improvement": "PDCA loop integration"
            }
        }
        
        return integrations.get(qms_system, {})

class QualityCultureAmbassador:
    """Quality culture ambassador program"""
    
    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.ambassadors = []
    
    def create_ambassador_program(self, num_ambassadors: int = 10) -> Dict:
        """Create ambassador program structure"""
        program = {
            "program_name": "Quality Culture Champions",
            "objectives": [
                "Promote quality culture awareness",
                "Facilitate improvement initiatives",
                "Provide feedback and insights",
                "Support training programs"
            ],
            "ambassador_roles": [
                {
                    "role": "Executive Sponsor",
                    "responsibilities": ["Strategic oversight", "Resource allocation", "Leadership communication"]
                },
                {
                    "role": "Department Champion",
                    "responsibilities": ["Local implementation", "Team engagement", "Progress monitoring"]
                },
                {
                    "role": "Quality Facilitator",
                    "responsibilities": ["Training delivery", "Process improvement", "Data analysis"]
                }
            ],
            "training_modules": [
                "Quality culture fundamentals",
                "Improvement methodologies",
                "Communication skills",
                "Data-driven decision making"
            ]
        }
        
        return program
    
    def track_ambassador_impact(self, ambassador_id: str, metrics: Dict) -> Dict:
        """Track ambassador impact metrics"""
        return {
            "ambassador_id": ambassador_id,
            "engagement_score": metrics.get("engagement_score", 0),
            "improvements_initiated": metrics.get("improvements_initiated", 0),
            "training_sessions": metrics.get("training_sessions", 0),
            "feedback_collected": metrics.get("feedback_collected", 0),
            "last_updated": datetime.now().isoformat()
        }

# Example usage
if __name__ == "__main__":
    # Create PDCA loop
    pdca = PDCALoop("demo_organization")
    
    # Simulate assessment results
    assessment_results = {
        "Leadership": 65,
        "Process": 58,
        "People": 72,
        "Results": 61
    }
    
    # Plan phase
    actions = pdca.plan_phase(assessment_results)
    print("Improvement actions planned:", len(actions))
    
    # Simulate progress
    for action in actions:
        pdca.do_phase(action.id, {"progress": 50})
    
    # Check phase
    new_results = {
        "Leadership": 75,
        "Process": 68,
        "People": 78,
        "Results": 70
    }
    
    improvements = pdca.check_phase(new_results)
    print("Improvements achieved:", improvements)
    
    # Generate report
    report = pdca.generate_improvement_report()
    print("Improvement report:", json.dumps(report, indent=2))