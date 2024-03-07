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
    "<i>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    unsafe_allow_html=True,
)
st.page_link("pages/2_🔮_ML_model.py", label="**Show me the model**", icon="🔮")

with st.expander("Model features"):
    st.write("AO nun ce sta ancora niente, passa più tardi")
