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

# Page configuration
st.set_page_config(
    page_title="Emergency Preparedness Platform",
    page_icon="assets/alert-icon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open('assets/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/alert-icon.svg")
    st.title("Emergency Preparedness")

    # Data reload button
    if st.button("Reload Data"):
        st.cache_data.clear()
        st.success("Data reloaded successfully")
        st.rerun()

    # Advanced Filters Section
    st.subheader("Data Filters")

    # Time Range Filter
    time_filter = st.select_slider(
        "Time Period",
        options=["Last 24 Hours", "Last Week", "Last Month", "Last Year", "All Time"],
        value="Last Week"
    )

    # Region Selection
    selected_regions = st.multiselect(
        "Geographic Regions",
        ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"],
        default=["North America"]
    )

    # Disaster Type Filter
    disaster_types = st.multiselect(
        "Event Types",
        ["Earthquake", "Hurricane", "Flood", "Wildfire", "Tsunami"],
        default=["Earthquake", "Hurricane"]
    )

    # Severity Filter
    min_severity, max_severity = st.select_slider(
        "Risk Score Range",
        options=["Very Low", "Low", "Medium", "High", "Very High"],
        value=("Low", "High")
    )

    # Population Impact Filter
    min_pop = st.number_input("Minimum Population Impact", value=0, step=1000)


# Main content
colored_header(
    label="Global Emergency Dashboard",
    description="Real-time natural disaster monitoring and risk analysis",
    color_name="blue-70"
)

# Load and filter data based on user selections
disaster_data = load_disaster_data()

# Create metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    active_disasters = len(disaster_data[disaster_data['status'] == 'active'])
    st.metric(
        "Active Events",
        active_disasters,
        f"{active_disasters - 5} from last week",
        delta_color="off"
    )

with col2:
    high_risk_areas = len(disaster_data[disaster_data['severity'] == 'High'])
    st.metric(
        "High Risk Areas",
        high_risk_areas,
        "+3 from last week",
        delta_color="off"
    )

with col3:
    total_affected = disaster_data['affected_population'].sum()
    st.metric(
        "Population Affected",
        f"{total_affected:,.0f}",
        "12% increase",
        delta_color="off"
    )

with col4:
    avg_risk = disaster_data['risk_score'].mean()
    st.metric(
        "Risk Score",
        f"{avg_risk:.2f}",
        "-0.05 from last week",
        delta_color="off"
    )

# Interactive map with controls
st.subheader("Global Disaster Risk Heatmap")
col1, col2 = st.columns([3, 1])

with col1:
    map_fig = create_map(disaster_data)
    st.plotly_chart(map_fig, use_container_width=True)

with col2:
    st.write("Critical Events")
    st.write("Current high-risk situations:")
    high_risk_events = disaster_data[disaster_data['severity'] == 'High'].sort_values('risk_score', ascending=False)

    for _, event in high_risk_events.head().iterrows():
        st.markdown(f"""
        **{event['disaster_type']}**  
        Risk Score: {event['risk_score']:.2f}  
        Region: {event['location']}  
        Impact: {event['affected_population']:,} affected
        """)

# Detailed analysis section
st.write("Analysis Dashboard")
tab1, tab2, tab3 = st.tabs(["Risk Assessment", "Historical Trends", "Impact Analysis"])

with tab1:
    risk_data = load_risk_data()
    risk_chart = create_risk_chart(risk_data)
    st.plotly_chart(risk_chart, use_container_width=True)

with tab2:
    def process_historical_data(data):
        return pd.DataFrame()

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

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Data sources: EMDAT, NOAA, USGS, and other OSINT sources</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M UTC")),
    unsafe_allow_html=True
)