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

# Demo Data Generator
def generate_demo_data() -> List[Dict]:
    """Generate realistic demo data for demonstration"""
    demo_fda = [
        {
            'source': 'FDA 510(k)',
            'company': 'Alcon Laboratories',
            'deviceName': 'AcrySof IQ Vivity Extended Vision Intraocular Lens',
            'productCode': 'MQW',
            'decisionDate': '2024-10-15',
            'status': 'Approved',
            'regulatoryClass': 'Class III'
        },
        {
            'source': 'FDA 510(k)',
            'company': 'Johnson & Johnson Vision Care',
            'deviceName': 'ACUVUE OASYS Contact Lens with Transitions',
            'productCode': 'MQJ',
            'decisionDate': '2024-09-22',
            'status': 'Approved',
            'regulatoryClass': 'Class II'
        },
        {
            'source': 'FDA 510(k)',
            'company': 'Bausch + Lomb',
            'deviceName': 'enVista Toric Intraocular Lens',
            'productCode': 'MOB',
            'decisionDate': '2024-08-30',
            'status': 'Approved',
            'regulatoryClass': 'Class III'
        },
        {
            'source': 'FDA 510(k)',
            'company': 'ZEISS Medical Technology',
            'deviceName': 'ARTEVO 800 Ophthalmic Surgical Microscope',
            'productCode': 'HQN',
            'decisionDate': '2024-11-05',
            'status': 'Approved',
            'regulatoryClass': 'Class II'
        },
        {
            'source': 'FDA 510(k)',
            'company': 'CooperVision Inc',
            'deviceName': 'MyDay Toric Contact Lens',
            'productCode': 'MQC',
            'decisionDate': '2024-07-18',
            'status': 'Approved',
            'regulatoryClass': 'Class II'
        }
    ]
    
    demo_trials = [
        {
            'source': 'ClinicalTrials.gov',
            'company': 'Novartis Pharmaceuticals',
            'trialTitle': 'Phase III Study of Aflibercept for Diabetic Retinopathy',
            'nctId': 'NCT05234567',
            'status': 'RECRUITING',
            'startDate': '2024-06-01',
            'phase': 'PHASE3'
        },
        {
            'source': 'ClinicalTrials.gov',
            'company': 'Alcon Research',
            'trialTitle': 'Safety and Efficacy of New Presbyopia Correcting IOL',
            'nctId': 'NCT05345678',
            'status': 'ACTIVE_NOT_RECRUITING',
            'startDate': '2024-03-15',
            'phase': 'PHASE2'
        },
        {
            'source': 'ClinicalTrials.gov',
            'company': 'Regeneron Pharmaceuticals',
            'trialTitle': 'Long-term Study of Anti-VEGF Therapy for Wet AMD',
            'nctId': 'NCT05456789',
            'status': 'RECRUITING',
            'startDate': '2024-08-20',
            'phase': 'PHASE3'
        }
    ]
    
    return demo_fda + demo_trials

# Data Fetching Functions
def fetch_fda_data(search_term: str, days_back: int = 365, api_key: str = None) -> List[Dict]:
    """Fetch FDA 510(k) data with improved error handling"""
    try:
        # Calculate dates
        date_to = datetime.now()
        date_from = date_to - timedelta(days=days_back)
        
        # Format dates as YYYYMMDD
        date_from_str = date_from.strftime('%Y%m%d')
        date_to_str = date_to.strftime('%Y%m%d')
        
        url = "https://api.fda.gov/device/510k.json"
        
        # Build search query - let requests handle the encoding
        search_query = f'decision_date:[{date_from_str} TO {date_to_str}]'
        
        params = {
            'search': search_query,
            'limit': 10
        }
        
        # Add API key if provided
        if api_key and api_key.strip():
            params['api_key'] = api_key.strip()
        
        # Make request - requests library will properly encode the URL
        response = requests.get(url, params=params, timeout=30)
        
        # Check response
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for item in data.get('results', []):
                # Format decision date properly
                decision_date = item.get('decision_date', '')
                if decision_date and len(decision_date) == 8:  # Format: YYYYMMDD
                    decision_date = f"{decision_date[:4]}-{decision_date[4:6]}-{decision_date[6:]}"
                
                results.append({
                    'source': 'FDA 510(k)',
                    'company': item.get('applicant', 'Unknown'),
                    'deviceName': item.get('device_name', 'Unknown Device'),
                    'productCode': item.get('product_code', ''),
                    'decisionDate': decision_date or 'N/A',
                    'status': 'Approved',
                    'regulatoryClass': item.get('device_class', 'Unknown')
                })
            
            return results
        elif response.status_code == 404:
            # No results found for this query
            return []
        else:
            # API error
            error_msg = f"FDA API status {response.status_code}"
            if response.status_code >= 500:
                error_msg += " (server issue - temporary)"
            st.warning(f"{error_msg}. Using clinical trials data. {'Try demo data for full functionality.' if not api_key else 'FDA servers may be experiencing issues.'}")
            return []
            
    except requests.exceptions.Timeout:
        st.warning("FDA API timeout - their servers may be slow. Continuing with clinical trials data.")
        return []
    except Exception as e:
        st.warning(f"FDA API unavailable: {str(e)}. Continuing with clinical trials data.")
        return []

