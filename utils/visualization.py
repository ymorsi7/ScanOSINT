import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_map(data):
    """Creates interactive map visualization of disasters"""
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add scatter plot for individual events
    scatter = go.Scattermapbox(
        lat=data['latitude'],
        lon=data['longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=data['risk_score'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Risk Score')
        ),
        text=data.apply(
            lambda x: f"Type: {x['disaster_type']}<br>"
                     f"Severity: {x['severity']}<br>"
                     f"Status: {x['status']}<br>"
                     f"Affected: {x['affected_population']:,}<br>"
                     f"Risk Score: {x['risk_score']:.2f}",
            axis=1
        ),
        hoverinfo='text',
        name='Events'
    )

    # Add heatmap layer
    heatmap = go.Densitymapbox(
        lat=data['latitude'],
        lon=data['longitude'],
        z=data['risk_score'],
        radius=30,
        colorscale='Viridis',
        showscale=False,
        hoverinfo='skip',
        opacity=0.6,
        name='Risk Heatmap'
    )

    # Add both traces to the figure
    fig.add_trace(heatmap)
    fig.add_trace(scatter)

    # Update layout
    fig.update_layout(
        mapbox=dict(
            style='carto-darkmatter',
            center=dict(lat=20, lon=0),
            zoom=1.5
        ),
        margin={"r":0,"t":30,"l":0,"b":0},
        height=600,
        title='Global Disaster Risk Heatmap',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.1)"
        )
    )

    return fig

def create_risk_chart(data):
    """Creates risk assessment visualization"""
    fig = px.scatter(
        data,
        x='factor',
        y='impact_score',
        size='impact_score',
        color='severity',
        hover_data=['region'],
        title='Risk Assessment Matrix',
        template='plotly_dark'
    )

    fig.update_layout(
        height=500,
        xaxis_title="Risk Factor",
        yaxis_title="Impact Score",
    )

    return fig

def create_historical_analysis(data):
    """Creates historical analysis visualization"""
    if data.empty:
        # Return an empty figure with a message
        fig = go.Figure()
        fig.add_annotation(
            text="No historical data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig

    fig = px.area(
        data,
        x='year',
        y='impact_score',
        color='disaster_type',
        title='Historical Disaster Impact Analysis',
        template='plotly_dark'
    )

    fig.update_layout(
        height=500,
        xaxis_title="Year",
        yaxis_title="Impact Score",
    )

    return fig