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
time_period = "2022-02"

fig = plot_features_and_target(df=df_eval, time_period=time_period)
st.plotly_chart(fig, use_container_width=True, config=PLT_CONFIG_NO_LOGO)
