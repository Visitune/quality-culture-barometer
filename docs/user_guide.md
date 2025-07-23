# Quality Culture Barometer - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Framework Overview](#framework-overview)
3. [Assessment Setup](#assessment-setup)
4. [Data Collection](#data-collection)
5. [Analysis & Reporting](#analysis--reporting)
6. [Continuous Improvement](#continuous-improvement)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### Quick Start (5 minutes)
1. **Choose Your Version**
   - **Freemium**: Up to 100 respondents, basic features
   - **Premium**: Up to 10,000 respondents, advanced analytics
   - **Enterprise**: Unlimited, custom solutions

2. **Select Framework**
   - **ISO 10010**: International standard for quality culture
   - **AFNOR**: French quality culture barometer
   - **PDA**: Pharmaceutical industry standard
   - **EFQM**: European excellence model
   - **Baldrige**: US excellence framework

3. **Launch Assessment**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Run dashboard
   streamlit run src/dashboard/quality_dashboard.py
   ```

### System Requirements
- Python 3.8+
- 4GB RAM minimum
- Modern web browser
- Internet connection for cloud features

## Framework Overview

### ISO 10010:2022 Quality Culture Framework
**Structure:**
- **Leadership**: Vision, commitment, resource allocation
- **Process**: Standardization, monitoring, improvement
- **People**: Competency, engagement, empowerment
- **Results**: Performance, customer satisfaction, continuous improvement

**Scoring:**
- 5-point Likert scale (1=Strongly Disagree to 5=Strongly Agree)
- Maturity levels: Initial → Developing → Defined → Managed → Optimizing
- Net Promoter Quality Score (NPQS): -100 to +100

### AFNOR Baromètre Culture Qualité
**Structure:**
- 20 items across 10 themes
- Double perspective: individual vs organizational view
- NPQS calculation: Promoters (9-10) - Detractors (0-6)

**Key Metrics:**
- Overall quality culture score
- Theme-specific scores
- Gap analysis (individual vs organizational)
- Benchmark comparison

## Assessment Setup

### Step 1: Configuration
```python
from src.core.assessment_engine import AssessmentEngine

# Initialize assessment
engine = AssessmentEngine(
    framework="ISO10010",
    version="premium",
    organization="Your Company"
)

# Configure parameters
config = {
    "max_respondents": 1000,
    "departments": ["Production", "R&D", "Sales", "Support"],
    "sites": ["Site A", "Site B", "Site C"],
    "anonymity": True,
    "language": "en"
}
```

### Step 2: Customization
```python
# Add custom questions
custom_items = [
    "Our quality culture supports innovation",
    "Quality metrics are transparent to all employees"
]

engine.add_custom_items(custom_items)

# Set demographic questions
demographics = {
    "department": ["Production", "R&D", "Sales", "Support"],
    "experience": ["<1yr", "1-3yrs", "3-5yrs", "5-10yrs", ">10yrs"],
    "role": ["Individual", "Team Lead", "Manager", "Executive"]
}

engine.set_demographics(demographics)
```

### Step 3: Distribution
```python
# Generate survey links
links = engine.generate_survey_links()

# Email templates
email_template = """
Subject: Quality Culture Assessment - Your Input Matters

Dear {name},

We're conducting a quality culture assessment to better understand our organization's strengths and areas for improvement.

Please take 10-15 minutes to complete the survey:
{survey_link}

Your responses are anonymous and will help us enhance our quality culture.

Thank you,
Quality Team
"""

# QR codes for physical locations
qr_codes = engine.generate_qr_codes()
```

## Data Collection

### Best Practices
1. **Communication Strategy**
   - Send announcement 1 week before
   - Reminder emails at 3 days, 1 day
   - Final reminder 24 hours before close
   - Share results timeline

2. **Response Rate Optimization**
   - Target: 70%+ response rate
   - Executive sponsorship visible
   - Department champions
   - Incentives (optional)

3. **Data Quality**
   - Validation rules built-in
   - Attention checks for quality
   - Time-based filtering
   - Pattern analysis for bots

### Monitoring Progress
```python
from src.analytics.statistical_pipeline import StatisticalPipeline

pipeline = StatisticalPipeline()
progress = pipeline.monitor_progress(
    survey_id="QC2024_001",
    expected_responses=1000,
    current_responses=750,
    response_rate=75
)

# Real-time dashboard
dashboard_url = pipeline.get_live_dashboard()
```

## Analysis & Reporting

### Automated Analysis
```python
from src.core.scoring_system import ScoringSystem

scorer = ScoringSystem(framework="ISO10010")
results = scorer.calculate_scores(responses_df)

# Key metrics
metrics = {
    "overall_score": results['overall'],
    "npqs": results['npqs'],
    "maturity_level": results['maturity'],
    "dimension_scores": results['dimensions'],
    "department_comparison": results['by_department']
}
```

### Interactive Dashboards
Access via: `http://localhost:8501`

**Dashboard Sections:**
1. **Overview**: Key metrics and trends
2. **Detailed Analysis**: Drill-down by dimension
3. **Benchmark**: Compare against industry
4. **Insights**: AI-powered recommendations
5. **Action Plan**: Generated improvement actions

### Report Generation
```python
# PDF reports
pdf_report = engine.generate_pdf_report(
    results=results,
    include_benchmark=True,
    include_recommendations=True
)

# Excel export
excel_file = engine.export_to_excel(
    results=results,
    include_raw_data=True,
    include_calculations=True
)

# PowerPoint presentation
pptx_file = engine.generate_presentation(
    results=results,
    template="executive_summary"
)
```

## Continuous Improvement

### PDCA Integration
```python
from src.continuous_improvement.pdca_loop import PDCALoop

pdca = PDCALoop(organization_id="your_org")

# Plan phase
actions = pdca.plan_phase(assessment_results)

# Do phase
for action in actions:
    pdca.do_phase(action.id, {"progress": 25})

# Check phase (after 3-6 months)
improvements = pdca.check_phase(new_assessment_results)

# Act phase
standardizations = pdca.act_phase(successful_actions)
```

### Quality Culture Ambassador Program
**Roles:**
- **Executive Sponsor**: Strategic oversight
- **Department Champions**: Local implementation
- **Quality Facilitators**: Training and support

**Training Modules:**
1. Quality culture fundamentals
2. Improvement methodologies
3. Communication skills
4. Data-driven decision making

### Regular Assessment Schedule
- **Baseline**: Initial comprehensive assessment
- **Pulse**: Quarterly mini-surveys (5-10 questions)
- **Full**: Annual comprehensive assessment
- **Targeted**: Issue-specific assessments

## Sector-Specific Guidance

### Pharmaceutical (FDA QMM)
**Additional Requirements:**
- GMP compliance questions
- Risk management focus
- Validation requirements
- Regulatory alignment

### Healthcare (NACCHO QI SAT 2.0)
**Focus Areas:**
- Patient safety culture
- Community engagement
- Service quality
- Population health outcomes

### Education (QCI Framework)
**Key Elements:**
- Student-centered quality
- Academic excellence
- Continuous improvement
- Stakeholder engagement

## Troubleshooting

### Common Issues

**Low Response Rate (<50%)**
- Check email deliverability
- Verify survey links work
- Increase communication frequency
- Consider incentives
- Engage department champions

**Suspicious Response Patterns**
- Implement attention checks
- Use time-based filtering
- Check for duplicate responses
- Validate demographic consistency

**Technical Issues**
- Browser compatibility: Chrome, Firefox, Safari, Edge
- Mobile responsiveness: iOS, Android
- Network requirements: HTTPS, no VPN blocks
- Data export: CSV, Excel, PDF formats

### Support Contacts
- **Technical Support**: support@qualitybarometer.com
- **Methodology Questions**: methodology@qualitybarometer.com
- **Training Requests**: training@qualitybarometer.com
- **Enterprise Support**: enterprise@qualitybarometer.com

### FAQ

**Q: How long does the assessment take?**
A: 10-15 minutes for standard assessment, 5 minutes for pulse surveys.

**Q: Is the survey anonymous?**
A: Yes, individual responses are anonymous. Demographic data is aggregated.

**Q: How often should we assess?**
A: Annual comprehensive assessment with quarterly pulse surveys.

**Q: Can we customize the questions?**
A: Premium and Enterprise versions support full customization.

**Q: What response rate should we target?**
A: Minimum 60%, ideal 70%+ for statistical validity.

## Next Steps

1. **Review Results**: Analyze findings with leadership team
2. **Develop Action Plan**: Prioritize improvement opportunities
3. **Assign Ownership**: Designate champions for each action
4. **Set Timeline**: 90-day improvement cycles
5. **Monitor Progress**: Monthly check-ins, quarterly assessments
6. **Celebrate Success**: Recognize improvements and share stories

## Resources

- **Video Tutorials**: [YouTube Playlist](https://youtube.com/quality-culture-tutorials)
- **Methodology Guide**: [PDF Download](docs/methodology-guide.pdf)
- **Case Studies**: [Success Stories](docs/case-studies)
- **API Documentation**: [Developer Guide](docs/api-reference)
- **Community Forum**: [Discussion Board](https://community.qualitybarometer.com)

---

For additional support, contact our team at hello@qualitybarometer.com