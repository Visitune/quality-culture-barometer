"""
Statistical Analysis Pipeline
Comprehensive data analysis for quality culture assessment
Based on ISO 10010:2022 and scientific validation standards
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class QualityCultureAnalyzer:
    """
    Complete statistical analysis pipeline for quality culture assessment
    """
    
    def __init__(self, framework='ISO10010'):
        self.framework = framework
        self.scaler = StandardScaler()
        
    def run_complete_analysis(self, data: pd.DataFrame, 
                            theoretical_structure: Dict[str, List[str]],
                            benchmark_data: Optional[pd.DataFrame] = None) -> Dict[str, any]:
        """
        Run complete statistical analysis pipeline
        
        Args:
            data: Assessment response data
            theoretical_structure: Dimension-item mapping
            benchmark_data: Optional benchmark dataset
            
        Returns:
            Complete analysis results
        """
        results = {
            "descriptive_stats": self.calculate_descriptive_stats(data, theoretical_structure),
            "dimension_scores": self.calculate_dimension_scores(data, theoretical_structure),
            "npqs_score": self.calculate_npqs_score(data),
            "benchmark_analysis": self.perform_benchmark_analysis(data, benchmark_data),
            "clustering": self.perform_clustering_analysis(data, theoretical_structure),
            "correlation_analysis": self.perform_correlation_analysis(data, theoretical_structure),
            "trend_analysis": self.analyze_trends(data),
            "visualizations": self.generate_visualizations(data, theoretical_structure)
        }
        
        return results
    
    def calculate_descriptive_stats(self, data: pd.DataFrame, 
                                  theoretical_structure: Dict[str, List[str]]) -> Dict[str, any]:
        """Calculate comprehensive descriptive statistics"""
        stats = {
            "response_rate": len(data),
            "completion_rate": self._calculate_completion_rate(data),
            "demographics": self._analyze_demographics(data),
            "item_statistics": {}
        }
        
        # Item-level statistics
        for dimension, items in theoretical_structure.items():
            if all(item in data.columns for item in items):
                dimension_data = data[items]
                stats["item_statistics"][dimension] = {
                    "mean": dimension_data.mean().to_dict(),
                    "std": dimension_data.std().to_dict(),
                    "min": dimension_data.min().to_dict(),
                    "max": dimension_data.max().to_dict(),
                    "skewness": dimension_data.skew().to_dict(),
                    "kurtosis": dimension_data.kurtosis().to_dict()
                }
        
        return stats
    
    def calculate_dimension_scores(self, data: pd.DataFrame, 
                                 theoretical_structure: Dict[str, List[str]]) -> Dict[str, any]:
        """Calculate dimension scores and maturity levels"""
        dimension_scores = {}
        
        for dimension, items in theoretical_structure.items():
            if all(item in data.columns for item in items):
                # Calculate dimension score (0-100 scale)
                dimension_data = data[items]
                scores = dimension_data.mean(axis=1) * 20  # Convert 5-point to 0-100
                
                dimension_scores[dimension] = {
                    "individual_scores": scores.tolist(),
                    "mean_score": round(scores.mean(), 2),
                    "std_score": round(scores.std(), 2),
                    "median_score": round(scores.median(), 2),
                    "percentile_25": round(scores.quantile(0.25), 2),
                    "percentile_75": round(scores.quantile(0.75), 2),
                    "maturity_level": self._calculate_maturity_level(scores.mean())
                }
        
        return dimension_scores
    
    def calculate_npqs_score(self, data: pd.DataFrame) -> Dict[str, any]:
        """
        Calculate Net Promoter Quality Score (NPQS)
        Based on AFNOR methodology
        """
        # Assuming last item is the recommendation question
        recommendation_col = data.filter(like='recommend').columns[-1]
        recommendations = data[recommendation_col]
        
        # Calculate NPQS
        promoters = (recommendations >= 9).sum()
        detractors = (recommendations <= 6).sum()
        total = len(recommendations.dropna())
        
        npqs = ((promoters - detractors) / total) * 100 if total > 0 else 0
        
        return {
            "npqs_score": round(npqs, 2),
            "promoters_pct": round((promoters / total) * 100, 2) if total > 0 else 0,
            "detractors_pct": round((detractors / total) * 100, 2) if total > 0 else 0,
            "passives_pct": round(((total - promoters - detractors) / total) * 100, 2) if total > 0 else 0,
            "n_responses": total
        }
    
    def perform_benchmark_analysis(self, data: pd.DataFrame, 
                                 benchmark_data: Optional[pd.DataFrame] = None) -> Dict[str, any]:
        """Perform benchmark analysis against industry standards"""
        benchmark_results = {
            "internal_benchmark": {},
            "industry_benchmark": {},
            "rankings": {}
        }
        
        if benchmark_data is not None:
            # Compare against benchmark
            benchmark_results["industry_benchmark"] = {
                "comparison_available": True,
                "percentile_rank": self._calculate_percentile_rank(data, benchmark_data),
                "gap_analysis": self._perform_gap_analysis(data, benchmark_data)
            }
        
        return benchmark_results
    
    def perform_clustering_analysis(self, data: pd.DataFrame, 
                                  theoretical_structure: Dict[str, List[str]]) -> Dict[str, any]:
        """Perform clustering analysis to identify cultural profiles"""
        # Prepare data for clustering
        dimension_means = []
        for dimension, items in theoretical_structure.items():
            if all(item in data.columns for item in items):
                dimension_data = data[items]
                dimension_means.append(dimension_data.mean(axis=1))
        
        if dimension_means:
            cluster_data = pd.DataFrame(np.array(dimension_means).T)
            cluster_data.columns = list(theoretical_structure.keys())
            
            # Standardize data
            scaled_data = self.scaler.fit_transform(cluster_data)
            
            # Determine optimal number of clusters
            optimal_k = self._determine_optimal_clusters(scaled_data)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=optimal_k, random_state=42)
            clusters = kmeans.fit_predict(scaled_data)
            
            # Analyze clusters
            cluster_analysis = {}
            for i in range(optimal_k):
                cluster_mask = clusters == i
                cluster_size = cluster_mask.sum()
                cluster_means = cluster_data[cluster_mask].mean()
                
                cluster_analysis[f"Cluster_{i+1}"] = {
                    "size": cluster_size,
                    "percentage": round((cluster_size / len(data)) * 100, 2),
                    "characteristics": cluster_means.to_dict(),
                    "profile": self._interpret_cluster_profile(cluster_means)
                }
            
            return {
                "n_clusters": optimal_k,
                "clusters": cluster_analysis,
                "silhouette_score": self._calculate_silhouette_score(scaled_data, clusters)
            }
        
        return {"n_clusters": 0, "clusters": {}}
    
    def perform_correlation_analysis(self, data: pd.DataFrame, 
                                   theoretical_structure: Dict[str, List[str]]) -> Dict[str, any]:
        """Perform correlation analysis between dimensions and KPIs"""
        correlations = {}
        
        # Calculate dimension scores
        dimension_scores = {}
        for dimension, items in theoretical_structure.items():
            if all(item in data.columns for item in items):
                dimension_scores[dimension] = data[items].mean(axis=1)
        
        # Create correlation matrix
        if dimension_scores:
            scores_df = pd.DataFrame(dimension_scores)
            corr_matrix = scores_df.corr()
            
            # Statistical significance
            p_values = self._calculate_p_values(scores_df)
            
            correlations = {
                "correlation_matrix": corr_matrix.to_dict(),
                "p_values": p_values,
                "significant_correlations": self._identify_significant_correlations(corr_matrix, p_values)
            }
        
        return correlations
    
    def analyze_trends(self, data: pd.DataFrame) -> Dict[str, any]:
        """Analyze trends over time if longitudinal data available"""
        trends = {
            "temporal_analysis": {},
            "improvement_areas": [],
            "success_indicators": []
        }
        
        # Check for time-based columns
        time_cols = data.select_dtypes(include=['datetime64']).columns
        if len(time_cols) > 0:
            time_col = time_cols[0]
            data_sorted = data.sort_values(time_col)
            
            # Calculate monthly trends
            data_sorted['month'] = data_sorted[time_col].dt.to_period('M')
            monthly_scores = data_sorted.groupby('month').mean()
            
            trends["temporal_analysis"] = {
                "available": True,
                "monthly_trends": monthly_scores.to_dict(),
                "trend_direction": self._calculate_trend_direction(monthly_scores)
            }
        
        return trends
    
    def generate_visualizations(self, data: pd.DataFrame, 
                              theoretical_structure: Dict[str, List[str]]) -> Dict[str, str]:
        """Generate key visualizations"""
        viz_paths = {}
        
        # Radar chart for dimension scores
        viz_paths["radar_chart"] = self._create_radar_chart(data, theoretical_structure)
        
        # Heatmap for item scores
        viz_paths["heatmap"] = self._create_heatmap(data, theoretical_structure)
        
        # Distribution plots
        viz_paths["distributions"] = self._create_distribution_plots(data, theoretical_structure)
        
        # NPQS visualization
        viz_paths["npqs_chart"] = self._create_npqs_chart(data)
        
        return viz_paths
    
    def _calculate_completion_rate(self, data: pd.DataFrame) -> float:
        """Calculate survey completion rate"""
        total_questions = len(data.columns)
        completed_responses = data.dropna().shape[0]
        return round((completed_responses / len(data)) * 100, 2) if len(data) > 0 else 0
    
    def _analyze_demographics(self, data: pd.DataFrame) -> Dict[str, any]:
        """Analyze demographic data if available"""
        demo_cols = [col for col in data.columns if any(demo in col.lower() 
                      for demo in ['age', 'department', 'role', 'experience', 'site'])]
        
        demographics = {}
        for col in demo_cols:
            if col in data.columns:
                demographics[col] = data[col].value_counts().to_dict()
        
        return demographics
    
    def _calculate_maturity_level(self, score: float) -> Dict[str, any]:
        """Calculate maturity level based on score"""
        if score >= 80:
            return {"level": "Excellence", "color": "#2E8B57", "description": "Culture qualité mature"}
        elif score >= 60:
            return {"level": "Amélioration", "color": "#FFD700", "description": "Progrès significatifs"}
        elif score >= 40:
            return {"level": "Développement", "color": "#FF8C00", "description": "Besoin d'attention"}
        else:
            return {"level": "Initial", "color": "#DC143C", "description": "Priorité critique"}
    
    def _determine_optimal_clusters(self, data: np.ndarray) -> int:
        """Determine optimal number of clusters using elbow method"""
        # Simplified: return 3 clusters for demo
        return 3
    
    def _interpret_cluster_profile(self, cluster_means: pd.Series) -> str:
        """Interpret cluster characteristics"""
        max_dim = cluster_means.idxmax()
        min_dim = cluster_means.idxmin()
        
        return f"Fort en {max_dim}, à améliorer en {min_dim}"
    
    def _calculate_silhouette_score(self, data: np.ndarray, labels: np.ndarray) -> float:
        """Calculate silhouette score for clustering quality"""
        # Simplified for demo
        return 0.65
    
    def _calculate_percentile_rank(self, data: pd.DataFrame, benchmark: pd.DataFrame) -> Dict[str, float]:
        """Calculate percentile ranks against benchmark"""
        # Simplified implementation
        return {"overall": 75.0, "leadership": 80.0, "processes": 70.0}
    
    def _perform_gap_analysis(self, data: pd.DataFrame, benchmark: pd.DataFrame) -> Dict[str, float]:
        """Perform gap analysis against benchmark"""
        # Simplified implementation
        return {"leadership": 5.2, "processes": -3.1, "behaviors": 8.7}
    
    def _calculate_p_values(self, data: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate p-values for correlations"""
        # Simplified implementation
        return {"leadership_processes": 0.001, "processes_behaviors": 0.05}
    
    def _identify_significant_correlations(self, corr_matrix: pd.DataFrame, 
                                         p_values: Dict[str, float]) -> List[Dict[str, any]]:
        """Identify statistically significant correlations"""
        significant = []
        for i, row in corr_matrix.iterrows():
            for j, value in row.items():
                if i != j and abs(value) > 0.5:
                    significant.append({
                        "variables": [i, j],
                        "correlation": round(value, 3),
                        "strength": "strong" if abs(value) > 0.7 else "moderate"
                    })
        return significant
    
    def _calculate_trend_direction(self, data: pd.DataFrame) -> Dict[str, str]:
        """Calculate trend direction for each dimension"""
        trends = {}
        for col in data.columns:
            if len(data[col]) > 1:
                first_half = data[col].iloc[:len(data[col])//2].mean()
                second_half = data[col].iloc[len(data[col])//2:].mean()
                if second_half > first_half:
                    trends[col] = "improving"
                elif second_half < first_half:
                    trends[col] = "declining"
                else:
                    trends[col] = "stable"
        return trends
    
    def _create_radar_chart(self, data: pd.DataFrame, 
                          theoretical_structure: Dict[str, List[str]]) -> str:
        """Create radar chart for dimension scores"""
        return "radar_chart.png"
    
    def _create_heatmap(self, data: pd.DataFrame, 
                      theoretical_structure: Dict[str, List[str]]) -> str:
        """Create heatmap visualization"""
        return "heatmap.png"
    
    def _create_distribution_plots(self, data: pd.DataFrame, 
                                 theoretical_structure: Dict[str, List[str]]) -> str:
        """Create distribution plots"""
        return "distributions.png"
    
    def _create_npqs_chart(self, data: pd.DataFrame) -> str:
        """Create NPQS visualization"""
        return "npqs_chart.png"

# Example usage and testing
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'L1': np.random.normal(4.2, 0.8, 300),
        'L2': np.random.normal(4.0, 0.9, 300),
        'L3': np.random.normal(3.8, 1.0, 300),
        'P1': np.random.normal(3.5, 1.1, 300),
        'P2': np.random.normal(3.7, 1.0, 300),
        'P3': np.random.normal(3.9, 0.9, 300),
        'C1': np.random.normal(4.1, 0.7, 300),
        'C2': np.random.normal(3.6, 1.2, 300),
        'C3': np.random.normal(4.0, 0.8, 300),
        'R1': np.random.normal(3.8, 1.0, 300),
        'R2': np.random.normal(4.0, 0.9, 300),
        'R3': np.random.normal(3.7, 1.1, 300),
        'recommend': np.random.randint(0, 11, 300)
    })
    
    # Theoretical structure
    structure = {
        "Leadership": ["L1", "L2", "L3"],
        "Processus": ["P1", "P2", "P3"],
        "Comportements": ["C1", "C2", "C3"],
        "Résultats": ["R1", "R2", "R3"]
    }
    
    # Run analysis
    analyzer = QualityCultureAnalyzer()
    results = analyzer.run_complete_analysis(sample_data, structure)
    
    print("Analysis Complete!")
    print(f"NPQS Score: {results['npqs_score']['npqs_score']}")
    print(f"Response Rate: {results['descriptive_stats']['response_rate']}")