import streamlit as st

from var import FAVICON, GLOBAL_STREAMLIT_STYLE

st.set_page_config(
    page_title="T-FORS AI @ INGV | Data",
    page_icon=FAVICON,
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(GLOBAL_STREAMLIT_STYLE, unsafe_allow_html=True)
