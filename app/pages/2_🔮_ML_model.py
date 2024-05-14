import datetime
from pathlib import Path

import streamlit as st
import pandas as pd
import shap

from plot import plot_features_and_target, st_shap
from model import get_shap_values, list_features_by_importance
from var import (
    FAVICON,
    GLOBAL_STREAMLIT_STYLE,
    DATA_PATH,
    PLT_CONFIG_NO_LOGO,
    VAR_NAMES_DICT,
    VAR_NAMES_INVERSE_DICT,
)

st.set_page_config(
    page_title="T-FORS AI @ INGV | ML model",
    page_icon=FAVICON,
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(GLOBAL_STREAMLIT_STYLE, unsafe_allow_html=True)

df_eval = pd.read_pickle(Path(DATA_PATH, "df_eval.pickle"))

st.markdown("# Model evaluation")

st.markdown("***")

start_date, end_date = (
    df_eval.loc["2022-03"].index.min(),
    df_eval.loc["2022-04-15"].index.max(),
)

st.markdown("### Features and target variable *vs* model output")

col_l, col_r = st.columns(2)

all_outputs = ["true", "pred_proba", "pred_f1_max", "pred_p_80", "pred_r_60"]
all_features = [ft_ for ft_ in list_features_by_importance() if ft_ not in all_outputs]

features = col_l.multiselect(
    label="Input features (ordered by importance)",
    options=[VAR_NAMES_DICT[ft_] for ft_ in all_features],
    default=[VAR_NAMES_DICT[ft_] for ft_ in ["hf", "iu_fix", "smr"]],
    max_selections=5,
)
features = [VAR_NAMES_INVERSE_DICT[ft_] for ft_ in features]

outputs = col_r.multiselect(
    label="Model outputs",
    options=[VAR_NAMES_DICT[op_] for op_ in all_outputs if op_ != "true"],
    default=[VAR_NAMES_DICT[op_] for op_ in ["pred_p_80", "pred_f1_max"]],
)
outputs = [VAR_NAMES_INVERSE_DICT[op_] for op_ in outputs]

plot_cols = ["true"] + outputs + features
df_plt = df_eval[plot_cols]

first_day, last_day = st.select_slider(
    "Chose the period to display",
    options=df_plt.index,
    value=[start_date, end_date],
    format_func=lambda value: str(value)[:10],
)

fig = plot_features_and_target(df=df_plt, time_period=[first_day, last_day])
st.plotly_chart(fig, use_container_width=True, config=PLT_CONFIG_NO_LOGO)

st.markdown("***")

st.markdown("### Event-level explanation (SHAP)")

feature_cols = [col_ for col_ in df_eval.columns if col_ not in all_outputs]

explainer, shap_vals = get_shap_values(X=df_eval[feature_cols])

col_l, col_r = st.columns(2)

min_date, max_date = (
    df_eval.index.min().date(),
    df_eval.index.max().date(),
)

date_shap = col_l.date_input(
    "Chose a day...",
    value=first_day.date(),
    min_value=min_date,
    max_value=max_date,
    format="YYYY/MM/DD",
)

time_shap = col_r.time_input("... and a time", datetime.time(15, 00), step=2 * 900)
row = df_eval[feature_cols].index.get_loc(f"{date_shap} {str(time_shap)[:5]}")

st_shap(
    shap.force_plot(
        explainer.expected_value,
        shap_vals[row, :],
        df_eval[feature_cols].iloc[row],
        link="logit",
        feature_names=[
            " ".join(
                [
                    col_.upper() if len(col_) < 3 else col_.capitalize()
                    for col_ in nome.split("_")
                ]
            )
            for nome in feature_cols
        ],
    ),
)
