from pathlib import Path

import streamlit as st
import pandas as pd

from plot import plot_features_and_target
from var import FAVICON, GLOBAL_STREAMLIT_STYLE, DATA_PATH, PLT_CONFIG_NO_LOGO

st.set_page_config(
    page_title="T-FORS AI @ INGV | ML model",
    page_icon=FAVICON,
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(GLOBAL_STREAMLIT_STYLE, unsafe_allow_html=True)

df_eval = pd.read_pickle(Path(DATA_PATH, "df_eval.pickle"))

st.markdown("## ML model evaluation")

start_date, end_date = (
    df_eval.loc["2022-03"].index.min(),
    df_eval.loc["2022-04-15"].index.max(),
)

first_day, last_day = st.select_slider(
    "Chose the period to display",
    options=df_eval.index,
    value=[start_date, end_date],
    format_func=lambda value: str(value)[:10],
)

fig = plot_features_and_target(df=df_eval, time_period=[first_day, last_day])
st.plotly_chart(fig, use_container_width=True, config=PLT_CONFIG_NO_LOGO)
