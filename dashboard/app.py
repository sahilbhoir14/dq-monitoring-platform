# dashboard/app.py — FINAL VERSION
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import sys
sys.path.append(".")

from dashboard.pages import overview, profiling, checks, trends

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "DQ Monitoring Platform"

navbar = dbc.NavbarSimple(
    brand="🔍 Data Quality Monitoring Platform — Retail Products",
    brand_style={"fontSize":"18px","fontWeight":"bold","color":"#00d4ff"},
    color="dark", dark=True,
    style={"borderBottom":"2px solid #00d4ff"}
)

tabs = dbc.Tabs([
    dbc.Tab(label="📊 Executive Overview", tab_id="tab-overview"),
    dbc.Tab(label="🔬 Data Profiling",     tab_id="tab-profiling"),
    dbc.Tab(label="✅ Quality Checks",     tab_id="tab-checks"),
    dbc.Tab(label="📈 Trend Analysis",     tab_id="tab-trends"),
], id="tabs", active_tab="tab-overview", style={"marginTop":"20px"})

app.layout = dbc.Container([
    navbar, tabs,
    html.Div(id="tab-content", style={"padding":"20px 0"})
], fluid=True, style={"backgroundColor":"#0a0e1a","minHeight":"100vh"})

@app.callback(
    Output("tab-content","children"),
    Input("tabs","active_tab")
)
def render_tab(tab):
    if tab == "tab-overview":  return overview.layout()
    if tab == "tab-profiling": return profiling.layout()
    if tab == "tab-checks":    return checks.layout()
    if tab == "tab-trends":    return trends.layout()

if __name__ == "__main__":
    app.run(debug=True)