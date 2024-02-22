from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from var import DATA_PATH, PLT_FONT_SIZE


def plot_features_and_target(
    df: pd.DataFrame, features: list = None, time_period: str = None
) -> go.Figure:
    df_plt = df.loc[f"{time_period}", ["hf", "iu_mav_3h", "smr", "true", "pred"]]

    n_cols = len(df_plt.columns)

    fig = make_subplots(
        rows=n_cols,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        subplot_titles=df_plt.columns,
    )

    for i, col in enumerate(df_plt.columns, start=1):
        fig.add_trace(
            go.Scatter(
                x=df_plt[col].index,
                y=df_plt[col].values,
                name=col,
            ),
            row=i,
            col=1,
        )

    fig.update_layout(
        template="plotly_white",
        height=800,
        width=1_000,
        autosize=False,
        title=f"Period: <b>{time_period}</b>",
    )
    return fig
