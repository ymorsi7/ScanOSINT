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
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(
                title='Risk Score',
                titleside='right',
                titlefont=dict(color='#e6e6e6'),
                tickfont=dict(color='#e6e6e6')
            )
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
        colorscale='Plasma',
        showscale=False,
        hoverinfo='skip',
        opacity=0.4,
        name='Risk Heatmap'
    )

    # Add both traces to the figure
    fig.add_trace(heatmap)
    fig.add_trace(scatter)

    # Update layout
    fig.update_layout(
        mapbox=dict(
            style='mapbox://styles/mapbox/navigation-night-v1',
            center=dict(lat=20, lon=0),
            zoom=1.5
        ),
        margin={"r":0,"t":30,"l":0,"b":0},
        height=600,
        title=dict(
            text='Global Disaster Risk Heatmap',
            font=dict(color='#e6e6e6')
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(48, 51, 57, 0.8)",
            font=dict(color='#e6e6e6')
        ),
        paper_bgcolor='rgba(48, 51, 57, 0.5)',
        plot_bgcolor='rgba(48, 51, 57, 0.5)'
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
        color_discrete_map={
            'High': '#ff6b6b',
            'Medium': '#ffd43b',
            'Low': '#69db7c'
        },
        hover_data=['region'],
        title='Risk Assessment Matrix',
        template='plotly_dark'
    )

    fig.update_layout(
        height=500,
        xaxis_title="Risk Factor",
        yaxis_title="Impact Score",
        paper_bgcolor='rgba(48, 51, 57, 0.5)',
        plot_bgcolor='rgba(48, 51, 57, 0.3)'
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
            showarrow=False,
            font=dict(color='#e6e6e6')
        )
        return fig

    fig = px.area(
        data,
        x='year',
        y='impact_score',
        color='disaster_type',
        title='Historical Disaster Impact Analysis',
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.update_layout(
        height=500,
        xaxis_title="Year",
        yaxis_title="Impact Score",
        paper_bgcolor='rgba(48, 51, 57, 0.5)',
        plot_bgcolor='rgba(48, 51, 57, 0.3)'
    )

    return fig