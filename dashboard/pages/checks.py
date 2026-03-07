# dashboard/pages/checks.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import sys
sys.path.append(".")

from scripts.ingestion      import load_retail_data
from scripts.profiling      import profile_dataset
from scripts.quality_checks import run_all_checks

df      = load_retail_data()
profile = profile_dataset(df)
checks  = run_all_checks(df)

checks_df = pd.DataFrame(checks).T.reset_index(drop=True)

def checks_heatmap():
    cols   = checks_df["column"].tolist()
    rules  = checks_df["rule"].tolist()
    passed = [1 if p else 0 for p in checks_df["passed"]]
    labels = ["✅ PASS" if p else "❌ FAIL" for p in checks_df["passed"]]
    fig = go.Figure(go.Heatmap(
        z=          [passed],
        x=          [f"{c}\n{r}" for c, r in zip(cols, rules)],
        y=          ["Status"],
        colorscale= [[0,"#3d0000"],[1,"#0a3d0a"]],
        text=       [labels],
        texttemplate="%{text}",
        showscale=  False,
        zmin=0, zmax=1
    ))
    fig.update_layout(
        title="Quality Rules — PASS / FAIL Status",
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font_color="white", height=220,
        xaxis=dict(tickangle=-30)
    )
    return fig

def failed_bar():
    failed_df = checks_df[checks_df["passed"] == False].copy()
    failed_df["failed_count"] = pd.to_numeric(
        failed_df["failed_count"], errors="coerce")
    fig = go.Figure(go.Bar(
        x=failed_df["column"],
        y=failed_df["failed_count"],
        marker_color="#ef4444",
        text=failed_df["failed_count"],
        textposition="outside"
    ))
    fig.update_layout(
        title="Failed Record Count per Column",
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font_color="white", height=320
    )
    return fig

def summary_cards():
    total  = len(checks_df)
    passed = int(checks_df["passed"].sum())
    failed = total - passed
    return dbc.Row([
        dbc.Col(dbc.Alert(f"✅ Passed: {passed}", color="success",
                          style={"textAlign":"center","fontWeight":"bold"})),
        dbc.Col(dbc.Alert(f"❌ Failed: {failed}", color="danger",
                          style={"textAlign":"center","fontWeight":"bold"})),
        dbc.Col(dbc.Alert(f"📋 Total Checks: {total}", color="info",
                          style={"textAlign":"center","fontWeight":"bold"})),
    ])

def checks_table():
    t = checks_df[["column","rule","status","failed_count"]].copy()
    t.columns = ["Column","Rule","Status","Failed Records"]
    return dash_table.DataTable(
        data=t.to_dict("records"),
        columns=[{"name":c,"id":c} for c in t.columns],
        style_table={"overflowX":"auto"},
        style_header={"backgroundColor":"#1F3864","color":"white",
                       "fontWeight":"bold","textAlign":"center"},
        style_cell={"backgroundColor":"#111827","color":"white",
                    "textAlign":"center","padding":"10px",
                    "border":"1px solid #1e2d45"},
        style_data_conditional=[
            {"if":{"filter_query":'{Status} contains "FAIL"'},
             "backgroundColor":"#3d0000","color":"#ff6b6b"},
            {"if":{"filter_query":'{Status} contains "PASS"'},
             "backgroundColor":"#0a3d0a","color":"#6ee7b7"},
        ],
        sort_action="native"
    )

def layout():
    return html.Div([
        html.H4("✅ Quality Check Results",
                style={"color":"#00d4ff","marginBottom":"20px"}),
        summary_cards(),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=checks_heatmap()), md=12),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=failed_bar()), md=12),
        ], className="mb-4"),
        html.H5("📋 Detailed Checks Table",
                style={"color":"white","marginBottom":"10px"}),
        checks_table()
    ])