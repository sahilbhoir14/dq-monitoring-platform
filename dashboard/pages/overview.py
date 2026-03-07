# dashboard/pages/overview.py
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import sys
sys.path.append(".")

from scripts.ingestion      import load_retail_data
from scripts.profiling      import profile_dataset
from scripts.quality_checks import run_all_checks
from scripts.scoring        import calculate_dq_score

# ── Load data once ───────────────────────────────────────
df      = load_retail_data()
profile = profile_dataset(df)
checks  = run_all_checks(df)
scores  = calculate_dq_score(df, profile, checks)

# ── KPI Card ─────────────────────────────────────────────
def kpi_card(title, value, color, icon):
    return dbc.Card([
        dbc.CardBody([
            html.Div(icon, style={"fontSize":"28px"}),
            html.H6(title,
                    style={"color":"#adb5bd","marginTop":"8px","fontSize":"12px",
                           "letterSpacing":"1px","textTransform":"uppercase"}),
            html.H2(str(value),
                    style={"color": color, "fontWeight":"bold","margin":"4px 0"})
        ])
    ], style={"backgroundColor":"#111827","border":f"1px solid {color}",
              "borderRadius":"8px","textAlign":"center"})

# ── Gauge Chart ───────────────────────────────────────────
def dq_gauge(score):
    fig = go.Figure(go.Indicator(
        mode  = "gauge+number+delta",
        value = score,
        delta = {"reference": 80},
        title = {"text": "Overall DQ Score", "font": {"color":"white"}},
        number= {"suffix": "%", "font": {"color":"white","size":40}},
        gauge = {
            "axis" : {"range": [0, 100], "tickcolor":"white"},
            "bar"  : {"color": "#00d4ff"},
            "steps": [
                {"range": [0,  50], "color": "#1a0a0a"},
                {"range": [50, 75], "color": "#1a1200"},
                {"range": [75,100], "color": "#0a1a0a"},
            ],
            "threshold": {
                "line" : {"color": "#f59e0b", "width": 4},
                "thickness": 0.75,
                "value": 80
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="#111827",
        font_color="white",
        height=280,
        margin=dict(t=40, b=20, l=30, r=30)
    )
    return fig

# ── Dimension Bar Chart ───────────────────────────────────
def dimension_bar(scores):
    dims = ["Completeness","Validity","Uniqueness","Consistency"]
    vals = [scores["completeness"], scores["validity"],
            scores["uniqueness"],   scores["consistency"]]
    colors = ["#10b981" if v >= 75 else "#f59e0b" if v >= 60
              else "#ef4444" for v in vals]

    fig = go.Figure(go.Bar(
        x=dims, y=vals,
        marker_color=colors,
        text=[f"{v}%" for v in vals],
        textposition="outside"
    ))
    fig.update_layout(
        title="DQ Score by Dimension",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        yaxis=dict(range=[0,110]),
        height=300,
        margin=dict(t=50, b=20)
    )
    return fig

# ── Pre-calculate values ──────────────────────────────────
passed  = sum(1 for r in checks.values() if r["passed"])
failed  = len(checks) - passed
nulls   = sum(v["null_count"] for v in profile.values())

# ── Page Layout ───────────────────────────────────────────
def layout():
    return html.Div([

        # KPI Row
        dbc.Row([
            dbc.Col(kpi_card("Overall DQ Score", f"{scores['overall_score']}%",
                             "#00d4ff", "🎯"), md=3),
            dbc.Col(kpi_card("Total Rows",        f"{len(df):,}",
                             "#10b981", "📋"), md=3),
            dbc.Col(kpi_card("Checks Passed",     f"{passed}/{len(checks)}",
                             "#10b981", "✅"), md=3),
            dbc.Col(kpi_card("Total Null Cells",  f"{nulls:,}",
                             "#ef4444", "⚠️"), md=3),
        ], className="mb-4"),

        # Charts Row
        dbc.Row([
            dbc.Col(dcc.Graph(figure=dq_gauge(scores["overall_score"])), md=5),
            dbc.Col(dcc.Graph(figure=dimension_bar(scores)),              md=7),
        ], className="mb-4"),

        # Grade Banner
        dbc.Alert(
            f"📊 Dataset Grade: {scores['grade']}  |  "
            f"Run: {scores['run_datetime']}",
            color="info",
            style={"textAlign":"center","fontWeight":"bold","letterSpacing":"1px"}
        )
    ])