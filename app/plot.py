import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import shap
import streamlit.components.v1 as components

from var import PLT_FONT_SIZE


def plot_features_and_target(
    df: pd.DataFrame,
    time_period: list,
) -> go.Figure:
    features_dict = {
        "hf": "HF-EU index",
        "iu_mav_3h": "Auroral electrojet (IU index, 3h moving average)",
        "smr": "SMR (ring current)",
        "true": "Target",
        "pred": "Model prediction",
    }

    df_plt = df.loc[f"{time_period[0]}":f"{time_period[-1]}", features_dict.keys()]

    n_cols = len(features_dict.keys())

    fig = make_subplots(
        rows=n_cols,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.07,
        subplot_titles=[*features_dict.values()],
    )

    for i, col in enumerate(df_plt.columns, start=1):
        fig.add_trace(
            go.Scatter(
                x=df_plt[col].index,
                y=df_plt[col].values,
                name=features_dict[col],
                showlegend=False,
            ),
            row=i,
            col=1,
        )
        fig.update_traces(hovertemplate="<b>%{y:,.1f}</b> <extra>%{x}</extra>")

    fig.update_layout(
        margin=dict(b=0),
        template="simple_white",
        height=900,
        hoverlabel_font_size=PLT_FONT_SIZE,
        title=dict(
            text=f"Features and target <i>vs</i> model prediction, from {time_period[0].date()} to {time_period[-1].date()}",
            font_size=PLT_FONT_SIZE + 4,
        ),
    )
    return fig


def plot_umap(
    umap_projections: np.ndarray,
    y: np.ndarray,
    n_comps: int,
) -> go.Figure:
    if n_comps == 3:
        fig = px.scatter_3d(
            x=umap_projections[:, 0],
            y=umap_projections[:, 1],
            z=umap_projections[:, 2],
            color=y,
            hover_name=y,
        )
        fig.update_traces(hovertemplate="Class <b>%{hovertext}</b><br>")
        fig.update_layout(
            margin=dict(t=0, b=0),
            height=950,
            template="plotly_dark",
            coloraxis=dict(colorbar=dict(title="Class", dtick=1)),
        )

    elif n_comps == 2:
        fig = px.scatter(
            x=umap_projections[:, 0],
            y=umap_projections[:, 1],
            color=y,
            hover_name=y,
        )
        fig.update_traces(hovertemplate="Class <b>%{hovertext}</b><br>")
        fig.update_layout(
            margin=dict(t=50, b=0),
            height=950,
            template="simple_white",
            coloraxis=dict(colorbar=dict(title="Class", dtick=1)),
        )
    return fig


def st_shap(plot, height: int = None) -> None:
    shap_html = f"""
    <head>
        {shap.getjs()}
        <style>
            body {{
                color: white !important;
            }}
        </style>
    </head>
    <body>{plot.html()}</body>
    """
    components.html(shap_html, height=height)
