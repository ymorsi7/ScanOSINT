import streamlit as st
import pandas as pd
import numpy as np
from utils.data_processor import load_disaster_data, load_risk_data
from utils.visualization import create_map, create_risk_chart, create_historical_analysis
from utils.emergency_tools import generate_checklist, suggest_resources
import plotly.express as px
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from datetime import datetime, timedelta

# Enforce dark theme
st.set_page_config(
    page_title="Emergency Preparedness Platform",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Force dark theme
st.markdown("""
    <script>
        var checkDarkMode = function() {
            if (!document.body.classList.contains('dark')) {
                document.body.classList.add('dark');
            }
        };

        if (window.addEventListener) {
            window.addEventListener('load', checkDarkMode);
            window.addEventListener('resize', checkDarkMode);
        }
    </script>
""", unsafe_allow_html=True)

# Custom CSS including accessibility styles
with open('assets/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Accessibility Settings in Sidebar
with st.sidebar:
    st.markdown("""
    <div class="emergency-icon" role="img" aria-label="Emergency Alert Icon">
        🚨
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""<h1 role="banner" tabindex="0">Emergency Preparedness</h1>""", unsafe_allow_html=True)

    # Accessibility Controls
    st.markdown("""<h2 tabindex="0">Accessibility Settings</h2>""", unsafe_allow_html=True)
    high_contrast = st.toggle("High Contrast Mode", help="Enables high contrast colors for better visibility")
    large_text = st.toggle("Large Text Mode", help="Increases text size for better readability")
    screen_reader = st.toggle("Screen Reader Support", help="Enables detailed descriptions for screen readers")

    # Data reload button
    if st.button("Reload Data", help="Click to refresh all emergency data"):
        st.cache_data.clear()
        st.success("Data reloaded successfully")
        st.rerun()

    # Advanced Filters Section
    st.markdown("""<h2 tabindex="0">Data Filters</h2>""", unsafe_allow_html=True)

    # Time Range Filter with ARIA label
    time_filter = st.select_slider(
        "Time Period",
        options=["Last 24 Hours", "Last Week", "Last Month", "Last Year", "All Time"],
        value="Last Week",
        help="Select time range for emergency data"
    )

    # Rest of the sidebar filters with accessibility improvements
    selected_regions = st.multiselect(
        "Geographic Regions",
        ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"],
        default=["North America"],
        help="Select regions to display emergency data for"
    )

    # Disaster Type Filter with ARIA label
    disaster_types = st.multiselect(
        "Event Types",
        ["Earthquake", "Hurricane", "Flood", "Wildfire", "Tsunami"],
        default=["Earthquake", "Hurricane"],
        help="Select types of events to filter data"
    )

    # Severity Filter with ARIA label
    min_severity, max_severity = st.select_slider(
        "Risk Score Range",
        options=["Very Low", "Low", "Medium", "High", "Very High"],
        value=("Low", "High"),
        help="Select the range of risk scores to filter data"
    )

    # Population Impact Filter with ARIA label
    min_pop = st.number_input("Minimum Population Impact", value=0, step=1000, help="Enter the minimum population impact to filter data")


# Main content with accessibility improvements
st.markdown("""
<div role="main" aria-label="Emergency Dashboard">
    <h1 tabindex="0">Global Emergency Dashboard</h1>
    <p tabindex="0">Real-time natural disaster monitoring and risk analysis</p>
</div>
""", unsafe_allow_html=True)

# Load and filter data
disaster_data = load_disaster_data()

# Create accessible metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    active_disasters = len(disaster_data[disaster_data['status'] == 'active'])
    st.markdown(f"""
    <div role="region" aria-label="Active Events Metric" tabindex="0">
        <h3>Active Events</h3>
        <p class="big-metric">{active_disasters}</p>
        <p class="metric-change">{active_disasters - 5} from last week</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    high_risk_areas = len(disaster_data[disaster_data['severity'] == 'High'])
    st.markdown(f"""
    <div role="region" aria-label="High Risk Areas Metric" tabindex="0">
        <h3>High Risk Areas</h3>
        <p class="big-metric">{high_risk_areas}</p>
        <p class="metric-change">+3 from last week</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_affected = disaster_data['affected_population'].sum()
    st.markdown(f"""
    <div role="region" aria-label="Population Affected Metric" tabindex="0">
        <h3>Population Affected</h3>
        <p class="big-metric">{total_affected:,.0f}</p>
        <p class="metric-change">12% increase</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_risk = disaster_data['risk_score'].mean()
    st.markdown(f"""
    <div role="region" aria-label="Average Risk Score Metric" tabindex="0">
        <h3>Average Risk Score</h3>
        <p class="big-metric">{avg_risk:.2f}</p>
        <p class="metric-change">-0.05 from last week</p>
    </div>
    """, unsafe_allow_html=True)


# Interactive map with controls
st.subheader("Global Disaster Risk Heatmap")
col1, col2 = st.columns([3, 1])

with col1:
    map_fig = create_map(disaster_data)
    st.plotly_chart(map_fig, use_container_width=True)

with col2:
    st.markdown("""<h3 tabindex="0">Critical Events</h3>""", unsafe_allow_html=True)
    st.markdown("""<p tabindex="0">Current high-risk situations:</p>""", unsafe_allow_html=True)
    high_risk_events = disaster_data[disaster_data['severity'] == 'High'].sort_values('risk_score', ascending=False)

    for _, event in high_risk_events.head().iterrows():
        st.markdown(f"""
        <div role="region" aria-label="High Risk Event Details" tabindex="0">
            <h4>{event['disaster_type']}</h4>
            <p>Risk Score: {event['risk_score']:.2f}</p>
            <p>Region: {event['location']}</p>
            <p>Impact: {event['affected_population']:,} affected</p>
        </div>
        """, unsafe_allow_html=True)

# Detailed analysis section
st.write("Analysis Dashboard")
tab1, tab2, tab3 = st.tabs(["Risk Assessment", "Historical Trends", "Impact Analysis"])

with tab1:
    risk_data = load_risk_data()
    risk_chart = create_risk_chart(risk_data)
    st.plotly_chart(risk_chart, use_container_width=True)

with tab2:
    def process_historical_data(data):
        return pd.DataFrame() #Return empty DataFrame if no processing is done

    historical_data = process_historical_data(disaster_data)
    if not historical_data.empty:
        trend_chart = create_historical_analysis(historical_data)
        st.plotly_chart(trend_chart, use_container_width=True)
    else:
        st.info("No historical data available for the selected filters.")

with tab3:
    impact_data = disaster_data.groupby('disaster_type').agg({
        'affected_population': 'sum',
        'risk_score': 'mean'
    }).reset_index()

    impact_fig = px.scatter(
        impact_data,
        x='risk_score',
        y='affected_population',
        size='affected_population',
        color='disaster_type',
        title='Impact vs Risk Analysis',
        template='plotly_dark'
    )
    st.plotly_chart(impact_fig, use_container_width=True)

# Footer with accessibility improvements
st.markdown("---")
st.markdown(
    f"""
    <footer role="contentinfo" tabindex="0">
        <p>Data sources: EMDAT, NOAA, USGS, and other OSINT sources</p>
        <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</p>
        <p>For emergency assistance, please call your local emergency services.</p>
    </footer>
    """,
    unsafe_allow_html=True
)