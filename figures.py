# figures.py
import plotly.graph_objects as go

def make_timeseries_panel(df, title):
    fig = go.Figure()

    for col in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col], mode="lines", name=col
        ))

    fig.update_layout(
        title=title,
        template="plotly_dark",
        height=480,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", y=-0.3)
    )
    return fig

def make_stress_gauge(current, mean):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current,
        delta={"reference": mean},
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 40], "color": "#2ca02c"},
                {"range": [40, 55], "color": "#1f77b4"},
                {"range": [55, 70], "color": "#ff7f0e"},
                {"range": [70, 100], "color": "#d62728"},
            ],
            "bar": {"color": "white"}
        },
        title={"text": "Composite Market Stress Score"}
    ))
    fig.update_layout(template="plotly_dark", height=450)
    return fig
