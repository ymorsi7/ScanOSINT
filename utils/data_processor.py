import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import streamlit as st

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_usgs_data():
    """
    Fetch real-time earthquake data from USGS
    """
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"
    try:
        response = requests.get(url)
        data = response.json()
        earthquakes = []
        for feature in data['features']:
            lat = feature['geometry']['coordinates'][1]
            lon = feature['geometry']['coordinates'][0]
            location = get_region_from_coordinates(lat, lon)
            earthquakes.append({
                'event_id': feature['id'],
                'disaster_type': 'Earthquake',
                'latitude': lat,
                'longitude': lon,
                'location': location,
                'magnitude': feature['properties']['mag'],
                'severity': 'High' if feature['properties']['mag'] >= 6 else 'Medium' if feature['properties']['mag'] >= 4 else 'Low',
                'status': 'active' if (datetime.now() - datetime.fromtimestamp(feature['properties']['time']/1000)).days < 1 else 'resolved',
                'affected_population': int(feature['properties']['felt']) if feature['properties']['felt'] else 0,
                'timestamp': datetime.fromtimestamp(feature['properties']['time']/1000)
            })
        return pd.DataFrame(earthquakes)
    except:
        return pd.DataFrame()

def get_region_from_coordinates(lat, lon):
    """
    Determine region based on coordinates
    """
    if lat > 15:
        if lon < -30:
            return "North America"
        elif lon < 60:
            return "Europe"
        else:
            return "Asia"
    else:
        if lon < -30:
            return "South America"
        elif lon < 60:
            return "Africa"
        else:
            return "Oceania"

@st.cache_data(ttl=300)
def fetch_gdacs_data():
    """
    Fetch disaster alerts from GDACS
    """
    url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/EVENTS.geojson"
    try:
        response = requests.get(url)
        data = response.json()
        disasters = []
        for feature in data['features']:
            props = feature['properties']
            disasters.append({
                'event_id': props['eventid'],
                'disaster_type': props['eventtype'],
                'latitude': feature['geometry']['coordinates'][1],
                'longitude': feature['geometry']['coordinates'][0],
                'severity': props['alertlevel'].capitalize(),
                'status': 'active' if props['alertscore'] > 0 else 'resolved',
                'affected_population': int(props['population']) if 'population' in props else 0,
                'timestamp': datetime.strptime(props['fromdate'], '%Y-%m-%d %H:%M:%S')
            })
        return pd.DataFrame(disasters)
    except:
        return pd.DataFrame()

def calculate_risk_score(row):
    """
    Calculate risk score based on multiple factors
    """
    severity_scores = {'High': 1.0, 'Medium': 0.6, 'Low': 0.3}
    time_factor = 1.0 if row['status'] == 'active' else 0.5
    population_factor = min(1.0, np.log10(row['affected_population'] + 1) / 6)

    return severity_scores[row['severity']] * time_factor * (1 + population_factor)

def load_disaster_data():
    """
    Load and process disaster data from various OSINT sources
    Returns processed DataFrame with disaster information
    """
    # Fetch data from multiple sources
    usgs_data = fetch_usgs_data()
    gdacs_data = fetch_gdacs_data()

    # Combine data sources
    combined_data = pd.concat([usgs_data, gdacs_data], ignore_index=True)

    if combined_data.empty:
        # Fallback to simulated data if API calls fail
        data = {
            'event_id': range(1, 101),
            'disaster_type': np.random.choice(
                ['Earthquake', 'Hurricane', 'Flood', 'Wildfire', 'Tsunami'],
                100
            ),
            'location': np.random.choice(
                ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania'],
                100
            ),
            'latitude': np.random.uniform(-90, 90, 100),
            'longitude': np.random.uniform(-180, 180, 100),
            'severity': np.random.choice(['High', 'Medium', 'Low'], 100),
            'status': np.random.choice(['active', 'resolved'], 100),
            'affected_population': np.random.randint(1000, 1000000, 100),
            'timestamp': [
                datetime.now() - timedelta(days=x) for x in range(100)
            ]
        }
        combined_data = pd.DataFrame(data)

    # Calculate risk scores
    combined_data['risk_score'] = combined_data.apply(calculate_risk_score, axis=1)

    return combined_data

def load_risk_data():
    """
    Load and process risk assessment data
    Returns processed DataFrame with risk information
    """
    disaster_data = load_disaster_data()

    # Aggregate risk data by region and disaster type
    risk_factors = []
    for region in ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania']:
        region_data = disaster_data[disaster_data['location'] == region]
        for disaster_type in ['Earthquake', 'Hurricane', 'Flood', 'Wildfire', 'Tsunami']:
            type_data = region_data[region_data['disaster_type'] == disaster_type]
            if not type_data.empty:
                avg_risk = type_data['risk_score'].mean()
                severity = 'High' if avg_risk > 0.7 else 'Medium' if avg_risk > 0.4 else 'Low'
                risk_factors.append({
                    'factor': f"{disaster_type} Risk",
                    'impact_score': avg_risk * 100,
                    'severity': severity,
                    'region': region
                })

    return pd.DataFrame(risk_factors)

def process_historical_data(df):
    """
    Process historical disaster data
    Returns a DataFrame with historical trends
    """
    disaster_data = load_disaster_data()

    # Group data by year and disaster type
    historical = disaster_data.copy()
    historical['year'] = historical['timestamp'].dt.year

    historical_trends = historical.groupby(['year', 'disaster_type']).agg({
        'affected_population': 'sum',
        'risk_score': 'mean'
    }).reset_index()

    # If no data, return empty DataFrame with correct columns
    if historical_trends.empty:
        return pd.DataFrame(columns=['year', 'disaster_type', 'impact_score'])

    # Calculate impact score
    historical_trends['impact_score'] = (
        historical_trends['risk_score'] * 
        np.log10(historical_trends['affected_population'] + 1)
    )

    return historical_trends