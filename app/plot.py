from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from var import PLT_FONT_SIZE


def plot_features_and_target(
    df: pd.DataFrame,
    time_period: list,
) -> go.Figure:
    features_dict = {
        "hf": "HF-EU index",
        "iu_mav_3h": "Auroral electrojet (IU index, 3h moving average)",
        "smr": "SMR (ring current)",
        "true": "Ground truth (from catalogue)",
        "pred": "Model prediction",
    }

    df_plt = df.loc[f"{time_period[0]}":f"{time_period[-1]}", features_dict.keys()]

    n_cols = len(features_dict.keys())

    fig = make_subplots(
        rows=n_cols,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
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
        template="plotly_white",
        height=800,
        width=1_000,
        # hoverlabel_font_size=PLT_FONT_SIZE,
        title=dict(
            text=f"<b>Features, target and model prediction, from {time_period[0].date()} to {time_period[-1].date()}</b>",
            font_size=PLT_FONT_SIZE + 4,
        ),
    )
    return fig
