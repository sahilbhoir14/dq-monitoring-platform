# dashboard/pages/profiling.py
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
sys.path.append(".")

from scripts.ingestion import load_retail_data
from scripts.profiling import profile_dataset

df      = load_retail_data()
profile = profile_dataset(df)

profile_df = pd.DataFrame(profile).T.reset_index()
profile_df.columns = ["column"] + list(profile_df.columns[1:])
profile_df["null_pct"]      = pd.to_numeric(profile_df["null_pct"],      errors="coerce")
profile_df["unique_values"] = pd.to_numeric(profile_df["unique_values"], errors="coerce")

def null_bar():
    colors = ["#ef4444" if v > 10 else "#f59e0b" if v > 0
              else "#10b981" for v in profile_df["null_pct"]]
    fig = go.Figure(go.Bar(
        x=profile_df["column"],
        y=profile_df["null_pct"],
        marker_color=colors,
        text=[f"{v}%" for v in profile_df["null_pct"]],
        textposition="outside"
    ))
    fig.update_layout(
        title="Null % Per Column",
        xaxis_title="Column", yaxis_title="Null %",
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font_color="white", height=320,
        yaxis=dict(range=[0, profile_df["null_pct"].max() + 15])
    )
    return fig

def dtype_pie():
    dtype_counts = profile_df["data_type"].value_counts().reset_index()
    dtype_counts.columns = ["data_type","count"]
    fig = px.pie(
        dtype_counts,
        names="data_type",
        values="count",
        title="Column Data Types",
        color_discrete_sequence=["#00d4ff","#10b981","#f59e0b","#ef4444"]
    )
    fig.update_layout(
        paper_bgcolor="#111827",
        font_color="white",
        height=320
    )
    return fig

def unique_bar():
    fig = px.bar(
        profile_df,
        x="column", y="unique_values",
        title="Unique Values Per Column",
        color="unique_values",
        color_continuous_scale=["#1e3a5f","#00d4ff"]
    )
    fig.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font_color="white", height=300
    )
    return fig

def profile_table():
    table_df = profile_df[["column","data_type","null_count",
                            "null_pct","unique_values"]].copy()
    table_df.columns = ["Column","Type","Null Count","Null %","Unique Values"]
    return dash_table.DataTable(
        data=table_df.to_dict("records"),
        columns=[{"name":c,"id":c} for c in table_df.columns],
        style_table={"overflowX":"auto"},
        style_header={"backgroundColor":"#1F3864","color":"white",
                       "fontWeight":"bold","textAlign":"center"},
        style_cell={"backgroundColor":"#111827","color":"white",
                    "textAlign":"center","padding":"10px",
                    "border":"1px solid #1e2d45"},
        style_data_conditional=[
            {"if":{"filter_query":"{Null %} > 10","column_id":"Null %"},
             "backgroundColor":"#3d0000","color":"#ff6b6b"},
            {"if":{"filter_query":"{Null %} > 0 && {Null %} <= 10",
                   "column_id":"Null %"},
             "backgroundColor":"#3d2e00","color":"#ffd166"},
        ],
        page_size=15,
        sort_action="native",
        filter_action="native"
    )

def layout():
    return html.Div([
        html.H4("🔬 Data Profiling Report",
                style={"color":"#00d4ff","marginBottom":"20px"}),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=null_bar()),  md=8),
            dbc.Col(dcc.Graph(figure=dtype_pie()), md=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=unique_bar()), md=12),
        ], className="mb-4"),
        html.H5("📋 Full Column Profile Table",
                style={"color":"white","marginBottom":"10px"}),
        profile_table()
    ])