import streamlit as st
from i18n import tr, set_language

# --- Homepage Content ---
def homepage_content():
    st.title(tr('Homepage'))
    st.markdown(tr('Welcome to the Finance Webapp!'))
    st.markdown(tr('This website provides:'))
    st.markdown('- ' + tr('Stock data visualization (line/candlestick) and information'))
    st.markdown('- ' + tr('Fundamental metrics'))
    st.markdown('- ' + tr('Sharia (Syariah) stock screening'))
    st.markdown('- ' + tr('Portfolio analysis (Classic and Hybrid)'))