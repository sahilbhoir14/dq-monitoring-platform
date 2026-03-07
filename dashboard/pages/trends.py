# dashboard/pages/trends.py
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def load_history():
    try:
        df = pd.read_csv("data/logs/dq_score_history.csv")
        df["run_datetime"] = pd.to_datetime(df["run_datetime"])
        return df
    except FileNotFoundError:
        # Return dummy data if not enough runs yet
        return pd.DataFrame({
            "run_datetime":  pd.date_range("2025-01-01", periods=7, freq="D"),
            "overall_score": [62, 65, 70, 68, 74, 78, 82],
            "completeness":  [70, 72, 75, 74, 78, 82, 85],
            "validity":      [55, 58, 65, 62, 70, 74, 79],
            "uniqueness":    [90, 90, 91, 92, 92, 93, 94],
            "consistency":   [80, 81, 82, 80, 83, 85, 86],
        })

# ── Overall Score Line Chart ──────────────────────────────
def score_line(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["run_datetime"], y=df["overall_score"],
        mode="lines+markers",
        name="Overall Score",
        line=dict(color="#00d4ff", width=3),
        marker=dict(size=8)
    ))
    fig.add_hline(
        y=80, line_dash="dash",
        line_color="#f59e0b",
        annotation_text="Target: 80%",
        annotation_font_color="#f59e0b"
    )
    fig.update_layout(
        title="Overall DQ Score Over Time",
        xaxis_title="Run Date",
        yaxis_title="DQ Score (%)",
        yaxis=dict(range=[0,105]),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=340
    )
    return fig

# ── All Dimensions Line Chart ──────────────────────────────
def dimensions_line(df):
    fig = go.Figure()
    dim_colors = {
        "completeness": "#10b981",
        "validity":     "#3b82f6",
        "uniqueness":   "#f59e0b",
        "consistency":  "#a78bfa"
    }
    for dim, color in dim_colors.items():
        if dim in df.columns:
            fig.add_trace(go.Scatter(
                x=df["run_datetime"], y=df[dim],
                mode="lines+markers",
                name=dim.title(),
                line=dict(color=color, width=2),
                marker=dict(size=6)
            ))
    fig.update_layout(
        title="DQ Dimensions Over Time",
        xaxis_title="Run Date",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0,105]),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=340,
        legend=dict(bgcolor="#111827")
    )
    return fig

# ── Score Summary Cards ────────────────────────────────────
def trend_cards(df):
    latest  = df["overall_score"].iloc[-1]
    highest = df["overall_score"].max()
    lowest  = df["overall_score"].min()
    avg     = round(df["overall_score"].mean(), 1)

    return dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Latest Score", style={"color":"#adb5bd"}),
            html.H3(f"{latest}%",   style={"color":"#00d4ff"})
        ]), style={"backgroundColor":"#111827","border":"1px solid #00d4ff"})),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Highest Score", style={"color":"#adb5bd"}),
            html.H3(f"{highest}%",   style={"color":"#10b981"})
        ]), style={"backgroundColor":"#111827","border":"1px solid #10b981"})),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Lowest Score", style={"color":"#adb5bd"}),
            html.H3(f"{lowest}%",   style={"color":"#ef4444"})
        ]), style={"backgroundColor":"#111827","border":"1px solid #ef4444"})),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Average Score", style={"color":"#adb5bd"}),
            html.H3(f"{avg}%",       style={"color":"#f59e0b"})
        ]), style={"backgroundColor":"#111827","border":"1px solid #f59e0b"})),
    ], className="mb-4")

# ── Page Layout ───────────────────────────────────────────
def layout():
    df = load_history()
    return html.Div([
        html.H4("📈 Trend Analysis",
                style={"color":"#00d4ff","marginBottom":"20px"}),
        trend_cards(df),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=score_line(df)),      md=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=dimensions_line(df)), md=12),
        ]),
    ])