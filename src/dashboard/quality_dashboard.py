"""
Quality Culture Dashboard
Interactive dashboard with clear explanations and user guidance
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

class QualityCultureDashboard:
    """Interactive dashboard with step-by-step guidance"""
    
    def __init__(self):
        self.frameworks = {
            "ISO10010": {
                "name": "ISO 10010:2022 Quality Culture",
                "description": "International standard for quality culture assessment with 4 dimensions: Leadership, Process, People, Results"
            },
            "AFNOR": {
                "name": "AFNOR Baromètre Culture Qualité", 
                "description": "French quality culture barometer with 20 items and NPQS scoring"
            },
            "PDA": {
                "name": "PDA Quality Culture Assessment",
                "description": "Pharmaceutical industry standard with 21 maturity elements across 5 domains"
            }
        }
        
    def run_dashboard(self):
        """Main dashboard with user guidance"""
        st.set_page_config(
            page_title="Quality Culture Barometer",
            page_icon="📊",
            layout="wide"
        )
        
        # Sidebar for configuration
        st.sidebar.title("🎯 Configuration Guide")
        
        # Step 1: Framework Selection
        st.sidebar.markdown("### 📋 Step 1: Choose Framework")
        selected_framework = st.sidebar.selectbox(
            "Select Assessment Framework",
            list(self.frameworks.keys()),
            format_func=lambda x: self.frameworks[x]["name"],
            help="Each framework has different focus areas and scoring methods"
        )
        
        # Display framework explanation
        st.sidebar.info(self.frameworks[selected_framework]["description"])
        
        # Step 2: Assessment Mode
        st.sidebar.markdown("### 🚀 Step 2: Select Mode")
        mode = st.sidebar.radio(
            "Choose Operation Mode",
            ["📊 Demo Mode", "🎯 New Assessment", "📈 Load Existing Data"],
            help="Demo shows sample data, New creates fresh assessment, Load uses your data"
        )
        
        # Main content area
        st.title("📊 Quality Culture Barometer")
        
        # Welcome section with clear instructions
        with st.expander("🎯 How to Use This Dashboard", expanded=True):
            st.markdown("""
            ### 🚀 Quick Start Guide
            
            **This dashboard helps you measure and improve your organization's quality culture.**
            
            #### 📋 **Step-by-Step Process:**
            
            1. **Choose Framework** (left sidebar)
               - **ISO 10010**: International standard with 4 dimensions
               - **AFNOR**: French baromètre with NPQS scoring
               - **PDA**: Pharmaceutical industry standard
            
            2. **Select Mode** (left sidebar)
               - **Demo Mode**: See sample results and features
               - **New Assessment**: Create a fresh survey
               - **Load Data**: Upload your existing responses
            
            3. **Configure Assessment** (main area)
               - Set organization details
               - Choose demographics
               - Customize questions
            
            4. **Deploy Survey**
               - Generate survey links
               - Send to participants
               - Monitor responses
            
            5. **Analyze Results**
               - View real-time dashboard
               - Export reports
               - Create action plans
            
            #### 🎯 **What You'll Get:**
            - **Overall Quality Culture Score** (0-100)
            - **Net Promoter Quality Score (NPQS)** (-100 to +100)
            - **Maturity Level** (Initial → Optimizing)
            - **Detailed Analysis** by department/role
            - **Benchmark Comparisons**
            - **Improvement Recommendations**
            """)
        
        # Mode-specific content
        if mode == "📊 Demo Mode":
            self.show_demo_mode(selected_framework)
        elif mode == "🎯 New Assessment":
            self.show_new_assessment(selected_framework)
        else:
            self.show_load_data(selected_framework)
    
    def show_demo_mode(self, framework: str):
        """Show demo with sample data and explanations"""
        st.header("📊 Demo Mode - Sample Results")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("💡 **This is demo data** - showing what your results will look like")
        
        # Generate demo data
        data = self.generate_demo_data(framework)
        
        # Key metrics with explanations
        st.markdown("### 📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Responses", len(data), 
                     help="Number of people who completed the assessment")
        with col2:
            st.metric("NPQS Score", "72.5", 
                     help="Net Promoter Quality Score: Promoters - Detractors")
        with col3:
            st.metric("Overall Score", "78.2/100", 
                     help="Average quality culture score across all dimensions")
        with col4:
            st.metric("Completion Rate", "94.3%", 
                     help="Percentage of people who completed the full assessment")
        
        # Detailed breakdown
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Detailed Analysis", "🎯 Benchmark", "📋 Action Items"])
        
        with tab1:
            self.show_overview_with_explanations(data, framework)
        
        with tab2:
            self.show_detailed_analysis(data, framework)
        
        with tab3:
            self.show_benchmark_comparison(data, framework)
        
        with tab4:
            self.show_action_items(data, framework)
    
    def show_new_assessment(self, framework: str):
        """Create new assessment configuration"""
        st.header("🎯 Create New Assessment")
        
        with st.form("new_assessment"):
            st.markdown("### 🏢 Organization Details")
            
            col1, col2 = st.columns(2)
            with col1:
                org_name = st.text_input("Organization Name", placeholder="e.g., Acme Corp")
                industry = st.selectbox("Industry", 
                    ["Manufacturing", "Healthcare", "Pharmaceutical", "Education", "Technology", "Other"])
            
            with col2:
                num_employees = st.number_input("Number of Employees", min_value=10, max_value=100000, value=100)
                sites = st.multiselect("Sites/Locations", ["Site A", "Site B", "Site C", "Remote"], default=["Site A"])
            
            st.markdown("### 👥 Demographics to Collect")
            demographics = st.multiselect(
                "Select demographic questions",
                ["Department", "Role Level", "Years of Experience", "Location", "Age Group", "Education Level"],
                default=["Department", "Role Level", "Years of Experience"]
            )
            
            st.markdown("### 📋 Assessment Configuration")
            col1, col2 = st.columns(2)
            with col1:
                target_responses = st.number_input("Target Response Count", min_value=10, max_value=10000, value=100)
                anonymity = st.checkbox("Ensure complete anonymity", value=True)
            
            with col2:
                survey_language = st.selectbox("Survey Language", ["English", "French", "Spanish", "German"])
                reminder_frequency = st.selectbox("Reminder Frequency", ["None", "Weekly", "Every 3 days", "Daily"])
            
            submitted = st.form_submit_button("🚀 Generate Assessment", use_container_width=True)
            
            if submitted and org_name:
                assessment_config = {
                    "framework": framework,
                    "organization": org_name,
                    "industry": industry,
                    "employees": num_employees,
                    "sites": sites,
                    "demographics": demographics,
                    "target_responses": target_responses,
                    "anonymity": anonymity,
                    "language": survey_language,
                    "reminders": reminder_frequency
                }
                
                st.success("✅ Assessment Created Successfully!")
                st.json(assessment_config)
                
                # Generate survey links
                st.markdown("### 🔗 Survey Distribution")
                survey_link = f"http://localhost:8501/survey/{org_name.lower().replace(' ', '_')}_{framework.lower()}"
                st.code(survey_link, language="text")
                
                st.markdown("**Share this link with your employees:**")
                st.info(f"📧 **Email Template:**\n\nDear Team,\n\nWe're conducting a quality culture assessment. Please take 10-15 minutes to complete:\n\n🔗 {survey_link}\n\nYour responses are {'anonymous' if anonymity else 'confidential'} and will help us improve our quality culture.\n\nThank you!")
    
    def show_load_data(self, framework: str):
        """Load existing assessment data"""
        st.header("📈 Load Existing Assessment Data")
        
        uploaded_file = st.file_uploader(
            "Upload your assessment data",
            type=['csv', 'xlsx', 'json'],
            help="Upload responses in CSV, Excel, or JSON format"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    data = pd.read_excel(uploaded_file)
                else:
                    data = pd.read_json(uploaded_file)
                
                st.success("✅ Data loaded successfully!")
                st.dataframe(data.head())
                
                # Process and display results
                self.show_results_from_data(data, framework)
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.info("💡 Expected format: Columns should include framework dimensions (Leadership, Process, People, Results) and demographics")
    
    def show_overview_with_explanations(self, data: pd.DataFrame, framework: str):
        """Show overview with detailed explanations"""
        st.markdown("### 📊 Quality Culture Overview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🎯 Radar Chart Explanation")
            st.info("This chart shows your organization's strengths and improvement areas across key dimensions")
            
            dimensions = ['Leadership', 'Process', 'People', 'Results']
            scores = [data[dim].mean() * 20 for dim in dimensions]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=dimensions,
                fill='toself',
                name='Your Score',
                line_color='rgb(55, 128, 191)'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(range=[0, 100], tickfont_size=12),
                    angularaxis=dict(tickfont_size=12)
                ),
                title="Quality Culture Dimensions",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Score Interpretation")
            
            score_ranges = {
                "90-100": "🏆 Excellent - World class quality culture",
                "80-89": "⭐ Very Good - Strong foundation with minor gaps",
                "70-79": "👍 Good - Solid performance, room for improvement",
                "60-69": "⚠️ Fair - Significant gaps need addressing",
                "50-59": "❌ Poor - Major transformation required",
                "<50": "🚨 Critical - Immediate action needed"
            }
            
            for range_text, interpretation in score_ranges.items():
                st.write(f"**{range_text}**: {interpretation}")
    
    def show_detailed_analysis(self, data: pd.DataFrame, framework: str):
        """Show detailed analysis with explanations"""
        st.markdown("### 🔍 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Department Comparison")
            st.info("Compare quality culture scores across different departments")
            
            dept_scores = data.groupby('department')[['Leadership', 'Process', 'People', 'Results']].mean() * 20
            
            fig = px.bar(
                dept_scores.reset_index().melt(id_vars='department'),
                x='department',
                y='value',
                color='variable',
                title="Scores by Department",
                labels={'value': 'Score (0-100)', 'variable': 'Dimension'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Distribution Analysis")
            st.info("See how scores are distributed across your organization")
            
            selected_dim = st.selectbox("Select Dimension", ['Leadership', 'Process', 'People', 'Results'])
            
            fig = px.histogram(
                data, 
                x=selected_dim * 20,
                nbins=20,
                title=f"{selected_dim} Score Distribution",
                labels={'x': 'Score (0-100)'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def show_benchmark_comparison(self, data: pd.DataFrame, framework: str):
        """Show benchmark with explanations"""
        st.markdown("### 🎯 Benchmark Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📊 Industry Comparison")
            st.info("Compare your organization's performance against industry standards")
            
            categories = ['Leadership', 'Process', 'People', 'Results']
            current = [84, 76, 82, 78]
            industry = [75, 70, 73, 71]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Your Organization', 
                x=categories, 
                y=current,
                marker_color='rgb(55, 128, 191)'
            ))
            fig.add_trace(go.Bar(
                name='Industry Average', 
                x=categories, 
                y=industry,
                marker_color='rgb(219, 64, 82)'
            ))
            fig.update_layout(
                title="Benchmark Comparison",
                yaxis_title="Score (0-100)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Benchmark Insights")
            
            insights = [
                "✅ **Leadership**: 9 points above industry average",
                "✅ **People**: 9 points above industry average", 
                "⚠️ **Process**: 6 points above, but lowest dimension",
                "✅ **Results**: 7 points above industry average"
            ]
            
            for insight in insights:
                st.write(insight)
    
    def show_action_items(self, data: pd.DataFrame, framework: str):
        """Show actionable recommendations"""
        st.markdown("### 📋 Action Items & Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Priority Actions")
            
            actions = [
                {
                    "priority": "🔴 High",
                    "action": "Improve Process Standardization",
                    "dimension": "Process",
                    "current_score": "76/100",
                    "target": "85/100",
                    "timeline": "3 months"
                },
                {
                    "priority": "🟡 Medium", 
                    "action": "Enhance Leadership Communication",
                    "dimension": "Leadership",
                    "current_score": "84/100",
                    "target": "90/100",
                    "timeline": "2 months"
                },
                {
                    "priority": "🟢 Low",
                    "action": "Celebrate People Engagement Success",
                    "dimension": "People", 
                    "current_score": "82/100",
                    "target": "85/100",
                    "timeline": "1 month"
                }
            ]
            
            for action in actions:
                with st.expander(f"{action['priority']} - {action['action']}"):
                    st.write(f"**Dimension:** {action['dimension']}")
                    st.write(f"**Current Score:** {action['current_score']}")
                    st.write(f"**Target Score:** {action['target']}")
                    st.write(f"**Timeline:** {action['timeline']}")
        
        with col2:
            st.markdown("#### 📊 Next Steps")
            
            st.info("""
            **Immediate Actions (Next 30 days):**
            1. Share results with leadership team
            2. Identify process improvement champions
            3. Schedule department-specific feedback sessions
            
            **Medium-term (1-3 months):**
            1. Implement process standardization training
            2. Establish regular check-ins
            3. Create improvement action plans
            
            **Long-term (3-6 months):**
            1. Re-assess to measure progress
            2. Expand assessment to other sites
            3. Integrate with continuous improvement
            """)
    
    def generate_demo_data(self, framework: str) -> pd.DataFrame:
        """Generate realistic demo data"""
        np.random.seed(42)
        n = 500
        
        if framework == "ISO10010":
            data = {
                'Leadership': np.random.normal(4.2, 0.6, n),
                'Process': np.random.normal(3.8, 0.7, n),
                'People': np.random.normal(4.1, 0.5, n),
                'Results': np.random.normal(3.9, 0.8, n),
            }
        elif framework == "AFNOR":
            data = {
                'Responsibility': np.random.normal(4.0, 0.5, n),
                'First_Time_Right': np.random.normal(3.7, 0.6, n),
                'Problem_Reporting': np.random.normal(4.2, 0.5, n),
                'Continuous_Improvement': np.random.normal(3.9, 0.7, n),
            }
        else:  # PDA
            data = {
                'Leadership_Commitment': np.random.normal(4.1, 0.5, n),
                'Quality_Systems': np.random.normal(3.9, 0.6, n),
                'Risk_Management': np.random.normal(4.0, 0.5, n),
                'Training_Competency': np.random.normal(3.8, 0.7, n),
            }
        
        data.update({
            'department': np.random.choice(['Production', 'R&D', 'Sales', 'Quality', 'Operations'], n),
            'site': np.random.choice(['Site A', 'Site B', 'Site C', 'Remote'], n),
            'role_level': np.random.choice(['Individual', 'Team Lead', 'Manager', 'Executive'], n),
            'experience': np.random.choice(['<1yr', '1-3yrs', '3-5yrs', '5-10yrs', '>10yrs'], n)
        })
        
        return pd.DataFrame(data)
    
    def show_results_from_data(self, data: pd.DataFrame, framework: str):
        """Display results from uploaded data"""
        st.success("✅ Data processed successfully!")
        
        # Calculate scores
        dimensions = [col for col in data.columns if col not in ['department', 'site', 'role_level', 'experience']]
        scores = data[dimensions].mean() * 20
        
        st.markdown("### 📊 Results Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Score", f"{scores.mean():.1f}/100")
        with col2:
            st.metric("Total Responses", len(data))
        with col3:
            st.metric("Dimensions", len(dimensions))
        
        # Display detailed results
        st.dataframe(scores.to_frame('Score').T)
        
        # Visualizations
        fig = px.bar(
            x=dimensions,
            y=scores.values,
            title="Dimension Scores",
            labels={'x': 'Dimension', 'y': 'Score (0-100)'}
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    dashboard = QualityCultureDashboard()
    dashboard.run_dashboard()