def fetch_clinical_trials(search_term: str, days_back: int = 365) -> List[Dict]:
    """Fetch ClinicalTrials.gov data"""
    try:
        url = "https://clinicaltrials.gov/api/v2/studies"
        
        # Build query
        query_parts = ["AREA[StudyType]Interventional"]
        
        if search_term:
            query_parts.append(f"AREA[Condition]{search_term}")
        
        query = " AND ".join(query_parts)
        
        params = {
            'query.term': query,
            'filter.overallStatus': 'RECRUITING,ACTIVE_NOT_RECRUITING,COMPLETED',
            'pageSize': 50,
            'format': 'json'
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            for study in data.get('studies', [])[:50]:  # Limit to first 50
                protocol = study.get('protocolSection', {})
                identification = protocol.get('identificationModule', {})
                status_module = protocol.get('statusModule', {})
                sponsor_module = protocol.get('sponsorCollaboratorsModule', {})
                design_module = protocol.get('designModule', {})
                
                # Format start date
                start_date = status_module.get('startDateStruct', {}).get('date', 'N/A')
                
                # Get phase
                phases = design_module.get('phases', [])
                phase = phases[0] if phases else 'Unknown'
                
                results.append({
                    'source': 'ClinicalTrials.gov',
                    'company': sponsor_module.get('leadSponsor', {}).get('name', 'Unknown'),
                    'trialTitle': identification.get('briefTitle', 'Unknown Trial'),
                    'nctId': identification.get('nctId', ''),
                    'status': status_module.get('overallStatus', 'Unknown'),
                    'startDate': start_date,
                    'phase': phase
                })
            
            return results
        else:
            st.warning(f"ClinicalTrials API returned status {response.status_code}")
            return []
    except Exception as e:
        st.warning(f"ClinicalTrials API temporarily unavailable: {str(e)}")
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
        
        # Optional API Key for better rate limits
        with st.expander("🔑 API Configuration (Optional)", expanded=False):
            # Try to get API key from secrets first, then allow manual input
            try:
                default_api_key = st.secrets["FDA_API_KEY"] if "FDA_API_KEY" in st.secrets else ""
            except:
                default_api_key = ""
            
            fda_api_key = st.text_input(
                "FDA API Key",
                value=default_api_key,
                type="password",
                help="Get free API key at open.fda.gov to avoid rate limits (120k requests/day vs 240/day)"
            )
            if fda_api_key:
                st.success("✓ FDA API key configured")
                st.caption(f"Key loaded: {fda_api_key[:10]}...")
            else:
                st.info("💡 Add FDA API key for higher rate limits")
        
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
        
        use_demo_data = st.checkbox(
            "Use Demo Data",
            value=False,
            help="Use sample data if APIs are unavailable"
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
            
            if use_demo_data:
                # Use demo data
                all_records = generate_demo_data()
                st.success(f"✅ Loaded demo dataset: {len(all_records)} records")
            else:
                # Fetch data from APIs
                search_query = search_term if therapeutic_area == "All Categories" else therapeutic_area.lower()
                
                fda_data = fetch_fda_data(search_query, days_back, fda_api_key if fda_api_key else None)
                clinical_data = fetch_clinical_trials(search_query, days_back)
                
                all_records = fda_data + clinical_data
                
                if not all_records:
                    st.warning("⚠️ No data found. APIs may be temporarily unavailable. Try enabling 'Use Demo Data' to see the system in action.")
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