"""
Scoring System for Quality Culture Assessment
Implements NPQS, Maturity Grids, and Statistical Validation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import stats
from sklearn.preprocessing import StandardScaler
import warnings

class NPQSScorer:
    """Net Promoter Quality Score calculation based on AFNOR methodology"""
    
    def __init__(self):
        self.promoter_threshold = 9
        self.passive_range = (7, 8)
        self.detractor_max = 6
        
    def calculate_npqs(self, responses: pd.Series) -> Dict[str, float]:
        """
        Calculate NPQS score from responses
        
        Args:
            responses: Series of responses (0-10 scale)
            
        Returns:
            Dict with NPQS score and category counts
        """
        if responses.empty:
            return {"npqs": 0.0, "promoters": 0, "passives": 0, "detractors": 0}
        
        promoters = (responses >= self.promoter_threshold).sum()
        passives = ((responses >= self.passive_range[0]) & 
                   (responses <= self.passive_range[1])).sum()
        detractors = (responses <= self.detractor_max).sum()
        
        total = len(responses)
        if total == 0:
            return {"npqs": 0.0, "promoters": 0, "passives": 0, "detractors": 0}
        
        npqs_score = ((promoters - detractors) / total) * 100
        
        return {
            "npqs": round(npqs_score, 2),
            "promoters": promoters,
            "passives": passives,
            "detractors": detractors,
            "promoter_pct": round((promoters / total) * 100, 2),
            "passive_pct": round((passives / total) * 100, 2),
            "detractor_pct": round((detractors / total) * 100, 2)
        }

class MaturityScorer:
    """Maturity grid scoring system (5 levels)"""
    
    def __init__(self):
        self.levels = {
            1: "Initial/Ad-hoc",
            2: "Managed",
            3: "Defined",
            4: "Quantitatively Managed",
            5: "Optimizing"
        }
        
    def calculate_maturity(self, responses: pd.DataFrame, 
                          weights: Optional[Dict[str, float]] = None) -> Dict[str, any]:
        """
        Calculate maturity scores for each dimension
        
        Args:
            responses: DataFrame with responses
            weights: Optional weights for dimensions
            
        Returns:
            Dict with maturity scores and levels
        """
        if responses.empty:
            return {"overall_maturity": 0, "dimension_scores": {}, "level": "Initial/Ad-hoc"}
        
        # Default equal weights if not provided
        if weights is None:
            weights = {col: 1.0 for col in responses.columns}
        
        dimension_scores = {}
        total_weight = 0
        
        for dimension in responses.columns:
            if dimension in weights:
                weighted_score = responses[dimension].mean() * weights[dimension]
                dimension_scores[dimension] = {
                    "score": round(responses[dimension].mean(), 2),
                    "weighted_score": round(weighted_score, 2),
                    "level": self._get_maturity_level(responses[dimension].mean()),
                    "std": round(responses[dimension].std(), 2)
                }
                total_weight += weights[dimension]
        
        # Calculate overall maturity
        overall_score = sum(
            scores["weighted_score"] for scores in dimension_scores.values()
        ) / total_weight
        
        overall_level = self._get_maturity_level(overall_score)
        
        return {
            "overall_maturity": round(overall_score, 2),
            "overall_level": overall_level,
            "dimension_scores": dimension_scores,
            "maturity_distribution": self._get_maturity_distribution(responses)
        }
    
    def _get_maturity_level(self, score: float) -> str:
        """Map score to maturity level"""
        if score >= 4.5:
            return "Optimizing"
        elif score >= 3.5:
            return "Quantitatively Managed"
        elif score >= 2.5:
            return "Defined"
        elif score >= 1.5:
            return "Managed"
        else:
            return "Initial/Ad-hoc"
    
    def _get_maturity_distribution(self, responses: pd.DataFrame) -> Dict[str, int]:
        """Get distribution of responses across maturity levels"""
        distribution = {}
        for col in responses.columns:
            levels = responses[col].apply(lambda x: self._get_maturity_level(x))
            distribution[col] = levels.value_counts().to_dict()
        return distribution

class EFQMRADARScorer:
    """EFQM RADAR scoring methodology"""
    
    def __init__(self):
        self.radar_weights = {
            "results": 0.25,
            "approach": 0.25,
            "deployment": 0.25,
            "assessment": 0.25
        }
        
    def calculate_radar_score(self, responses: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate RADAR scores
        
        Args:
            responses: DataFrame with RADAR criteria responses
            
        Returns:
            Dict with RADAR scores
        """
        if responses.empty:
            return {"total_score": 0, "radar_scores": {}}
        
        radar_scores = {}
        for criterion, weight in self.radar_weights.items():
            if criterion in responses.columns:
                score = responses[criterion].mean()
                radar_scores[criterion] = {
                    "score": round(score, 2),
                    "weighted_score": round(score * weight, 2)
                }
        
        total_score = sum(
            scores["weighted_score"] for scores in radar_scores.values()
        )
        
        return {
            "total_score": round(total_score, 2),
            "radar_scores": radar_scores
        }

