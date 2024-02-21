import streamlit as st

from var import FAVICON, APP_VERSION, GLOBAL_STREAMLIT_STYLE

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
    "Large Scale Travelling Ionospheric Disturbances (**LSTIDs**) are a type of space weather\
    disturbance that could compromise the performance of critical space and ground infrastructure.\
    The **EU-funded** [T-FORS project](https://cordis.europa.eu/project/id/101081835) is developing models that could aid in issuing forecasts and\
    warnings for such events several hours ahead. **Machine learning** algorithms are used to\
    **forecast** the occurrence and propagation of LSTIDs."
)

st.markdown("***")

st.markdown("### What do you care about?")

col_l, col_r = st.columns(2)

col_l.page_link("pages/1_📊_Data.py", label="**Show me the data**", icon="📊")
col_r.page_link("pages/2_🔮_ML_model.py", label="**Give me predictions**", icon="🔮")
