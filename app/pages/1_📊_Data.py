from pathlib import Path

import streamlit as st
import numpy as np
import pandas as pd

from model import evaluate_umap
from plot import plot_umap
from var import FAVICON, DATA_PATH, GLOBAL_STREAMLIT_STYLE, PLT_CONFIG

st.set_page_config(
    page_title="T-FORS AI @ INGV | Data",
    page_icon=FAVICON,
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(GLOBAL_STREAMLIT_STYLE, unsafe_allow_html=True)

st.markdown("# Data wrangling")

st.markdown("***")

st.markdown("### Dimensionality reduction with UMAP")

all_features = [
    "iu_mav_6h",
    "hf",
    "solar_zenith_angle",
    "hp_30",
    "smr",
    "true",
]

df_eval = pd.read_pickle(Path(DATA_PATH, "df_eval.pickle"))[all_features].fillna(0)

col_l, col_m, col_r = st.columns([1, 0.3, 0.8], gap="large")

features = col_l.multiselect(
    label="Choose the input features",
    options=[ft_ for ft_ in all_features if ft_ != "true"],
    default=[ft_ for ft_ in all_features if ft_ not in ["true", "smr", "hp_30"]],
)

X = df_eval[features]
y = df_eval["true"]

n_comps = col_m.radio(
    label="Choose the dimensions", options=[2, 3], index=0, horizontal=True
)

n_neighbors = col_r.select_slider(
    label="Choose the size of neighborhoods",
    options=np.linspace(15, X.shape[0] // 10, num=5, dtype=int),
)

with st.expander("Help, how do I choose those parameters?"):
    st.markdown(
        """
- <i><b>Input features</b></i> are the features on which UMAP is fit; the list includes only the
most important features for the CatBoost model (<i>ML model</i> page). In general, more features
lead to a considerable increase in training time.
- <i><b>Dimensions</b></i> controls the dimensionality of the reduced space we embed
the data into.
- <i><b>Size of neighborhoods</b></i> determines how UMAP balances local versus global
structure in the data; it does so by constraining the size of the local neighborhood UMAP
looks at when attempting to learn the manifold structure of the data. Thus, lower values will
force UMAP to concentrate on the local structure (potentially to the detriment of the big
picture), while larger values will push it to look at larger neighborhoods of each point,
losing fine-detail structure for the sake of getting the broader picture of the data.
""",
        unsafe_allow_html=True,
    )

umap_projections = evaluate_umap(X=X, n_comps=n_comps, n_neighbors=n_neighbors)

fig = plot_umap(umap_projections=umap_projections, y=y.values, n_comps=n_comps)

st.plotly_chart(fig, use_container_width=True, config=PLT_CONFIG)
