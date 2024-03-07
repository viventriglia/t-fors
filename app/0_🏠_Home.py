import streamlit as st

from var import (
    FAVICON,
    LOGO,
    EU_LOGO_NEG,
    APP_VERSION,
    GLOBAL_STREAMLIT_STYLE,
)

st.set_page_config(
    page_title="T-FORS AI @ INGV | Home",
    page_icon=FAVICON,
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(GLOBAL_STREAMLIT_STYLE, unsafe_allow_html=True)

st.title(f"T-FORS | Forecasting LSTIDs with AI")
st.text(f"v{APP_VERSION}")

st.markdown("***")

st.markdown(
    """
    Large Scale Travelling Ionospheric Disturbances (<b>LSTIDs</b>) are a type of space weather
    disturbance that could compromise the performance of critical space and ground infrastructure.
    The <b>EU-funded [T-FORS project](https://cordis.europa.eu/project/id/101081835)</b> is developing
    models that could aid in issuing forecasts and warnings for such events several hours ahead.
    <b>Machine learning</b> algorithms are used to <b>forecast</b> the occurrence and propagation of LSTIDs.
    """,
    unsafe_allow_html=True,
)

hide_img_fs = """
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
"""
st.markdown(hide_img_fs, unsafe_allow_html=True)

col_l, col_m_l, col_m_r, col_r = st.columns([1, 0.9, 0.9, 1])
col_m_l.image(LOGO, width=200)
col_m_r.image(EU_LOGO_NEG, width=250)

st.markdown("***")

st.markdown("### What can I find here?")

st.markdown(
    """
    The analysed data range from geomagnetic indicators to sensor data from ionosondes
    scattered across the European continent. To get an intuition of the complexity behind our task,
    it may be informative to consider a low-dimensionality representation of the dataset.
    On the first page, you can find a representation of the data according to the <i>Uniform
    Manifold Approximation and Projection</i> (<b>[UMAP](https://arxiv.org/abs/1802.03426)</b>)
    algorithm, performing non-linear dimensionality reduction.
    """,
    unsafe_allow_html=True,
)
st.page_link("pages/1_📊_Data.py", label="**Show me the data**", icon="📊")

st.markdown(
    """
    The developed model comes from an efficient, fast and scalable gradient-boosting on decision
    trees framework (<b>[CatBoost](https://catboost.ai/)</b>). Our problem can be framed as a
    <b>multivariate time-series binary classification</b>, with:
    - 40+ time series as <b>input</b>;
    - a binary classification as <b>output</b> (a LSTID event is starting or not within 3 hours).

    An <b>explanatory</b> framework (<b>[SHAP](https://shap.readthedocs.io/en/latest/)</b>) is then
    employed to test features influence on the model output from an <b>event-level</b> perspective.
    """,
    unsafe_allow_html=True,
)
st.page_link("pages/2_🔮_ML_model.py", label="**Show me the model**", icon="🔮")

with st.expander("Complete list of features"):
    st.warning(icon="🚧", body="Coming soon!")
