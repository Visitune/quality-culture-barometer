"""
Quality Culture Assessment Engine
Core assessment framework based on ISO 10010:2022 and international standards
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class AssessmentType(Enum):
    """Supported assessment frameworks"""
    ISO_10010 = "iso_10010"
    AFNOR = "afnor"
    PDA = "pda"
    EFQM = "efqm"
    BALDRIGE = "baldrige"
    CUSTOM = "custom"

class Sector(Enum):
    """Supported industry sectors"""
    GENERIC = "generic"
    PHARMACEUTICAL = "pharmaceutical"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    MANUFACTURING = "manufacturing"
    FINANCIAL = "financial"

@dataclass
class AssessmentConfig:
    """Configuration for assessment deployment"""
    assessment_type: AssessmentType
    sector: Sector
    version: str  # 'freemium' or 'premium'
    sample_size: int
    anonymity_level: str  # 'full', 'partial', 'none'
    language: str = 'fr'
    include_external_stakeholders: bool = False

class QualityCultureAssessment:
    """
    Main assessment engine implementing ISO 10010:2022 methodology
    """
    
    def __init__(self, config: AssessmentConfig):
        self.config = config
        self.framework = self._load_framework()
        self.items_bank = self._load_items_bank()
        self.scoring_engine = ScoringEngine(config)
        
    def _load_framework(self) -> Dict:
        """Load the appropriate framework based on assessment type"""
        frameworks = {
            AssessmentType.ISO_10010: self._load_iso10010_framework(),
            AssessmentType.AFNOR: self._load_afnor_framework(),
            AssessmentType.PDA: self._load_pda_framework(),
            AssessmentType.EFQM: self._load_efqm_framework(),
            AssessmentType.BALDRIGE: self._load_baldrige_framework()
        }
        return frameworks.get(self.config.assessment_type, {})
    
    def _load_iso10010_framework(self) -> Dict:
        """ISO 10010:2022 framework structure"""
        return {
            "dimensions": {
                "leadership": {
                    "weight": 0.25,
                    "subthemes": ["vision_alignment", "commitment", "resource_allocation"]
                },
                "engagement": {
                    "weight": 0.20,
                    "subthemes": ["employee_involvement", "empowerment", "recognition"]
                },
                "process_approach": {
                    "weight": 0.20,
                    "subthemes": ["systematic_approach", "continuous_improvement", "evidence_based"]
                },
                "customer_focus": {
                    "weight": 0.15,
                    "subthemes": ["understanding_needs", "satisfaction_measurement", "relationship_management"]
                },
                "learning_development": {
                    "weight": 0.20,
                    "subthemes": ["knowledge_management", "competence_development", "innovation"]
                }
            },
            "methodology": {
                "steps": [
                    "understand_context",
                    "determine_desired_culture",
                    "assess_current_culture",
                    "identify_gaps",
                    "develop_action_plan",
                    "implement_changes",
                    "monitor_improvement"
                ]
            }
        }
    
    def _load_afnor_framework(self) -> Dict:
        """AFNOR Quality Culture Barometer structure"""
        return {
            "dimensions": {
                "responsibility": {"weight": 0.10},
                "first_time_right": {"weight": 0.10},
                "problem_reporting": {"weight": 0.10},
                "continuous_improvement": {"weight": 0.10},
                "customer_focus": {"weight": 0.10},
                "leadership": {"weight": 0.10},
                "engagement": {"weight": 0.10},
                "training": {"weight": 0.10},
                "communication": {"weight": 0.10},
                "results_orientation": {"weight": 0.10}
            },
            "methodology": {
                "double_perspective": True,  # Individual vs company view
                "npqs_calculation": True,
                "slider_scale": True
            }
        }
    
    def _load_pda_framework(self) -> Dict:
        """PDA Quality Culture Assessment for pharmaceutical"""
        return {
            "dimensions": {
                "leadership": {"maturity_elements": 5},
                "communication": {"maturity_elements": 4},
                "ownership": {"maturity_elements": 4},
                "continuous_improvement": {"maturity_elements": 4},
                "technical_excellence": {"maturity_elements": 4}
            },
            "methodology": {
                "maturity_levels": 5,
                "audit_combination": True,
                "regulatory_compliance": True
            }
        }
    
    def _load_efqm_framework(self) -> Dict:
        """EFQM RADAR framework"""
        return {
            "criteria": {
                "leadership": {"weight": 0.10},
                "strategy": {"weight": 0.08},
                "people": {"weight": 0.09},
                "partnerships": {"weight": 0.09},
                "processes": {"weight": 0.14},
                "customer_results": {"weight": 0.20},
                "people_results": {"weight": 0.12},
                "society_results": {"weight": 0.06},
                "business_results": {"weight": 0.15}
            },
            "methodology": {
                "radar_approach": True,
                "scoring_matrix": True
            }
        }
    
    def _load_baldrige_framework(self) -> Dict:
        """Baldrige Excellence Framework"""
        return {
            "criteria": {
                "leadership": {"weight": 0.12},
                "strategy": {"weight": 0.08},
                "customers": {"weight": 0.12},
                "measurement": {"weight": 0.09},
                "workforce": {"weight": 0.12},
                "operations": {"weight": 0.12},
                "results": {"weight": 0.45}
            },
            "methodology": {
                "scoring_guidelines": True,
                "maturity_levels": True
            }
        }
    
    def _load_items_bank(self) -> Dict:
        """Load the appropriate items bank based on sector and type"""
        # This would load from JSON files in production
        return {
            "generic": self._load_generic_items(),
            "pharmaceutical": self._load_pharma_items(),
            "healthcare": self._load_healthcare_items(),
            "education": self._load_education_items()
        }
    
    def _load_generic_items(self) -> List[Dict]:
        """Generic items applicable across sectors"""
        return [
            {
                "id": "L1",
                "dimension": "leadership",
                "text": "La Direction communique clairement ses attentes qualité",
                "type": "likert_5",
                "mirror": True
            },
            {
                "id": "B3",
                "dimension": "behaviors",
                "text": "Je signale immédiatement tout écart",
                "type": "likert_5",
                "mirror": True
            },
            {
                "id": "P2",
                "dimension": "process",
                "text": "Les indicateurs qualité sont accessibles en temps réel",
                "type": "likert_5",
                "mirror": True
            }
        ]
    
    def _load_pharma_items(self) -> List[Dict]:
        """Pharmaceutical sector specific items"""
        return [
            {
                "id": "PH1",
                "dimension": "regulatory",
                "text": "Les exigences réglementaires sont intégrées dans nos processus",
                "type": "likert_5"
            },
            {
                "id": "PH2",
                "dimension": "validation",
                "text": "Les validations sont réalisées selon les bonnes pratiques",
                "type": "likert_5"
            }
        ]
    
    def _load_healthcare_items(self) -> List[Dict]:
        """Healthcare sector specific items"""
        return [
            {
                "id": "HC1",
                "dimension": "patient_safety",
                "text": "La sécurité des patients est notre priorité absolue",
                "type": "likert_5"
            }
        ]
    
    def _load_education_items(self) -> List[Dict]:
        """Education sector specific items"""
        return [
            {
                "id": "ED1",
                "dimension": "student_focus",
                "text": "La réussite des étudiants guide nos décisions",
                "type": "likert_5"
            }
        ]
    
    def generate_assessment(self) -> Dict:
        """Generate the complete assessment structure"""
        items = self._select_items()
        structure = {
            "framework": self.framework,
            "items": items,
            "scoring_method": self.scoring_engine.get_methodology(),
            "validation_criteria": self._get_validation_criteria()
        }
        return structure
    
    def _select_items(self) -> List[Dict]:
        """Select appropriate items based on configuration"""
        base_items = self.items_bank["generic"]
        
        if self.config.sector != Sector.GENERIC:
            sector_items = self.items_bank.get(self.config.sector.value, [])
            base_items.extend(sector_items)
        
        # Filter based on version
        if self.config.version == "freemium":
            return base_items[:20]  # Limit items for freemium
        return base_items
    
    def _get_validation_criteria(self) -> Dict:
        """Get validation criteria for the assessment"""
        return {
            "minimum_sample_size": max(200, len(self._select_items()) * 10),
            "cronbach_alpha_threshold": 0.7,
            "ave_threshold": 0.5,
            "response_rate_target": 0.7
        }

class ScoringEngine:
    """Handles scoring calculations for different frameworks"""
    
    def __init__(self, config: AssessmentConfig):
        self.config = config
        
    def get_methodology(self) -> Dict:
        """Return appropriate scoring methodology"""
        methodologies = {
            AssessmentType.AFNOR: self._afnor_methodology(),
            AssessmentType.ISO_10010: self._iso10010_methodology(),
            AssessmentType.PDA: self._pda_methodology(),
            AssessmentType.EFQM: self._efqm_methodology(),
            AssessmentType.BALDRIGE: self._baldrige_methodology()
        }
        return methodologies.get(self.config.assessment_type, {})
    
    def _afnor_methodology(self) -> Dict:
        """AFNOR NPQS scoring methodology"""
        return {
            "type": "npqs",
            "calculation": "promoters - detractors",
            "scale": "0-10",
            "categories": {
                "promoters": [9, 10],
                "passives": [7, 8],
                "detractors": [0, 1, 2, 3, 4, 5, 6]
            }
        }
    
    def _iso10010_methodology(self) -> Dict:
        """ISO 10010 maturity scoring"""
        return {
            "type": "maturity",
            "levels": 5,
            "scale": "1-5",
            "descriptions": [
                "Initial/Ad-hoc",
                "Managed",
                "Defined",
                "Quantitatively Managed",
                "Optimizing"
            ]
        }
    
    def _pda_methodology(self) -> Dict:
        """PDA maturity scoring"""
        return {
            "type": "maturity_matrix",
            "levels": 5,
            "dimensions": ["leadership", "communication", "ownership", "ci", "technical"],
            "scoring": "0-100"
        }
    
    def _efqm_methodology(self) -> Dict:
        """EFQM RADAR scoring"""
        return {
            "type": "radar",
            "approach": {"weight": 0.25},
            "deployment": {"weight": 0.25},
            "assessment": {"weight": 0.25},
            "refinement": {"weight": 0.25}
        }
    
    def _baldrige_methodology(self) -> Dict:
        """Baldrige scoring"""
        return {
            "type": "maturity_levels",
            "levels": 6,
            "scale": "0-1000",
            "approach": "ADLI",
            "results": "LeTCI"
        }