class StatisticalValidator:
    """Statistical validation for assessment reliability and validity"""
    
    def __init__(self, alpha_threshold: float = 0.7, ave_threshold: float = 0.5):
        self.alpha_threshold = alpha_threshold
        self.ave_threshold = ave_threshold
        
    def calculate_reliability(self, responses: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate Cronbach's alpha for reliability
        
        Args:
            responses: DataFrame with item responses
            
        Returns:
            Dict with reliability metrics
        """
        if responses.empty or len(responses.columns) < 2:
            return {"cronbach_alpha": 0.0, "reliable": False}
        
        # Calculate Cronbach's alpha
        item_variances = responses.var()
        total_variance = responses.sum(axis=1).var()
        n_items = len(responses.columns)
        
        alpha = (n_items / (n_items - 1)) * (
            1 - item_variances.sum() / total_variance
        )
        
        return {
            "cronbach_alpha": round(alpha, 3),
            "reliable": alpha >= self.alpha_threshold,
            "n_items": n_items,
            "n_responses": len(responses)
        }
    
    def calculate_validity(self, responses: pd.DataFrame, 
                          dimensions: Dict[str, List[str]]) -> Dict[str, any]:
        """
        Calculate validity metrics (convergent and discriminant)
        
        Args:
            responses: DataFrame with responses
            dimensions: Dict mapping dimensions to item lists
            
        Returns:
            Dict with validity metrics
        """
        validity_results = {}
        
        for dimension, items in dimensions.items():
            if all(item in responses.columns for item in items):
                dimension_data = responses[items]
                
                # Average Variance Extracted (AVE)
                ave = self._calculate_ave(dimension_data)
                
                # Composite Reliability
                cr = self._calculate_composite_reliability(dimension_data)
                
                validity_results[dimension] = {
                    "ave": round(ave, 3),
                    "composite_reliability": round(cr, 3),
                    "valid": ave >= self.ave_threshold and cr >= self.alpha_threshold
                }
        
        return validity_results
    
    def _calculate_ave(self, data: pd.DataFrame) -> float:
        """Calculate Average Variance Extracted"""
        if data.empty:
            return 0.0
        
        # Simplified AVE calculation
        correlations = data.corr()
        n_items = len(data.columns)
        
        if n_items == 1:
            return data.iloc[:, 0].var()
        
        # Average of squared factor loadings
        loadings = []
        for col in data.columns:
            loading = abs(data[col].corr(data.mean(axis=1)))
            loadings.append(loading ** 2)
        
        ave = np.mean(loadings)
        return ave
    
    def _calculate_composite_reliability(self, data: pd.DataFrame) -> float:
        """Calculate Composite Reliability (CR)"""
        if data.empty:
            return 0.0
        
        # Simplified CR calculation
        loadings = []
        for col in data.columns:
            loading = abs(data[col].corr(data.mean(axis=1)))
            loadings.append(loading)
        
        sum_loadings = sum(loadings)
        sum_squared_loadings = sum([l ** 2 for l in loadings])
        
        cr = (sum_loadings ** 2) / ((sum_loadings ** 2) + sum_squared_loadings)
        return cr

class BenchmarkAnalyzer:
    """Benchmark analysis against industry standards"""
    
    def __init__(self):
        self.benchmark_data = {
            "industry_averages": {
                "npqs": 25.0,
                "maturity": 3.2,
                "leadership": 3.4,
                "engagement": 3.1,
                "process": 3.3
            },
            "percentiles": {
                25: {"npqs": 10, "maturity": 2.5},
                50: {"npqs": 25, "maturity": 3.2},
                75: {"npqs": 40, "maturity": 3.8},
                90: {"npqs": 55, "maturity": 4.3}
            }
        }
    
    def calculate_benchmark_position(self, scores: Dict[str, float]) -> Dict[str, any]:
        """
        Calculate benchmark position for given scores
        
        Args:
            scores: Dict with calculated scores
            
        Returns:
            Dict with benchmark analysis
        """
        benchmark = {}
        
        for metric, score in scores.items():
            if metric in self.benchmark_data["industry_averages"]:
                avg = self.benchmark_data["industry_averages"][metric]
                percentile = self._calculate_percentile(metric, score)
                
                benchmark[metric] = {
                    "score": score,
                    "industry_average": avg,
                    "difference": round(score - avg, 2),
                    "percentile": percentile,
                    "performance_level": self._get_performance_level(percentile)
                }
        
        return benchmark
    
    def _calculate_percentile(self, metric: str, score: float) -> int:
        """Calculate percentile position"""
        percentiles = self.benchmark_data["percentiles"]
        
        if metric == "npqs":
            if score >= 55:
                return 90
            elif score >= 40:
                return 75
            elif score >= 25:
                return 50
            else:
                return 25
        elif metric == "maturity":
            if score >= 4.3:
                return 90
            elif score >= 3.8:
                return 75
            elif score >= 3.2:
                return 50
            else:
                return 25
        
        return 50
    
    def _get_performance_level(self, percentile: int) -> str:
        """Get performance level based on percentile"""
        if percentile >= 90:
            return "Excellent"
        elif percentile >= 75:
            return "Good"
        elif percentile >= 50:
            return "Average"
        else:
            return "Needs Improvement"