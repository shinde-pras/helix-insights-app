import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import List, Dict

# Plotly imports
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="Helix Insights - Competitive Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Helix Insights Brand
st.markdown("""
<style>
    /* Brand Colors: Deep Navy (#1a2332), Teal (#00b4d8), Sky Blue (#90e0ef) */
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #00b4d8;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0096c7;
    }
    h1 {
        color: #1a2332;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    h2, h3 {
        color: #1a2332;
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #00b4d8;
    }
    .critical-alert {
        background: #fee;
        border-left: 4px solid #dc2626;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .high-alert {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Madison Intelligence Agent - Core Logic
class MadisonIntelligenceAgent:
    
    @staticmethod
    def is_date_recent(date_string: str, days_threshold: int) -> bool:
        """Check if date is within threshold"""
        if not date_string or date_string == 'N/A':
            return False
        try:
            date = datetime.strptime(date_string, '%Y-%m-%d')
            now = datetime.now()
            diff_days = (now - date).days
            return 0 <= diff_days <= days_threshold
        except:
            return False
    
    @staticmethod
    def analyze_record(record: Dict) -> Dict:
        """Madison AI threat analysis - exact logic from n8n"""
        threat_score = 0
        threat_level = 'LOW'
        strategic_implications = []
        confidence = 0
        
        source = record.get('source', '')
        company = (record.get('company', '') or '').lower()
        device_name = (record.get('deviceName', '') or '').lower()
        trial_title = (record.get('trialTitle', '') or '').lower()
        decision_date = record.get('decisionDate') or record.get('startDate', '')
        product_code = (record.get('productCode', '') or '').lower()
        
        # Factor 1: Recent Activity
        if MadisonIntelligenceAgent.is_date_recent(decision_date, 730):
            threat_score += 35
            confidence += 25
            strategic_implications.append('Recent approval/trial within last 2 years')
        elif MadisonIntelligenceAgent.is_date_recent(decision_date, 1825):
            threat_score += 20
            confidence += 15
            strategic_implications.append('Activity within last 5 years')
        
        # Factor 2: Ophthalmology Categories
        ophthalmic_terms = [
            'contact lens', 'intraocular', 'iol', 'lens', 
            'ophthalmic', 'vision', 'eye', 'retina', 'cornea',
            'cataract', 'glaucoma', 'myopia', 'surgical',
            'vitreous', 'retinal', 'ocular', 'subretinal', 'aspirator'
        ]
        
        search_text = f"{device_name} {trial_title} {product_code}"
        if any(term in search_text for term in ophthalmic_terms):
            threat_score += 30
            confidence += 20
            strategic_implications.append('High-value ophthalmology product category')
        
        # Factor 3: Advanced/Surgical Devices
        advanced_terms = ['surgical', 'implant', 'laser', 'aspirator', 'injector', 'advanced']
        if any(term in search_text for term in advanced_terms):
            threat_score += 25
            confidence += 15
            strategic_implications.append('Advanced surgical or premium device')
        
        # Factor 4: FDA Approval
        if 'FDA' in source:
            threat_score += 20
            confidence += 15
            strategic_implications.append('FDA 510(k) clearance provides market access')
        
        # Factor 5: Clinical Trial
        if 'Clinical' in source:
            threat_score += 15
            confidence += 10
            strategic_implications.append('Active clinical development')
            
            advanced_phases = ['phase 3', 'phase iii', 'phase 2', 'phase ii']
            if any(phase in trial_title for phase in advanced_phases):
                threat_score += 30
                confidence += 20
                strategic_implications.append('Advanced clinical phase')
        
        # Factor 6: Major Competitors
        major_competitors = [
            'alcon', 'bausch', 'coopervision', 'zeiss', 'johnson',
            'novartis', 'essilor', 'hoya', 'menicon', 'paragon',
            'optical', 'vision', 'staar', 'amo'
        ]
        
        if any(comp in company for comp in major_competitors):
            threat_score += 25
            confidence += 20
            strategic_implications.append('Established ophthalmology competitor')
        
        # Determine Threat Level
        if threat_score >= 70:
            threat_level = 'CRITICAL'
            confidence = min(confidence + 25, 95)
        elif threat_score >= 50:
            threat_level = 'HIGH'
            confidence = min(confidence + 15, 90)
        elif threat_score >= 30:
            threat_level = 'MEDIUM'
            confidence = min(confidence + 10, 85)
        elif threat_score >= 10:
            threat_level = 'LOW'
            confidence = max(confidence, 70)
        else:
            confidence = 60
        
        # Generate Action Items
        action_items = MadisonIntelligenceAgent.generate_action_items(
            threat_level, company, device_name or trial_title
        )
        
        return {
            'threatScore': threat_score,
            'threatLevel': threat_level,
            'confidence': confidence,
            'strategicImplications': strategic_implications,
            'actionItems': action_items,
            'analysisTimestamp': datetime.now().isoformat(),
            'agentVersion': 'Madison_Intelligence_v1.3'
        }
    
    @staticmethod
    def generate_action_items(threat_level: str, company: str, device: str) -> List[Dict]:
        """Generate actionable recommendations"""
        actions = []
        company_name = company or 'Competitor'
        device_name = device or 'device'
        
        if threat_level == 'CRITICAL':
            actions.append({
                'priority': 'URGENT',
                'action': f"IMMEDIATE: Executive briefing on {company_name}'s {device_name}",
                'timeline': 'Within 48 hours',
                'owner': 'Executive Leadership'
            })
        
        if threat_level in ['HIGH', 'CRITICAL']:
            actions.append({
                'priority': 'HIGH',
                'action': f"Competitive deep-dive: {company_name} strategy and positioning",
                'timeline': 'Within 2 weeks',
                'owner': 'Competitive Intelligence'
            })
        
        if threat_level in ['MEDIUM', 'HIGH', 'CRITICAL']:
            actions.append({
                'priority': 'MEDIUM',
                'action': f"Monitor {company_name} market activities",
                'timeline': 'Next 90 days',
                'owner': 'Market Intelligence'
            })
        
        actions.append({
            'priority': 'LOW',
            'action': 'Include in quarterly competitive review',
            'timeline': 'Quarterly',
            'owner': 'Strategic Planning'
        })
        
        return actions

# Data Fetching Functions
def fetch_fda_data(search_term: str, days_back: int = 365) -> List[Dict]:
    """Fetch FDA 510(k) data"""
    try:
        date_from = (datetime.now() - timedelta(days=days_back)).strftime('%Y%m%d')
        date_to = datetime.now().strftime('%Y%m%d')
        
        url = "https://api.fda.gov/device/510k.json"
        params = {
            'search': f'decision_date:[{date_from}+TO+{date_to}]',
            'limit': 100
        }
        
        if search_term:
            params['search'] += f'+AND+openfda.device_name:"{search_term}"'
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for item in data.get('results', []):
                results.append({
                    'source': 'FDA 510(k)',
                    'company': item.get('applicant', 'Unknown'),
                    'deviceName': item.get('device_name', 'Unknown Device'),
                    'productCode': item.get('product_code', ''),
                    'decisionDate': item.get('decision_date', 'N/A'),
                    'status': 'Approved',
                    'regulatoryClass': item.get('device_class', 'Unknown')
                })
            
            return results
        return []
    except Exception as e:
        st.error(f"FDA API Error: {str(e)}")
        return []

def fetch_clinical_trials(search_term: str, days_back: int = 365) -> List[Dict]:
    """Fetch ClinicalTrials.gov data"""
    try:
        url = "https://clinicaltrials.gov/api/v2/studies"
        
        query = "AREA[StudyType]Interventional"
        if search_term:
            query += f" AND AREA[Condition]{search_term}"
        
        params = {
            'query.term': query,
            'filter.overallStatus': 'RECRUITING,ACTIVE_NOT_RECRUITING,COMPLETED',
            'pageSize': 100,
            'format': 'json'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for study in data.get('studies', []):
                protocol = study.get('protocolSection', {})
                identification = protocol.get('identificationModule', {})
                status_module = protocol.get('statusModule', {})
                sponsor_module = protocol.get('sponsorCollaboratorsModule', {})
                
                results.append({
                    'source': 'ClinicalTrials.gov',
                    'company': sponsor_module.get('leadSponsor', {}).get('name', 'Unknown'),
                    'trialTitle': identification.get('briefTitle', 'Unknown Trial'),
                    'nctId': identification.get('nctId', ''),
                    'status': status_module.get('overallStatus', 'Unknown'),
                    'startDate': status_module.get('startDateStruct', {}).get('date', 'N/A'),
                    'phase': protocol.get('designModule', {}).get('phases', ['Unknown'])[0] if protocol.get('designModule', {}).get('phases') else 'Unknown'
                })
            
            return results
        return []
    except Exception as e:
        st.error(f"ClinicalTrials API Error: {str(e)}")
        return []

def generate_executive_summary(analyzed_records: List[Dict]) -> Dict:
    """Generate executive summary from analyzed records"""
    threat_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    critical_threats = []
    high_threats = []
    total_confidence = 0
    
    for record in analyzed_records:
        intel = record['madisonIntelligence']
        threat_counts[intel['threatLevel']] += 1
        total_confidence += intel['confidence']
        
        if intel['threatLevel'] == 'CRITICAL':
            critical_threats.append({
                'company': record.get('company', 'Unknown'),
                'product': (record.get('deviceName') or record.get('trialTitle', 'Unknown'))[:100],
                'threatScore': intel['threatScore'],
                'confidence': intel['confidence'],
                'urgentAction': intel['actionItems'][0]['action'] if intel['actionItems'] else 'Review immediately'
            })
        elif intel['threatLevel'] == 'HIGH':
            high_threats.append({
                'company': record.get('company', 'Unknown'),
                'product': (record.get('deviceName') or record.get('trialTitle', 'Unknown'))[:100],
                'threatScore': intel['threatScore'],
                'confidence': intel['confidence']
            })
    
    critical_threats.sort(key=lambda x: x['threatScore'], reverse=True)
    high_threats.sort(key=lambda x: x['threatScore'], reverse=True)
    
    avg_confidence = round(total_confidence / len(analyzed_records)) if analyzed_records else 0
    
    return {
        'threatOverview': threat_counts,
        'averageConfidence': avg_confidence,
        'totalRecords': len(analyzed_records),
        'criticalThreats': critical_threats[:5],
        'highThreats': high_threats[:5],
        'executiveSummary': f"Helix Insights analyzed {len(analyzed_records)} competitive records from FDA device approvals and clinical trial databases. Analysis identified {threat_counts['CRITICAL']} CRITICAL threats requiring immediate executive action, {threat_counts['HIGH']} HIGH priority items for strategic competitive review, {threat_counts['MEDIUM']} MEDIUM priority items for ongoing monitoring, and {threat_counts['LOW']} LOW priority items for quarterly review. Average threat assessment confidence level: {avg_confidence}%."
    }

# Main Application
def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🧬 Helix Insights")
        st.markdown("**Competitive Intelligence Dashboard** • Powered by Madison AI Framework")
    with col2:
        st.markdown("### ")
        st.markdown("[Visit Portfolio →](https://helix-insights.vercel.app)")
    
    st.markdown("---")
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Analysis Configuration")
        
        search_term = st.text_input(
            "Search Term (Optional)",
            placeholder="e.g., ophthalmology, diabetes",
            help="Leave blank for broad scan across all categories"
        )
        
        therapeutic_area = st.selectbox(
            "Therapeutic Focus",
            ["All Categories", "Ophthalmology", "Cardiology", "Orthopedics", "Neurology", "Oncology"]
        )
        
        time_range = st.selectbox(
            "Time Range",
            ["Last 6 months", "Last 1 year", "Last 2 years"],
            index=1
        )
        
        analysis_depth = st.radio(
            "Analysis Depth",
            ["Quick Scan", "Deep Analysis"],
            help="Quick: Top 50 results | Deep: Up to 200 results"
        )
        
        st.markdown("---")
        st.markdown("### About Madison AI")
        st.info("Multi-factor threat scoring system analyzing FDA approvals, clinical trials, and competitive positioning.")
    
    # Convert selections to parameters
    days_map = {"Last 6 months": 180, "Last 1 year": 365, "Last 2 years": 730}
    days_back = days_map[time_range]
    
    # Run Analysis Button
    if st.button("🚀 Run Competitive Analysis", type="primary"):
        with st.spinner("Fetching competitive intelligence data..."):
            # Fetch data
            search_query = search_term if therapeutic_area == "All Categories" else therapeutic_area.lower()
            
            fda_data = fetch_fda_data(search_query, days_back)
            clinical_data = fetch_clinical_trials(search_query, days_back)
            
            all_records = fda_data + clinical_data
            
            if not all_records:
                st.warning("No data found for the specified criteria. Try broadening your search.")
                return
            
            st.success(f"✅ Retrieved {len(all_records)} records ({len(fda_data)} FDA + {len(clinical_data)} Clinical Trials)")
        
        with st.spinner("Running Madison AI threat analysis..."):
            # Analyze each record
            analyzed_records = []
            for record in all_records:
                intelligence = MadisonIntelligenceAgent.analyze_record(record)
                record['madisonIntelligence'] = intelligence
                analyzed_records.append(record)
            
            # Generate executive summary
            summary = generate_executive_summary(analyzed_records)
        
        st.success("✅ Analysis complete!")
        
        # Display Results
        st.markdown("---")
        st.header("📊 Executive Dashboard")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", summary['totalRecords'])
        with col2:
            st.metric("🔴 Critical", summary['threatOverview']['CRITICAL'])
        with col3:
            st.metric("🟡 High", summary['threatOverview']['HIGH'])
        with col4:
            st.metric("Avg Confidence", f"{summary['averageConfidence']}%")
        
        # Threat Distribution Chart
        st.subheader("Threat Distribution")
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure(data=[go.Pie(
                labels=['Critical', 'High', 'Medium', 'Low'],
                values=[
                    summary['threatOverview']['CRITICAL'],
                    summary['threatOverview']['HIGH'],
                    summary['threatOverview']['MEDIUM'],
                    summary['threatOverview']['LOW']
                ],
                marker=dict(colors=['#dc2626', '#f59e0b', '#fbbf24', '#10b981']),
                hole=0.4
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallback bar chart
            chart_data = pd.DataFrame({
                'Threat Level': ['Critical', 'High', 'Medium', 'Low'],
                'Count': [
                    summary['threatOverview']['CRITICAL'],
                    summary['threatOverview']['HIGH'],
                    summary['threatOverview']['MEDIUM'],
                    summary['threatOverview']['LOW']
                ]
            })
            st.bar_chart(chart_data.set_index('Threat Level'))
        
        # Executive Summary
        st.subheader("Executive Summary")
        st.info(summary['executiveSummary'])
        
        # Critical Alerts
        if summary['criticalThreats']:
            st.subheader("🚨 Critical Threats - Immediate Action Required")
            for threat in summary['criticalThreats']:
                st.markdown(f"""
                <div class="critical-alert">
                    <strong>{threat['company']}</strong><br>
                    {threat['product']}<br>
                    <small>Threat Score: {threat['threatScore']} | Confidence: {threat['confidence']}%</small><br>
                    <strong>Action:</strong> {threat['urgentAction']}
                </div>
                """, unsafe_allow_html=True)
        
        # High Priority Items
        if summary['highThreats']:
            st.subheader("⚠️ High Priority Threats")
            for threat in summary['highThreats']:
                st.markdown(f"""
                <div class="high-alert">
                    <strong>{threat['company']}</strong><br>
                    {threat['product']}<br>
                    <small>Threat Score: {threat['threatScore']} | Confidence: {threat['confidence']}%</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Detailed Records Table
        st.subheader("📋 Detailed Analysis Results")
        
        df_records = []
        for record in analyzed_records:
            intel = record['madisonIntelligence']
            df_records.append({
                'Company': record.get('company', 'Unknown'),
                'Product/Trial': (record.get('deviceName') or record.get('trialTitle', 'Unknown'))[:50],
                'Source': record.get('source', ''),
                'Threat Level': intel['threatLevel'],
                'Threat Score': intel['threatScore'],
                'Confidence': f"{intel['confidence']}%",
                'Date': record.get('decisionDate') or record.get('startDate', 'N/A')
            })
        
        df = pd.DataFrame(df_records)
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download Report
        st.subheader("📥 Export Analysis")
        
        report_json = json.dumps({
            'summary': summary,
            'detailedRecords': analyzed_records
        }, indent=2)
        
        st.download_button(
            label="Download Full Report (JSON)",
            data=report_json,
            file_name=f"helix_insights_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Information Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6b7280; padding: 2rem;'>
        <strong>Helix Insights</strong> • Transforming competitive intelligence from hours to seconds<br>
        Built with Madison AI Framework • Data sources: FDA 510(k) & ClinicalTrials.gov<br>
        <a href='https://helix-insights.vercel.app' target='_blank'>Learn More →</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()